from src.chatbot_general.openai_helper import ask_gpt

def agriculture_chat(user_query: str) -> str:
    if not user_query or not user_query.strip():
        return "Please ask a valid agriculture-related question."

    return ask_gpt(user_query)
