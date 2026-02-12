import streamlit as st
from transformers import pipeline

st.title("🤖 Tiny Local Chatbot")

@st.cache_resource  # Load model only once
def load_model():
    return pipeline("text-generation", model="distilgpt2")  # ~350 MB

chatbot = load_model()

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input("You:")
if user_input:
    response = chatbot(user_input, max_length=50, do_sample=True)[0]['generated_text']
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response))

for speaker, text in st.session_state.history:
    st.write(f"**{speaker}:** {text}")
