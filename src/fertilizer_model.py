import joblib
import numpy as np
import os

# ============================================
# Resolve absolute project root safely
# ============================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
MODEL_DIR = os.path.join(PROJECT_ROOT, "models")

# ============================================
# Model file paths
# ============================================
MODEL_PATH = os.path.join(MODEL_DIR, "fertilizer_model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "fertilizer_label_encoders.pkl")
TARGET_ENCODER_PATH = os.path.join(MODEL_DIR, "fertilizer_target_encoder.pkl")

# ============================================
# Load model & encoders (safe)
# ============================================
model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
encoders = joblib.load(ENCODER_PATH) if os.path.exists(ENCODER_PATH) else None
target_encoder = joblib.load(TARGET_ENCODER_PATH) if os.path.exists(TARGET_ENCODER_PATH) else None


# ============================================
# Safe categorical encoding
# ============================================
def safe_encode(encoder, value):
    """
    Encode unseen categorical values safely.
    Falls back to closest match or index 0.
    """
    try:
        return encoder.transform([value])[0]
    except Exception:
        value_clean = value.lower().strip()
        for idx, lbl in enumerate(encoder.classes_):
            if lbl.lower().strip() == value_clean:
                return idx
        return 0  # fallback


# ============================================
# Fertilizer Recommendation Logic
# ============================================
def recommend_fertilizer(
    temp,
    humidity,
    moisture,
    soil_type,
    crop_type,
    nitrogen,
    potassium,
    phosphorus
):
    """
    Predict fertilizer using 8 features:
    [temp, humidity, moisture, soil, crop, N, K, P]
    """

    # ---------- HARD SAFETY CHECK ----------
    if model is None:
        return "Model file missing: fertilizer_model.pkl"

    if encoders is None:
        return "Encoder file missing: fertilizer_label_encoders.pkl"

    if target_encoder is None:
        return "Target encoder missing: fertilizer_target_encoder.pkl"

    try:
        soil_encoded = safe_encode(encoders["Soil Type"], soil_type)
        crop_encoded = safe_encode(encoders["Crop Type"], crop_type)

        features = np.array([[
            temp,
            humidity,
            moisture,
            soil_encoded,
            crop_encoded,
            nitrogen,
            potassium,
            phosphorus
        ]])

        y_pred = model.predict(features)[0]
        fertilizer = target_encoder.inverse_transform([y_pred])[0]

        return fertilizer

    except Exception as e:
        return f"Error in fertilizer recommendation: {str(e)}"
