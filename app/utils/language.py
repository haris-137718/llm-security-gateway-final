from langdetect import detect

def detect_language(text: str) -> str:
    try:
        lang = detect(text[:300])
        lang_map = {'en': 'en', 'ur': 'ur', 'ko': 'ko'}
        return lang_map.get(lang, 'en')
    except:
        return 'en'
