"""
Central place to define legal keywords that the JusticeAI backend
will search for in incoming text. Includes helpers for definitions
and difficulty (e.g. Wikipedia summary, legal jargon flag).
"""

import json
import urllib.error
import urllib.parse
import urllib.request

# List of legal keywords/phrases to detect.
# This can be extended in the future as needed.
LEGAL_KEYWORDS = [
    "harassment",
    "fraud",
    "domestic violence",
    "cybercrime",
    "eviction",
    "complaint",
    "FIR",
]

# Terms often considered uncommon or legally technical; used for optional is_complex flag.
# Stored lowercase for case-insensitive matching.
LEGAL_JARGON_OR_HARD = {"fir", "eviction", "cybercrime", "domestic violence"}


def get_definition(keyword: str, max_chars: int = 300) -> str:
    """
    Fetch a short definition/description for a keyword using Wikipedia API.
    Returns a truncated extract or empty string on failure (no network, no page, etc.).
    """
    if not keyword or not keyword.strip():
        return ""
    # Wikipedia API expects title-style: capitalize words, spaces allowed (encoded).
    title = keyword.strip().replace(" ", "_")
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(title)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JusticeAI-Backend/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        extract = (data.get("extract") or "").strip()
        if extract and len(extract) > max_chars:
            extract = extract[: max_chars - 3] + "..."
        return extract
    except (urllib.error.URLError, OSError, json.JSONDecodeError, KeyError):
        return ""


def is_hard_or_uncommon(keyword: str) -> bool:
    """
    Return True if the keyword is considered legally technical or uncommon
    (based on a small predefined set). Can be extended with dictionary API later.
    """
    return keyword.strip().lower() in LEGAL_JARGON_OR_HARD

