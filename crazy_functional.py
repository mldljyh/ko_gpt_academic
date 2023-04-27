from toolbox import HotReload  # HotReload 的意思是热更新，修改函数插件后，不需要重启程序，代码直接生效


def get_crazy_functions():
    ###################### 第一组插件 ###########################
    from crazy_functions.读文章写摘要 import 读文章写摘要
    from crazy_functions.生成函数注释 import 批量生成函数注释
    from crazy_functions.解析项目源代码 import 解析项目本身
    from crazy_functions.解析项目源代码 import 解析一个Python项目
    from crazy_functions.解析项目源代码 import 解析一个C项目的头文件
    from crazy_functions.解析项目源代码 import 解析一个C项目
    from crazy_functions.解析项目源代码 import 解析一个Golang项目
    from crazy_functions.解析项目源代码 import 解析一个Java项目
    from crazy_functions.解析项目源代码 import 解析一个Rect项目
    from crazy_functions.高级功能函数模板 import 高阶功能模板函数
    from crazy_functions.代码重写为全英文_多线程 import 全项目切换英文
    from crazy_functions.Latex全文润色 import Latex英文润色
    from crazy_functions.询问多个大语言模型 import 同时问询
    from crazy_functions.解析项目源代码 import 解析一个Lua项目
    from crazy_functions.解析项目源代码 import 解析一个CSharp项目
    from crazy_functions.总结word文档 import 总结word文档
    from crazy_functions.解析JupyterNotebook import 解析ipynb文件
    from crazy_functions.对话历史存档 import 对话历史存档
    from crazy_functions.批量Markdown翻译 import Markdown英译中
    function_plugins = {

        "Python 프로젝트 분석": {
            "Color": "stop",    # 버튼 색상
            "Function": HotReload(解析一个Python项目)
        },
        "현재 대화 저장": {
            "AsButton":False,
            "Function": HotReload(对话历史存档)
        },
        "[테스트 기능] Jupyter Notebook 파일 분석": {
            "Color": "stop",
            "AsButton":False,
            "Function": HotReload(解析ipynb文件),
            "AdvancedArgs": True,  # 호출 시 고급 매개변수 입력 영역 활성화 (기본값: False)
            "ArgsReminder": "0을 입력하면 노트북의 Markdown 블록을 분석하지 않습니다", # 고급 매개변수 입력 영역의 표시 팁
        },
        "Word 문서 일괄 요약": {
            "Color": "stop",
            "Function": HotReload(总结word文档)
        },
        "C++ 프로젝트 헤더 파일 분석": {
            "Color": "stop",    # 버튼 색상
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(解析一个C项目的头文件)
        },
        "C++ 프로젝트(.cpp/.hpp/.c/.h) 분석）": {
            "Color": "stop",    # 버튼 색상
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(解析一个C项目)
        },
        "Go 프로젝트 분석": {
            "Color": "stop",    # 버튼 색상
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(解析一个Golang项目)
        },
        "Java 프로젝트 분석": {
            "Color": "stop",  # 버튼 색상
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(解析一个Java项目)
        },
        "React 프로젝트 분석": {
            "Color": "stop",  # 버튼 색상
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(解析一个Rect项目)
        },
        "Lua 프로젝트 분석": {
            "Color": "stop",    # 버튼 색상
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(解析一个Lua项目)
        },
        "CSharp 프로젝트 분석": {
            "Color": "stop",    # 버튼 색상
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(解析一个CSharp项目)
        },
        "Tex 논문 읽고 요약 작성": {
            "Color": "stop",    # 버튼 색상
            "Function": HotReload(读文章写摘要)
        },
        "Markdown/Readme를 한국어로 번역합니다.": {
            # HotReload는 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고도 코드가 즉시 적용되도록 함
            "Color": "stop",
            "Function": HotReload(Markdown英译中)
        },
        "일괄 함수 주석 생성": {
            "Color": "stop",    # 버튼 색상
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(批量生成函数注释)
        },
        "[다중 스레드 데모] 프로젝트 자체 분석 (소스 코드 자체 번역)": {
            "Function": HotReload(解析项目本身)
        },
        "[다중 스레드 데모] 프로젝트 소스 코드 전체를 영어로 변경": {
            # HotReload는 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고도 코드가 즉시 적용되도록 함
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(全项目切换英文)
        },
        "[함수 플러그인 템플릿 데모] 오늘의 역사": {
            # HotReload는 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고도 코드가 즉시 적용되도록 함
            "Function": HotReload(高阶功能模板函数)
        },

    }
    ###################### 세 번째 그룹 플러그인 ###########################
    # [세 번째 그룹 플러그인]: 충분히 테스트되지 않은 함수 플러그인이 여기에 있습니다.
    from crazy_functions.批量总结PDF文档 import 批量总结PDF文档
    from crazy_functions.批量总结PDF文档pdfminer import 批量总结PDF文档pdfminer
    from crazy_functions.批量翻译PDF文档_多线程 import 批量翻译PDF文档
    from crazy_functions.谷歌检索小助手 import 谷歌检索小助手
    from crazy_functions.理解PDF文档内容 import 理解PDF文档内容标准文件输入
    from crazy_functions.Latex全文润色 import Latex中文润色
    from crazy_functions.Latex全文翻译 import Latex中译英
    from crazy_functions.Latex全文翻译 import Latex英译中
    from crazy_functions.批量Markdown翻译 import Markdown中译英

    function_plugins.update({
        "일괄 번역 PDF 문서 (다중 스레드)": {
            "Color": "stop",
            "AsButton": True,  # 드롭다운 메뉴에 추가
            "Function": HotReload(批量翻译PDF文档)
        },
        "여러 GPT 모델에 질문하기": {
            "Color": "stop",    # 버튼 색상
            "Function": HotReload(同时问询)
        },
        "[테스트 기능] 일괄 요약 PDF 문서": {
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Function": HotReload(批量总结PDF文档)
        },
        "[테스트 기능] 일괄 요약 PDF 문서(pdfminer)": {
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(批量总结PDF文档pdfminer)
        },
        "Google 학술 검색 도우미 (Google 학술 검색 페이지 URL 입력)": {
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(谷歌检索小助手)
        },

        "PDF 문서 내용 이해 (ChatPDF 모방)": {
            # HotReload의 의미는 핫 업데이트이며, 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고 직접 코드를 적용합니다
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(理解PDF文档内容标准文件输入)
        },
        "[테스트 기능] 영어 Latex 프로젝트 전체 번역 평가(경로 입력 또는 압축 파일 업로드)": {
            # HotReload의 의미는 핫 업데이트이며, 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고 직접 코드를 적용합니다
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(Latex英文润色)
        },
        "[테스트 기능] 중국어 Latex 프로젝트 전체 번역 평가(경로 입력 또는 압축 파일 업로드)": {
            # HotReload의 의미는 핫 업데이트이며, 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고 직접 코드를 적용합니다
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(Latex中文润色)
        },
        "[테스트 기능] Latex 프로젝트 전체 한-영 번역(경로 입력 또는 압축 파일 업로드)": {
            # HotReload의 의미는 핫 업데이트이며, 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고 직접 코드를 적용합니다
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(Latex中译英)
        },
        "[테스트 기능] Latex 프로젝트 전체 영-한 번역(경로 입력 또는 압축 파일 업로드)": {
            # HotReload의 의미는 핫 업데이트이며, 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고 직접 코드를 적용합니다
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(Latex英译中)
        },
        "[테스트 기능] 일괄 Markdown 중-영 번역(경로 입력 또는 압축 파일 업로드)": {
            # HotReload의 의미는 핫 업데이트이며, 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고 직접 코드를 적용합니다
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(Markdown中译英)
        },


    })

    ###################### 第三组插件 ###########################
    # [第三组插件]: 尚未充分测试的函数插件，放在这里
    from crazy_functions.下载arxiv论文翻译摘要 import 下载arxiv论文并翻译摘要
    function_plugins.update({
        "한 번에 arxiv 논문 다운로드 및 번역 요약 작성 (먼저 번호를 입력하고 1812.10695와 같이 입력)": {
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(下载arxiv论文并翻译摘要)
        }
    })

    from crazy_functions.联网的ChatGPT import 连接网络回答问题
    function_plugins.update({
        "인터넷에 연결하여 질문에 대한 답변을 찾습니다 (질문을 입력한 후 버튼을 클릭하면 구글에 액세스해야 함)": {
            "Color": "stop",
            "AsButton": False,  # 드롭다운 메뉴에 추가
            "Function": HotReload(连接网络回答问题)
        }
    })

    from crazy_functions.解析项目源代码 import 解析任意code项目
    function_plugins.update({
        "프로젝트 소스코드 분석(수동으로 지정하고 소스 코드 파일 타입을 필터링하여)": {
            "Color": "stop",
            "AsButton": False,
            "AdvancedArgs": True, # 호출하면 고급 인수 입력 영역을 호출합니다 (기본값은 False입니다)
            "ArgsReminder": "쉼표로 구분하여 입력하고 *는 와일드 카드입니다. ^는 일치하지 않습니다. 입력하지 않으면 모두 일치합니다. 예 : \"*.c, ^*.cpp, config.toml, ^*.toml\"", # 고급 인수 입력 영역의 표시 팁
            "Function": HotReload(解析任意code项目)
        },
    })
    from crazy_functions.询问多个大语言模型 import 同时问询_指定模型
    function_plugins.update({
        "여러 GPT 모델에 질문하기(수동으로 어떤 모델을 질의할지 지정)": {
            "Color": "stop",
            "AsButton": False,
            "AdvancedArgs": True, # 호출하면 고급 인수 입력 영역을 호출합니다 (기본값은 False입니다)
            "ArgsReminder": "최대 수신 LLM 인터페이스 어느 것이든 지원하며 &로 구분합니다. 예 : chatglm & gpt-3.5-turbo & api2d-gpt-4", # 고급 인수 입력 영역의 표시 팁
        },
    })
    ###################### 第n组插件 ###########################
    return function_plugins
