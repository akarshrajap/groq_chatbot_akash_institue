# Groq Chatbot — Streamlit Web UI

A lightweight Streamlit-based chat UI for experimenting with Groq-hosted LLMs. The app provides a conversational interface, small interactive helper tools (calculator and greeting), and a secure fallback mode so it remains useful even without an API key.

Quick highlights:
- Streamlit frontend with session-based conversation history
- Groq LLM integration (model configurable via `.env`)
- Local safe fallback evaluator for arithmetic and simple stubs

---

**Table of contents**

- Project overview
- Quick start
- Environment
- Running
- Project layout
- Troubleshooting
- License

---

## Project overview

This repository contains a Streamlit app (`main.py`) that demonstrates an LLM-driven chat UI with small built-in tools and a resilient fallback mode. It's intended for local experimentation and exploration.

Use cases:
- Prototyping chat interactions with Groq models
- Local demonstrations without an API key (limited fallback behavior)

---

## Quick start

1. Create and activate a Python virtual environment:

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a `.env` file (optional — required for full LLM access):

```powershell
Copy-Item .env.example .env
# then edit .env and set GROQ_API_KEY and GROQ_MODEL
```

4. Run the app:

```powershell
streamlit run main.py
```

Visit http://localhost:8501 in your browser.

---

## Environment

Recommended environment variables (see `.env.example`):

- `GROQ_API_KEY` — your Groq API key (optional; without it the app uses fallback behavior)
- `GROQ_MODEL` — model id (default: `qwen/qwen3.6-27b`)

The app uses `python-dotenv` to load variables from `.env`.

---

## Running (notes)

- To change the Streamlit port: `streamlit run main.py --server.port 8502`
- If `streamlit` is not found, ensure the virtual environment is active and `pip install -r requirements.txt` completed successfully.

---

## Project layout

```
./
├─ main.py           # Streamlit app (UI, tool bindings, fallback logic)
├─ requirements.txt  # Python dependencies
├─ .env.example      # Example environment variables
└─ README.md         # This file
```

---

## Troubleshooting

- PowerShell execution policy error when activating venv:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  ```
- App falls back to local stubs: check `.env` and `GROQ_API_KEY` formatting (no quotes, no trailing spaces).
- Port in use: run `streamlit run main.py --server.port 8502`.

---

## Dependencies

Installable via `requirements.txt`. Typical packages include `streamlit`, `langchain`, `langgraph`, and `python-dotenv`.

---

## License

MIT — see project license for details.
