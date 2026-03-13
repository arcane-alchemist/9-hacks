"""Translation module using deep-translator."""

from deep_translator import GoogleTranslator
from language_detector import detect_language


def translate_to_english(text: str) -> str:
    """
    Translate text to English using Google Translate.
    
    Args:
        text: Text in any language (detected automatically)
        
    Returns:
        Translated text in English
        
    Raises:
        ValueError: If translation fails
    """
    try:
        # Detect source language
        source_lang = detect_language(text)
        
        if source_lang == "en":
            return text  # Already in English
        
        # Translate to English
        translator = GoogleTranslator(source_language=source_lang, target_language="en")
        translated_text = translator.translate(text)
        
        return translated_text
    except Exception as e:
        raise ValueError(f"Translation failed: {str(e)}")


def translate_from_english(text: str, target_lang: str) -> str:
    """
    Translate text from English to target language.
    
    Args:
        text: Text in English
        target_lang: ISO 639-1 code of target language
        
    Returns:
        Translated text
        
    Raises:
        ValueError: If translation fails
    """
    if target_lang == "en":
        return text  # Already in English
    
    try:
        translator = GoogleTranslator(source_language="en", target_language=target_lang)
        translated_text = translator.translate(text)
        return translated_text
    except Exception as e:
        raise ValueError(f"Translation to {target_lang} failed: {str(e)}")
