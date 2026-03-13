"""Main FastAPI application for JusticeAI."""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

from models import QueryRequest, QueryResponse, GenerateLetterRequest, LetterResponse, DLSAResponse
from language_detector import detect_language
from translator import translate_to_english, translate_from_english
from classifier import classify_domain
from rag import RAGSystem
from llm import call_llm, validate_response_schema
from letter_generator import generate_letter
from dlsa_db import get_dlsa_by_pincode, get_dlsa_by_district
from config import LETTER_TEMPLATES
from office_locator import locate_specific_office
from models import OfficeLocatorRequest, OfficeLocatorResponse
from fastapi import File, UploadFile
from document_analyzer import analyze_document
from models import DocumentAnalysisResponse
from models import HealthCheckRequest, HealthCheckResponse
from health_analyzer import evaluate_health_check
from health_questions import get_questions_for_domain, HEALTH_QUESTIONS

from textbee_bot import textbee_router

rag_system = RAGSystem()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("ðŸš€ Starting JusticeAI backend...")
    rag_system.load_statutes()
    print("âœ“ RAG system initialized")
    yield
    print("ðŸ›‘ Shutting down JusticeAI backend...")

app = FastAPI(
    title="JusticeAI Backend",
    description="AI-powered legal companion for underserved Indians",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from textbee_bot import textbee_router
app.include_router(textbee_router)

app.include_router(textbee_router)

@app.get("/")
def root():
    return {
        "status": "running",
        "service": "JusticeAI Backend",
        "version": "1.0.0"
    }

@app.post("/query", response_model=QueryResponse)
def query_legal_issue(request: QueryRequest):
    try:
        user_language = detect_language(request.text)
        english_query = translate_to_english(request.text)
        domain, score, needs_clarification = classify_domain(english_query, request.situation_type)
        retrieved_chunks = rag_system.retrieve(english_query)
        llm_response = call_llm(request.text, retrieved_chunks, user_language)
        if not validate_response_schema(llm_response):
            raise ValueError("LLM response missing required fields")
        dlsa_office = None
        if request.pincode:
            dlsa_office = get_dlsa_by_pincode(request.pincode)
        llm_response["dlsa_office"] = dlsa_office
        return QueryResponse(**llm_response)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate-letter", response_model=LetterResponse)
def generate_letter_endpoint(request: GenerateLetterRequest):
    try:
        if request.type not in LETTER_TEMPLATES:
            raise ValueError(f"Invalid letter type.")
        letter_content = generate_letter(request.type, request.user_name, request.district, request.date, request.details)
        return LetterResponse(letter_content=letter_content, template_type=request.type)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/locate-office", response_model=OfficeLocatorResponse)
def locate_specific_office_endpoint(request: OfficeLocatorRequest):
    """Unified routing: Gets the domain-specific authority & the free DLSA safety net in one call."""
    try:
        # 1. Fetch domain-specific office via Gemini routing
        office_info = locate_specific_office(request.pincode, request.domain)
        
        # 2. Fetch fall-back safety net (Free DLSA clinic)
        office_info['dlsa_office'] = get_dlsa_by_pincode(request.pincode)
        
        return OfficeLocatorResponse(**office_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/analyze-document', response_model=DocumentAnalysisResponse)
async def analyze_document_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        analysis_result = analyze_document(contents, file.content_type)
        return DocumentAnalysisResponse(**analysis_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to analyze document: {str(e)}')


@app.get('/health-questions/{domain}')
def get_health_questions(domain: str):
    """Fetch the proactive health check questions for a specific domain."""
    if domain.lower() not in HEALTH_QUESTIONS:
        raise HTTPException(status_code=404, detail="Domain not found. Available domains: " + ", ".join(HEALTH_QUESTIONS.keys()))
    questions = get_questions_for_domain(domain)
    return {"domain": domain, "questions": questions}


@app.post('/health-check', response_model=HealthCheckResponse)
def evaluate_legal_health(request: HealthCheckRequest):
    """Submits the answers and generates a preventative action plan without a risk score."""
    try:
        result = evaluate_health_check(request.domain, request.answers)
        return HealthCheckResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Failed to evaluate health check: {str(e)}')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
