"""Pydantic models for request/response validation."""

from typing import Optional, List
from pydantic import BaseModel, Field


# ==================== REQUEST MODELS ====================

class QueryRequest(BaseModel):
    """Schema for POST /query endpoint."""
    text: str = Field(..., description="User's legal query in any supported language")
    pincode: Optional[str] = Field(None, description="Optional pincode for DLSA lookup")
    history: Optional[List[dict]] = Field(default_factory=list, description="Chat loop")
    situation_type: Optional[str] = Field(
        None, 
        description="Optional pre-selected domain from frontend"
    )


class GenerateLetterRequest(BaseModel):
    """Schema for POST /generate-letter endpoint."""
    type: str = Field(..., description="Letter type: labour_complaint, rti_application, fir_draft, dv_protection_order")
    user_name: str = Field(..., description="Name of the applicant/complainant")
    district: str = Field(..., description="District name")
    date: str = Field(..., description="Date in DD-MM-YYYY format")
    details: str = Field(..., description="Specific details/facts to include in the letter")


# ==================== RESPONSE MODELS ====================

class DLSAOffice(BaseModel):
    """DLSA office details."""
    name: str
    address: str
    phone: str
    timings: str
    free: bool = True


class QueryResponse(BaseModel):
    """Schema for POST /query response."""
    detected_language: str = Field(..., description="ISO 639-1 language code")
    domain: str = Field(..., description="Classified domain")
    rights_summary: str = Field(..., description="Summary of legal rights (in user's language)")
    cited_sections: List[str] = Field(..., description="List of cited law sections (always in English)")
    action_steps: List[str] = Field(..., description="Max 4 action steps (in user's language)")
    letter_types: List[str] = Field(..., description="Suggested letter templates")
    dlsa_office: Optional[DLSAOffice] = Field(None, description="Nearest DLSA office if pincode provided")
    complexity_flag: bool = Field(..., description="True if case is complex (criminal, bodily harm, high property)")
    clarification_needed: bool = Field(..., description="True if more info is needed")
    clarification_question: Optional[str] = Field(None, description="Question in user's language if clarification needed")
    disclaimer: str = Field(..., description="Legal disclaimer (in user's language)")
    deadline: Optional[str] = Field(None, description="Extracted deadline if any")


class LetterResponse(BaseModel):
    """Schema for POST /generate-letter response."""
    letter_content: str = Field(..., description="Formatted letter ready to use")
    template_type: str = Field(..., description="Which template was used")


class DLSAResponse(BaseModel):
    """Schema for GET /dlsa/{pincode} response."""
    found: bool
    office: Optional[DLSAOffice] = None
    message: Optional[str] = None


class OfficeLocatorRequest(BaseModel):
    """Schema for POST /locate-office endpoint."""
    pincode: str = Field(..., description="User's 6-digit pincode")
    domain: str = Field(..., description="The legal domain (e.g. labour, family_dv) to determine which authority to route to.")

class OfficeLocatorResponse(BaseModel):
    """Schema for POST /locate-office response."""
    office_name: str = Field(..., description="Name of the specific authority")
    address: str = Field(..., description="Approximate address or instruction to use maps")
    google_maps_search_term: str = Field(..., description="Exact string to ping Google maps with")
    what_to_take_with_you: str = Field(..., description="List of physical documents to carry")
    dlsa_office: Optional[DLSAOffice] = Field(None, description="Nearest DLSA office for free legal aid fallback")



class DocumentAnalysisResponse(BaseModel):
    document_type: str = Field(..., description="Type of document (e.g. FIR, Notice)")
    simple_summary: str = Field(..., description="Summary in simple language")
    action_required: str = Field(..., description="Actions the user should take")
    is_urgent: bool = Field(..., description="True if action is needed immediately")
    urgency_reason: str = Field(default="", description="Explanation of why it is urgent")


from typing import Dict

class HealthCheckRequest(BaseModel):
    domain: str = Field(..., description="The domain for the health check (e.g. labour, tenant, consumer)")
    answers: Dict[str, str] = Field(..., description="Dictionary mapping the exact question string to yes/no/not_sure")

class HealthCheckResponse(BaseModel):
    critical_vulnerabilities: List[str] = Field(..., description="List of immediate risks identified from their answers")
    preventative_action_plan: List[str] = Field(..., description="Actionable bullet points on how to fix these gaps now")
    applicable_laws: List[str] = Field(..., description="The specific Indian acts involved based on the missing documentation")
