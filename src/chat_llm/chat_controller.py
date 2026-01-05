# ===========================================
# AgriMind – General Chat Controller
# ===========================================
from src.chat_llm.prompt_templates import build_prompt
from src.chat_llm.llm_engine import run_llama

def generate_chat_response(user_query: str) -> str:
    prompt = build_prompt(user_query)
    return run_llama(prompt)
