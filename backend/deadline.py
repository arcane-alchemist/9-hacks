import re
from typing import Optional, Tuple
import dateparser
from fastapi import APIRouter
from pydantic import BaseModel

deadline_router = APIRouter()

class DeadlineRequest(BaseModel):
    text: str

def _find_relative_deadline(text: str) -> Optional[str]:
    """
    Try to find deadlines expressed relatively, such as:
    - "within 7 days"
    - "within 15 days"
    - "before 30 days"
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
            return match.group(0)
    return None

def _find_absolute_date(text: str) -> Optional[Tuple[str, str]]:
    """
    Try to find specific date expressions such as:
    - "12 March 2026"
    - "12/03/2026"
    - "12-03-2026"
    """
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

def extract_deadline(text: str) -> dict:
    if not text:
        return {"deadline_detected": False}

    relative = _find_relative_deadline(text)
    if relative:
        return {
            "deadline_detected": True,
            "deadline_text": relative.strip(),
        }

    absolute = _find_absolute_date(text)
    if absolute:
        original_text, normalized = absolute
        return {
            "deadline_detected": True,
            "deadline_text": original_text.strip(),
            "normalized_date": normalized,
        }

    return {"deadline_detected": False}

@deadline_router.post("/detect-deadline")
def detect_deadline(request: DeadlineRequest):
    """
    API endpoint to detect deadlines in legal text.
    """
    return extract_deadline(request.text)
