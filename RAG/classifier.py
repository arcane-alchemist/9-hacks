"""Domain classifier using keyword scoring (no ML model)."""

from config import DOMAIN_KEYWORDS, DOMAIN_SCORE_THRESHOLD


def classify_domain(text: str, situation_type: str = None) -> tuple[str, int, bool]:
    """
    Classify user query into one of six legal domains using keyword scoring.
    
    Args:
        text: Input text (query in any language, usually already detected)
        situation_type: Optional pre-selected domain from frontend
        
    Returns:
        Tuple of (domain, score, needs_clarification)
        - domain: One of 'labour', 'family_dv', 'civil', 'criminal', 'rti', 'scst'
        - score: Confidence score (higher is better)
        - needs_clarification: True if score is below threshold and no situation_type provided
    """
    # If situation_type provided, use it directly
    if situation_type and situation_type in DOMAIN_KEYWORDS:
        return situation_type, 100, False
    
    # Convert text to lowercase for keyword matching
    text_lower = text.lower()
    
    # Score each domain
    domain_scores = {}
    for domain, keywords in DOMAIN_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in text_lower:
                score += 1
        domain_scores[domain] = score
    
    # Find domain with highest score
    if not domain_scores or max(domain_scores.values()) == 0:
        # No keywords matched
        return "general", 0, True
    
    best_domain = max(domain_scores, key=domain_scores.get)
    best_score = domain_scores[best_domain]
    
    # Check if clarification is needed
    needs_clarification = best_score < DOMAIN_SCORE_THRESHOLD
    
    return best_domain, best_score, needs_clarification
