from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
from toolbox import CatchException, report_execption, write_results_to_file
from toolbox import update_ui

def get_meta_information(url, chatbot, history):
    import requests
    import arxiv
    import difflib
    from bs4 import BeautifulSoup
    from toolbox import get_conf
    proxies, = get_conf('proxies')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    }
    # 发送 GET 请求
    response = requests.get(url, proxies=proxies, headers=headers)

    # 解析网页内容
    soup = BeautifulSoup(response.text, "html.parser")

    def string_similar(s1, s2):
        return difflib.SequenceMatcher(None, s1, s2).quick_ratio()

    profile = []
    # 获取所有文章的标题和作者
    for result in soup.select(".gs_ri"):
        title = result.a.text.replace('\n', ' ').replace('  ', ' ')
        author = result.select_one(".gs_a").text
        try:
            citation = result.select_one(".gs_fl > a[href*='cites']").text  # 引用次数是链接中的文本，直接取出来
        except:
            citation = 'cited by 0'
        abstract = result.select_one(".gs_rs").text.strip()  # 摘要在 .gs_rs 中的文本，需要清除首尾空格
        search = arxiv.Search(
            query = title,
            max_results = 1,
            sort_by = arxiv.SortCriterion.Relevance,
        )
        paper = next(search.results())
        if string_similar(title, paper.title) > 0.90: # same paper
            abstract = paper.summary.replace('\n', ' ')
            is_paper_in_arxiv = True
        else:   # different paper
            abstract = abstract
            is_paper_in_arxiv = False
        paper = next(search.results())
        print(title)
        print(author)
        print(citation)
        profile.append({
            'title':title,
            'author':author,
            'citation':citation,
            'abstract':abstract,
            'is_paper_in_arxiv':is_paper_in_arxiv,
        })

        chatbot[-1] = [chatbot[-1][0], title + f'"Arxiv에 있는지 확인해 주세요. (Arxiv에 없으면 완전한 초록을 얻을 수 없습니다): {is_paper_in_arxiv}"' + abstract]
        yield from update_ui(chatbot=chatbot, history=[]) # 刷新界面
    return profile

@CatchException
def 谷歌检索小助手(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    # 基本信息：功能、贡献者
    chatbot.append([
        "함수 플러그인 기능이 뭐에요?",
        "사용자가 제공한 구글 학술 검색 페이지에서 발견된 모든 논문을 분석하면, \"binary-husky\"라는 플러그인이 초기화되는 것을 볼 수 있습니다."])
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面

    # 尝试导入依赖，如果缺少依赖，则给出安装建议
    try:
        import arxiv
        import math
        from bs4 import BeautifulSoup
    except:
        report_execption(chatbot, history, 
            a = f"해석 프로젝트: {txt}", 
            b = f"소프트웨어 의존성을 가져오지 못했습니다. 이 모듈을 사용하려면 추가적인 의존성이 필요하며, 설치 방법은 ```pip install --upgrade beautifulsoup4 arxiv```입니다.")
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面
        return

    # 清空历史，以免输入溢出
    history = []
    meta_paper_info_list = yield from get_meta_information(txt, chatbot, history)
    batchsize = 5
    for batch in range(math.ceil(len(meta_paper_info_list)/batchsize)):
        if len(meta_paper_info_list[:batchsize]) > 0:
            i_say = "아래는 일부 학술 자료의 데이터이며, 다음 내용을 추출했습니다:" + \
            "1. Title in English；2. Translation of the title in Korean:3. Author:4. Publication in Arxiv (Boolean value):5. Translation of the abstract in Korean" + \
            f"다음은 정보 출처입니다: {str(meta_paper_info_list[:batchsize])}" 

            inputs_show_user = f"이 페이지에 나타난 모든 기사를 분석하십시오: {txt}, 이것은 {batch+1}번째 일괄 처리입니다."
            gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
                inputs=i_say, inputs_show_user=inputs_show_user,
                llm_kwargs=llm_kwargs, chatbot=chatbot, history=[],
                sys_prompt="당신은 학술 번역가이며, 데이터에서 정보를 추출해야 합니다. Markdown 테이블을 사용해야 합니다. 각 문헌을 하나씩 처리해야 합니다."
            )

            history.extend([ f"제{batch+1}배치", gpt_say ])
            meta_paper_info_list = meta_paper_info_list[batchsize:]

    chatbot.append(["상태?", 
        "\"Related Works\"를 AI에게 작성하도록 시도해 볼 수 있습니다. 모든 작업이 이미 완료되었습니다.\"Related Works\" section about \"你搜索的研究领域\" for me."])
    msg = '일반적인/보통의/정상적인/양호한/정상/정상상태'
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
    res = write_results_to_file(history)
    chatbot.append(("완료했나요?", res)); 
    yield from update_ui(chatbot=chatbot, history=history, msg=msg) # 刷新界面
