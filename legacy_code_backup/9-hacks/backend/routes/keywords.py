from flask import Blueprint, jsonify, request

from utils.keyword_list import LEGAL_KEYWORDS


# Blueprint for keyword detection routes
keywords_bp = Blueprint("keywords", __name__)


def detect_keywords_in_text(text: str) -> list[str]:
    """
    Scan the provided text for legal keywords.

    Matching is case-insensitive and supports multi-word phrases
    such as "domestic violence".
    """
    if not text:
        return []

    lowered_text = text.lower()
    found = []

    for keyword in LEGAL_KEYWORDS:
        if keyword.lower() in lowered_text:
            found.append(keyword)

    # Remove duplicates while preserving order
    unique_found = list(dict.fromkeys(found))
    return unique_found


@keywords_bp.route("/detect-keywords", methods=["POST"])
def detect_keywords():
    """
    API endpoint:
    POST /detect-keywords

    Expected JSON body:
    {
        "text": "legal message"
    }

    Returns:
    {
        "keywords_found": ["harassment", "cybercrime"]
    }
    """
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")

    keywords_found = detect_keywords_in_text(text)
    return jsonify({"keywords_found": keywords_found})

