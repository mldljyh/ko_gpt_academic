from toolbox import update_ui
from toolbox import CatchException, report_execption, write_results_to_file
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
fast_debug = False


def 解析Paper(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, glob, os
    print('begin analysis on:', file_manifest)
    for index, fp in enumerate(file_manifest):
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()

        prefix = "다음으로 이 논문 파일들을 하나씩 분석하고 내용을 요약해주세요." if index==0 else ""
        i_say = prefix + f'아래의 텍스트 조각에 대해 간략한 요약을 한국어로 번역해주세요. 파일 이름은 {os.path.relpath(fp, project_folder)}이며, 내용은 ```{file_content}```입니다.'
        i_say_show_user = prefix + f'"[{index}/{len(file_manifest)}] 이 상황에서 {os.path.abspath(fp)}라는 파일 경로에 대한 요약을 작성해주세요."'
        chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

        if not fast_debug: 
            msg = '정상적입니다.'
            # ** gpt request **
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(i_say, i_say_show_user, llm_kwargs, chatbot, history=[], sys_prompt=system_prompt)   # 带超时倒计时

            chatbot[-1] = (i_say_show_user, gpt_say)
            history.append(i_say_show_user); history.append(gpt_say)
            yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
            if not fast_debug: time.sleep(2)

    all_file = ', '.join([os.path.relpath(fp, project_folder) for index, fp in enumerate(file_manifest)])
    i_say = f'당신의 분석에 따라, 전체 글에 대해 요약하고 학술적인 언어로 한국어 요약문을 작성한 후, {all_file}를 포함하는 영어 요약문을 작성하십시오.'
    chatbot.append((i_say, "[Local Message] waiting gpt response."))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    if not fast_debug: 
        msg = '정상적입니다.'
        # ** gpt request **
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(i_say, i_say, llm_kwargs, chatbot, history=history, sys_prompt=system_prompt)   # 带超时倒计时

        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say); history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
        res = write_results_to_file(history)
        chatbot.append(("완료했나요?", res))
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面



@CatchException
def 读文章写摘要(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # 清空历史，以免输入溢出
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = '비어있는 입력창'
        report_execption(chatbot, history, a = f"해석 프로젝트: {txt}", b = f"해당 지역 프로젝트를 찾을 수 없거나 접근 권한이 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)] # + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)] + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.c', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"해석 프로젝트: {txt}", b = f".tex 파일을 찾을 수 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    yield from 解析Paper(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
