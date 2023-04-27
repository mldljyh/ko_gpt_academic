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
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个C项目的头文件)
        },
        "C++ 프로젝트(.cpp/.hpp/.c/.h) 분석）": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个C项目)
        },
        "Go 프로젝트 분석": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个Golang项目)
        },
        "Java 프로젝트 분석": {
            "Color": "stop",  # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个Java项目)
        },
        "React 프로젝트 분석": {
            "Color": "stop",  # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个Rect项目)
        },
        "Lua 프로젝트 분석": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个Lua项目)
        },
        "CSharp 프로젝트 분석": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(解析一个CSharp项目)
        },
        "Tex 논문 읽고 요약 작성": {
            "Color": "stop",    # 按钮颜色
            "Function": HotReload(读文章写摘要)
        },
        "Markdown/Readme를 한국어로 번역합니다.": {
            # HotReload는 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고도 코드가 즉시 적용되도록 함
            "Color": "stop",
            "Function": HotReload(Markdown英译中)
        },
        "일괄 함수 주석 생성": {
            "Color": "stop",    # 按钮颜色
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(批量生成函数注释)
        },
        "[다중 스레드 데모] 프로젝트 자체 분석 (소스 코드 자체 번역)": {
            "Function": HotReload(解析项目本身)
        },
        "[다중 스레드 데모] 프로젝트 소스 코드 전체를 영어로 변경": {
            # HotReload는 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고도 코드가 즉시 적용되도록 함
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(全项目切换英文)
        },
        "[함수 플러그인 템플릿 데모] 오늘의 역사": {
            # HotReload는 함수 플러그인 코드를 수정한 후 프로그램을 다시 시작하지 않고도 코드가 즉시 적용되도록 함
            "Function": HotReload(高阶功能模板函数)
        },

    }
    ###################### 第二组插件 ###########################
    # [第二组插件]: 经过充分测试
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
        "批量翻译PDF文档（多线程）": {
            "Color": "stop",
            "AsButton": True,  # 加入下拉菜单中
            "Function": HotReload(批量翻译PDF文档)
        },
        "询问多个GPT模型": {
            "Color": "stop",    # 按钮颜色
            "Function": HotReload(同时问询)
        },
        "[测试功能] 批量总结PDF文档": {
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Function": HotReload(批量总结PDF文档)
        },
        "[测试功能] 批量总结PDF文档pdfminer": {
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(批量总结PDF文档pdfminer)
        },
        "谷歌学术检索助手（输入谷歌学术搜索页url）": {
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(谷歌检索小助手)
        },

        "理解PDF文档内容 （模仿ChatPDF）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(理解PDF文档内容标准文件输入)
        },
        "[测试功能] 英文Latex项目全文润色（输入路径或上传压缩包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Latex英文润色)
        },
        "[测试功能] 中文Latex项目全文润色（输入路径或上传压缩包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Latex中文润色)
        },
        "[测试功能] Latex项目全文中译英（输入路径或上传压缩包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Latex中译英)
        },
        "[测试功能] Latex项目全文英译中（输入路径或上传压缩包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Latex英译中)
        },
        "[测试功能] 批量Markdown中译英（输入路径或上传压缩包）": {
            # HotReload 的意思是热更新，修改函数插件代码后，不需要重启程序，代码直接生效
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(Markdown中译英)
        },


    })

    ###################### 第三组插件 ###########################
    # [第三组插件]: 尚未充分测试的函数插件，放在这里
    from crazy_functions.下载arxiv论文翻译摘要 import 下载arxiv论文并翻译摘要
    function_plugins.update({
        "一键下载arxiv论文并翻译摘要（先在input输入编号，如1812.10695）": {
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(下载arxiv论文并翻译摘要)
        }
    })

    from crazy_functions.联网的ChatGPT import 连接网络回答问题
    function_plugins.update({
        "连接网络回答问题（先输入问题，再点击按钮，需要访问谷歌）": {
            "Color": "stop",
            "AsButton": False,  # 加入下拉菜单中
            "Function": HotReload(连接网络回答问题)
        }
    })

    from crazy_functions.解析项目源代码 import 解析任意code项目
    function_plugins.update({
        "解析项目源代码（手动指定和筛选源代码文件类型）": {
            "Color": "stop",
            "AsButton": False,
            "AdvancedArgs": True, # 调用时，唤起高级参数输入区（默认False）
            "ArgsReminder": "输入时用逗号隔开, *代表通配符, 加了^代表不匹配; 不输入代表全部匹配。例如: \"*.c, ^*.cpp, config.toml, ^*.toml\"", # 高级参数输入区的显示提示
            "Function": HotReload(解析任意code项目)
        },
    })
    from crazy_functions.询问多个大语言模型 import 同时问询_指定模型
    function_plugins.update({
        "询问多个GPT模型（手动指定询问哪些模型）": {
            "Color": "stop",
            "AsButton": False,
            "AdvancedArgs": True, # 调用时，唤起高级参数输入区（默认False）
            "ArgsReminder": "支持任意数量的llm接口，用&符号分隔。例如chatglm&gpt-3.5-turbo&api2d-gpt-4", # 高级参数输入区的显示提示
            "Function": HotReload(同时问询_指定模型)
        },
    })
    ###################### 第n组插件 ###########################
    return function_plugins
