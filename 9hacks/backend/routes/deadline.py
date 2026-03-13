import re
from datetime import datetime, timezone
from typing import Optional, Tuple

from flask import Blueprint, jsonify, request
import dateparser


# Blueprint for deadline-related routes
deadline_bp = Blueprint("deadline", __name__)

# Threshold in days: deadlines within this many days are marked critical
CRITICAL_DEADLINE_DAYS = 45


def _find_relative_deadline(text: str) -> Optional[str]:
    """
    Try to find deadlines expressed relatively, such as:
    - "within 7 days"
    - "within 15 days"
    - "before 30 days"

    Returns the matched phrase text if found, else None.
    """
    patterns = [
        r"\bwithin\s+(\d+)\s+days?\b",
        r"\bwithin\s+(\d+)\s+calendar\s+days?\b",
        r"\bbefore\s+(\d+)\s+days?\b",
        r"\bnot later than\s+(\d+)\s+days?\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            # Return the exact phrase that indicates the deadline
            return match.group(0)

    return None


def _find_absolute_date(text: str) -> Optional[Tuple[str, str]]:
    """
    Try to find specific date expressions such as:
    - "12 March 2026"
    - "12/03/2026"
    - "12-03-2026"

    Returns a tuple of (matched_text, normalized_date_string) if found, else None.
    """
    # Common day-month-year formats (with month name)
    month_names = (
        "January|February|March|April|May|June|July|August|September|October|November|December|"
        "Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
    )

    patterns = [
        rf"\b(\d{{1,2}}\s+(?:{month_names})\s+\d{{4}})\b",
        r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            raw_date = match.group(1)
            parsed = dateparser.parse(raw_date)
            if parsed:
                # Normalize the parsed date in ISO format for consistency
                normalized = parsed.strftime("%Y-%m-%d")
                return match.group(0), normalized

    return None


def _extract_days_from_relative(relative_phrase: str) -> Optional[int]:
    """
    Extract numeric days from a relative deadline phrase (e.g. "within 15 days" -> 15).
    Used to determine if deadline is critical (<= 45 days).
    """
    match = re.search(r"\b(\d+)\s+days?\b", relative_phrase, re.IGNORECASE)
    return int(match.group(1)) if match else None


def _is_absolute_date_within_days(normalized_date_str: str, within_days: int) -> bool:
    """
    Return True if the given ISO date (YYYY-MM-DD) is within `within_days` from today.
    """
    try:
        deadline_date = datetime.strptime(normalized_date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = (deadline_date - now).days
        return 0 <= delta <= within_days
    except (ValueError, TypeError):
        return False


def _is_critical_deadline(
    text: str,
    relative_phrase: Optional[str],
    absolute_normalized: Optional[str],
) -> bool:
    """
    Mark as critical if text says "urgent" or deadline is within CRITICAL_DEADLINE_DAYS (45).
    """
    # Explicit urgency in text
    if re.search(r"\burgent\b", text, re.IGNORECASE):
        return True
    # Relative deadline within 45 days
    if relative_phrase:
        days = _extract_days_from_relative(relative_phrase)
        if days is not None and days <= CRITICAL_DEADLINE_DAYS:
            return True
    # Absolute date within 45 days from today
    if absolute_normalized and _is_absolute_date_within_days(absolute_normalized, CRITICAL_DEADLINE_DAYS):
        return True
    return False


def extract_deadline(text: str) -> dict:
    """
    High-level helper to extract deadline-related information from text.

    Returns a JSON-serializable dictionary:
    - If deadline found:
      {"deadline_detected": True, "deadline_text": "within 7 days"}
      or for absolute dates:
      {"deadline_detected": True, "deadline_text": "12 March 2026", "normalized_date": "2026-03-12"}
    - If none found:
      {"deadline_detected": False}
    """
    if not text:
        return {"deadline_detected": False}

    # First search for relative deadline phrases
    relative = _find_relative_deadline(text)
    if relative:
        critical = _is_critical_deadline(text, relative, None)
        return {
            "deadline_detected": True,
            "deadline_text": relative.strip(),
            "critical": critical,
        }

    # Next search for specific date expressions
    absolute = _find_absolute_date(text)
    if absolute:
        original_text, normalized = absolute
        critical = _is_critical_deadline(text, None, normalized)
        return {
            "deadline_detected": True,
            "deadline_text": original_text.strip(),
            "normalized_date": normalized,
            "critical": critical,
        }

    # No deadline found
    return {"deadline_detected": False}


@deadline_bp.route("/detect-deadline", methods=["POST"])
def detect_deadline():
    """
    API endpoint:
    POST /detect-deadline

    Expected JSON body:
    {
        "text": "legal message text"
    }

    Returns a JSON response with detected deadline information.
    """
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")

    result = extract_deadline(text)
    return jsonify(result)

