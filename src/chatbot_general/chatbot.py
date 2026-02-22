def agriculture_chat(user_query: str) -> str:
    q = user_query.lower()

    # Greetings
    if any(x in q for x in ["hi", "hello", "vanakkam", "வணக்கம்"]):
        return "🌾 Hello! I am AgriMind. I can help you with crops, fertilizer, soil and farming tips."

    # Crop related
    if any(x in q for x in ["crop", "பயிர்", "what crop", "best crop"]):
        return (
            "🌱 Crop selection depends on soil nutrients (N, P, K), pH, season and rainfall.\n"
            "👉 Use the Crop Recommendation page to get accurate advice for your land."
        )

    # Fertilizer
    if any(x in q for x in ["fertilizer", "உரம்"]):
        return (
            "🧪 Fertilizer depends on crop type, soil moisture and nutrients.\n"
            "👉 Use the Fertilizer Recommendation tool for correct dosage."
        )

    # Soil
    if any(x in q for x in ["soil", "மண்", "ph"]):
        return (
            "🌍 Soil pH affects nutrient absorption.\n"
            "Ideal pH: 6.0 – 7.5 for most crops."
        )

    # Weather
    if "weather" in q or "climate" in q:
        return (
            "🌦️ Weather plays a major role in crop success.\n"
            "Rainfall, temperature and humidity must match crop requirements."
        )

    # Default fallback
    return (
        "🤖 I can help with:\n"
        "• Crop recommendation\n"
        "• Fertilizer guidance\n"
        "• Soil health\n"
        "• Sustainable farming tips\n\n"
        "Please ask clearly in Tamil or English."
    )
