import streamlit as st
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "tinyllama"

st.set_page_config(page_title="Local LLM Chat", layout="centered")
st.title("Local LLM Chat Ollama")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Reset conversation
if st.button("Reset Conversation"):
    st.session_state.messages = []
    st.rerun()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_prompt = st.chat_input("Ask something...")

if user_prompt:
    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Send request to Ollama
    payload = {
    "model": MODEL_NAME,
    "prompt": user_prompt,
    "stream": False,
    "options": {
        "num_ctx": 512
    }
}

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=300)
        response.raise_for_status()
        model_reply = response.json().get("response", "")
    except Exception as e:
        model_reply = f"Error: {e}"

    # Save assistant response
    st.session_state.messages.append(
        {"role": "assistant", "content": model_reply}
    )

    with st.chat_message("assistant"):
        st.markdown(model_reply)
