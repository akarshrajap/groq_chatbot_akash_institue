import os
import ast
import warnings
import traceback
import streamlit as st
from dotenv import load_dotenv

# Filter deprecation and user warnings for a clean Streamlit interface
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()

# Check optional Groq/LangChain/LangGraph dependencies
HAS_GROQ = True
try:
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
    from langchain_groq import ChatGroq
    from langchain_core.tools import tool
    from langgraph.prebuilt import create_react_agent
except Exception:
    HAS_GROQ = False

# Decorator fallback if langchain @tool is unavailable
def _noop_tool(fn=None):
    if fn is None:
        return lambda f: f
    return fn

tool_decorator = tool if HAS_GROQ else _noop_tool


# --- AGENT TOOLS ---

@tool_decorator
def calculator(a: float, b: float) -> str:
    """Perform addition of two numbers and return a human-readable result.

    Args:
        a: First number.
        b: Second number.

    Returns:
        A formatted string with the sum of `a` and `b`.
    """
    return f"The sum of {a} and {b} is {a + b}"


@tool_decorator
def say_hello(name: str) -> str:
    """Return a friendly personalized greeting for the given name.

    Args:
        name: The name of the person to greet.

    Returns:
        A friendly greeting string addressed to `name`.
    """
    cleaned_name = name.strip() if name else "there"
    return f"Hello {cleaned_name}, I hope you are having a wonderful day!"


# --- INTERACTIVE TOOL UI PANELS ---

def calculator_interface():
    st.markdown("##### 🧮 Quick Calculator Tool")
    col1, col2 = st.columns(2)
    with col1:
        a = st.number_input("First Number (A)", value=10.0, step=1.0, key="calc_a")
    with col2:
        b = st.number_input("Second Number (B)", value=5.0, step=1.0, key="calc_b")

    if st.button("Compute Sum", type="primary", use_container_width=True):
        res = calculator(a, b)
        st.success(f"**Result:** {res}")


def greeting_interface():
    st.markdown("##### 👋 Greeting Tool")
    name = st.text_input("Name", value="Akarsh", key="greet_name")
    if st.button("Generate Greeting", type="primary", use_container_width=True):
        res = say_hello(name)
        st.info(f"**Greeting:** {res}")


# --- FALLBACK HEURISTIC & SAFE AST STUB ---

def generate_response_stub(query: str) -> str:
    """Provides safe offline fallback responses when Groq API key is unavailable or fails."""
    q = query.lower().strip()
    
    # Handle greeting triggers
    if any(q.startswith(w) for w in ["hello", "hi", "hey", "greet"]):
        parts = query.strip().split()
        target_name = "there"
        if len(parts) > 1 and parts[1].lower() not in ["there", "to", "bot", "assistant"]:
            target_name = parts[1]
        elif len(parts) > 2 and parts[1].lower() in ["to", "for"]:
            target_name = parts[2]
        return say_hello(target_name)
        
    # Handle simple arithmetic queries like "25 + 75" or "10 * 5"
    if any(op in q for op in ["+", "-", "*", "/", "^"]):
        try:
            cleaned = q.replace("^", "**")
            allowed_chars = "0123456789+-*/().eE ^"
            filtered = "".join(ch for ch in cleaned if ch in allowed_chars).strip()
            if filtered:
                def safe_eval(expr: str) -> float:
                    node = ast.parse(expr, mode="eval")
                    for n in ast.walk(node):
                        if not isinstance(n, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Load, ast.operator, ast.unaryop, ast.Constant, ast.Pow)):
                            raise ValueError("Unsupported expression")
                        if isinstance(n, ast.Call):
                            raise ValueError("Function calls disallowed")
                    return eval(compile(node, "<ast>", "eval"), {"__builtins__": {}}, {})

                result = safe_eval(filtered)
                return f"Result of `{filtered}` is **{result}**"
        except Exception:
            pass

    return f"🤖 **(Groq Offline Fallback)** I received your message: *\"{query}\"*\n\n*To enable real AI responses, please configure your `GROQ_API_KEY` in the sidebar or `.env` file.*"


# --- GROQ AGENT RESPONSE GENERATOR ---

def extract_message_text(msg) -> str:
    """Helper to cleanly extract text content from LangChain message objects."""
    if hasattr(msg, "content"):
        content = msg.content
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            # Extract text elements if content is structured as a list of blocks
            parts = []
            for item in content:
                if isinstance(item, str):
                    parts.append(item)
                elif isinstance(item, dict) and item.get("type") == "text":
                    parts.append(item.get("text", ""))
            return "".join(parts)
        return str(content)
    return str(msg)


def generate_response(query: str, history: list, api_key: str, model_name: str, temperature: float) -> str:
    """Generates an AI response using ChatGroq & LangGraph ReAct agent with fallback support."""
    if not api_key:
        return generate_response_stub(query)

    if not HAS_GROQ:
        return "⚠️ Required dependencies (`langchain-groq`, `langgraph`) are missing.\n\n" + generate_response_stub(query)

    try:
        model = ChatGroq(
            groq_api_key=api_key,
            model=model_name,
            temperature=temperature
        )

        tools = [calculator, say_hello]
        
        # Build LangGraph ReAct Agent
        agent = create_react_agent(model, tools=tools)

        # Convert chat history to LangChain message instances
        langchain_messages = [
            SystemMessage(content="You are a helpful, intelligent AI Assistant powered by Groq. You have access to tools for calculations and greetings. Use them when appropriate.")
        ]
        
        for role, text in history:
            if role == "user":
                langchain_messages.append(HumanMessage(content=text))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=text))
                
        # Append current user prompt
        langchain_messages.append(HumanMessage(content=query))

        # Invoke ReAct agent execution graph
        response_state = agent.invoke({"messages": langchain_messages})
        
        # Retrieve final assistant output
        if "messages" in response_state and len(response_state["messages"]) > 0:
            final_msg = response_state["messages"][-1]
            return extract_message_text(final_msg)
        else:
            return "No response generated by agent."

    except Exception as e:
        err_msg = str(e)
        # Attempt direct model fallback if ReAct agent graph invocation hits an issue
        try:
            model = ChatGroq(groq_api_key=api_key, model=model_name, temperature=temperature)
            resp = model.invoke([HumanMessage(content=query)])
            return extract_message_text(resp)
        except Exception as direct_err:
            st.toast(f"Groq API Error: {err_msg}", icon="⚠️")
            return f"⚠️ **Groq API Request Failed**: {err_msg}\n\nFalling back to offline mode:\n" + generate_response_stub(query)


# --- STREAMLIT UI MAIN APP ---

def app():
    st.set_page_config(
        page_title="Groq AI Chatbot",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for modern dark-mode styling and chat UI layout
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
        }
        .hero-banner {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 2.5rem 1.5rem;
            border-radius: 16px;
            text-align: center;
            border: 1px solid #334155;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            margin-bottom: 2rem;
        }
        .hero-title {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(90deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .hero-subtitle {
            color: #94a3b8;
            font-size: 1.1rem;
        }
        .status-badge-ok {
            background-color: #064e3b;
            color: #34d399;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .status-badge-warn {
            background-color: #78350f;
            color: #fbbf24;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "show_tools" not in st.session_state:
        st.session_state.show_tools = False

    # --- SIDEBAR CONFIGURATION ---
    with st.sidebar:
        st.title("⚡ Groq Settings")
        st.markdown("---")

        # API Key management
        env_key = os.getenv("GROQ_API_KEY", "")
        user_api_key = st.text_input(
            "Groq API Key",
            value=env_key,
            type="password",
            placeholder="gsk_...",
            help="Enter your Groq API Key or set GROQ_API_KEY in .env"
        )
        api_key = user_api_key.strip() if user_api_key else env_key.strip()

        if api_key:
            st.markdown('<span class="status-badge-ok">🟢 Groq API Connected</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="status-badge-warn">🟡 Offline / Fallback Mode</span>', unsafe_allow_html=True)

        st.markdown("---")

        # Model selection
        model_name = st.selectbox(
            "Model Selection",
            options=[
                "qwen/qwen3.6-27b",
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it"
            ],
            index=0,
            help="Choose the Groq LLM model architecture"
        )

        # Temperature setting
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.1,
            help="Lower values yield deterministic responses; higher values yield creative outputs."
        )

        st.markdown("---")

        # Utility actions
        st.session_state.show_tools = st.checkbox("🛠️ Show Interactive Tool Panel", value=st.session_state.show_tools)

        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.caption("Powered by **Groq Cloud**, **LangChain** & **LangGraph**")

    # --- MAIN CONTENT AREA ---
    col_left, col_center, col_right = st.columns([1, 10, 1])

    with col_center:
        # Hero Banner Header
        st.markdown(
            """
            <div class="hero-banner">
                <div class="hero-title">⚡ Groq AI Assistant</div>
                <div class="hero-subtitle">Ultra-fast conversational AI with integrated ReAct tools</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Optional Interactive Tools Drawer
        if st.session_state.show_tools:
            with st.expander("🛠️ Interactive Tools Panel", expanded=True):
                tool_choice = st.radio("Select Tool", ["Calculator", "Greeting Tool"], horizontal=True)
                if tool_choice == "Calculator":
                    calculator_interface()
                else:
                    greeting_interface()
            st.markdown("---")

        # Render Chat History
        for role, text in st.session_state.messages:
            avatar = "👤" if role == "user" else "⚡"
            with st.chat_message(role, avatar=avatar):
                st.markdown(text)

        # Streamlit Chat Input (auto-clears on submit)
        user_input = st.chat_input("Type your message here (e.g., 'What is 125 + 375?' or 'Say hello to Alice')...")

        if user_input:
            # Display user message immediately
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            # Generate AI response with spinner
            with st.chat_message("assistant", avatar="⚡"):
                with st.spinner("Thinking with Groq LLM..."):
                    response_text = generate_response(
                        query=user_input,
                        history=st.session_state.messages,
                        api_key=api_key,
                        model_name=model_name,
                        temperature=temperature
                    )
                    st.markdown(response_text)

            # Store in session state history
            st.session_state.messages.append(("user", user_input))
            st.session_state.messages.append(("assistant", response_text))


if __name__ == "__main__":
    app()