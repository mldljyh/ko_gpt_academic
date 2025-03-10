from toolbox import update_ui
from toolbox import CatchException, report_execption, write_results_to_file
fast_debug = True


class PaperFileGroup():
    def __init__(self):
        self.file_paths = []
        self.file_contents = []
        self.sp_file_contents = []
        self.sp_file_index = []
        self.sp_file_tag = []

        # count_token
        from request_llm.bridge_all import model_info
        enc = model_info["gpt-3.5-turbo"]['tokenizer']
        def get_token_num(txt): return len(
            enc.encode(txt, disallowed_special=()))
        self.get_token_num = get_token_num

    def run_file_split(self, max_token_limit=1900):
        """
        将长文本分离开来
        """
        for index, file_content in enumerate(self.file_contents):
            if self.get_token_num(file_content) < max_token_limit:
                self.sp_file_contents.append(file_content)
                self.sp_file_index.append(index)
                self.sp_file_tag.append(self.file_paths[index])
            else:
                from .crazy_utils import breakdown_txt_to_satisfy_token_limit_for_pdf
                segments = breakdown_txt_to_satisfy_token_limit_for_pdf(
                    file_content, self.get_token_num, max_token_limit)
                for j, segment in enumerate(segments):
                    self.sp_file_contents.append(segment)
                    self.sp_file_index.append(index)
                    self.sp_file_tag.append(
                        self.file_paths[index] + f".part-{j}.txt")



def parseNotebook(filename, enable_markdown=1):
    import json

    CodeBlocks = []
    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        notebook = json.load(f)
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code' and cell['source']:
            # remove blank lines
            cell['source'] = [line for line in cell['source'] if line.strip()
                              != '']
            CodeBlocks.append("".join(cell['source']))
        elif enable_markdown and cell['cell_type'] == 'markdown' and cell['source']:
            cell['source'] = [line for line in cell['source'] if line.strip()
                              != '']
            CodeBlocks.append("Markdown:"+"".join(cell['source']))

    Code = ""
    for idx, code in enumerate(CodeBlocks):
        Code += f"This is {idx+1}th code block: \n"
        Code += code+"\n"

    return Code 


def ipynb解释(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt):
    from .crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency

    enable_markdown = plugin_kwargs.get("advanced_arg", "1")
    try:
        enable_markdown = int(enable_markdown)
    except ValueError:
        enable_markdown = 1

    pfg = PaperFileGroup()

    for fp in file_manifest:
        file_content = parseNotebook(fp, enable_markdown=enable_markdown)
        pfg.file_paths.append(fp)
        pfg.file_contents.append(file_content)

    #  <-------- 拆分过长的IPynb文件 ---------->
    pfg.run_file_split(max_token_limit=1024)
    n_split = len(pfg.sp_file_contents)

    inputs_array = [r"This is a Jupyter Notebook file, tell me about Each Block in Korean. Focus Just On Code." +
                    r"If a block starts with `Markdown` which means it's a markdown block in ipynbipynb. " +
                    r"Start a new line for a block and block num use Korean." +
                    f"\n\n{frag}" for frag in pfg.sp_file_contents]
    inputs_show_user_array = [f"{f}의 분석은 다음과 같습니다." for f in pfg.sp_file_tag]
    sys_prompt_array = ["You are a professional programmer."] * n_split

    gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
        inputs_array=inputs_array,
        inputs_show_user_array=inputs_show_user_array,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot,
        history_array=[[""] for _ in range(n_split)],
        sys_prompt_array=sys_prompt_array,
        # max_workers=5,  # OpenAI所允许的最大并行过载
        scroller_max_len=80
    )

    #  <-------- 整理结果，退出 ---------->
    block_result = "  \n".join(gpt_response_collection)
    chatbot.append(("해석 결과는 다음과 같습니다.", block_result))
    history.extend(["해석 결과는 다음과 같습니다.", block_result])
    yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面

    #  <-------- 写入文件，退出 ---------->
    res = write_results_to_file(history)
    chatbot.append(("완료되었나요?", res))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

@CatchException
def 解析ipynb文件(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    chatbot.append([
        "함수 플러그인 기능이 뭐에요?",
        "IPynb 파일을 분석합니다. 기고자: codycjy."])
    yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面

    history = []    # 清空历史
    import glob
    import os
    if os.path.exists(txt):
        project_folder = txt
    else:
        if txt == "":
            txt = '아무것도 채워져 있지 않은 입력란.'
        report_execption(chatbot, history,
                         a=f"분석 프로젝트: {txt}", b=f"이 지역의 프로젝트를 찾을 수 없거나 접근 권한이 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面
        return
    if txt.endswith('.ipynb'):
        file_manifest = [txt]
    else:
        file_manifest = [f for f in glob.glob(
            f'{project_folder}/**/*.ipynb', recursive=True)]
    if len(file_manifest) == 0:
        report_execption(chatbot, history,
                         a=f"분석 프로젝트: {txt}", b=f".ipynb 파일을 찾을 수 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history)  # 刷新界面
        return
    yield from ipynb解释(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, )
