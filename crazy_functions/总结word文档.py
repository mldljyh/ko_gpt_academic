from toolbox import update_ui
from toolbox import CatchException, report_execption, write_results_to_file
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
fast_debug = False


def 解析docx(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, os
    # pip install python-docx 用于docx格式，跨平台
    # pip install pywin32 用于doc格式，仅支持Win平台
    for index, fp in enumerate(file_manifest):
        if fp.split(".")[-1] == "docx":
            from docx import Document
            doc = Document(fp)
            file_content = "\n".join([para.text for para in doc.paragraphs])
        else:
            import win32com.client
            word = win32com.client.Dispatch("Word.Application")
            word.visible = False
            # 打开文件
            print('fp', os.getcwd())
            doc = word.Documents.Open(os.getcwd() + '/' + fp)
            # file_content = doc.Content.Text
            doc = word.ActiveDocument
            file_content = doc.Range().Text
            doc.Close()
            word.Quit()

        print(file_content)
        # private_upload里面的文件名在解压zip后容易出现乱码（rar和7z格式正常），故可以只分析文章内容，不输入文件名
        from .crazy_utils import breakdown_txt_to_satisfy_token_limit_for_pdf
        from request_llm.bridge_all import model_info
        max_token = model_info[llm_kwargs['llm_model']]['max_token']
        TOKEN_LIMIT_PER_FRAGMENT = max_token * 3 // 4
        paper_fragments = breakdown_txt_to_satisfy_token_limit_for_pdf(
            txt=file_content,  
            get_token_fn=model_info[llm_kwargs['llm_model']]['token_cnt'], 
            limit=TOKEN_LIMIT_PER_FRAGMENT
        )
        this_paper_history = []
        for i, paper_frag in enumerate(paper_fragments):
            i_say = f'아래는 {os.path.relpath(fp, project_folder)}이라는 파일명으로 된 글 조각입니다. 내용은 ```{paper_frag}```입니다.'
            i_say_show_user = f'이 글 조각에 대한 요약을 한 번 해볼까요? {os.path.abspath(fp)}은(는) {i+1}/{len(paper_fragments)}번째 조각입니다.'
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, 
                inputs_show_user=i_say_show_user, 
                llm_kwargs=llm_kwargs,
                chatbot=chatbot, 
                history=[],
                sys_prompt="글 요약하기."
            )

            chatbot[-1] = (i_say_show_user, gpt_say)
            history.extend([i_say_show_user,gpt_say])
            this_paper_history.extend([i_say_show_user,gpt_say])

        # 已经对该文章的所有片段总结完毕，如果文章被切分了，
        if len(paper_fragments) > 1:
            i_say = f"위의 대화를 기반으로, {os.path.abspath(fp)}의 내용을 요약하면 무엇인가요?"
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, 
                inputs_show_user=i_say, 
                llm_kwargs=llm_kwargs,
                chatbot=chatbot, 
                history=this_paper_history,
                sys_prompt="글 요약하기."
            )

            history.extend([i_say,gpt_say])
            this_paper_history.extend([i_say,gpt_say])

        res = write_results_to_file(history)
        chatbot.append(("다 했어요?", res))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    res = write_results_to_file(history)
    chatbot.append(("모든 파일을 요약 완료했나요?", res))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面


@CatchException
def 总结word文档(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    import glob, os

    # 基本信息：功能、贡献者
    chatbot.append([
        "함수 플러그인 기능이 뭐에요?",
        "여러 개의 워드 문서를 일괄 요약합니다. 함수 플러그인 기여자: JasonGuo1입니다."])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        from docx import Document
    except:
        report_execption(chatbot, history,
                         a=f"해석 프로젝트: {txt}",
                         b=f"소프트웨어 종속성을 가져오는 데 실패했습니다. 이 모듈을 사용하려면 추가 종속성이 필요하며, 설치 방법은 ```pip install --upgrade python-docx pywin32```입니다.")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 清空历史，以免输入溢出
    history = []

    # 检测输入参数，如没有给定输入参数，直接退出
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = '아무것도 없는 입력창입니다.'
        report_execption(chatbot, history, a=f"해석 프로젝트: {txt}", b=f"해당 지역의 프로젝트를 찾을 수 없거나 접근 권한이 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 搜索需要处理的文件清单
    if txt.endswith('.docx') or txt.endswith('.doc'):
        file_manifest = [txt]
    else:
        file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.docx', recursive=True)] + \
                        [f for f in glob.glob(f'{project_folder}/**/*.doc', recursive=True)]

    # 如果没找到任何文件
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a=f"해석 프로젝트: {txt}", b=f".docx나 .doc 파일을 찾을 수 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 开始正式执行任务
    yield from 解析docx(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
