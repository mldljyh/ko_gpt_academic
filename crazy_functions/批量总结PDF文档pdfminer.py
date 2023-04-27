from toolbox import update_ui
from toolbox import CatchException, report_execption, write_results_to_file
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive

fast_debug = False

def readPdf(pdfPath):
    """
    读取pdf文件，返回文本内容
    """
    import pdfminer
    from pdfminer.pdfparser import PDFParser
    from pdfminer.pdfdocument import PDFDocument
    from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.pdfdevice import PDFDevice
    from pdfminer.layout import LAParams
    from pdfminer.converter import PDFPageAggregator

    fp = open(pdfPath, 'rb')

    # Create a PDF parser object associated with the file object
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    # device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS.
    # Set parameters for analysis.
    laparams = LAParams(
        char_margin=10.0,
        line_margin=0.2,
        boxes_flow=0.2,
        all_texts=False,
    )
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # loop over all pages in the document
    outTextList = []
    for page in PDFPage.create_pages(document):
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()
        for obj in layout._objs:
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                # print(obj.get_text())
                outTextList.append(obj.get_text())

    return outTextList


def 解析Paper(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, glob, os
    from bs4 import BeautifulSoup
    print('begin analysis on:', file_manifest)
    for index, fp in enumerate(file_manifest):
        if ".tex" in fp:
            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                file_content = f.read()
        if ".pdf" in fp.lower():
            file_content = readPdf(fp)
            file_content = BeautifulSoup(''.join(file_content), features="lxml").body.text.encode('gbk', 'ignore').decode('gbk')

        prefix = "다음에는 여러분께서 아래의 논문들을 파일 별로 분석하시고, 그 내용을 간략하게 요약해주시기 바랍니다." if index==0 else ""
        i_say = prefix + f'아래는 파일명이 {os.path.relpath(fp, project_folder)} 이고, 내용이 ```{file_content}```인 글 조각입니다. 이 글 조각에 대한 요약을 해주세요.'
        i_say_show_user = prefix + f'[{index}/{len(file_manifest)}] 해당 파일의 경로: {os.path.abspath(fp)}입니다. 이하 내용을 간략히 요약해주세요.'
        chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

        if not fast_debug:
            msg = '정상적입니다.'
            # ** gpt request **
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, 
                inputs_show_user=i_say_show_user, 
                llm_kwargs=llm_kwargs,
                chatbot=chatbot, 
                history=[],
                sys_prompt="글 요약하기."
            )  # 带超时倒计时
            chatbot[-1] = (i_say_show_user, gpt_say)
            history.append(i_say_show_user); history.append(gpt_say)
            yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
            if not fast_debug: time.sleep(2)

    all_file = ', '.join([os.path.relpath(fp, project_folder) for index, fp in enumerate(file_manifest)])
    i_say = f'당신이 위에서 분석한 바에 따라서 이 글을 요약해주세요. 학술용어를 사용하여 한국어 요약문을 작성한 후, 영어 요약문을 작성해주세요({all_file} 포함).'
    chatbot.append((i_say, "[Local Message] waiting gpt response."))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    if not fast_debug:
        msg = '정상적입니다.'
        # ** gpt request **
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, 
            inputs_show_user=i_say, 
            llm_kwargs=llm_kwargs,
            chatbot=chatbot, 
            history=history,
            sys_prompt="글 요약하기."
        )  # 带超时倒计时
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say); history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
        res = write_results_to_file(history)
        chatbot.append(("다 끝났어요?", res))
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面



@CatchException
def 批量总结PDF文档pdfminer(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    history = []    # 清空历史，以免输入溢出
    import glob, os

    # 基本信息：功能、贡献者
    chatbot.append([
        "함수 플러그인 기능이 무엇인가요?",
        "여러 개의 PDF 문서를 한꺼번에 요약하는 것입니다. 이번 버전에서는 pdfminer 플러그인과 token 축약 기능이 탑재되어 있습니다. 이 함수 플러그인은 Euclid-Jie님이 공헌하셨습니다."])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        import pdfminer, bs4
    except:
        report_execption(chatbot, history, 
            a = f"분석 프로젝트: {txt}", 
            b = f"소프트웨어 종속성 가져오기가 실패했습니다. 이 모듈을 사용하려면 추가 종속성이 필요하며, 설치 방법은 `pip install --upgrade pdfminer beautifulsoup4`입니다.")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = '비어있는 입력란'
        report_execption(chatbot, history, a = f"분석 프로젝트: {txt}", b = f"해당 지역 프로젝트를 찾을 수 없거나 접근 권한이 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)] + \
                    [f for f in glob.glob(f'{project_folder}/**/*.pdf', recursive=True)] # + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)] + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.c', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"분석 프로젝트: {txt}", b = f".tex나 .pdf 파일을 찾을 수 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    yield from 解析Paper(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)

