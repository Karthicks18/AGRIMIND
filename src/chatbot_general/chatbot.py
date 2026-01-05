from src.chatbot_general.prompt import build_prompt
from src.chatbot_general.llm_engine import run_llama

def agriculture_chat(question: str) -> str:
    prompt = build_prompt(question)
    return run_llama(prompt)
