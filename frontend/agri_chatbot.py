import streamlit as st
import requests

API = "http://127.0.0.1:8000/chatbot_agri"

st.set_page_config(page_title="AgriMind Agriculture Chatbot", layout="centered")

st.markdown("<h1 style='text-align:center;'>🌾 AgriMind Agriculture Chatbot</h1>", unsafe_allow_html=True)
st.write("Ask any question about farming, crops, seasons, pests, or soil.")

question = st.text_input("💬 Ask your agriculture question:")

if st.button("Ask"):
    if question.strip():
        res = requests.post(API, json={"question": question}).json()
        st.markdown(
            f"<div style='background:#1e293b;padding:1rem;border-radius:8px;'>"
            f"<p style='color:white;'>{res['response']}</p></div>",
            unsafe_allow_html=True
        )
    else:
        st.warning("Please enter a question.")
