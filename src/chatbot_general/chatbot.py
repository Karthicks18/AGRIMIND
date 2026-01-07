def agriculture_chat(query: str) -> str:
    q = query.lower()

    if "paddy" in q and "fertilizer" in q:
        return (
            "For paddy cultivation, Urea or DAP is commonly recommended. "
            "Apply nitrogen in split doses and ensure sufficient water availability."
        )

    if "soil" in q and "sandy" in q:
        return (
            "Sandy soils drain quickly. Use organic manure and apply fertilizers "
            "in smaller, frequent doses to improve nutrient retention."
        )

    if "best crop" in q:
        return (
            "The best crop depends on soil nutrients, pH, rainfall, and season. "
            "Use the Crop Recommendation feature for accurate results."
        )

    if "fertilizer" in q:
        return (
            "Fertilizer selection depends on soil nutrients, crop type, and moisture. "
            "Use the Fertilizer Recommendation section for personalized advice."
        )

    return (
        "I am AgriMind 🌱. You can ask me about crops, fertilizers, soil health, "
        "and farming practices."
    )
