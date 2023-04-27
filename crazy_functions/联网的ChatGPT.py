from toolbox import CatchException, update_ui
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive, input_clipping
import requests
from bs4 import BeautifulSoup
from request_llm.bridge_all import model_info

def google(query, proxies):
    query = query # 在此处替换您要搜索的关键词
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
    response = requests.get(url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for g in soup.find_all('div', class_='g'):
        anchors = g.find_all('a')
        if anchors:
            link = anchors[0]['href']
            if link.startswith('/url?q='):
                link = link[7:]
            if not link.startswith('http'):
                continue
            title = g.find('h3').text
            item = {'title': title, 'link': link}
            results.append(item)

    for r in results:
        print(r['link'])
    return results

def scrape_text(url, proxies) -> str:
    """Scrape text from a webpage

    Args:
        url (str): The URL to scrape text from

    Returns:
        str: The scraped text
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
        'Content-Type': 'text/plain',
    }
    try: 
        response = requests.get(url, headers=headers, proxies=proxies, timeout=8)
        if response.encoding == "ISO-8859-1": response.encoding = response.apparent_encoding
    except: 
        return "그 페이지에 접속할 수 없습니다."
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text

@CatchException
def 连接网络回答问题(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
    """
    txt             输入栏用户输入的文本，例如需要翻译的一段话，再例如一个包含了待处理文件的路径
    llm_kwargs      gpt模型参数，如温度和top_p等，一般原样传递下去就行
    plugin_kwargs   插件模型的参数，暂时没有用武之地
    chatbot         聊天显示框的句柄，用于显示给用户
    history         聊天历史，前情提要
    system_prompt   给gpt的静默提醒
    web_port        当前软件运行的端口号
    """
    history = []    # 清空历史，以免输入溢出
    chatbot.append((f"인터넷 정보를 참고하여 다음 질문에 대답해 주세요: {txt}", 
                    "[Local Message] 주의하세요, 여러분은 [함수 플러그인]의 템플릿을 호출하고 있습니다. 이 템플릿을 사용하면 ChatGPT 네트워크 정보를 종합하는 기능을 구현할 수 있습니다. 이 함수는 더 많은 재미있는 기능을 구현하고자 하는 개발자를 대상으로 합니다. 새로운 기능 모듈을 공유하고자 한다면 PR을 주저하지 마세요!"))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 由于请求gpt需要一段时间，我们先及时地做一次界面更新

    # ------------- < 第1步：爬取搜索引擎的结果 > -------------
    from toolbox import get_conf
    proxies, = get_conf('proxies')
    urls = google(txt, proxies)
    history = []

    # ------------- < 第2步：依次访问网页 > -------------
    max_search_result = 5   # 最多收纳多少个网页的结果
    for index, url in enumerate(urls[:max_search_result]):
        res = scrape_text(url['link'], proxies)
        history.extend([f"검색 결과 중 {index}번째:", res])
        chatbot.append([f"검색 결과 중 {index}번째:", res[:500]+"......"])
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 由于请求gpt需要一段时间，我们先及时地做一次界面更新

    # ------------- < 第3步：ChatGPT综合 > -------------
    i_say = f"위의 검색 결과에서 정보를 추출하고, 그 후 질문에 대답해주세요: {txt}"
    i_say, history = input_clipping(    # 裁剪输入，从最长的条目开始裁剪，防止爆token
        inputs=i_say, 
        history=history, 
        max_token_limit=model_info[llm_kwargs['llm_model']]['max_token']*3//4
    )
    gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
        inputs=i_say, inputs_show_user=i_say, 
        llm_kwargs=llm_kwargs, chatbot=chatbot, history=history, 
        sys_prompt="주어진 검색 결과 중에서 정보를 추출하여 가장 관련성이 높은 두 개의 검색 결과를 요약하고, 그 다음 질문에 답해주세요."
    )
    chatbot[-1] = (i_say, gpt_say)
    history.append(i_say);history.append(gpt_say)
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 界面更新

