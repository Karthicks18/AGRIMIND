# Fertilizer Recommendation Model (FINAL – BACKEND COMPATIBLE)

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import shap
import matplotlib.pyplot as plt
import joblib
import os

# ========================================================
# 1) INFERENCE FUNCTION (Safe to import into api.py)
# ========================================================
def recommend_fertilizer(temperature, humidity, moisture, soil_type, crop_type, nitrogen, potassium, phosphorus):
    """Loads the pre-trained models and makes a prediction for the API."""
    try:
        # Securely find the models directory
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_dir = os.path.join(base_dir, "..", "models")
        
        # Load the saved models
        model = joblib.load(os.path.join(model_dir, "fertilizer_model.pkl"))
        label_encoders = joblib.load(os.path.join(model_dir, "fertilizer_label_encoders.pkl"))
        target_le = joblib.load(os.path.join(model_dir, "fertilizer_target_encoder.pkl"))
        
        # Encode the text inputs
        soil_encoded = label_encoders["Soil Type"].transform([soil_type])[0]
        crop_encoded = label_encoders["Crop Type"].transform([crop_type])[0]
        
        # Format the data exactly how the Random Forest expects it
        input_data = pd.DataFrame([[
            soil_encoded, crop_encoded, temperature, humidity, moisture, nitrogen, potassium, phosphorus
        ]], columns=["Soil Type", "Crop Type", "Temparature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous"])
        
        # Make prediction
        prediction = model.predict(input_data)
        return target_le.inverse_transform(prediction)[0]
        
    except Exception as e:
        return f"Model Error: {str(e)}"

# ========================================================
# 2) TRAINING SCRIPT (Will ONLY run if executed directly)
# ========================================================
if __name__ == "__main__":
    print("🚀 Starting manual fertilizer model training...")
    
    # 1) Load Dataset securely
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "fertilizer.csv")
    
    df = pd.read_csv(csv_path)
    print("Columns:", df.columns.tolist())

    # 2) Define Columns (MATCH BACKEND ORDER)
    TARGET_COL = "Fertilizer Name"
    CATEGORICAL_COLS = ["Soil Type", "Crop Type"]
    NUMERIC_COLS = ["Temparature", "Humidity", "Moisture", "Nitrogen", "Potassium", "Phosphorous"]

    # 3) Encode Categorical Columns
    label_encoders = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le

    target_le = LabelEncoder()
    df[TARGET_COL] = target_le.fit_transform(df[TARGET_COL])

    # 4) Prepare Data
    X = df[CATEGORICAL_COLS + NUMERIC_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 5) Train Model (NO SCALING – SAFE)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # 6) Evaluate
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred, target_names=target_le.classes_))

    # 7) SAVE FILES TO /models (IMPORTANT)
    models_dir = os.path.join(base_dir, "..", "models")
    os.makedirs(models_dir, exist_ok=True)

    joblib.dump(model, os.path.join(models_dir, "fertilizer_model.pkl"))
    joblib.dump(label_encoders, os.path.join(models_dir, "fertilizer_label_encoders.pkl"))
    joblib.dump(target_le, os.path.join(models_dir, "fertilizer_target_encoder.pkl"))

    print("✅ fertilizer_model.pkl safely saved to /models")

    # 8) SHAP (Optional – for report)
    explainer = shap.TreeExplainer(model)
    shap_values = explainer(X_test, check_additivity=False)

    shap.summary_plot(shap_values.values, X_test, feature_names=X_test.columns, show=False)
    plt.savefig(os.path.join(base_dir, "fertilizer_shap_summary.png"), bbox_inches="tight")
    plt.close()