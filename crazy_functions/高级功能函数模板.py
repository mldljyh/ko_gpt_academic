from toolbox import CatchException, update_ui
from .crazy_utils import request_gpt_model_in_new_thread_with_ui_alive
import datetime
@CatchException
def 高阶功能模板函数(txt, llm_kwargs, plugin_kwargs, chatbot, history, system_prompt, web_port):
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
    chatbot.append(("이게 뭐하는 기능이에요?", "[지역 메시지] 주의하세요. [함수 플러그인]의 템플릿을 호출하고 있습니다. 이 함수는 더 많은 재미있는 기능을 구현하려는 개발자를 대상으로 합니다. 이것은 새로운 기능 함수를 만들기 위한 템플릿으로 사용될 수 있습니다. (이 함수는 20줄 정도의 코드만 사용합니다.) 또한, 우리는 여러 파일을 동기화 처리할 수 있는 멀티 스레드 데모도 제공합니다. 새로운 기능 모듈을 공유하고 싶다면 적극적으로 PR을 보내주세요!"))
    yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 由于请求gpt需要一段时间，我们先及时地做一次界面更新
    for i in range(5):
        currentMonth = (datetime.date.today() + datetime.timedelta(days=i)).month
        currentDay = (datetime.date.today() + datetime.timedelta(days=i)).day
        i_say = f'지금 {currentMonth}월 {currentDay} 일 에 일어난 역사적 사건 중 어떤 것이 있나요? 두 가지를 나열하고 관련 이미지를 보내주세요. 이미지를 보내실 때, Markdown을 사용하여 PUT_YOUR_QUERY_HERE를 해당 사건의 가장 중요한 단어로 대체해주세요.'
        gpt_say = yield from request_gpt_model_in_new_thread_with_ui_alive(
            inputs=i_say, inputs_show_user=i_say, 
            llm_kwargs=llm_kwargs, chatbot=chatbot, history=[], 
            sys_prompt="사진을 보내고 싶다면 Markdown을 사용하고, 역슬래시를 사용하지 말고 코드 블록을 사용하지 않도록 주의해주세요. Unsplash API (https://source.unsplash.com/1280x720/? < PUT_YOUR_QUERY_HERE >)를 사용해주세요."
        )
        chatbot[-1] = (i_say, gpt_say)
        history.append(i_say);history.append(gpt_say)
        yield from update_ui(chatbot=chatbot, history=history) # 刷新界面 # 界面更新
