import os
import httpx
import requests 
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# -------- EXISTING LOGIC (UNCHANGED) --------
from src.crop_model import predict_crop
from src.fertilizer_model import recommend_fertilizer

# ===========================================
# APP INIT
# ===========================================
app = FastAPI(title="AgriMind API", version="3.3")

# ✅ CORRECT CORS FOR file://, localhost, Render
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=False,      
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================
# ROOT
# ===========================================
@app.get("/")
def root():
    return {"status": "AgriMind backend running"}

# ===========================================
# 🌱 CROP RECOMMENDATION
# ===========================================
@app.get("/recommend_crop")
def recommend_crop_api(
    district: str, N: int, P: int, K: int, ph: float
):
    try:
        temperature = 25
        humidity = 70
        rainfall = 200

        msg, local_crops, weather, _ = predict_crop(
            N=N, P=P, K=K, temperature=temperature,
            humidity=humidity, ph=ph, rainfall=rainfall,
            district=district, api_key=None
        )

        return {
            "success": True,
            "message": msg,
            "district": district,
            "local_crops": local_crops,
            "weather": weather
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

# ===========================================
# 🧪 FERTILIZER RECOMMENDATION
# ===========================================
@app.get("/recommend_fertilizer")
def recommend_fertilizer_api(
    temperature: float, humidity: float, moisture: float,
    soil_type: str, crop_type: str, nitrogen: int,
    potassium: int, phosphorus: int
):
    try:
        fert = recommend_fertilizer(
            temperature, humidity, moisture,
            soil_type, crop_type, nitrogen,
            potassium, phosphorus
        )
        return {"success": True, "fertilizer": fert}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ===========================================
# 💬 CHATBOT 
# ===========================================
# ✅ THE FIX: Look for the variable name, not the key itself.
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class ChatRequest(BaseModel):
    query: str
    language: str = "en-IN"

@app.post("/chat")
def chat_api(request: ChatRequest):
    user_message = request.query
    
    system_instruction = """
    You are 'AgriBot', an expert agricultural assistant. 
    You must ONLY answer questions related to agriculture, farming, crops, fertilizers, weather, and pest control. 
    Keep answers highly concise, actionable, and easy for a farmer to understand. Speak in the language the user speaks to you.
    """
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_message}
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response_data = response.json()
        
        if response.status_code == 200:
            reply_text = response_data['choices'][0]['message']['content']
            return {"success": True, "response": reply_text}
        else:
            return {"success": False, "response": f"API Error: {response_data}"}
            
    except Exception as e:
        return {"success": False, "response": f"Server Error: {str(e)}"}