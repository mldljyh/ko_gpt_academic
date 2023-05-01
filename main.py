import os; os.environ['no_proxy'] = '*' # 避免代理网络产生意外污染

def main():
    import gradio as gr
    from request_llm.bridge_all import predict
    from toolbox import format_io, find_free_port, on_file_uploaded, on_report_generated, get_conf, ArgsGeneralWrapper, DummyWith
    # 建议您复制一个config_private.py放自己的秘密, 如API和代理网址, 避免不小心传github被别人看到
    proxies, WEB_PORT, LLM_MODEL, CONCURRENT_COUNT, AUTHENTICATION, CHATBOT_HEIGHT, LAYOUT, API_KEY, AVAIL_LLM_MODELS = \
        get_conf('proxies', 'WEB_PORT', 'LLM_MODEL', 'CONCURRENT_COUNT', 'AUTHENTICATION', 'CHATBOT_HEIGHT', 'LAYOUT', 'API_KEY', 'AVAIL_LLM_MODELS')

    # 만약 WEB_PORT가 -1이라면, 무작위로 WEB 포트를 선택합니다.
    PORT = find_free_port() if WEB_PORT <= 0 else WEB_PORT
    if not AUTHENTICATION: AUTHENTICATION = None

    from check_proxy import get_current_version
    initial_prompt = "Serve me as a writing and programming assistant."
    title_html = f"<h1 align=\"center\">학술용 ChatGPT {get_current_version()}</h1>"
    description =  """코드가 오픈소스로 공개되어 업데이트 중입니다. [여기🚀](https://github.com/binary-husky/chatgpt_academic)를 클릭하시면 방문할 수 있습니다. 열정적인 개발자분들❤️[도움을 주신 분들](https://github.com/binary-husky/chatgpt_academic/graphs/contributors)께 감사드립니다."""

    # 문의 기록, 파이썬 버전은 3.9 이상을 권장합니다. (최신 버전일수록 더 좋습니다.)
    import logging
    os.makedirs("gpt_log", exist_ok=True)
    try:logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO, encoding="utf-8")
    except:logging.basicConfig(filename="gpt_log/chat_secrets.log", level=logging.INFO)
    print("모든 문의 기록은 자동으로 로컬 디렉토리인 ./gpt_log/chat_secrets.log에 저장됩니다. 개인 정보 보호에 주의하세요!")

    # 일반적인 기능 모듈 몇 가지입니다.
    from core_functional import get_core_functions
    functional = get_core_functions()

    # 高级函数插件
    from crazy_functional import get_crazy_functions
    crazy_fns = get_crazy_functions()

    # 处理markdown文本格式的转变
    gr.Chatbot.postprocess = format_io

    # 외관 색깔을 조금 바꿔주는 작업을 하겠습니다.
    from theme import adjust_theme, advanced_css
    set_theme = adjust_theme()

    # 代理与自动更新
    from check_proxy import check_proxy, auto_update, warm_up_modules
    proxy_info = check_proxy(proxies)

    gr_L1 = lambda: gr.Row().style()
    gr_L2 = lambda scale: gr.Column(scale=scale)
    if LAYOUT == "TOP-DOWN":
        gr_L1 = lambda: DummyWith()
        gr_L2 = lambda scale: gr.Row()
        CHATBOT_HEIGHT /= 2

    cancel_handles = []
    with gr.Blocks(title="학술용 ChatGPT", theme=set_theme, analytics_enabled=False, css=advanced_css) as demo:
        gr.HTML(title_html)
        cookies = gr.State({'api_key': API_KEY, 'llm_model': LLM_MODEL})
        with gr_L1():
            with gr_L2(scale=2):
                chatbot = gr.Chatbot(label=f"현재 모델: {LLM_MODEL}")
                chatbot.style(height=CHATBOT_HEIGHT)
                history = gr.State([])
            with gr_L2(scale=1):
                with gr.Accordion("입력 영역", open=True) as area_input_primary:
                    with gr.Row():
                        txt = gr.Textbox(show_label=False, placeholder="Input question here.").style(container=False)
                    with gr.Row():
                        submitBtn = gr.Button("제출", variant="primary")
                    with gr.Row():
                        resetBtn = gr.Button("재설정", variant="secondary"); resetBtn.style(size="sm")
                        stopBtn = gr.Button("중지", variant="secondary"); stopBtn.style(size="sm")
                        clearBtn = gr.Button("지우기", variant="secondary", visible=False); clearBtn.style(size="sm")
                    with gr.Row():
                        status = gr.Markdown(f"팁: Enter 키를 눌러 제출하고, Shift+Enter 키를 눌러 줄바꿈하세요. 현재 모델: {LLM_MODEL} \n {proxy_info}")
                with gr.Accordion("기본 기능 영역", open=True) as area_basic_fn:
                    with gr.Row():
                        for k in functional:
                            variant = functional[k]["Color"] if "Color" in functional[k] else "secondary"
                            functional[k]["Button"] = gr.Button(k, variant=variant)
                with gr.Accordion("함수 플러그인 영역", open=True) as area_crazy_fn:
                    with gr.Row():
                        gr.Markdown("주의: \"빨간색\"으로 표시된 함수 플러그인은 입력 영역에서 경로를 매개변수로 읽어와야 합니다.")
                    with gr.Row():
                        for k in crazy_fns:
                            if not crazy_fns[k].get("AsButton", True): continue
                            variant = crazy_fns[k]["Color"] if "Color" in crazy_fns[k] else "secondary"
                            crazy_fns[k]["Button"] = gr.Button(k, variant=variant)
                            crazy_fns[k]["Button"].style(size="sm")
                    with gr.Row():
                        with gr.Accordion("추가 함수 플러그인", open=True):
                            dropdown_fn_list = [k for k in crazy_fns.keys() if not crazy_fns[k].get("AsButton", True)]
                            with gr.Row():
                                dropdown = gr.Dropdown(dropdown_fn_list, value=r"플러그인 리스트를 열어주세요.", label="").style(container=False)
                            with gr.Row():
                                plugin_advanced_arg = gr.Textbox(show_label=True, label="여기는 특수 함수 플러그인의 고급 매개변수 입력 영역입니다.", visible=False, 
                                                                 placeholder="여기는 특수 함수 플러그인의 고급 매개 변수 입력 영역입니다.").style(container=False)
                            with gr.Row():
                                switchy_bt = gr.Button(r"먼저 플러그인 목록에서 선택해주세요.", variant="secondary")
                    with gr.Row():
                        with gr.Accordion("\"파일 업로드 영역\"을 펼쳐주세요. 로컬 파일을 업로드하여 빨간색 함수 플러그인에서 호출할 수 있습니다.", open=False) as area_file_up:
                            file_upload = gr.Files(label="어떤 파일이든 가능하지만, 압축 파일(zip, tar) 업로드를 권장합니다.", file_count="multiple")
                with gr.Accordion("모델 변경 & SysPrompt & 상호작용 인터페이스 레이아웃", open=(LAYOUT == "TOP-DOWN")):
                    system_prompt = gr.Textbox(show_label=True, placeholder=f"System Prompt", label="System prompt", value=initial_prompt)
                    top_p = gr.Slider(minimum=-0, maximum=1.0, value=1.0, step=0.01,interactive=True, label="Top-p (nucleus sampling)",)
                    temperature = gr.Slider(minimum=-0, maximum=2.0, value=1.0, step=0.01, interactive=True, label="Temperature",)
                    max_length_sl = gr.Slider(minimum=256, maximum=4096, value=512, step=1, interactive=True, label="Local LLM MaxLength",)
                    checkboxes = gr.CheckboxGroup(["기본 기능 구역", "\"함수 플러그인 구역\"입니다.", "하단 입력 영역", "입력 삭제 버튼입니다.", "플러그인 매개 변수 영역"], value=["기본 기능 구역", "\"함수 플러그인 구역\"입니다."], label="기능 영역 표시/숨기기 기능입니다.")
                    md_dropdown = gr.Dropdown(AVAIL_LLM_MODELS, value=LLM_MODEL, label="LLM 모델 교체/원천 요청").style(container=False)

                    gr.Markdown(description)
                with gr.Accordion("예비 입력 영역", open=True, visible=False) as area_input_secondary:
                    with gr.Row():
                        txt2 = gr.Textbox(show_label=False, placeholder="Input question here.", label="입력구역2").style(container=False)
                    with gr.Row():
                        submitBtn2 = gr.Button("\"제출\"", variant="primary")
                    with gr.Row():
                        resetBtn2 = gr.Button("재설정", variant="secondary"); resetBtn2.style(size="sm")
                        stopBtn2 = gr.Button("정지.", variant="secondary"); stopBtn2.style(size="sm")
                        clearBtn2 = gr.Button("정화(정리하다, 청소하다)", variant="secondary", visible=False); clearBtn2.style(size="sm")
        # 기능구 영역 표시 스위치와 기능구 영역의 상호 작용
        def fn_area_visibility(a):
            ret = {}
            ret.update({area_basic_fn: gr.update(visible=("기본 기능 구역" in a))})
            ret.update({area_crazy_fn: gr.update(visible=("\"함수 플러그인 구역\"입니다." in a))})
            ret.update({area_input_primary: gr.update(visible=("하단 입력 영역" not in a))})
            ret.update({area_input_secondary: gr.update(visible=("하단 입력 영역" in a))})
            ret.update({clearBtn: gr.update(visible=("입력 삭제 버튼입니다." in a))})
            ret.update({clearBtn2: gr.update(visible=("입력 삭제 버튼입니다." in a))})
            ret.update({plugin_advanced_arg: gr.update(visible=("플러그인 매개 변수 영역" in a))})
            if "하단 입력 영역" in a: ret.update({txt: gr.update(value="")})
            return ret
        checkboxes.select(fn_area_visibility, [checkboxes], [area_basic_fn, area_crazy_fn, area_input_primary, area_input_secondary, txt, txt2, clearBtn, clearBtn2, plugin_advanced_arg] )
        # 반복해서 나타나는 컨트롤 핸들 조합을 정리하세요.
        input_combo = [cookies, max_length_sl, md_dropdown, txt, txt2, top_p, temperature, chatbot, history, system_prompt, plugin_advanced_arg]
        output_combo = [cookies, chatbot, history, status]
        predict_args = dict(fn=ArgsGeneralWrapper(predict), inputs=input_combo, outputs=output_combo)
        # "제출"按钮、재설정按钮
        cancel_handles.append(txt.submit(**predict_args))
        cancel_handles.append(txt2.submit(**predict_args))
        cancel_handles.append(submitBtn.click(**predict_args))
        cancel_handles.append(submitBtn2.click(**predict_args))
        resetBtn.click(lambda: ([], [], "이미 초기화되었습니다."), None, [chatbot, history, status])
        resetBtn2.click(lambda: ([], [], "이미 초기화되었습니다."), None, [chatbot, history, status])
        clearBtn.click(lambda: ("",""), None, [txt, txt2])
        clearBtn2.click(lambda: ("",""), None, [txt, txt2])
        # 기본 기능 구역的回调函数注册
        for k in functional:
            click_handle = functional[k]["Button"].click(fn=ArgsGeneralWrapper(predict), inputs=[*input_combo, gr.State(True), gr.State(k)], outputs=output_combo)
            cancel_handles.append(click_handle)
        # 파일 업로드 영역에서 파일을 받은 후 챗봇과 상호작용합니다.
        file_upload.upload(on_file_uploaded, [file_upload, chatbot, txt, txt2, checkboxes], [chatbot, txt, txt2])
        # 函数插件-固定按钮区
        for k in crazy_fns:
            if not crazy_fns[k].get("AsButton", True): continue
            click_handle = crazy_fns[k]["Button"].click(ArgsGeneralWrapper(crazy_fns[k]["Function"]), [*input_combo, gr.State(PORT)], output_combo)
            click_handle.then(on_report_generated, [file_upload, chatbot], [file_upload, chatbot])
            cancel_handles.append(click_handle)
        # 함수 플러그인 - 드롭다운 메뉴와 동적 버튼의 상호작용
        def on_dropdown_changed(k):
            variant = crazy_fns[k]["Color"] if "Color" in crazy_fns[k] else "secondary"
            ret = {switchy_bt: gr.update(value=k, variant=variant)}
            if crazy_fns[k].get("AdvancedArgs", False): # 고급 플러그인 매개변수 영역을 호출할까요?
                ret.update({plugin_advanced_arg: gr.update(visible=True,  label=f"플러그인 [{k}]의 고급 매개변수 설명:" + crazy_fns[k].get("ArgsReminder", [f"고급 매개변수 기능에 대한 설명이 제공되지 않았습니다."]))})
            else:
                ret.update({plugin_advanced_arg: gr.update(visible=False, label=f"플러그인 [{k}]는 고급 설정이 필요하지 않습니다.")})
            return ret
        dropdown.select(on_dropdown_changed, [dropdown], [switchy_bt, plugin_advanced_arg] )
        def on_md_dropdown_changed(k):
            return {chatbot: gr.update(label="현재 모델:"+k)}
        md_dropdown.select(on_md_dropdown_changed, [md_dropdown], [chatbot] )
        # 가변 버튼의 콜백 함수 등록
        def route(k, *args, **kwargs):
            if k in [r"플러그인 리스트를 열어주세요.", r"먼저 플러그인 목록에서 선택해주세요."]: return
            yield from ArgsGeneralWrapper(crazy_fns[k]["Function"])(*args, **kwargs)
        click_handle = switchy_bt.click(route,[switchy_bt, *input_combo, gr.State(PORT)], output_combo)
        click_handle.then(on_report_generated, [file_upload, chatbot], [file_upload, chatbot])
        cancel_handles.append(click_handle)
        # "종료 버튼의 콜백 함수 등록"
        stopBtn.click(fn=None, inputs=None, outputs=None, cancels=cancel_handles)
        stopBtn2.click(fn=None, inputs=None, outputs=None, cancels=cancel_handles)

    # gradio的inbrowser触发不太稳定，回滚代码到原始的浏览器打开函数
    def auto_opentab_delay():
        import threading, webbrowser, time
        print(f"만약 브라우저가 자동으로 열리지 않으면, 아래 URL을 복사하여 이동해주세요:")
        print(f"(밝은 컬러 테마): http://localhost:{PORT}")
        print(f"(어두운 테마): http://localhost:{PORT}/?__dark-theme=true")
        def open():

            time.sleep(2)       # 브라우저를 열어주세요.

            DARK_MODE, = get_conf('DARK_MODE')
            if DARK_MODE: webbrowser.open_new_tab(f"http://localhost:{PORT}/?__dark-theme=true")
            else: webbrowser.open_new_tab(f"http://localhost:{PORT}")
        threading.Thread(target=open, name="open-browser", daemon=True).start()
        threading.Thread(target=auto_update, name="self-upgrade", daemon=True).start()
        threading.Thread(target=warm_up_modules, name="warm-up", daemon=True).start()

    auto_opentab_delay()
    demo.queue(concurrency_count=CONCURRENT_COUNT).launch(server_name="0.0.0.0", server_port=PORT, auth=AUTHENTICATION, favicon_path="docs/logo.png")

    # 만약 2차 경로에서 실행이 필요하다면
    # CUSTOM_PATH, = get_conf('CUSTOM_PATH')
    # if CUSTOM_PATH != "/": 
    #     from toolbox import run_gradio_in_subpath
    #     run_gradio_in_subpath(demo, auth=AUTHENTICATION, port=PORT, custom_path=CUSTOM_PATH)
    # else: 
    #     demo.launch(server_name="0.0.0.0", server_port=PORT, auth=AUTHENTICATION, favicon_path="docs/logo.png")

if __name__ == "__main__":
    main()
