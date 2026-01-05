import streamlit as st
import requests
from datetime import date

# -------------------------------
# CONFIG
# -------------------------------
BACKEND_URL = "http://127.0.0.1:8000"  # FastAPI backend URL
st.set_page_config(page_title="AgriMind Smart Farming Assistant", layout="wide")

# -------------------------------
# HEADER
# -------------------------------
st.title("🌾 AgriMind: AI-Powered Smart Farming Assistant")
st.markdown("""
AgriMind helps farmers make **data-driven decisions** for sustainable agriculture.
Choose your service below to get started 👇
""")

# -------------------------------
# MAIN MENU
# -------------------------------
option = st.radio(
    "Select what you need:",
    ["🌱 Crop Recommendation", "🧪 Fertilizer Recommendation", "💬 Farm Chat Assistant"],
    horizontal=True
)

# -------------------------------
# 1️⃣ CROP RECOMMENDATION MODULE
# -------------------------------
if option.startswith("🌱"):
    st.subheader("Crop Recommendation 🌾")

    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("Latitude", value=11.0, step=0.1)
        lon = st.number_input("Longitude", value=78.0, step=0.1)
        date_input = st.date_input("Date of Planning", date.today())
    with col2:
        N = st.number_input("Nitrogen (N)", 0, 200, 50)
        P = st.number_input("Phosphorus (P)", 0, 200, 40)
        K = st.number_input("Potassium (K)", 0, 200, 45)

    if st.button("🔍 Get Crop Recommendation"):
        with st.spinner("Analyzing live weather, market trends, and soil..."):
            params = {
                "lat": lat,
                "lon": lon,
                "N": N,
                "P": P,
                "K": K,
                "date": str(date_input)
            }
            try:
                r = requests.get(f"{BACKEND_URL}/recommend_crop", params=params, timeout=30)
                data = r.json()

                best = data.get("best_crop", {})
                all_options = data.get("all_options", [])

                st.success(f"✅ **Recommended Crop:** {best.get('crop')}")
                st.write(f"🕓 Duration: {best.get('duration_days')} days")
                st.write(f"💰 Expected Profit: ₹{best.get('expected_profit'):.2f}")
                st.write(f"📈 Market Trend: {best.get('market_trend_pct')}%")
                st.write(f"🌾 Harvest Date: {best.get('harvest_date')}")

                st.markdown("### 📋 Fertilizer Schedule Suggestion")
                ferts = best.get("recommended_fertilizers", {})
                for ftype, days in ferts.items():
                    st.write(f"**{ftype.title()}** → Apply on Days: {', '.join(map(str, days))}")

                st.markdown("---")
                st.markdown("### 📊 Comparison of All Crop Options")
                st.dataframe(all_options)

            except Exception as e:
                st.error(f"⚠️ Unable to fetch recommendation: {e}")

# -------------------------------
# 2️⃣ FERTILIZER RECOMMENDATION MODULE
# -------------------------------
elif option.startswith("🧪"):
    st.subheader("Fertilizer Recommendation 🌿")

    crop_name = st.text_input("Enter Crop Name (e.g., Tomato, Paddy, Maize)")
    crop_age = st.number_input("Enter Crop Age (in days)", 0, 200, 30)

    if st.button("🔍 Get Fertilizer Recommendation"):
        with st.spinner("Generating fertilizer schedule..."):
            params = {"crop": crop_name, "age": int(crop_age)}
            try:
                r = requests.get(f"{BACKEND_URL}/recommend_fertilizer", params=params, timeout=20)
                data = r.json()

                if "error" in data:
                    st.error(data["error"])
                elif "message" in data:
                    st.info(data["message"])
                else:
                    st.success(f"✅ Fertilizer Plan for {data['crop']} ({data['stage']} Stage)")
                    st.table(data["next_fertilizer_schedule"])
            except Exception as e:
                st.error(f"⚠️ Unable to fetch fertilizer recommendation: {e}")

# -------------------------------
# 3️⃣ CHATBOT MODULE
# -------------------------------
else:
    st.subheader("FarmGPT – Multilingual Chat Assistant 💬")
    st.write("Ask me anything about crops, fertilizers, or local farming guidance (English/Tamil).")

    user_query = st.text_area("Type your question here...")
    if st.button("💬 Ask"):
        with st.spinner("Thinking..."):
            try:
                # For now, a simple placeholder until your chatbot logic is complete
                # Later, connect to /chat endpoint of FastAPI
                if "tomato" in user_query.lower():
                    response = "Tomato is best grown between 20–25°C. Apply urea at 25 and 45 days."
                elif "fertilizer" in user_query.lower():
                    response = "Use balanced NPK 10:26:26 during flowering stage for high yield."
                else:
                    response = "I’m AgriMind Assistant 🌿 – I’ll soon answer from live AI models!"
                st.success(response)
            except Exception as e:
                st.error(f"⚠️ Chatbot error: {e}")

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.caption("© 2025 AgriMind – AI for Sustainable Farming | Developed by Karthick and Team 🌱")
