import os
import json
import google.generativeai as genai

def locate_specific_office(pincode: str, domain: str) -> dict:
    """
    Uses Gemini to determine the exact name of the authority/office
    a user should visit based on their case domain and pincode.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is required for office locator.")

    genai.configure(api_key=api_key)
    
    # We use flash since this is a simple fast logic task
    model = genai.GenerativeModel('gemini-2.5-flash')

    system_instruction = """
    You are an expert Indian Legal routing assistant. The user will provide a Pincode and a Case Domain (e.g. labour, family_dv, rti).
    Your job is to tell the user the exact specific Government or Legal Office they need to physically visit to file their complaint.
    
    DOMAIN MAPPING RULES:
    - If 'labour': They must go to the 'Office of the Labour Commissioner' or 'Deputy Labour Commissioner'.
    - If 'family_dv': They must go to the 'Local Magistrate Court', 'Mahila Thana (Women's Police Station)', or 'Protection Officer'.
    - If 'criminal': They must go to the 'Local Police Station' or 'Superintendent of Police'.
    - If 'rti': They must go to the 'Public Information Officer (PIO)' of the relevant department.
    - If 'civil': They must go to the 'Civil Court' or 'Sub-Divisional Magistrate'.
    - If 'scst': They must go to the 'Special Court (SC/ST Act)' or 'Superintendent of Police'.
    
    ADDRESS RULE:
    You must provide the most accurate address you know for that pincode. If you do not know the EXACT verified street address, DO NOT invent one. Instead, say "Local Office for [Pincode]" and provide a highly specific Google Maps search term so they can find it themselves.
    
    Return pure JSON only, matching this exact schema:
    {
      "office_name": "String (Name of the specific authority)",
      "address": "String (The address or 'Check Google Maps for exact location in [District name]')",
      "google_maps_search_term": "String (e.g. 'Labour Commissioner office near 400001')",
      "what_to_take_with_you": "String (List 3 things they MUST carry physically to the office based on the domain)"
    }
    """

    prompt = f"Pincode: {pincode}\nDomain: {domain}"

    try:
        response = model.generate_content(
            system_instruction + "\n\n" + prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        raise ValueError(f"Failed to locate office: {str(e)}")

