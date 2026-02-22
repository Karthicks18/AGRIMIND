import requests

RASA_URL = "http://localhost:5005/webhooks/rest/webhook"

def ask_rasa(message: str) -> str:
    try:
        res = requests.post(
            RASA_URL,
            json={"sender": "farmer", "message": message},
            timeout=5
        )
        replies = res.json()
        if replies:
            return replies[0].get("text", "Please rephrase your question.")
        return "I could not understand. Please ask about crops or fertilizers."
    except Exception:
        return "Chatbot service temporarily unavailable."
