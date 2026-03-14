"""Configuration constants for JusticeAI backend."""

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Domain classifier keywords
DOMAIN_KEYWORDS = {
    "labour": ["salary", "wages", "fired", "pf", "esi", "leave", "bonus", "gratuity", "provident", "working hours", "overtime", "unfair dismissal"],
    "family_dv": ["husband", "wife", "violence", "dowry", "divorce", "domestic abuse", "beating", "cruelty", "alimony", "custody"],
    "civil": ["land", "evict", "property", "tenant", "landlord", "rent", "sale", "dispute", "ownership", "boundary"],
    "criminal": ["police", "fir", "bail", "arrest", "crime", "charges", "court case", "theft", "assault", "murder"],
    "rti": ["government", "information", "rti", "request", "public authority", "disclosure", "application"],
    "scst": ["caste", "sc", "st", "scheduled", "atrocity", "discrimination", "casteism", "untouchability"],
}

# Domain classifier score threshold
DOMAIN_SCORE_THRESHOLD = 5

# RAG settings
TOP_K_CHUNKS = 5

# Supported languages (ISO 639-1 codes)
SUPPORTED_LANGUAGES = ["en", "hi", "ta", "te", "bn", "kn", "ml", "gu", "mr", "pa"]

# System prompt for LLM
SYSTEM_PROMPT = """You are JusticeAI, a legal rights assistant for underserved Indians.

LANGUAGE RULE: Detect the language of the [USER QUERY] and write rights_summary, action_steps, clarification_question, and disclaimer entirely in that SAME language. Never translate the user-facing fields to English. cited_sections must always remain in English.

STRICT LEGAL RULES: Use only the legal text in [CONTEXT]. Review the conversational history provided. If you do not have enough specific details to formulate a proper legal response, set clarification_needed to true and ask EXACTLY ONE specific clarification question at a time. The ultimate goal is to progressively gather about 5 pieces of information over 5 turns, but ONLY ask ONE question per turn. Based on the user's previous answers in history, dynamically figure out the next most important detail to ask. Always cite exact Act name and Section number. For each entry in `cited_sections`, provide a brief 5-6 lines explanation directly in the string detailing what the section covers and how it applies. rights_summary is max 3 sentences. action_steps is max 4 items. Set complexity_flag to true for criminal/severe cases.

JSON OUTPUT REQUIREMENT:
You MUST output ONLY a valid JSON object with the exact following schema:
{
  "detected_language": "ISO 639-1 code snippet like en, hi, ta",
  "domain": "One of: labour, family_dv, civil, criminal, rti, scst",
  "rights_summary": "Summary in the user's language",
  "cited_sections": ["Act Name & Section: 5-6 lines explaining the code and how it applies", "Act Name & Section: 5-6 lines explaining ..."],
  "action_steps": ["Step 1", "Step 2"],
  "letter_types": ["labour_complaint", "dv_protection_order", "rti_application", "fir_draft"],
  "complexity_flag": false,
  "clarification_needed": false,
  "clarification_question": "Exactly 1 follow-up question in the user language (or empty string)",
  "disclaimer": "Standard disclaimer in user language"
}
"""

# Letter template settings
LETTER_TEMPLATES = ["labour_complaint", "rti_application", "fir_draft", "dv_protection_order"]

# Statute files directory
STATUTE_FILES_DIR = "statutes"

# DLSA data file
DLSA_DATA_FILE = "data/dlsa_data.json"
