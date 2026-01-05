import joblib
import numpy as np
import os

# ------------------ Load Model & Encoders ------------------
base_path = os.path.join(os.path.dirname(__file__), "..", "models")

model_path = os.path.join(base_path, "fertilizer_model.pkl")
encoder_path = os.path.join(base_path, "fertilizer_label_encoders.pkl")
target_encoder_path = os.path.join(base_path, "fertilizer_target_encoder.pkl")

model = joblib.load(model_path) if os.path.exists(model_path) else None
encoders = joblib.load(encoder_path) if os.path.exists(encoder_path) else None
target_encoder = joblib.load(target_encoder_path) if os.path.exists(target_encoder_path) else None


# ------------------ Safe Encoding ------------------
def safe_encode(encoder, value):
    """Safely encode unseen labels (fallback to 0)."""
    try:
        return encoder.transform([value])[0]
    except Exception:
        all_labels = list(encoder.classes_)
        value_clean = value.lower().strip()
        for i, lbl in enumerate(all_labels):
            if lbl.lower().strip() == value_clean:
                return i
        return 0  # fallback index


# ------------------ Fertilizer Recommendation ------------------
def recommend_fertilizer(temp, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorus):
    """
    Predict the best fertilizer using 8 input features:
    [temp, humidity, moisture, soil_type, crop_type, N, K, P]
    and decode numeric output to fertilizer name.
    """
    if model is None or encoders is None or target_encoder is None:
        return "Model or encoder files missing. Please check /models directory."

    try:
        # Encode categorical features
        soil_encoded = safe_encode(encoders["Soil Type"], soil_type)
        crop_encoded = safe_encode(encoders["Crop Type"], crop_type)

        # Create 8-feature input
        features = np.array([[temp, humidity, moisture, soil_encoded, crop_encoded,
                              nitrogen, potassium, phosphorus]])

        # Predict (numeric)
        y_pred = model.predict(features)[0]

        # Decode back to fertilizer name
        fert_name = target_encoder.inverse_transform([y_pred])[0]

        return fert_name

    except Exception as e:
        return f"Error in fertilizer recommendation: {str(e)}"
