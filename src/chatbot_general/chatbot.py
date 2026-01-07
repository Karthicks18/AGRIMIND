from src.chatbot_general.openai_helper import ask_gpt

def agriculture_chat(user_query: str) -> str:
    """
    Central chatbot controller for AgriMind.
    Currently uses GPT-3.5 via OpenAI.
    Can be extended later with rule-based logic.
    """
    if not user_query or not user_query.strip():
        return "Please ask a valid agriculture-related question."

    return ask_gpt(user_query)
