import streamlit as st
import requests

st.title("💬 DeepSeek + Streamlit Chatbot")

# --- API Configuration ---
API_URL = "https://api.deepseek.com/chat/completions"
API_KEY = st.secrets["DEEPSEEK_API_KEY"]  # Streamlit Cloud secrets

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input ---
if prompt := st.chat_input("Ask DeepSeek..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call DeepSeek API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",  # or "deepseek-reasoner" for R1
        "messages": st.session_state.messages[-5:],  # last 5 for context
        "stream": False
    }

    with st.spinner("DeepSeek is thinking..."):
        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            reply = response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            reply = f"❌ Error: {str(e)}"

    # Display response
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
