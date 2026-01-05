from src.crop_logic import generate_crop_plan
from src.fertilizer_logic import get_fertilizer_schedule

@app.get("/recommend_crop")
def recommend_crop(lat: float, lon: float, N: float, P: float, K: float, date: str):
    best, all_plans = generate_crop_plan(lat, lon, N, P, K, selected_date=date)
    return {"best_crop": best, "all_options": all_plans}

@app.get("/recommend_fertilizer")
def recommend_fertilizer(crop: str, age: int):
    return get_fertilizer_schedule(crop, age)

option = st.selectbox("Choose your need:", ["Crop Recommendation", "Fertilizer Recommendation", "Chatbot"])
if option == "Crop Recommendation":
    # inputs: lat, lon, date, N, P, K
elif option == "Fertilizer Recommendation":
    # inputs: crop name, age (days)
else:
    # chatbot UI
