from flask import Blueprint, jsonify, request


# Blueprint for letter generation routes
letter_bp = Blueprint("letter_generator", __name__)


def _get_letter_template(language: str) -> str:
    """
    Return a basic complaint letter template for the specified language.

    This is a simple placeholder implementation that mimics what an AI
    or translation service might produce. The template includes a
    placeholder `{issue}` which will be filled with the user's issue.
    """
    language = (language or "").strip().lower()

    templates = {
        "english": (
            "To,\n"
            "The Concerned Authority,\n"
            "Subject: Complaint regarding {issue}.\n\n"
            "Respected Sir/Madam,\n\n"
            "I am writing this letter to formally lodge a complaint regarding {issue}. "
            "I request you to kindly look into this matter at the earliest and take "
            "appropriate legal action as per the applicable laws.\n\n"
            "Thank you.\n"
            "Yours faithfully,\n"
            "[Your Name]\n"
        ),
        "hindi": (
            "सेवा में,\n"
            "माननीय प्राधिकारी महोदय/महोदया,\n"
            "विषय: {issue} के संबंध में शिकायत।\n\n"
            "महोदय/महोदया,\n\n"
            "मैं यह पत्र {issue} के संबंध में औपचारिक शिकायत दर्ज करने के लिए लिख रहा/रही हूँ। "
            "कृपया आप इस मामले पर शीघ्र संज्ञान लेकर लागू कानूनों के अनुसार आवश्यक कानूनी "
            "कार्रवाई करने की कृपा करें।\n\n"
            "धन्यवाद।\n"
            "भवदीय,\n"
            "[आपका नाम]\n"
        ),
        "telugu": (
            "కు,\n"
            "గౌరవనీయ అధికారికి,\n"
            "విషయం: {issue} గురించి ఫిర్యాదు.\n\n"
            "మహోదయ/మహోదయీ,\n\n"
            "నేను ఈ లేఖను {issue} విషయంలో అధికారిక ఫిర్యాదు చేయడానికి రాస్తున్నాను. "
            "దయచేసి ఈ విషయాన్ని అత్యవసరంగా పరిగణించి, ప్రస్తుతం అమల్లో ఉన్న చట్టాల ప్రకారం "
            "అవసరమైన చర్యలు తీసుకోవాలని వినమ్రంగా కోరుకుంటున్నాను.\n\n"
            "ధన్యవాదాలు.\n"
            "మీది,\n"
            "[మీ పేరు]\n"
        ),
        "tamil": (
            "அனுப்புவோர்,\n"
            "கௌரவ அதிகாரி அவர்களுக்கு,\n"
            "பொருள்: {issue} குறித்து புகார்.\n\n"
            "மதிப்பிற்குரியவரே,\n\n"
            "மேலே குறிப்பிட்ட {issue} தொடர்பாக இந்தக் கடிதத்தின் மூலம் நான் "
            "அதிகாரப்பூர்வமான புகாரை வழங்குகிறேன். தயவுசெய்து இந்த விவகாரத்தை அவசரமாக "
            "கவனித்து, சம்பந்தப்பட்ட சட்ட விதிகளின்படி தேவையான நடவடிக்கை எடுக்குமாறு பணிவுடன் "
            "கோருகிறேன்.\n\n"
            "நன்றி.\n"
            "உங்கள் நம்பிக்கையுடன்,\n"
            "[உங்கள் பெயர்]\n"
        ),
    }

    # Fallback to English if language is not supported
    return templates.get(language, templates["english"])


def generate_complaint_letter(issue: str, language: str) -> str:
    """
    Generate a simple legal complaint letter text for the given issue
    in the requested language using the placeholder templates.
    """
    if not issue:
        issue = "legal complaint"

    template = _get_letter_template(language)
    return template.format(issue=issue)


@letter_bp.route("/generate-letter", methods=["POST"])
def generate_letter():
    """
    API endpoint:
    POST /generate-letter

    Expected JSON body:
    {
        "issue": "harassment complaint",
        "language": "telugu"
    }

    Supported languages:
    - english
    - hindi
    - telugu
    - tamil

    Returns:
    {
        "generated_letter": "translated complaint letter text"
    }
    """
    data = request.get_json(silent=True) or {}
    issue = data.get("issue", "")
    language = data.get("language", "english")

    letter_text = generate_complaint_letter(issue, language)
    return jsonify({"generated_letter": letter_text})

