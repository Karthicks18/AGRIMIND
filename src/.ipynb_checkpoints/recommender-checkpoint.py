# src/services/recommender.py
import os, pickle, numpy as np, pandas as pd
from dotenv import load_dotenv
from ingestion.weather_ingestion import fetch_weather, engineer_weather_features
from ingestion.market_ingestion import fetch_mandi_prices, engineer_market_features
from market_mapping import CROP_TO_COMMODITY

load_dotenv()

# Load crop model stack (trained earlier)
CROP_MODEL_PATH = "models/crop_model.pkl"
CROP_SCALER_PATH = "notebooks/models/crop_scaler.pkl"  # adjust to your actual saved paths
CROP_LABEL_PATH = "notebooks/models/crop_label_encoder.pkl"

with open(CROP_MODEL_PATH, "rb") as f: CROP_MODEL = pickle.load(f)
with open(CROP_SCALER_PATH, "rb") as f: CROP_SCALER = pickle.load(f)
with open(CROP_LABEL_PATH, "rb") as f: CROP_LE = pickle.load(f)

# Load fertilizer stack
import joblib
FERT_MODEL = joblib.load("models/fertilizer_model.pkl")
FERT_SCALER = joblib.load("models/fertilizer_scaler.pkl")
FERT_LABEL_ENC = joblib.load("models/fertilizer_label_encoders.pkl")
FERT_TARGET_ENC = joblib.load("models/fertilizer_target_encoder.pkl")

# Simple yield and cost priors for profit proxy (replace with real values later)
YIELD_BASE = {"rice": 2200, "wheat": 2000, "maize": 1800, "cotton": 1500}  # kg/acre
FERT_COST_PER_ACRE = 2500  # INR placeholder

def score_crop(candidate: str, prob: float, market: dict, weather: dict,
               w_prob=0.5, w_trend=0.3, w_z=0.1, w_rain=-0.1) -> float:
    # higher rain may be good or bad depending; here penalize big 7d rainfall
    trend = market.get("price_trend7")
    z = market.get("price_z30")
    rain = weather.get("rainfall")
    comp = (
        w_prob * prob +
        w_trend * (trend if trend is not None else 0.0) +
        w_z * (z if z is not None else 0.0) +
        w_rain * (rain if rain is not None else 0.0) / 100.0
    )
    return float(comp)

def recommend(lat: float, lon: float, soil_inputs: dict, region: dict, top_k: int = 5):
    # 1) Weather features
    wdf = fetch_weather(lat, lon, days=7)
    wfe = engineer_weather_features(wdf)

    # 2) Build crop-model features: N,P,K from user; temperature/humidity/rainfall from forecast
    cols = ['N','P','K','temperature','humidity','ph','rainfall']
    x = np.array([[soil_inputs['N'], soil_inputs['P'], soil_inputs['K'],
                   wfe['temperature'], wfe['humidity'], soil_inputs['ph'], wfe['rainfall']]])
    x_scaled = CROP_SCALER.transform(x)
    proba = CROP_MODEL.predict_proba(x_scaled)[0]
    labels = CROP_LE.inverse_transform(np.arange(len(proba)))

    # 3) Market features per candidate
    scored = []
    for lab, p in zip(labels, proba):
        commodity = CROP_TO_COMMODITY.get(lab.lower(), lab)
        mdf = fetch_mandi_prices(commodity=commodity,
                                 state=region.get("state"), district=region.get("district"),
                                 market=region.get("market"), days=30)
        mfe = engineer_market_features(mdf)
        s = score_crop(lab, p, mfe, wfe)
        # Profit proxy
        price = mfe.get("price_latest") or mfe.get("price_med30") or 0
        yield_kg = YIELD_BASE.get(lab.lower(), 1500)
        profit_proxy = price * yield_kg - FERT_COST_PER_ACRE
        scored.append({
            "crop": lab, "model_prob": float(p), "score": s,
            "price_latest": price, "trend7": mfe.get("price_trend7"),
            "z30": mfe.get("price_z30"), "rain7": wfe["rainfall"],
            "profit_proxy": profit_proxy
        })

    ranked = sorted(scored, key=lambda d: d["score"], reverse=True)[:top_k]
    # 4) Fertilizer recommendation for top-1 crop (simple demo)
    top_crop = ranked[0]["crop"]
    fert_input = {
        # You must collect soil/crop fields for your fertilizer model schema
        "Soil Type": region.get("soil_type","Loamy"),
        "Crop Type": top_crop,
        "Temparature": wfe["temperature"],
        "Humidity": wfe["humidity"],
        "Moisture": soil_inputs.get("moisture", 30),
        "Nitrogen": soil_inputs["N"],
        "Phosphorous": soil_inputs["P"],
        "Potassium": soil_inputs["K"]
    }
    # encode + scale
    Xf = pd.DataFrame([fert_input])
    # encode categoricals using saved encoders
    for col, enc in FERT_LABEL_ENC.items():
        Xf[col] = enc.transform(Xf[col])
    # scale numerics
    num = ["Temparature","Humidity","Moisture","Nitrogen","Phosphorous","Potassium"]
    Xf[num] = FERT_SCALER.transform(Xf[num])
    fert_pred = FERT_MODEL.predict(Xf)
    fert_name = FERT_TARGET_ENC.inverse_transform(fert_pred)[0]

    return {"ranked_crops": ranked, "fertilizer_for_top": fert_name, "weather": wfe}
