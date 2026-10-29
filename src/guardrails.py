import re
from pydantic import ValidationError
from src.schemas import CustomerInsight

MAX_INPUT_CHARS = 4000

class InputRejected(ValueError):
    pass

def validate_user_text(text: str) -> str:
    if not isinstance(text, str):
        raise InputRejected("Input must be text.")
    cleaned = text.strip()
    if not cleaned:
        raise InputRejected("Input cannot be empty.")
    if len(cleaned) > MAX_INPUT_CHARS:
        raise InputRejected(f"Input is too long (maximum {MAX_INPUT_CHARS} characters).")
    # This is a basic input hygiene check, not a complete prompt-injection defense.
    if re.search(r"(?i)(reveal|print|show)\s+(the\s+)?(api key|secret key|system prompt)", cleaned):
        raise InputRejected("Request appears to ask for secrets or internal instructions.")
    return cleaned

def validate_llm_result(payload) -> CustomerInsight:
    if isinstance(payload, CustomerInsight):
        payload = payload.model_dump()
    return CustomerInsight.model_validate(payload)
