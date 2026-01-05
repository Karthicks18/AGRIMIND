def handle_chat(query, context):
    """
    Simple AI chatbot logic that responds based on keywords.
    Later, this can be extended with NLP or fine-tuned models.
    """
    query = query.lower()

    if "crop" in query:
        return "You can use the Crop Recommendation module to know which crop suits your area and soil."
    elif "fertilizer" in query:
        return "Use the Fertilizer module for NPK guidance and dosage suggestions."
    elif "weather" in query:
        return "Weather affects yield heavily — try viewing live conditions in your district."
    elif "market" in query or "price" in query:
        return "Market data integration is coming soon to show live crop price trends."
    else:
        return "I’m AgriMind Assistant 🌾 — ask me about crops, fertilizers, or farming tips."
