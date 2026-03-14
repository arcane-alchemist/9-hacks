"""Legal Health Check Analyzer using Groq LLM."""

import os
import json
from pydantic import BaseModel, Field
from typing import List, Dict

def evaluate_health_check(domain: str, answers: Dict[str, str]) -> dict:
    """
    Evaluates the yes/no answers using Groq to identify vulnerabilities.
    Returns a structured dictionary adhering to HealthCheckResponse.
    """
    from openai import OpenAI
    
    # Import the model for strict schema parsing
    from models import HealthCheckResponse
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
         raise ValueError("GROQ_API_KEY is not set.")
        
    client = OpenAI(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1"
    )

    # Format the user's answers into a readable string
    answers_str = "\n".join([f"Q: {q}\nA: {a}" for q, a in answers.items()])

    prompt = f"""
    You are a proactive Indian legal assistant evaluating a citizen's legal health in the domain of '{domain}'.
    The citizen was asked several foundational questions to identify missing legal protections.
    
    Here are their answers:
    {answers_str}

    Based strictly on these answers (pay close attention to any 'no' or 'not_sure' answers which represent severe missing paperwork or protections), identify:
    1. The critical vulnerabilities they currently face.
    2. A preventative action plan to fix these gaps.
    3. The applicable Indian laws related to these vulnerabilities.

    Output the result STRICTLY as a JSON object matching the below schema. 
    Ensure fields are arrays of strings. Do not include markdown formatting or extra dialogue.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a specialized legal health analyzer. Output ONLY valid JSON adhering strictly to the user's requested schema. No markdown backticks."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )

    try:
        content = response.choices[0].message.content
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Groq: {e}\nContent was: {response.choices[0].message.content}")
        return {
            "critical_vulnerabilities": ["Error generating report. Review manually."],
            "preventative_action_plan": [],
            "applicable_laws": []
        }
