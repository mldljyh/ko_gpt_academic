from toolbox import update_ui
from toolbox import CatchException, report_execption, write_results_to_file
import re
import unicodedata
fast_debug = False
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive

def is_paragraph_break(match):
    """
    根据给定的匹配结果来判断换行符是否表示段落分隔。
    如果换行符前为句子结束标志（句号，感叹号，问号），且下一个字符为大写字母，则换行符更有可能表示段落分隔。
    也可以根据之前的内容长度来判断段落是否已经足够长。
    """
    prev_char, next_char = match.groups()

    # 句子结束标志
    sentence_endings = ".!?"

    # 设定一个最小段落长度阈值
    min_paragraph_length = 140

    if prev_char in sentence_endings and next_char.isupper() and len(match.string[:match.start(1)]) > min_paragraph_length:
        return "\n\n" 
    else:
        return " "

def normalize_text(text):
    """
    通过把连字（ligatures）等文本特殊符号转换为其基本形式来对文本进行归一化处理。
    例如，将连字 "fi" 转换为 "f" 和 "i"。
    """
    # 对文本进行归一化处理，分解连字
    normalized_text = unicodedata.normalize("NFKD", text)

    # 替换其他特殊字符
    cleaned_text = re.sub(r'[^\x00-\x7F]+', '', normalized_text)

    return cleaned_text

def clean_text(raw_text):
    """
    对从 PDF 提取出的原始文本进行清洗和格式化处理。
    1. 对原始文本进行归一化处理。
    2. 替换跨行的连词，例如 “Espe-\ncially” 转换为 “Especially”。
    3. 根据 heuristic 规则判断换行符是否是段落分隔，并相应地进行替换。
    """
    # 对文本进行归一化处理
    normalized_text = normalize_text(raw_text)

    # 替换跨行的连词
    text = re.sub(r'(\w+-\n\w+)', lambda m: m.group(1).replace('-\n', ''), normalized_text)

    # 根据前后相邻字符的特点，找到原文本中的换行符
    newlines = re.compile(r'(\S)\n(\S)')

    # 根据 heuristic 规则，用空格或段落分隔符替换原换行符
    final_text = re.sub(newlines, lambda m: m.group(1) + is_paragraph_break(m) + m.group(2), text)

    return final_text.strip()

def 解析PDF(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    import time, glob, os, fitz
    print('begin analysis on:', file_manifest)
    for index, fp in enumerate(file_manifest):
        with fitz.open(fp) as doc:
            file_content = ""
            for page in doc:
                file_content += page.get_text()
            file_content = clean_text(file_content)
            print(file_content)

        prefix = "다음으로, 아래의 논문 파일을 파일별로 분석하시고, 내용을 요약해주세요." if index==0 else ""
        i_say = prefix + f'아래 문서 조각에 대해 한국어로 개요를 작성하여 주세요. 파일 이름은 {os.path.relpath(fp, project_folder)}, 문서 내용은 ```{file_content}```입니다.'
        i_say_show_user = prefix + f'"[{index}/{len(file_manifest)}] 이 아래의 글 조각에 대해 개요를 작성해주세요: {os.path.abspath(fp)}"'
        chatbot.append((i_say_show_user, "[Local Message] waiting gpt response."))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

        if not fast_debug: 
            msg = '정상입니다.'
            # ** gpt request **
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, 
                inputs_show_user=i_say_show_user, 
                llm_kwargs=llm_kwargs,
                chatbot=chatbot, 
                history=[],
                sys_prompt="글을 요약하다."
            )  # 带超时倒计时
                

            chatbot[-1] = (i_say_show_user, gpt_say)
            history.append(i_say_show_user); history.append(gpt_say)
            yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
            if not fast_debug: time.sleep(2)

    all_file = ', '.join([os.path.relpath(fp, project_folder) for index, fp in enumerate(file_manifest)])
    i_say = f'위의 자신의 분석에 기반하여 전문을 요약하고, 학술적인 언어를 사용하여 중국어 요약문을 작성한 후, {all_file}을 포함한 영어 요약문도 작성하십시오.'
    chatbot.append((i_say, "[Local Message] waiting gpt response."))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    if not fast_debug: 
        msg = '정상입니다.'
        # ** gpt request **
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, 
            inputs_show_user=i_say, 
            llm_kwargs=llm_kwargs,
            chatbot=chatbot, 
            history=history,
            sys_prompt="글을 요약하다."
        )  # 带超时倒计时

        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say); history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
        res = write_results_to_file(history)
        chatbot.append(("끝났어요? 완료되었나요?", res))
        yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面


@CatchException
def 批量总结PDF文档(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    import glob, os

    # 基本信息：功能、贡献者
    chatbot.append([
        "함수 플러그인 기능이 뭐에요?",
        "여러 개의 PDF 문서를 요약하는 작업. 함수 플러그인 기여자: ValeriaWong, Eralien."])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        import fitz
    except:
        report_execption(chatbot, history, 
            a = f"해석 프로젝트: {txt}", 
            b = f"소프트웨어 의존성 가져오기 실패. 이 모듈을 사용하려면 추가 종속성이 필요합니다. 다음과 같이 설치하십시오. ```pip install --upgrade pymupdf```")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 清空历史，以免输入溢出
    history = []

    # 检测输入参数，如没有给定输入参数，直接退出
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "": txt = '비어있는 입력란'
        report_execption(chatbot, history, a = f"해석 프로젝트: {txt}", b = f"해당 로컬 프로젝트를 찾을 수 없거나 접근 권한이 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 搜索需要处理的文件清单
    file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.pdf', recursive=True)] # + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.tex', recursive=True)] + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.cpp', recursive=True)] + \
                    # [f for f in glob.glob(f'{project_folder}/**/*.c', recursive=True)]
    
    # 如果没找到任何文件
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"해석 프로젝트: {txt}", b = f".tex나 .pdf 파일을 찾을 수 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 开始正式执行任务
    yield from 解析PDF(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt)
