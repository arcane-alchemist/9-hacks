"""Legal document analyzer using Gemini Vision."""

import os
from pydantic import BaseModel, Field
import google.generativeai as genai

# Models
class DocumentAnalysisResponse(BaseModel):
    document_type: str = Field(..., description="The type of document (e.g., FIR, Eviction Notice, Employment Contract)")
    simple_summary: str = Field(..., description="A 2-3 sentence summary of what the document says in simple English")
    action_required: str = Field(..., description="Clear instructions on what the user needs to do next")
    is_urgent: bool = Field(..., description="True if the document requires immediate short-term action (e.g., court summons in 2 days)")
    urgency_reason: str = Field(default="", description="If urgent, briefly explain why. If not urgent, leave empty.")

def analyze_document(image_bytes: bytes, mime_type: str) -> dict:
    """
    Passes an uploaded image to Gemini to identify and summarize it.
    """
    # Ensure api key is configured
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if gemini_api_key:
        genai.configure(api_key=gemini_api_key)
    
    # We will use the 2.5-flash model as it fully supports powerful vision/multimodal reasoning
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = """
    You are an expert Indian Legal Assistant helping an underserved citizen understand a document they received.
    Analyze the uploaded image of the document carefully. Translate from regional languages if necessary.
    
    Please provide:
    1. The exact type or name of the document.
    2. A simple, easy-to-understand summary of what it means.
    3. The exact steps the user should take right now in response.
    4. Whether it is a time-critical emergency (e.g., an eviction tomorrow or an active warrant).
    
    Output strictly in the provided JSON schema.
    """
    
    image_part = {
        "mime_type": mime_type,
        "data": image_bytes
    }
    
    # Passing the prompt and the raw image bytes to Gemini, enforcing JSON output using the Pydantic schema
    response = model.generate_content(
        [prompt, image_part],
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=DocumentAnalysisResponse
        )
    )
    
    # Gemini returns a string representation of the JSON, so we just parse it
    import json
    return json.loads(response.text)
