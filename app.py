import streamlit as st
import requests
import json

# ---------------- CONFIG ----------------
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3"

st.set_page_config(page_title="Ollama Chatbot", page_icon="🤖")
st.title("🤖 Ollama Chatbot")
st.caption("Powered by Ollama + Streamlit")

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
prompt = st.chat_input("Type your message...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response (streaming)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": st.session_state.messages,
                "stream": True
            },
            stream=True,
            timeout=120
        )

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "message" in data:
                    token = data["message"]["content"]
                    full_response += token
                    response_placeholder.markdown(full_response)

    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )
 