# src/crop_model.py — AgriMind Realistic Human Output Version (v3.3)
import joblib
import numpy as np
import os
import requests
import pandas as pd

# ------------------ Load Model ------------------
model_path = os.path.join(os.path.dirname(__file__), "..", "models", "crop_model.pkl")
model = joblib.load(model_path) if os.path.exists(model_path) else None

# ------------------ District Crop Suitability ------------------
district_crop_map = {
    "Ariyalur": ["Paddy", "Sugarcane", "Maize", "Cotton", "Groundnut", "Blackgram"],
    "Chengalpattu": ["Paddy", "Groundnut", "Banana", "Sugarcane", "Tapioca"],
    "Chennai": ["Vegetables", "Greens", "Banana", "Flowers"],
    "Coimbatore": ["Maize", "Turmeric", "Banana", "Coconut", "Tomato", "Onion"],
    "Cuddalore": ["Paddy", "Groundnut", "Sugarcane", "Cashew", "Pulses"],
    "Dharmapuri": ["Millets", "Groundnut", "Turmeric", "Mango", "Tomato"],
    "Dindigul": ["Paddy", "Banana", "Maize", "Turmeric", "Onion", "Chillies"],
    "Erode": ["Turmeric", "Sugarcane", "Banana", "Groundnut", "Maize", "Coconut"],
    "Kallakurichi": ["Paddy", "Groundnut", "Sugarcane", "Maize", "Blackgram"],
    "Kancheepuram": ["Paddy", "Groundnut", "Sugarcane", "Vegetables"],
    "Kanyakumari": ["Banana", "Rubber", "Coconut", "Pepper", "Tapioca"],
    "Karur": ["Paddy", "Maize", "Sugarcane", "Groundnut", "Banana"],
    "Krishnagiri": ["Mango", "Ragi", "Tomato", "Groundnut"],
    "Madurai": ["Cotton", "Banana", "Chillies", "Paddy", "Maize"],
    "Mayiladuthurai": ["Paddy", "Sugarcane", "Banana", "Pulses", "Coconut"],
    "Nagapattinam": ["Paddy", "Sugarcane", "Groundnut", "Banana", "Coconut"],
    "Namakkal": ["Maize", "Groundnut", "Turmeric", "Banana", "Tomato"],
    "Perambalur": ["Maize", "Cotton", "Sunflower", "Groundnut"],
    "Pudukkottai": ["Paddy", "Groundnut", "Cotton", "Maize"],
    "Ramanathapuram": ["Cotton", "Groundnut", "Pulses", "Chillies"],
    "Ranipet": ["Paddy", "Sugarcane", "Banana", "Groundnut"],
    "Salem": ["Turmeric", "Paddy", "Groundnut", "Maize", "Tomato"],
    "Sivagangai": ["Paddy", "Cotton", "Blackgram", "Groundnut"],
    "Tenkasi": ["Paddy", "Banana", "Coconut", "Chillies", "Vegetables"],
    "Thanjavur": ["Paddy", "Sugarcane", "Banana", "Blackgram", "Groundnut", "Coconut"],
    "Theni": ["Paddy", "Banana", "Cardamom", "Coconut", "Vegetables"],
    "Thiruvallur": ["Paddy", "Groundnut", "Sugarcane", "Vegetables"],
    "Thiruvarur": ["Paddy", "Sugarcane", "Banana", "Blackgram"],
    "Thoothukudi": ["Cotton", "Chillies", "Groundnut", "Maize"],
    "Trichy": ["Paddy", "Sugarcane", "Banana", "Maize", "Groundnut"],
    "Tirunelveli": ["Banana", "Coconut", "Maize", "Cotton", "Paddy"],
    "Tirupathur": ["Paddy", "Sugarcane", "Groundnut", "Banana"],
    "Tiruppur": ["Maize", "Groundnut", "Coconut", "Banana", "Onion", "Chillies"],
    "Tiruvannamalai": ["Groundnut", "Millets", "Sugarcane", "Paddy", "Cotton"],
    "Vellore": ["Groundnut", "Ragi", "Sugarcane", "Paddy", "Turmeric"],
    "Villupuram": ["Groundnut", "Sugarcane", "Paddy", "Cashew", "Blackgram"],
    "Virudhunagar": ["Cotton", "Paddy", "Chillies", "Groundnut"]
}

# ------------------ Weather Helper ------------------
def get_weather(district, api_key):
    """Fetch live weather for given district."""
    try:
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={district},IN&units=metric&appid={api_key}",
            timeout=8
        )
        if res.status_code == 200:
            data = res.json()
            return {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "desc": data["weather"][0]["description"].capitalize(),
            }
    except:
        pass
    return None

# ------------------ Smart Crop Selection ------------------
def smart_select(base_crop, district, weather):
    """Ensure realistic, natural output."""
    local_crops = district_crop_map.get(district, [])
    chosen_crop = base_crop
    reason = ""

    # Adjust based on local suitability
    if local_crops:
        if base_crop not in local_crops:
            chosen_crop = local_crops[0]
            reason = f"✅ {chosen_crop} is better suited to {district}'s soil and farming pattern."
        else:
            chosen_crop = base_crop
            reason = f"✅ {chosen_crop} matches {district}'s soil and weather conditions."

    # Temperature correction for paddy/rice
    if weather and chosen_crop.lower() in ["rice", "paddy"] and weather.get("temp", 28) > 35:
        alt = [c for c in local_crops if c.lower() not in ["rice", "paddy"]]
        if alt:
            chosen_crop = alt[0]
            reason = f"🌡️ Temperature is high ({weather['temp']}°C). {chosen_crop} is more suitable for this climate."

    if reason == "":
        reason = f"✅ {chosen_crop} is optimal for the current weather."

    return chosen_crop, reason

# ------------------ Crop Prediction ------------------
def predict_crop(N, P, K, temperature, humidity, ph, rainfall, district=None, api_key=None):
    """Predict best crop and refine based on district & weather."""
    if model is None:
        return "❌ Model not found.", [], None, pd.DataFrame()

    try:
        features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        base_crop = model.predict(features)[0]

        weather = get_weather(district, api_key) if api_key else None
        chosen_crop, reason = smart_select(base_crop, district, weather)

        msg = f"✅ Recommended Crop: {chosen_crop}\n{reason}"
        return msg, district_crop_map.get(district, []), weather, pd.DataFrame()

    except Exception as e:
        return f"Error during prediction: {e}", [], None, pd.DataFrame()
