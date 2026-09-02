# Groq Chatbot - AI Assistant with Tool Integration

A Python-based interactive AI chatbot powered by **Groq LLM** and built with **LangChain** and **LanGraph**. This chatbot leverages the ReAct (Reasoning and Acting) framework to intelligently use tools and provide meaningful responses to user queries.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Available Tools](#available-tools)
- [Environment Configuration](#environment-configuration)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Project Overview

This chatbot is an intelligent conversational agent that can:
- Engage in natural language conversations
- Perform calculations on demand
- Greet users interactively
- Stream responses in real-time for a better user experience
- Leverage Groq's high-speed LLM inference for fast responses

The project demonstrates modern AI development practices using production-grade frameworks and libraries.

---

## ✨ Features

- **Real-time Response Streaming**: Responses are streamed as they're generated for immediate feedback
- **Tool Integration**: Extensible tool framework allowing the agent to use custom functions
- **ReAct Framework**: Advanced reasoning and acting pattern for intelligent decision-making
- **Environment Variable Management**: Secure API key handling via `.env` file
- **Clean Interactive Interface**: User-friendly command-line interface with clear prompts
- **Warning Suppression**: Cleaner output by filtering unnecessary deprecation warnings

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Input                             │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            Main Application (main.py)                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │  - Environment Configuration (load_dotenv)     │   │
│  │  - Tool Definitions (@tool decorators)         │   │
│  │  - Interactive Loop (REPL)                     │   │
│  └─────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┴───────────┐
         │                       │
┌────────▼──────────┐   ┌────────▼──────────┐
│   LangChain       │   │   LanGraph        │
│  - ChatGroq       │   │  - ReAct Agent    │
│  - Message Types  │   │  - Agent Executor │
│  - Tool Binding   │   │  - Stream Handler │
└────────┬──────────┘   └────────┬──────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   Groq LLM API        │
         │  (qwen/qwen3.6-27b)   │
         └───────────────────────┘
```

### Component Breakdown:

1. **Main Application (`main.py`)**
   - Loads environment variables from `.env` file
   - Initializes the Groq LLM with specified model
   - Defines custom tools (calculator, say_hello)
   - Manages the interactive conversation loop

2. **LangChain Integration**
   - `ChatGroq`: Interface to Groq API
   - `HumanMessage`: User message representation
   - `@tool`: Decorator for defining agent tools

3. **LanGraph Framework**
   - `create_react_agent`: Creates a ReAct agent with tools
   - Handles tool selection, reasoning, and execution
   - Manages message streaming

4. **Tool Layer**
   - **Calculator Tool**: Performs arithmetic operations
   - **Greeting Tool**: Provides personalized greetings

---

## 📋 Prerequisites

Before you begin, ensure you have the following:

- **Python 3.8 or higher** installed on your system
- **Groq API Key** (obtain from [Groq Console](https://console.groq.com))
- **pip** (Python package manager)
- **Git** (optional, for cloning repositories)

---

## 🚀 Installation & Setup

### Step 1: Navigate to Project Directory

```bash
cd d:\KLE_Gangavathi\groq_chatbot
```

### Step 2: Create Virtual Environment

Create a Python virtual environment to isolate project dependencies:

```bash
# Windows (PowerShell)
python -m venv .venv

# Windows (Command Prompt)
python -m venv .venv

# macOS/Linux
python3 -m venv .venv
```

### Step 3: Activate Virtual Environment

#### On Windows (PowerShell):
```bash
.\.venv\Scripts\Activate.ps1
```

If you encounter an execution policy error, run:
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

#### On Windows (Command Prompt):
```bash
.venv\Scripts\activate.bat
```

#### On macOS/Linux:
```bash
source .venv/bin/activate
```

You should see `(.venv)` prefix in your terminal prompt once activated.

### Step 4: Install Dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Step 5: Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
# Windows (PowerShell)
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Or use your preferred text editor and create .env manually
```

**Example `.env` file:**
```
GROQ_API_KEY=your_actual_groq_api_key_here
GROQ_MODEL=qwen/qwen3.6-27b
```

**Where to get your Groq API Key:**
1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key and copy it
5. Paste it into the `.env` file

---

## 💻 Usage

### Running the Chatbot

Once the virtual environment is activated and dependencies are installed:

```bash
python main.py
```

### Interactive Session Example

```
Initializing Groq model: qwen/qwen3.6-27b...
Welcome! I'm your PythonAIChatbot assistant. Type 'quit' to exit.
You can ask me to perform calculations or chat with me.

You: What is 10 plus 5?
Assistant: Tool has been called.
The sum of 10 and 5 is 15

You: Say hello to Alice
Assistant: Tool has been called.
Hello Alice, I hope you are well today

You: quit
```

### Example Queries

- **Calculations**: "Add 25 and 75", "What's 100 + 50?"
- **Greetings**: "Say hello to John", "Greet Sarah"
- **General Chat**: "How are you?", "Tell me a joke"

---

## 📁 Project Structure

```
groq_chatbot/
│
├── main.py                 # Main application file
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .venv/                  # Virtual environment (auto-created)
│   ├── Scripts/            # Executable files
│   ├── Lib/                # Installed packages
│   └── pyvenv.cfg         # Virtual environment config
│
└── README.md              # This file
```

---

## 🛠️ Available Tools

### 1. Calculator Tool
**Purpose**: Performs basic arithmetic calculations

**Usage**: Ask the agent to calculate sums
```
User: Add 50 and 30
Assistant: The sum of 50 and 30 is 80
```

**Parameters**:
- `a` (float): First number
- `b` (float): Second number

**Returns**: String with calculation result

### 2. Say Hello Tool
**Purpose**: Provides personalized greetings

**Usage**: Ask the agent to greet someone
```
User: Greet Marcus
Assistant: Hello Marcus, I hope you are well today
```

**Parameters**:
- `name` (string): Person's name

**Returns**: Greeting message string

---

## ⚙️ Environment Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GROQ_API_KEY` | (required) | Your Groq API authentication key |
| `GROQ_MODEL` | `qwen/qwen3.6-27b` | LLM model to use |

### Available Groq Models

- `qwen/qwen3.6-27b` (default)
- `qwen/qwen-2-7b`
- `mixtral-8x7b-32768`
- `llama2-70b-4096`
- `llama2-90b-3-8b`

To use a different model, update the `GROQ_MODEL` variable in your `.env` file.

---

## 🔧 Extending the Chatbot

### Adding New Tools

To add new functionality, define a new tool using the `@tool` decorator:

```python
@tool
def weather(city: str) -> str:
    """Useful for getting weather information"""
    # Your implementation here
    return f"Weather in {city}: ..."

# Add to tools list in main()
tools = [calculator, say_hello, weather]
```

---

## ❓ Troubleshooting

### Issue: "GROQ_API_KEY is not set in environment"

**Solution**: Ensure your `.env` file exists and contains:
```
GROQ_API_KEY=your_actual_key_here
```

### Issue: Virtual Environment Not Activating

**Windows PowerShell Solution**:
```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### Issue: "ModuleNotFoundError" when running

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
# Verify activation (should see (.venv) in prompt)
pip install -r requirements.txt
```

### Issue: Slow Response Times

**Solution**: The model might be processing a complex query. This is normal. Groq provides fast inference, but reasoning-intensive tasks may take longer.

### Issue: API Rate Limiting

**Solution**: If you encounter rate limits, wait a few moments before sending the next request or upgrade your Groq API plan.

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| langchain-core | >=1.5.2 | Core LangChain functionality |
| langchain-groq | >=1.1.3 | Groq LLM integration |
| langgraph | >=1.2.10 | Agent orchestration framework |
| python-dotenv | >=1.2.2 | Environment variable management |

---

## 📝 Notes

- The chatbot uses temperature setting of `0` for deterministic responses
- Deprecation and user warnings are suppressed for a clean interface
- The agent uses the ReAct framework for intelligent tool selection
- All responses are streamed in real-time for better UX

---

## 📄 License

This project is open source and available for personal and educational use.

---

## 🤝 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Verify your Groq API key is valid
3. Ensure all dependencies are installed correctly
4. Check that Python version is 3.8 or higher

---

**Happy chatting! 🚀**
