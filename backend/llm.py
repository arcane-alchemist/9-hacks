"""LLM integration with Groq."""

import json
import os
import re
from openai import OpenAI
from config import SYSTEM_PROMPT


def call_llm(user_query: str, context_chunks: list[dict], user_language: str, history: list[dict] = None) -> dict:
    """
    Call Groq with RAG context and get structured JSON response.

    Args:
        user_query: Original user query in their language (not translated)
        context_chunks: List of retrieved statute chunks
        user_language: ISO 639-1 language code of user query

    Returns:
        Parsed JSON response from LLM as dict

    Raises:
        ValueError: If LLM response is invalid JSON or parsing fails
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
        
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )

    # Build context string from retrieved chunks
    context_str = "\n---\n".join([
        f"Source: {chunk['source']}\n\n{chunk['content']}"
        for chunk in context_chunks
    ])

    # Build user message
    user_message = f"""[USER QUERY]\n{user_query}\n\n[CONTEXT]\n{context_str if context_str else 'No relevant statutes found in knowledge base.'}\n"""

    try:
        # Call Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
            ] + (history or []) + [ {"role": "user", "content": user_message}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        # Extract response content
        response_text = response.choices[0].message.content

        # Clean up any potential markdown code blocks
        cleaned_text = re.sub(r'^`json\s*', '', response_text, flags=re.MULTILINE)
        cleaned_text = re.sub(r'^`\s*$', '', cleaned_text, flags=re.MULTILINE)
        cleaned_text = cleaned_text.strip()

        # Parse JSON
        try:
            response_json = json.loads(cleaned_text)
            return response_json
        except json.JSONDecodeError as e:
            raise ValueError(f"LLM returned invalid JSON: {cleaned_text[:200]}... Error: {str(e)}")
    except Exception as e:
        raise ValueError(f"LLM call failed: {str(e)}")


def validate_response_schema(response: dict) -> bool:
    """
    Validate that LLM response contains all required fields.
    """
    required_fields = [
        "detected_language",
        "domain",
        "rights_summary",
        "cited_sections",
        "action_steps",
        "letter_types",
        "complexity_flag",
        "clarification_needed",
        "disclaimer"
    ]

    return all(field in response for field in required_fields)
