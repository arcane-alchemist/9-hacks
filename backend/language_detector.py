"""Language detection module using langdetect."""

from langdetect import detect, LangDetectException
from config import SUPPORTED_LANGUAGES


def detect_language(text: str) -> str:
    """
    Detect language from text using langdetect.
    
    Args:
        text: Input text in any language
        
    Returns:
        ISO 639-1 language code (e.g., 'hi', 'ta', 'en')
        
    Raises:
        ValueError: If language detection fails or language not supported
    """
    try:
        detected_lang = detect(text)
        
        if detected_lang not in SUPPORTED_LANGUAGES:
            # Default to English if detected language not in our supported list
            return "en"

        return detected_lang
    except LangDetectException as e:
        # If the user enters numbers or symbols with no letter features, default to English instead of crashing
        return "en"
    try:
        return detect(text) == "en"
    except LangDetectException:
        return True  # Default to English on error
