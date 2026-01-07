# ===========================================
# AgriMind Backend API (FINAL – STABLE)
# ===========================================
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# -------- IMPORT YOUR EXISTING LOGIC --------
from src.crop_model import predict_crop
from src.fertilizer_model import recommend_fertilizer
from src.chatbot_general.chatbot import agriculture_chat

# ===========================================
# APP INIT
# ===========================================
app = FastAPI(title="AgriMind API", version="3.2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (safe for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================
# STATIC WEB FILES
# ===========================================
app.mount("/web", StaticFiles(directory="web", html=True), name="web")

# ===========================================
# ROOT
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
        # default weather (same as before)
        temperature = 25
        humidity = 70
        rainfall = 200

        msg, local_crops, weather, _ = predict_crop(
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
            "message": msg,
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
        fert = recommend_fertilizer(
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
            "fertilizer": fert
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
