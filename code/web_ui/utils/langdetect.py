from lingua import Language, LanguageDetectorBuilder
languages = [Language.ENGLISH, Language.FRENCH, Language.GERMAN, Language.SPANISH]
detector = LanguageDetectorBuilder.from_languages(*languages).build()

def detect_language(text):
    detected_language = detector.detect_language_of(text)
    if detected_language == Language.ENGLISH:
        return "English"
    elif detected_language == Language.FRENCH:
        return "French"
    elif detected_language == Language.GERMAN:
        return "German"
    elif detected_language == Language.SPANISH:
        return "Spanish"
    else:
        return "Unknown"