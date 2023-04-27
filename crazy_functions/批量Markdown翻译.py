from toolbox import update_ui
from toolbox import CatchException, report_execption, write_results_to_file
fast_debug = False

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
        def get_token_num(txt): return len(enc.encode(txt, disallowed_special=()))
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
                segments = breakdown_txt_to_satisfy_token_limit_for_pdf(file_content, self.get_token_num, max_token_limit)
                for j, segment in enumerate(segments):
                    self.sp_file_contents.append(segment)
                    self.sp_file_index.append(index)
                    self.sp_file_tag.append(self.file_paths[index] + f".part-{j}.md")

        print('Segmentation: done')

def 多文件翻译(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='en'):
    import time, os, re
    from .crazy_utils import request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency

    #  <-------- 读取Markdown文件，删除其中的所有注释 ----------> 
    pfg = PaperFileGroup()

    for index, fp in enumerate(file_manifest):
        with open(fp, 'r', encoding='utf-8', errors='replace') as f:
            file_content = f.read()
            # 记录删除注释后的文本
            pfg.file_paths.append(fp)
            pfg.file_contents.append(file_content)

    #  <-------- 拆分过长的Markdown文件 ----------> 
    pfg.run_file_split(max_token_limit=1500)
    n_split = len(pfg.sp_file_contents)

    #  <-------- 多线程润色开始 ----------> 
    if language == 'en->ko':
        inputs_array = ["This is a Markdown file, translate it into Korean, do not modify any existing Markdown commands:" + 
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        inputs_show_user_array = [f"번역 {f}" for f in pfg.sp_file_tag]
        sys_prompt_array = ["You are a professional academic paper translator." for _ in range(n_split)]
    elif language == 'ko->en':
        inputs_array = [f"This is a Markdown file, translate it into English, do not modify any existing Markdown commands:" + 
                        f"\n\n{frag}" for frag in pfg.sp_file_contents]
        inputs_show_user_array = [f"번역 {f}" for f in pfg.sp_file_tag]
        sys_prompt_array = ["You are a professional academic paper translator." for _ in range(n_split)]

    gpt_response_collection = yield from request_gpt_model_multi_threads_with_very_awesome_ui_and_high_efficiency(
        inputs_array=inputs_array,
        inputs_show_user_array=inputs_show_user_array,
        llm_kwargs=llm_kwargs,
        chatbot=chatbot,
        history_array=[[""] for _ in range(n_split)],
        sys_prompt_array=sys_prompt_array,
        # max_workers=5,  # OpenAI所允许的最大并行过载
        scroller_max_len = 80
    )

    #  <-------- 整理结果，退出 ----------> 
    create_report_file_name = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + f"-chatgpt.polish.md"
    res = write_results_to_file(gpt_response_collection, file_name=create_report_file_name)
    history = gpt_response_collection
    chatbot.append((f"{fp} 완료되었나요?", res))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面


def get_files_from_everything(txt):
    import glob, os

    success = True
    if txt.startswith('http'):
        # 网络的远程文件
        txt = txt.replace("https://github.com/", "https://raw.githubusercontent.com/")
        txt = txt.replace("/blob/", "/")
        import requests
        from toolbox import get_conf
        proxies, = get_conf('proxies')
        r = requests.get(txt, proxies=proxies)
        with open('./gpt_log/temp.md', 'wb+') as f: f.write(r.content)
        project_folder = './gpt_log/'
        file_manifest = ['./gpt_log/temp.md']
    elif txt.endswith('.md'):
        # 直接给定文件
        file_manifest = [txt]
        project_folder = os.path.dirname(txt)
    elif os.path.exists(txt):
        # 本地路径，递归搜索
        project_folder = txt
        file_manifest = [f for f in glob.glob(f'{project_folder}/**/*.md', recursive=True)]
    else:
        success = False

    return success, file_manifest, project_folder


@CatchException
def Markdown英译中(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # 基本信息：功能、贡献者
    chatbot.append([
        "함수 플러그인 기능이 뭔가요?",
        "Markdown 프로젝트 전체를 번역합니다. 함수 플러그인 기여자: Binary-Husky"])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        import tiktoken
        import glob, os
    except:
        report_execption(chatbot, history,
                         a=f"분석 프로젝트: {txt}",
                         b=f"소프트웨어 의존성 가져오기 실패. 이 모듈을 사용하려면 추가 종속성이 필요합니다. 설치 방법은 ```pip install --upgrade tiktoken```입니다.")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    history = []    # 清空历史，以免输入溢出

    success, file_manifest, project_folder = get_files_from_everything(txt)

    if not success:
        # 什么都没有
        if txt == "": txt = '입력창이 아무것도 없어 빈 공간이 있는 것 같습니다.'
        report_execption(chatbot, history, a = f"분석 프로젝트: {txt}", b = f"\"이 지역의 프로젝트를 찾을 수 없거나 접근 권한이 없습니다: {txt}\"")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"분석 프로젝트: {txt}", b = f".md 파일을 찾을 수 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    yield from 多文件翻译(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='en->ko')





@CatchException
def Markdown中译英(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # 基本信息：功能、贡献者
    chatbot.append([
        "함수 플러그인 기능이 뭔가요?",
        "Markdown 프로젝트 전체를 번역합니다. 함수 플러그인 기여자: Binary-Husky"])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        import tiktoken
        import glob, os
    except:
        report_execption(chatbot, history,
                         a=f"분석 프로젝트: {txt}",
                         b=f"소프트웨어 의존성 가져오기 실패. 이 모듈을 사용하려면 추가 종속성이 필요합니다. 설치 방법은 ```pip install --upgrade tiktoken```입니다.")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    history = []    # 清空历史，以免输入溢出
    success, file_manifest, project_folder = get_files_from_everything(txt)
    if not success:
        # 什么都没有
        if txt == "": txt = '입력창이 아무것도 없어 빈 공간이 있는 것 같습니다.'
        report_execption(chatbot, history, a = f"분석 프로젝트: {txt}", b = f"\"이 지역의 프로젝트를 찾을 수 없거나 접근 권한이 없습니다: {txt}\"")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    if len(file_manifest) == 0:
        report_execption(chatbot, history, a = f"분석 프로젝트: {txt}", b = f"'.md' 파일을 찾을 수 없습니다: {txt}")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return
    yield from 多文件翻译(file_manifest, project_folder, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, language='ko->en')