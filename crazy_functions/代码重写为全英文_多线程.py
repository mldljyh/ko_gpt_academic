import threading
from request_llm.bridge_all import predict_no_ui_long_connection
from toolbox import update_ui
from toolbox import CatchException, write_results_to_file, report_execption
from .crazy_utils import breakdown_txt_to_satisfy_token_limit

def extract_code_block_carefully(txt):
    splitted = txt.split('```')
    n_code_block_seg = len(splitted) - 1
    if n_code_block_seg <= 1: return txt
    # 剩下的情况都开头除去 ``` 结尾除去一次 ```
    txt_out = '```'.join(splitted[1:-1])
    return txt_out



def break_txt_into_half_at_some_linebreak(txt):
    lines = txt.split('\n')
    n_lines = len(lines)
    pre = lines[:(n_lines//2)]
    post = lines[(n_lines//2):]
    return "\n".join(pre), "\n".join(post)


@CatchException
def 全项目切换英文(txt, llm_kwargs, plugin_kwargs, chatbot, history, sys_prompt, web_port):
    # 第1步：清空历史，以免输入溢出
    history = []

    # 第2步：尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        import tiktoken
    except:
        report_execption(chatbot, history, 
            a = f"해석 프로젝트: {txt}", 
            b = f"소프트웨어 종속성 가져오기가 실패했습니다. 이 모듈을 사용하려면 추가 종속성이 필요하며, 설치 방법은 ```pip install --upgrade tiktoken```입니다.")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 第3步：集合文件
    import time, glob, os, shutil, re
    os.makedirs('gpt_log/generated_english_version', exist_ok=True)
    os.makedirs('gpt_log/generated_english_version/crazy_functions', exist_ok=True)
    file_manifest = [f for f in glob.glob('./*.py') if ('test_project' not in f) and ('gpt_log' not in f)] + \
                    [f for f in glob.glob('./crazy_functions/*.py') if ('test_project' not in f) and ('gpt_log' not in f)]
    # file_manifest = ['./toolbox.py']
    i_say_show_user_buffer = []

    # 第4步：随便显示点什么防止卡顿的感觉
    for index, fp in enumerate(file_manifest):
        # if 'test_project' in fp: continue
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()
        i_say_show_user =f'[{index}/{len(file_manifest)}] Please translate all Korean characters in the following code into English and only output the resulting English code. Please use a code block to output the code: {os.path.abspath(fp)}'
        i_say_show_user_buffer.append(i_say_show_user)
        chatbot.append((i_say_show_user, "[Local Message] 다중 스레드 작업을 기다리는 동안 중간 과정은 표시하지 않습니다."))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面


    # 第5步：Token限制下的截断与处理
    MAX_TOKEN = 3000
    from request_llm.bridge_all import model_info
    enc = model_info["gpt-3.5-turbo"]['tokenizer']
    def get_token_fn(txt): return len(enc.encode(txt, disallowed_special=()))


    # 第6步：任务函数
    mutable_return = [None for _ in file_manifest]
    observe_window = [[""] for _ in file_manifest]
    def thread_worker(fp,index):
        if index > 10: 
            time.sleep(60)
            print('OpenAI는 무료 사용자의 요청 횟수를 분당 20회로 제한하고, 요청 빈도를 낮추도록 조치했습니다.')
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()
        i_say_template = lambda fp, file_content: f'Please translate all Korean characters in the following code to English, and only output the code. The file name is {fp} and the file code is ```{file_content}```.'
        try:
            gpt_say = ""
            # 分解代码文件
            file_content_breakdown = breakdown_txt_to_satisfy_token_limit(file_content, get_token_fn, MAX_TOKEN)
            for file_content_partial in file_content_breakdown:
                i_say = i_say_template(fp, file_content_partial)
                # # ** gpt request **
                gpt_say_partial = predict_no_ui_long_connection(inputs=i_say, llm_kwargs=llm_kwargs, history=[], sys_prompt=sys_prompt, observe_window=observe_window[index])
                gpt_say_partial = extract_code_block_carefully(gpt_say_partial)
                gpt_say += gpt_say_partial
            mutable_return[index] = gpt_say
        except ConnectionAbortedError as token_exceed_err:
            print('최소한 하나의 스레드 작업 토큰이 오버플로우되어 실패했습니다.', e)
        except Exception as e:
            print('적어도 하나의 스레드 작업이 예기치 않게 실패했습니다.', e)

    # 第7步：所有线程同时开始执行任务函数
    handles = [threading.Thread(target=thread_worker, args=(fp,index)) for index, fp in enumerate(file_manifest)]
    for h in handles:
        h.daemon = True
        h.start()
    chatbot.append(('시작했어요?', f'"다중 스레드 작업이 이미 시작되었습니다."'))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 第8步：循环轮询各个线程是否执行完毕
    cnt = 0
    while True:
        cnt += 1
        time.sleep(0.2)
        th_alive = [h.is_alive() for h in handles]
        if not any(th_alive): break
        # 更好的UI视觉效果
        observe_win = []
        for thread_index, alive in enumerate(th_alive): 
            observe_win.append("[ ..."+observe_window[thread_index][0][-60:].replace('\n','').replace('```','...').replace(' ','.').replace('<br/>','.....').replace('$','.')+"... ]")
        stat = [f'진행중: {obs}\n\n' if alive else '완료됨\n\n' for alive, obs in zip(th_alive, observe_win)]
        stat_str = ''.join(stat)
        chatbot[-1] = (chatbot[-1][0], f'멀티스레드 작업이 시작되었습니다. 상태:  \n\n{stat_str}' + ''.join(['.']*(cnt%10+1)))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 第9步：把结果写入文件
    for index, h in enumerate(handles):
        h.join() # 这里其实不需要join了，肯定已经都结束了
        fp = file_manifest[index]
        gpt_say = mutable_return[index]
        i_say_show_user = i_say_show_user_buffer[index]

        where_to_relocate = f'gpt_log/generated_english_version/{fp}'
        if gpt_say is not None:
            with open(where_to_relocate, 'w+', encoding='utf-8') as f:  
                f.write(gpt_say)
        else:  # 失败
            shutil.copyfile(file_manifest[index], where_to_relocate)
        chatbot.append((i_say_show_user, f'[Local Message] {os.path.abspath(fp)}의 변환을 완료했습니다. \n\n{os.path.abspath(where_to_relocate)}에 저장되었습니다.'))
        history.append(i_say_show_user); history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        time.sleep(1)

    # 第10步：备份一个文件
    res = write_results_to_file(history)
    chatbot.append(("Task execution report를 작성해주세요.", res))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
