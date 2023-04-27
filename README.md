**gpt_academy 한글화 프로젝트 입니다. gpt-3.5-turbo를 통해 번역하여 오역이 있을 수 있습니다.**

**기능 제안이나 버그 문의는 원 프로젝트인 gpt_academy로 부탁드립니다.**

**[gpt_academy](https://github.com/mldljyh/ko_gpt_academic/)**



> **노트**
>
> 이 프로젝트에서 사용하는 Gradio 구성 요소의 새로운 pip 패키지(Gradio 3.26~3.27)에는 심각한 버그가 있습니다. 따라서 설치할 때는 엄격히 requirements.txt에서 **지정된 version**을 선택하십시오.
> 
> `pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`
>


# <img src="docs/logo.png" width="40" > 학술용 GPT (ChatGPT Academic)


**이 프로젝트를 좋아한다면 Star를 주세요. 더 많은 유용한 학술 바로가기 또는 기능 플러그인을 고안한 경우, issues 또는 pull requests를 부담없이 오픈하세요.**

 이 프로젝트의 README는 [영어|](docs/README_EN.md)[일본어|](docs/README_JP.md)[러시아|](docs/README_RS.md)[프랑스어](docs/README_FR.md)에 의해 자체 번역되었습니다.

> **노트**
>
> 1. **빨간색**으로 표시된 기능 플러그인(버튼)만 파일 읽기를 지원합니다. 일부 플러그인은 플러그인 영역의 **드롭다운 메뉴**에 있습니다. 또한 새로운 플러그인의 PR도 **최우선**으로 환영합니다!
>
> 2. 이 프로젝트의 각 파일 기능은 자체 분석 보고서 [`self_analysis.md`](https://github.com/binary-husky/chatgpt_academic/wiki/chatgpt-academic%E9%A1%B9%E7%9B%AE%E8%87%AA%E8%AF%91%E8%A7%A3%E6%8A%A5%E5%91%8A)에서 자세히 설명되어 있습니다. version이 업데이트되면서 언제든지 관련 기능 플러그인을 클릭하여 GPT를 호출하여 프로젝트의 자체 분석 보고서를 다시 생성할 수 있습니다. 일반적인 문제는 [`위키`](https://github.com/binary-husky/chatgpt_academic/wiki/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98)에서 확인할 수 있습니다.
>
> 3. OpenAI 및 API2D의 API 키 공존이 지원되며 구성 파일에 `API_KEY="openai-key1,openai-key2,api2d-key3"`와 같이 입력할 수 있습니다. `API_KEY`를 일시적으로 변경해야 할 때는 입력 영역에서 일시적인 `API_KEY`를 입력한 후 엔터 키를 누르면 적용됩니다.



<div align="center">

기능 | 설명
--- | ---
원 키 편집 | 원 키 편집, 논문 문법 오류 검색을 지원합니다.
원 키 한영 상호 번역 | 원 키 한영 상호 번역 지원 
원 키 코드 해석 | 코드 표시, 코드 해석, 코드 생성, 코드에 주석 추가
[사용자 정의 단축키](https://www.bilibili.com/video/BV14s4y1E7jN) | 사용자 정의 단축키 지원
모듈화 디자인 | 사용자 정의 강력한 [ 기능 플러그인](https://github.com/binary-husky/chatgpt_academic/tree/master/crazy_functions)을 지원하며 플러그인은 [ 핫 업데이트](https://github.com/binary-husky/chatgpt_academic/wiki/%E5%87%BD%E6%95%B0%E6%8F%92%E4%BB%B6%E6%8C%87%E5%8D%97)를 지원합니다.
[자체 프로그램 분석](https://www.bilibili.com/video/BV1cj411A7VW) | [기능 플러그인] [원 키 이해](https://github.com/binary-husky/chatgpt_academic/wiki/chatgpt-academic%E9%A1%B9%E7%9B%AE%E8%87%AA%E8%AF%91%E8%A7%A3%E6%8A%A5%E5%91%8A) 이 프로젝트의 소스 코드 
[프로그램 분석](https://www.bilibili.com/video/BV1cj411A7VW) | [기능 플러그인] 원 키 다른 Python/C/C++/Java/Lua/... 프로젝트 트리를 분석할 수 있습니다.
논문 읽기, 번역 | [기능 플러그인] LaTeX/pdf 논문 전문을 원 키로 읽고 요약을 생성합니다.
LaTeX [번역](https://www.bilibili.com/video/BV1nk4y1Y7Js/), [편집](https://www.bilibili.com/video/BV1FT411H7c5/) | [기능 플러그인] LaTeX 논문을 한 번에 번역하거나 편집 할 수 있습니다.
일괄 주석 생성 | [기능 플러그인] 함수 주석을 일괄 생성 할 수 있습니다.
Markdown [한-영 번역](https://www.bilibili.com/video/BV1yo4y157jV/) | [기능 플러그인] 상단에서 5 가지 언어의 [README](https://github.com/binary-husky/chatgpt_academic/blob/master/docs/README_EN.md)를 본 적이 있나요?
chat 분석 보고서 생성 | [기능 플러그인] 실행 후 요약 보고서를 자동으로 생성합니다.
[PDF 논문 번역 기능](https://www.bilibili.com/video/BV1KT411x7Wn) | [기능 플러그인] PDF 논문 제목 및 요약 추출 + 전체 문서 번역 (다중 스레드)
[Arxiv 도우미](https://www.bilibili.com/video/BV1LM4y1279X) | [기능 플러그인] arxiv 글 URL을 입력하면 요약을 한 번에 번역하고 PDF를 다운로드 할 수 있습니다.
[Google Scholar 통합 도우미](https://www.bilibili.com/video/BV19L411U7ia) | [기능 플러그인] 임의의 Google Scholar 검색 페이지 URL을 제공하면 GPT가 작성하는 [연관 작업](https://www.bilibili.com/video/BV1GP411U7Az/)을 지원합니다.
인터넷 정보 집합 + GPT | [기능 플러그인] GPT가 인터넷에서 정보를 가져 와서 답변하게하여 정보가 영원히 올바르지 않도록 합니다.
식 / 이미지 / 표시 | 동시에 [TeX 형식과 렌더링 형식](https://user-images.githubusercontent.com/96192199/230598842-1d7fcddd-815d-40ee-af60-baf488a199df.png)으로 공식을 표시 할 수 있습니다. 공식, 코드 강조를 지원합니다.
다중 스레드 기능 플러그인 지원 | 다중 스레드로 chatgpt를 호출하는 것을 지원하여 대용량 텍스트 또는 프로그램을 한 번에 처리 할 수 있습니다.
무채색 gradio [테마](https://github.com/binary-husky/chatgpt_academic/issues/173) 시작 | 브라우저 url 뒤에 ```/?__dark-theme=true```를 추가하여 dark 테마로 전환 할 수 있습니다.
[여러 LLM 모델](https://www.bilibili.com/video/BV1wT411p7yf) 지원, [API2D](https://api2d.com/) 인터페이스 지원 | GPT3.5, GPT4 및 [Tsinghua ChatGLM](https://github.com/THUDM/ChatGLM-6B)에 모두 서비스되는 느낌은 좋을 것입니다.
더 많은 LLM 모델 연결 | Newbing 테스트 인터페이스 (새로운 Bing AI) 추가
…… | ……

</div>

- 새 인터페이스 (`config.py`에서 LAYOUT 옵션을 수정하여 "좌우 레이아웃"과 "상하 레이아웃"으로 전환 할 수 있음)
<div align="center">
<img src="https://user-images.githubusercontent.com/96192199/230361456-61078362-a966-4eb5-b49e-3c62ef18b860.gif" width="700" >
</div>


- 모든 버튼은 functional.py를 동적으로 읽어 사용자 정의 기능을 쉽게 추가 할 수 있으며 클립 보드를 해제합니다.
<div align="center">
<img src="https://user-images.githubusercontent.com/96192199/231975334-b4788e91-4887-412f-8b43-2b9c5f41d248.gif" width="700" >
</div>

- 경화 / 오류 수정
<div align="center">
<img src="https://user-images.githubusercontent.com/96192199/231980294-f374bdcb-3309-4560-b424-38ef39f04ebd.gif" width="700" >
</div>


- 수식이 포함된 출력인 경우, tex 형식과 렌더링 형식 모두 표시되어 복사 및 읽기가 용이합니다.
<div align="center">
<img src="https://user-images.githubusercontent.com/96192199/230598842-1d7fcddd-815d-40ee-af60-baf488a199df.png" width="700" >
</div>

- 프로젝트 코드를 보기 귀찮으세요? Chatgpt에 직접 프로젝트를 말해보세요
<div align="center">
<img src="https://user-images.githubusercontent.com/96192199/226935232-6b6a73ce-8900-4aee-93f9-733c7e6fef53.png" width="700" >
</div>

- 여러 대형 언어 모델의 혼합 호출(ChatGLM + OpenAI-GPT3.5 + [API2D](https://api2d.com/)-GPT4)
<div align="center">
<img src="https://user-images.githubusercontent.com/96192199/232537274-deca0563-7aa6-4b5d-94a2-b7c453c47794.png" width="700" >
</div>

---

## 설치 방법1: 직접 실행하기 (Windows, Linux 또는 MacOS)

1. 프로젝트 다운로드
```sh
git clone https://github.com/mldljyh/ko_gpt_academic.git
cd chatgpt_academic
```

2. API_KEY 구성

`config.py`에서 API KEY 등을 구성하십시오. [설정](https://github.com/binary-husky/gpt_academic/issues/1) .

(P.S. 프로그램 실행시 이름이 `config_private.py`인 개인 설정 파일이 있는지 우선적으로 검사하고 해당 파일의 구성으로 `config.py`의 동일한 구성을 덮어씁니다. 따라서 구성 읽기 논리를 이해할 수 있다면 `config.py`의 옆에 새 구성 파일 인 `config_private.py`을 만들고 `config.py`의 동일한 구성을 `config_private.py`에 복사하는 것이 좋습니다. `config_private.py`은 git으로 관리되지 않으므로 개인 정보를 더 안전하게 보호할 수 있습니다.)

3. 종속성 설치
```sh

# (선택1: python이 익숙한 경우) 추천

python -m pip install -r requirements.txt
# 참고: 공식 pip source 또는 Ali pip source를 사용하세요. 다른 pip sources(일부 대학의 pip)에서 문제가 발생할 수 있습니다. 일시적으로 pip source를 변경하는 방법: python -m pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# (선택2: python이 익숙하지 않은 경우) anaconda를 사용하여 단계도 유사합니다:
# (II-1)conda create -n gptac_venv python=3.11
# (II-2)conda activate gptac_venv
# (II-3)python -m pip install -r requirements.txt
```

화보협력 ChatGLM 백엔드를 지원하려면 추가 종속성을 설치해야 합니다(전제 조건: python에 익숙하고 컴퓨터 구성이 충분함):
```sh
python -m pip install -r request_llm/requirements_chatglm.txt
```

4. 실행
```sh
python main.py
```

5. 테스트 함수 플러그인
```
- 테스트 함수 플러그인 템플릿 함수 (GPT가 무슨 일이 일어났는지 대답하는 것이 필요합니다).이 함수를 기반으로 보다 복잡한 기능을 구현할 수 있습니다. "[함수 플러그인 템플릿 데모] 오늘은 무슨일이 일어났나요?"
```

## 설치 방법2: 도커 사용

1. ChatGPT 만 (대부분의 사람들이 선택할 것을 권장합니다.)

``` sh
# 프로젝트 다운로드
git clone https://github.com/mldljyh/ko_gpt_academic.git
cd chatgpt_academic
# "Proxy", "API_KEY" 및 "WEB_PORT"(예: 50923) 등을 구성합니다.
config.py를 임의의 텍스트 편집기로 편집합니다.
# 설치
docker build -t gpt-academic .
# (마지막 단계-선택1) Linux 환경에서 --net=host 옵션을 사용하는 것이 더 편리합니다.
docker run --rm -it --net=host gpt-academic
# (마지막 단계-선택2) macOS/Windows 환경에서는 컨테이너의 포트(예:50923)를 호스트의 포트에 노출하여 -p 옵션을 사용할 수 있습니다.
docker run --rm -it -p 50923:50923 gpt-academic
```

2. ChatGPT + ChatGLM(Docker에 익숙하고 Dockerfile을 이해하고 충분한 컴퓨터 구성이 필요합니다.)

``` sh
# Dockerfile 수정
cd docs && nano Dockerfile+ChatGLM
# 빌드 (Dockerfile+ChatGLM은 docs 경로에 있으며, cd docs 가 주의 사항입니다.)
docker build -t gpt-academic --network=host -f Dockerfile+ChatGLM .
# 실행 (1) 직접 실행하기:
docker run --rm -it --net=host --gpus=all gpt-academic
# 실행 (2) 컨테이너에 진입하여 조정한 후 실행하려면:
docker run --rm -it --net=host --gpus=all gpt-academic bash
```

## 설치 - 방법 3 : 다른 배포 방식 (클라우드 서버 지식과 경험이 필요)

1. 원격 클라우드 서버 배포
[배포 위키-1] (https://github.com/binary-husky/chatgpt_academic/wiki/Cloud-Server-Remote-Deploy-Guide)

2. WSL2 사용 (Windows Subsystem for Linux 서브 시스템)
[배포 위키-2] (https://github.com/binary-husky/chatgpt_academic/wiki/WSL2-Deploy-Guide)

3. 2차 URL (예: `http://localhost/subpath`)에서 실행하는 방법
[FastAPI 실행 안내서] (docs / WithFastapi.md)를 방문하세요.

---

## 새로운 편의 버튼 / 사용자 정의 함수 플러그인 만들기

1. 새로운 편의 버튼 (학술 바로 가기 키) 사용자 정의
임의의 텍스트 편집기를 열고 `core_functional.py`를 열어 다음 항목을 추가하고 프로그램을 다시 시작하십시오. (버튼이 이미 추가되고 볼 수 있으면 프리픽스 및 서픽스가 모두 핫 수정을 지원하므로 프로그램을 다시 시작하지 않고도 즉시 작동합니다.)
예 :
```
"코드 한국어 번역" : {
     # 접두사는 당신의 요구를 설명하는 데 사용됩니다. 예를 들어 번역, 코드 해석, 양식 완성 등
     "Prefix": "다음 내용을 한국어로 번역하고 전문용어가 나오면 마크다운 테이블로 하나씩 설명하십시오 :\n\n",

     # 서픽스는 접두사와 함께 입력 내용을 따옴표로 묶기위한 것입니다.
     "Suffix": "",
},
```
<div align = "center">
<img src = "https://user-images.githubusercontent.com/96192199/226899272-477c2134-ed71-4326-810c-29891fe4a508.png" width = "500">
</div>


2. 사용자 정의 함수 플러그인
강력한 기능을 실행하는 사용자 정의 함수 플러그인을 작성하십시오.
이 프로젝트의 플러그인 작성 및 디버깅은 기술적으로 어렵지 않으며 Python의 기본지식만 있으면 제공된 템플릿을 모방하여 자신의 플러그인 기능을 구현할 수 있습니다.
자세한 내용은 [함수 플러그인 가이드](https://github.com/binary-husky/chatgpt_academic/wiki/%ED%95%A8%EC%88%98-%ED%94%8C%EB%9F%AC%EA%B7%B8%EC%9D%B8-%EA%B0%80%EC%9D%B4%EB%93%9C)를 참조하십시오.

## version :
- version 3.5(Todo): 자연어로 이 프로젝트의 모든 함수 플러그인을 호출하는 기능 추가(우선 순위 높음)
- version 3.4(Todo): ChatGPT LM 대규모 모델의 로컬 다중 스레드 지원 개선
- version 3.3: +인터넷 정보 통합 기능
- version 3.2: 함수 플러그인이 더 많은 매개 변수 인터페이스를 지원합니다 (대화 저장 기능, 모든 언어 코드 해석 + 동시에 임의의 LLM 조합 요청)
- version 3.1: 여러 GPT 모델을 동시에 쿼리하는 기능 지원! API2D 지원, 여러 apikey의 부하 분산도 지원합니다.
- version 3.0: chatglm 및 기타 소형 llm 지원
- version 2.6: 플러그인 구조 재구성, 상호 작용 향상, 더 많은 플러그인 추가
- version 2.5: 자동 업데이트, 긴 프로젝트 소스 코드를 요약 할 때 텍스트가 너무 길고 토큰이 넘침 문제 해결
- version 2.4: (1) PDF 전체 문서 번역 기능 추가; (2) 위치 전환 입력 기능 추가; (3) 수직 레이아웃 옵션 추가; (4) 멀티 스레드 함수 플러그인 최적화.
- version 2.3: 멀티 스레드 상호 작용 강화
- version 2.2: 함수 플러그인을 지원하는 핫 리로드
- version 2.1: 축소 가능한 레이아웃
- version 2.0: 모듈식 함수 플러그인 도입
- version 1.0: 기본 기능


```
코드는 다른 많은 우수한 프로젝트의 디자인을 참고했습니다. 주요 내용은 다음과 같습니다 :

# 참조 프로젝트 1 : ChuanhuChatGPT에서 여러 기술을 참고했습니다.
https://github.com/GaiZhenbiao/ChuanhuChatGPT

# 참조 프로젝트 2 : Tsinghua ChatGLM-6B :
https://github.com/THUDM/ChatGLM-6B
```

