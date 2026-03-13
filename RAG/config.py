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

STRICT LEGAL RULES: Use only the legal text in [CONTEXT]. If [CONTEXT] does not cover the query, set clarification_needed to true and ask one specific clarification_question. Always cite exact Act name and Section number. rights_summary is max 3 sentences. action_steps is max 4 items. Set complexity_flag to true for criminal/severe cases.

JSON OUTPUT REQUIREMENT:
You MUST output ONLY a valid JSON object with the exact following schema:
{
  "detected_language": "ISO 639-1 code snippet like en, hi, ta",
  "domain": "One of: labour, family_dv, civil, criminal, rti, scst",
  "rights_summary": "Summary in the user's language",
  "cited_sections": ["English citation 1", "English citation 2"],
  "action_steps": ["Step 1", "Step 2"],
  "letter_types": ["labour_complaint", "dv_protection_order", "rti_application", "fir_draft"],
  "complexity_flag": false,
  "clarification_needed": false,
  "clarification_question": "Question in user language (or empty string)",
  "disclaimer": "Standard disclaimer in user language"
}
"""

# Letter template settings
LETTER_TEMPLATES = ["labour_complaint", "rti_application", "fir_draft", "dv_protection_order"]

# Statute files directory
STATUTE_FILES_DIR = "statutes"

# DLSA data file
DLSA_DATA_FILE = "data/dlsa_data.json"
