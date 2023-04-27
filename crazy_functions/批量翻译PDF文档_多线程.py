from toolbox import CatchException, report_execption, write_results_to_file
from toolbox import update_ui
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from .crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency
from .crazy_utils import read_and_clean_pdf_text
from colorful import *

@CatchException
def 批量翻译PDF文档(txt, llm_kwargs, plugin_kwargs, chatbot, history, sys_prompt, web_port):
    import glob
    import os

    # 基本信息：功能、贡献者
    chatbot.append([
        "함수 플러그인 기능이 뭐에요?",
        "PDF 문서를 대량으로 번역합니다. 함수 플러그인 기여자: Binary-Husky."])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        import fitz
        import tiktoken
    except:
        report_execption(chatbot, history,
                         a=f"분석 프로젝트: {txt}",
                         b=f"소프트웨어 의존성을 가져오는 데 실패했습니다. 이 모듈을 사용하려면 추가적인 의존성이 필요하며, 설치 방법은 ```pip install --upgrade pymupdf tiktoken``` 입니다.")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 清空历史，以免输入溢出
    history = []

    # 检测输入参数，如没有给定输入参数，直接退出
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "":
            txt = '비어 있는 입력란'
        report_execption(chatbot, history,
                         a=f"분석 프로젝트: {txt}", b=f"해당 지역의 프로젝트를 찾을 수 없거나 접근 권한이 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 搜索需要处理的文件清单
    file_manifest = [f for f in glob.glob(
        f'{project_folder}/**/*.pdf', recursive=True)]

    # 如果没找到任何文件
    if len(file_manifest) == 0:
        report_execption(chatbot, history,
                         a=f"분석 프로젝트: {txt}", b=f".tex나 .pdf 형식의 파일을 찾을 수 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 开始正式执行任务
    yield from 解析PDF(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, sys_prompt)


def 解析PDF(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, sys_prompt):
    import os
    import tiktoken
    TOKEN_LIMIT_PER_FRAGMENT = 1280
    generated_conclusion_files = []
    for index, fp in enumerate(file_manifest):

        # 读取PDF文件
        file_content, page_one = read_and_clean_pdf_text(fp)

        # 递归地切割PDF文件
        from .crazy_utils import breakdown_txt_to_satisfy_token_limit_for_pdf
        from request_llm.bridge_all import model_info
        enc = model_info["gpt-3.5-turbo"]['tokenizer']
        def get_token_num(txt): return len(enc.encode(txt, disallowed_special=()))
        paper_fragments = breakdown_txt_to_satisfy_token_limit_for_pdf(
            txt=file_content,  get_token_fn=get_token_num, limit=TOKEN_LIMIT_PER_FRAGMENT)
        page_one_fragments = breakdown_txt_to_satisfy_token_limit_for_pdf(
            txt=str(page_one), get_token_fn=get_token_num, limit=TOKEN_LIMIT_PER_FRAGMENT//4)

        # 为了更好的效果，我们剥离Introduction之后的部分（如果有）
        paper_meta = page_one_fragments[0].split('introduction')[0].split('Introduction')[0].split('INTRODUCTION')[0]
        
        # 单线，获取文章meta信息
        paper_meta_info = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=f"아래는 학술 논문의 기본 정보입니다. \"제목\", \"수록된 학회 또는 저널\", \"저자\", \"요약\", \"번호\", \"저자 이메일\" 중에서 이 6 가지를 추출해주세요. markdown 형식으로 출력하고, 마지막으로 요약 부분을 번역해주세요. 추출해야 할 부분은 {paper_meta}입니다.",
            inputs_show_user=f"{fp}에서 \"제목\", \"수록된 학회 또는 저널\" 등 기본 정보를 추출해주세요.",
            llm_kwargs=llm_kwargs,
            chatbot=chatbot, history=[],
            sys_prompt="Your job is to collect information from materials。",
        )

        # 多线，翻译
        gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
            inputs_array=[
                f"당신은 다음 내용을 번역해주시기 바랍니다: {frag}" for frag in paper_fragments],
            inputs_show_user_array=[f"\n---\n 원문： \n\n {frag.replace('#', '')}  \n---\n 번역：\n " for frag in paper_fragments],
            llm_kwargs=llm_kwargs,
            chatbot=chatbot,
            history_array=[[paper_meta] for _ in paper_fragments],
            sys_prompt_array=[
                "당신은 학술 번역가로서 학술 논문을 정확하게 중국어로 번역하는 역할을 맡아야 합니다. 글에서 매 문장마다 번역하는 데 유의해야 합니다." for _ in paper_fragments],
            # max_workers=5  # OpenAI所允许的最大并行过载
        )

        # 整理报告的格式
        for i,k in enumerate(gpt_response_collection): 
            if i%2==0:
                gpt_response_collection[i] = f"\n\n---\n\n ## 원문[{i//2}/{len(gpt_response_collection)//2}]： \n\n {paper_fragments[i//2].replace('#', '')}  \n\n---\n\n ## 翻译[{i//2}/{len(gpt_response_collection)//2}]：\n "
            else:
                gpt_response_collection[i] = gpt_response_collection[i]
        final = ["1. 논문 개요", paper_meta_info.replace('# ', '### ') + '\n\n---\n\n', "2. 논문 번역", ""]
        final.extend(gpt_response_collection)
        create_report_file_name = f"{os.path.basename(fp)}.trans.md"
        res = write_results_to_file(final, file_name=create_report_file_name)

        # 更新UI
        generated_conclusion_files.append(f'./gpt_log/{create_report_file_name}')
        chatbot.append((f"{fp} 끝났나요?", res))
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 准备文件的下载
    import shutil
    for pdf_path in generated_conclusion_files:
        # 重命名文件
        rename_file = f'./gpt_log/총정리 논문-{os.path.basename(pdf_path)}'
        if os.path.exists(rename_file):
            os.remove(rename_file)
        shutil.copyfile(pdf_path, rename_file)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
    chatbot.append(("출력 파일 목록을 제공해주세요.", str(generated_conclusion_files)))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
