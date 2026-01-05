# =========================================================
# AgriMind Streamlit – RESTORED FULL APP + CHATBOT
# =========================================================
import streamlit as st
import requests
import time

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="AgriMind", layout="wide")

st.markdown(
    "<h1 style='text-align:center;color:#176B87;'>🌾 AgriMind: Smart Farming Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Crop & Fertilizer Recommendation + Agriculture Chatbot</p>",
    unsafe_allow_html=True
)

# ===================== SIDEBAR =====================
module = st.sidebar.radio(
    "📘 Select Module",
    [
        "🌱 Crop Recommendation",
        "🧪 Fertilizer Recommendation",
        "💬 Agriculture Chatbot"
    ]
)

# ===================== CROP MODULE (OLD) =====================
def crop_module():
    st.subheader("🌱 Crop Recommendation")

    district = st.text_input("District", "Coimbatore")

    c1, c2, c3, c4 = st.columns(4)
    N = c1.number_input("Nitrogen (N)", 0, 140, 90)
    P = c2.number_input("Phosphorus (P)", 0, 140, 42)
    K = c3.number_input("Potassium (K)", 0, 200, 43)
    ph = c4.number_input("Soil pH", 3.0, 9.0, 6.5)

    if st.button("Recommend Crop"):
        with st.spinner("Analyzing crop suitability..."):
            res = requests.get(
                f"{API_BASE}/recommend_crop",
                params={
                    "district": district,
                    "N": N,
                    "P": P,
                    "K": K,
                    "ph": ph
                }
            ).json()

        st.success(res["recommendation"])
        if "district_suitable_crops" in res:
            st.info("Suitable crops: " + ", ".join(res["district_suitable_crops"]))


# ===================== FERTILIZER MODULE (OLD) =====================
def fertilizer_module():
    st.subheader("🧪 Fertilizer Recommendation")

    crop = st.text_input("Crop Name", "Maize")
    soil = st.selectbox("Soil Type", ["Loamy", "Red", "Black", "Sandy"])

    c1, c2, c3 = st.columns(3)
    N = c1.number_input("Nitrogen (N)", 0, 140, 50)
    P = c2.number_input("Phosphorus (P)", 0, 140, 30)
    K = c3.number_input("Potassium (K)", 0, 140, 40)

    if st.button("Recommend Fertilizer"):
        with st.spinner("Analyzing fertilizer needs..."):
            res = requests.get(
                f"{API_BASE}/recommend_fertilizer",
                params={
                    "crop_type": crop,
                    "soil_type": soil,
                    "nitrogen": N,
                    "phosphorus": P,
                    "potassium": K
                }
            ).json()

        st.success(f"Recommended Fertilizer: {res['recommended_fertilizer']}")


# ===================== CHATBOT MODULE (NEW) =====================
def chatbot_module():
    st.subheader("💬 Agriculture Chatbot")
    st.write("Ask any question about farming, crops, pests, seasons, or soil.")

    question = st.text_input("Your question:")

    if st.button("Ask AgriMind"):
        if not question.strip():
            st.warning("Please enter a question.")
            return

        with st.spinner("AgriMind is thinking..."):
            res = requests.post(
                f"{API_BASE}/chatbot_agri",
                json={"question": question}
            ).json()
            time.sleep(1)

        st.markdown(
            f"""
            <div style='background:#1e293b;padding:1rem;border-radius:8px;'>
                <p style='color:white;font-size:16px;'>{res['response']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ===================== ROUTING =====================
if module == "🌱 Crop Recommendation":
    crop_module()
elif module == "🧪 Fertilizer Recommendation":
    fertilizer_module()
else:
    chatbot_module()
