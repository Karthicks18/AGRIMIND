# ===========================================
# AgriMind Backend API (FINAL – STABLE)
# ===========================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# -------- IMPORT YOUR EXISTING LOGIC --------
from src.crop_model import predict_crop
from src.fertilizer_model import recommend_fertilizer
from src.chatbot_general.chatbot import agriculture_chat

# ===========================================
# APP INIT
# ===========================================
app = FastAPI(
    title="AgriMind API",
    version="3.2",
    description="AI-powered Crop, Fertilizer & Agriculture Chatbot System"
)

# ===========================================
# ✅ CORS CONFIG (CRITICAL FIX)
# ===========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allows file://, GitHub Pages, localhost
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, OPTIONS
    allow_headers=["*"],
)

# ===========================================
# STATIC WEB FILES (OPTIONAL)
# ===========================================
# This allows: https://backend-url/web/crop.html
app.mount("/web", StaticFiles(directory="web", html=True), name="web")

# ===========================================
# ROOT HEALTH CHECK
# ===========================================
@app.get("/")
def root():
    return {"status": "AgriMind backend running"}

# ===========================================
# 🌱 CROP RECOMMENDATION API
# ===========================================
@app.get("/recommend_crop")
def recommend_crop_api(
    district: str,
    N: int,
    P: int,
    K: int,
    ph: float
):
    try:
        # Default weather values (as per your existing logic)
        temperature = 25
        humidity = 70
        rainfall = 200

        message, local_crops, weather, _ = predict_crop(
            N=N,
            P=P,
            K=K,
            temperature=temperature,
            humidity=humidity,
            ph=ph,
            rainfall=rainfall,
            district=district,
            api_key=None
        )

        return {
            "success": True,
            "message": message,
            "district": district,
            "local_crops": local_crops,
            "weather": weather
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ===========================================
# 🧪 FERTILIZER RECOMMENDATION API
# ===========================================
@app.get("/recommend_fertilizer")
def recommend_fertilizer_api(
    temperature: float,
    humidity: float,
    moisture: float,
    soil_type: str,
    crop_type: str,
    nitrogen: int,
    potassium: int,
    phosphorus: int
):
    try:
        fertilizer = recommend_fertilizer(
            temperature,
            humidity,
            moisture,
            soil_type,
            crop_type,
            nitrogen,
            potassium,
            phosphorus
        )

        return {
            "success": True,
            "fertilizer": fertilizer
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# ===========================================
# 💬 AGRICULTURE CHATBOT API
# ===========================================
class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat_api(request: ChatRequest):
    try:
        reply = agriculture_chat(request.query)
        return {
            "success": True,
            "response": reply
        }

    except Exception as e:
        return {
            "success": False,
            "response": f"Chatbot error: {e}"
        }
