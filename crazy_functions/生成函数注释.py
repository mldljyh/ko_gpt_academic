from toolbox import update_ui
from toolbox import CatchException, report_execption, write_results_to_file
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
fast_debug = False

def 生成函数注释(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, os
    print('begin analysis on:', file_manifest)
    for index, fp in enumerate(file_manifest):
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()

        i_say = f'아래의 프로그램 파일에 대한 요약과 모든 함수에 대한 주석을 생성해주세요. markdown 테이블을 사용하여 결과를 출력하며, 파일명은 {os.path.relpath(fp, project_folder)}이고 파일 내용은```{file_content}```입니다.'
        i_say_show_user = f'"[{index}/{len(file_manifest)}] 이 프로그램 파일에 대해 개요를 작성하고 파일 내 모든 함수에 주석을 달아주세요: {os.path.abspath(fp)}"'
        chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

        if not fast_debug: 
            msg = '지금 상태가 정상입니다.'
            # ** gpt request **
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                i_say, i_say_show_user, llm_kwargs, chatbot, history=[], sys_prompt=system_prompt)   # 带超时倒计时

            chatbot[-1] = (i_say_show_user, gpt_say)
            history.append(i_say_show_user); history.append(gpt_say)
            yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
            if not fast_debug: time.sleep(2)

    if not fast_debug: 
        res = write_results_to_file(history)
        chatbot.append(("끝났어요? 완성했나요?", res))
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面



@CatchException
def 批量生成函数注释(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # 清空历史，以免输入溢出
    import glob, os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = '빈 빈한 입력란'
        report_execption(chatbot, history, a = f"해석 프로젝트: {txt}", b = f"해당 로컬 프로젝트를 찾을 수 없거나 접근 권한이 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.py', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)]

    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"해석 프로젝트: {txt}", b = f"'.tex' 확장자 파일을 찾을 수 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    yield from 生成函数注释(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
