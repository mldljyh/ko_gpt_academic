# 'primary' 颜色对应 theme.py 中的 primary_hue
# 'secondary' 颜色对应 theme.py 中的 neutral_hue
# 'stop' 颜色对应 theme.py 中的 color_er
# 默认버튼 색상是 secondary
from toolbox import clear_line_break


def get_core_functions():
    return {
        "영어 학술 교정": {
            # 前言
            "Prefix":   r"Below is a paragraph from an academic paper. Polish the writing to meet the academic style, " +
                        r"improve the spelling, grammar, clarity, concision and overall readability. When necessary, rewrite the whole sentence. " +
                        r"Furthermore, list all modification and explain the reasons to do so in markdown table." + "\n\n",
            # 后语
            "Suffix":   r"",
            "Color":    r"secondary",    # 버튼 색상
        },
        "한국어 학술 교정": {
            "Prefix":   r"한국어 학술 논문 작성 개선 보조로서, 제공된 텍스트의 맞춤법, 문법, 명확성, 간결성 및 전체적인 가독성을 향상시키는 것이 당신의 임무입니다. " +
                        r"동시에, 긴 문장을 분할하고 중복을 줄이며 개선 제안을 제공해야 합니다. 텍스트의 수정 버전만 제공하고 설명은 포함하지 마십시오. 다음 텍스트를 편집하십시오." + "\n\n",
            "Suffix":   r"",
        },
        "문법 오류 찾기": {
            "Prefix":   r"Can you help me ensure that the grammar and the spelling is correct? " +
                        r"Do not try to polish the text, if no mistake is found, tell me that this paragraph is good." +
                        r"If you find grammar or spelling mistakes, please list mistakes you find in a two-column markdown table, " +
                        r"put the original text the first column, " +
                        r"put the corrected text in the second column and highlight the key words you fixed.""\n"
                        r"Example:""\n"
                        r"Paragraph: How is you? Do you knows what is it?""\n"
                        r"| Original sentence | Corrected sentence |""\n"
                        r"| :--- | :--- |""\n"
                        r"| How **is** you? | How **are** you? |""\n"
                        r"| Do you **knows** what **is** **it**? | Do you **know** what **it** **is** ? |""\n"
                        r"Below is a paragraph from an academic paper. "
                        r"You need to report all grammar and spelling mistakes as the example before."
                        + "\n\n",
            "Suffix":   r"",
            "PreProcess": clear_line_break,    # 预处理：清除换行符
        },
        "한영 번역": {
            "Prefix":   r"Please translate following sentence to English:" + "\n\n",
            "Suffix":   r"",
        },
        "학술 한영 상호 번역": {
            "Prefix":   r"I want you to act as a scientific English-Korean translator, " +
                        r"I will provide you with some paragraphs in one language " +
                        r"and your task is to accurately and academically translate the paragraphs only into the other language. " +
                        r"Do not repeat the original provided paragraphs after translation. " +
                        r"You should use artificial intelligence tools, " +
                        r"such as natural language processing, and rhetorical knowledge " +
                        r"and experience about effective writing techniques to reply. " +
                        r"I'll give you my paragraphs as follows, tell me what language it is written in, and then translate:" + "\n\n",
            "Suffix": "",
            "Color": "secondary",
        },
        "영한 번역": {
            "Prefix":   r"자연스러운 한국어로 번역해주세요：" + "\n\n",
            "Suffix":   r"",
        },
        "이미지 찾기": {
            "Prefix":   r"인터넷에서 이미지를 찾아주세요. Unsplash API(https://source.unsplash.com/960x640/?<英语关键词>)를 사용하여 이미지 URL을 가져와서 " +
                        r"Markdown 형식으로 포장하고 역슬래시나 코드 블록을 사용하지 않도록 해주세요. 이제 다음 설명을 따라 이미지를 보내주세요：" + "\n\n",
            "Suffix":   r"",
        },
        "코드 설명": {
            "Prefix":   r"다음 코드를 설명해주세요：" + "\n```\n",
            "Suffix":   "\n```\n",
        },
    }
