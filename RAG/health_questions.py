"""Legal Health Checkup Question Bank."""

# A statically defined set of questions mapped to different user personas/domains.
# In a real production system, this could be fetched from a database.

HEALTH_QUESTIONS = {
    "labour": [
        "Do you have a written employment contract or offer letter?",
        "Are you paid your salary directly into a bank account? (Not in cash)",
        "Does your employer provide you with regular salary slips/payslips?",
        "Are your working hours clearly documented and agreed upon?",
        "If you work overtime, are you compensated strictly according to rules?",
        "Is there a deduction made from your salary for PF (Provident Fund) or ESI?",
        "Have you been forced to submit original education certificates or passports to your employer?"
    ],
    "tenant": [
        "Do you have a written and signed rent agreement?",
        "Has the rent agreement been officially registered and notarized?",
        "Do you receive a formal receipt every time you pay rent?",
        "Is there a documented video/photo record of the property condition before you moved in?",
        "Does the agreement clearly specify the rules for deducting your security deposit?",
        "Does your landlord demand rent in pure cash without a digital paper trail?"
    ],
    "consumer": [
        "Did you receive a formally printed bill/invoice for your purchase?",
        "Does the product have a documented warranty or guarantee card?",
        "Was the payment made via digital means (UPI, Card, Bank Transfer) providing a receipt?",
        "Has the seller clearly stated the return or refund policy in writing?",
        "Did you buy the product from a registered entity (and not just an unverified social media page)?"
    ],
    "women": [
        "Do you have independent access to a bank account in your own name?",
        "Are your original educational and identity documents securely in your possession?",
        "If married, is your marriage officially registered with a marriage certificate?",
        "In your workplace, is there an officially established Internal Complaints Committee (ICC)?",
        "Are you aware of the local Women's Helpline numbers or nearest Mahila Thana?"
    ]
}

def get_questions_for_domain(domain: str) -> list[str]:
    """Return the predefined questions for a specific legal domain."""
    return HEALTH_QUESTIONS.get(domain.lower(), HEALTH_QUESTIONS.get("labour"))  # Default to labour
