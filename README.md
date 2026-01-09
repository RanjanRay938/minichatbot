# Mini Chatbot — Ollama + Streamlit UI

A minimal demo chat UI that uses Ollama (local LLM API) as the backend and Streamlit for the web UI. The app streams assistant responses as they arrive from Ollama.

This repository includes:
- `app.py` — a tiny Streamlit app that posts chat messages to an Ollama HTTP API and streams tokens back into the UI.

## Features
- Simple chat interface using Streamlit's chat components
- Streams model output token-by-token for live assistant responses
- Uses local Ollama API (default: http://localhost:11434)

## Requirements
- Python 3.9+
- Ollama installed and running locally (API reachable)
- Internet access only if you need to download models for Ollama
- Python packages:
  - streamlit
  - requests

You can install Python dependencies with:
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install streamlit requests
```

(Or create a `requirements.txt` with `streamlit` and `requests` and run `pip install -r requirements.txt`.)

## Configuration
The example `app.py` uses two constants at the top:

- `OLLAMA_URL` (default: `http://localhost:11434/api/chat`) — the HTTP endpoint for Ollama's chat API.
- `MODEL_NAME` (default: `llama3`) — the model name to request from Ollama.

If your Ollama server/API runs on a different host/port or you want a different model, update these variables in `app.py` or modify the code to read them from environment variables.

Important: Ensure an appropriate model is available/installed in your local Ollama installation and that Ollama is running. By default the app expects Ollama's API to be reachable at `http://localhost:11434`.

## Running Ollama (brief)
This README does not replace the Ollama docs. The exact commands to start Ollama or to pull models depend on your Ollama version and setup. In general:
- Start the Ollama service/daemon so the HTTP API is available.
- Ensure a model (for example `llama3`, or any model your Ollama supports) is available to serve.

If you run into connection errors, confirm the API URL and port and that your Ollama instance is running.

## Run the Streamlit app
From the repository root:
```bash
streamlit run app.py
```

Open the local Streamlit URL printed in the terminal (usually `http://localhost:8501`) and use the chat input to interact with the model.

## How the app works (high level)
- The app stores chat history in `st.session_state.messages`.
- On user input, it appends a user message and sends the full message list to Ollama via POST to `OLLAMA_URL`.
- The request is made with `"stream": True` and `stream=True` in `requests.post()` to iterate over the API's streamed lines.
- Tokens are collected and incrementally rendered into the Streamlit chat placeholder, then stored into session history as the assistant response.

## Troubleshooting
- Connection refused to `http://localhost:11434`:
  - Ensure Ollama is running and listening on that port.
  - Confirm firewall or local networking is not blocking localhost connections.
- Model not found or error from Ollama:
  - Verify the `MODEL_NAME` exists in your Ollama installation.
  - Check Ollama logs for details.
- Long responses/timeouts:
  - The app uses a 120s `requests.post()` timeout; adjust as needed in `app.py`.
- Stream intermittently not updating:
  - Some model backends or network layers may buffer output. Check Ollama server behavior and configuration.

## Security & Privacy
- Requests and responses are sent to your local Ollama instance. Keep models and data usage compliant with your privacy requirements.
- This demo does not include authentication for the Ollama API. If you expose the API remotely, add authentication and TLS.

## Extending the demo
- Make `OLLAMA_URL` and `MODEL_NAME` configurable via environment variables or a settings UI.
- Add message timestamping, user names, or role controls.
- Add moderation or safety layers before sending content to the model.

## License
This repository/demo is provided as-is. Add a license file if you want to specify usage terms.

---

What I did: I prepared a focused README.md for this repo explaining prerequisites, configuration, and how to run the Streamlit + Ollama chat demo.

What's next: if you'd like, I can (a) create and commit this README into the repository for you, (b) add a requirements.txt, or (c) modify app.py to read configuration from environment variables. Tell me which you'd prefer.
