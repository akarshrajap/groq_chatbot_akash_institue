# 🚀 Groq Chatbot with Streamlit Web UI

A modern, responsive interactive AI Assistant powered by **Groq Cloud LLMs**, built using **Streamlit**, **LangChain**, and **LangGraph**. Features real-time conversational intelligence, integrated UI and agent tools (Calculator & Greetings), and resilient fallback execution.

---

## 📋 Table of Contents

- [Project Overview](#-project-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation & Setup](#-installation--setup)
- [Running the Application](#-running-the-application)
- [Project Structure](#-project-structure)
- [Available Tools & Capabilities](#-available-tools--capabilities)
- [Environment Configuration](#-environment-configuration)
- [Troubleshooting](#-troubleshooting)
- [Dependencies](#-dependencies)
- [License](#-license)

---

## 🎯 Project Overview

This project provides a sleek, web-based conversational interface for interacting with high-performance LLMs hosted on Groq. Designed for speed, flexibility, and ease of use, the application features:

- **Web-based Chat Interface**: Built with Streamlit, custom CSS styling, and persistent conversation history.
- **Ultra-Fast LLM Processing**: Powered by Groq's LPU™ Inference Engine for near-instantaneous replies.
- **Interactive Tool Drawer**: A dedicated toggleable widget panel for direct access to helper tools like Quick Calculator and Greeting Tool.
- **Graceful Fallback Mode**: If an API key is not configured or network connectivity is limited, the app seamlessly falls back to a safe AST-based math evaluator and heuristic response stub.

---

## ✨ Key Features

- 🌐 **Modern Streamlit Web App**: Clean, responsive dark-themed hero banner and conversational message bubbles.
- ⚡ **Groq LLM Integration**: Effortless integration with high-speed models (such as `qwen/qwen3.6-27b`, `llama-3.3-70b-versatile`, and `mixtral-8x7b-32768`).
- 🛠️ **Extensible Tool Framework**:
  - **Quick Calculator (`ncalculator`)**: Dedicated UI input controls and backend arithmetic solver.
  - **Greeting Tool (`say_hello`)**: Personalized greeting generator.
  - **Expandable Tool Drawer (`+`)**: Quick toggle between conversational chat and interactive widgets.
- 🛡️ **Safe & Resilient Execution**: Built-in AST arithmetic parsing and error sanitization ensure uninterrupted usage even during service disruptions.
- 💬 **Session State Persistence**: Retains multi-turn conversation history across interactions during a user session.
- 🔐 **Environment Management**: Secure API key management via `.env` with `python-dotenv`.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Streamlit Frontend (Browser)                       │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  - Dark Hero Header & Conversational Chat Flow                    │  │
│  │  - Interactive Tool Drawer (+) [Calculator & Greeting Widgets]    │  │
│  │  - Query Form & Session State Manager                             │  │
│  └─────────────────────────────────┬─────────────────────────────────┘  │
└────────────────────────────────────┼────────────────────────────────────┘
                                     │ User Query / Actions
┌────────────────────────────────────▼────────────────────────────────────┐
│                    Application Core (`main.py`)                         │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │  - Environment Loader (`python-dotenv`)                           │  │
│  │  - Tool Definitions (`@tool` / Fallback decorators)               │  │
│  │  - Response Generator & Error Sanitization Handler                │  │
│  └──────────────────┬───────────────────────────────┬────────────────┘  │
└─────────────────────┼───────────────────────────────┼───────────────────┘
                      │                               │
        [Groq API Key Available]             [No Key / Fallback Mode]
                      │                               │
        ┌─────────────▼─────────────┐   ┌─────────────▼─────────────┐
        │   LangChain / LangGraph   │   │   Safe AST Heuristic Stub │
        │  - ChatGroq Interface     │   │  - Arithmetic AST Parser  │
        │  - Tool Binding & Agent   │   │  - Local Tool Delegation  │
        └─────────────┬─────────────┘   └─────────────┬─────────────┘
                      │                               │
        ┌─────────────▼─────────────┐                 │
        │      Groq Cloud API       │                 │
        │   (qwen/qwen3.6-27b)      │                 │
        └─────────────┬─────────────┘                 │
                      │                               │
                      └───────────────┬───────────────┘
                                      │
                        ┌─────────────▼─────────────┐
                        │   Sanitized Chat Output   │
                        └───────────────────────────┘
```

---

## 📋 Prerequisites

Before running the application, make sure you have:

- **Python 3.8+** installed on your system.
- **Groq API Key** (Free registration at [Groq Console](https://console.groq.com)).
- **pip** (Python package installer).

---

## 🚀 Installation & Setup

### 1. Clone or Open the Project

Open your terminal and navigate to the project directory:

```bash
cd groq_chatbot_streamlitUi
```

### 2. Create a Virtual Environment

Isolate dependencies by creating a Python virtual environment:

```bash
# Windows (PowerShell or CMD)
python -m venv .venv

# macOS / Linux
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

#### On Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```
> *Note: If you receive a script execution error in PowerShell, run:*
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
> ```

#### On Windows (Command Prompt):
```cmd
.venv\Scripts\activate.bat
```

#### On macOS/Linux:
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

Install required libraries from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory (you can copy `.env.example`):

```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# macOS / Linux
cp .env.example .env
```

Edit `.env` and fill in your Groq API credentials:

```env
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=qwen/qwen3.6-27b
```

---

## 💻 Running the Application

Launch the Streamlit web application:

```bash
streamlit run main.py
```

Once started, Streamlit will automatically open your default browser to:

```
http://localhost:8501
```

---

## 📁 Project Structure

```
groq_chatbot_streamlitUi/
│
├── main.py                 # Streamlit web app, UI layout, agent & fallback logic
├── requirements.txt        # Python dependencies (Streamlit, LangChain, Groq, etc.)
├── .env                    # Environment variables (API keys and model config)
├── .env.example            # Template for environment configuration
├── .gitignore              # Files and directories ignored by Git
└── README.md               # Project documentation
```

---

## 🛠️ Available Tools & Capabilities

### 1. 💬 Conversational Chat
- Ask general queries, request explanations, or prompt creative generation.
- Handles multi-turn chat directly in the main conversation window.

### 2. 🧮 Calculator Tool (`ncalculator`)
- **Interactive UI**: Open the tool panel using the **`+`** button, select **`ncalculator`**, enter numeric values, and click **Compute sum**.
- **Chat Math**: You can also ask calculation queries in chat (e.g., `What is 150 + 275?`), which will be processed by the LLM or the local safe AST evaluator.

### 3. 👋 Greeting Tool
- **Interactive UI**: Open the tool panel (**`+`** button), select **`greeting tool`**, enter a name, and click **Greet**.
- **Chat Greeting**: Ask the chatbot to greet someone (e.g., `Say hello to Alice`), and receive personalized greeting messages.

---

## ⚙️ Environment Configuration

| Variable | Required | Default | Description |
|---|:---:|---|---|
| `GROQ_API_KEY` | Optional* | `None` | Your Groq Cloud API authentication key |
| `GROQ_MODEL` | Optional | `qwen/qwen3.6-27b` | Groq model identifier |

*\*Note: The application includes local fallback stubs and can run without an API key, but full LLM capabilities require a valid `GROQ_API_KEY`.*

### Popular Groq Models Supported:

- `qwen/qwen3.6-27b` *(Default)*
- `llama-3.3-70b-versatile`
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

---

## ❓ Troubleshooting

### 1. `streamlit: command not found`
Ensure that your virtual environment is active (`.venv`) and packages are installed:
```bash
pip install -r requirements.txt
```

### 2. "GROQ_API_KEY is not set" / Falling back to stub
- Check that your `.env` file exists in the root directory.
- Verify `GROQ_API_KEY` does not contain quotes or trailing whitespace.
- Obtain a key from [Groq Console](https://console.groq.com/keys).

### 3. PowerShell Script Execution Error
Run PowerShell with permissions for the current session:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

### 4. Port 8501 Already in Use
You can specify a different port when launching Streamlit:
```bash
streamlit run main.py --server.port 8502
```

---

## 📦 Dependencies

| Package | Minimum Version | Purpose |
|---|---|---|
| **streamlit** | `>=1.22.0` | Interactive web application framework |
| **langchain-core** | `>=1.5.2` | Core abstractions and message primitives |
| **langchain-groq** | `>=1.1.3` | Groq LLM integration |
| **langgraph** | `>=1.2.10` | Agent orchestration and graph patterns |
| **python-dotenv** | `>=1.2.2` | `.env` configuration file loader |

---

## 📄 License

This project is licensed under the MIT License — open-source for personal, educational, and commercial exploration.
