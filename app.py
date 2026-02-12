import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="HealthAssist Gemini", page_icon="🏥")
st.title("🏥 HealthAssist Gemini")

# --- LOAD API KEY FROM SECRETS ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("API Key not found! Please add GEMINI_API_KEY to your .streamlit/secrets.toml file.")
    st.stop()

# --- SYSTEM PROMPT SETUP ---
system_instruction = (
    "You are a helpful healthcare assistant. Provide evidence-based info. "
    "Always state you are an AI, not a doctor. In emergencies, tell users to call 911."
)

# Initialize model once
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=system_instruction
)

# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar for controls
with st.sidebar:
    st.title("Medical Assistant Settings")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            # Reconstruct history for Gemini format
            history = [
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ]
            
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt, stream=True)
            
            for chunk in response:
                full_response += chunk.text
                response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")
