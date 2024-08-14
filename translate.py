from googletrans import Translator
from pypinyin import pinyin, Style

def translate(text):
    translator = Translator()
    input_lang = translator.detect(text).lang

    try:
        zh = translator.translate(text, src=input_lang, dest='zh-cn')
        zh = ''.join([p[0] for p in pinyin(zh.text, style=Style.NORMAL)])

        translations = {
            'English': text,
            'Chinese': zh,
            'Latin': translator.translate(text, src=input_lang, dest='la').text,
            'Esperanto': translator.translate(text, src=input_lang, dest='eo').pronunciation or text,
            'Russian': translator.translate(text, src=input_lang, dest='ru').pronunciation or text,
            'Hindi': translator.translate(text, src=input_lang, dest='hi').pronunciation or text,
            'Arabic': translator.translate(text, src=input_lang, dest='ar').pronunciation or text,
            'Finnish': translator.translate(text, src=input_lang, dest='fi').text,
            'Swahili': translator.translate(text, src=input_lang, dest='sw').text
        }

    except Exception as e:
        return {"Error": str(e)}

    return translations
