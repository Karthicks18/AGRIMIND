from src.chatbot_general.openai_helper import ask_gpt

def agriculture_chat(query: str) -> str:
    return ask_gpt(query)

def agriculture_chat(user_query: str):
    # 1️⃣ Rule-based answers first
    local_answer = rule_based_answer(user_query)
    if local_answer:
        return local_answer

    # 2️⃣ GPT fallback
    gpt_reply = ask_gpt35(user_query)
    if gpt_reply:
        return gpt_reply

    # 3️⃣ Final fallback
    return "Based on available data, please consult local agricultural officers for best advice."
