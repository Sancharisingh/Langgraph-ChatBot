```markdown
# LangGraph Chatbot (Streamlit + Gemini)

A multi-turn chat UI built with **Streamlit**, **LangGraph**, and **Google Gemini** (`gemini-2.5-flash`). The assistant can call tools (web search, calculator, stock quotes); conversations are **persisted per thread** in SQLite via LangGraph’s checkpointer.

## Features

- **Streamlit chat UI** – Sidebar for “New chat” and switching conversations; streaming assistant replies.
- **LangGraph agent** – Chat node ↔ tools loop with `tools_condition` routing.
- **Persistent threads** – `SqliteSaver` on `chatbot.db`; thread list is restored from checkpoints.
- **Tools**
  - **DuckDuckGo search** (`langchain_community.tools.DuckDuckGoSearchRun`)
  - **Calculator** – add / sub / mul / div
  - **Stock quote** – Alpha Vantage `GLOBAL_QUOTE` (see [API key note](#alpha-vantage-stock-tool) below)

## Prerequisites

- Python 3.10+ (3.13 is fine if your stack supports it)
- **Google AI API key** for Gemini ([Google AI Studio](https://aistudio.google.com/apikey))

## Setup

1. **Clone / open the project**
   ```bash
   cd /path/to/Chatbot
   ```

2. **Virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # macOS/Linux
   # .venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit langgraph langchain-core langchain-google-genai langchain-community python-dotenv requests
   ```

4. **Environment variables**  
   Create a `.env` in the project root (this repo’s `.gitignore` already ignores `.env`):
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Run the app

```bash
source .venv/bin/activate   # if not already active
streamlit run streamlit_frontend.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

## Optional: Jupyter notebook

`chatbot.ipynb` is a simpler, **in-memory** (`MemorySaver`) graph without the Streamlit app or SQLite file. To use it:

```bash
pip install jupyter ipykernel
jupyter notebook chatbot.ipynb
```

Run cells in order; the notebook flow differs from the Streamlit + `langgraph_backend.py` stack.

## Project structure

```
Chatbot/
├── streamlit_frontend.py   # Streamlit UI, streaming, thread sidebar
├── langgraph_backend.py    # Graph, Gemini + tools, SQLite checkpointer
├── chatbot.ipynb           # Standalone notebook prototype
├── chatbot.db              # Created at runtime (SQLite checkpoints)
├── .env                    # GOOGLE_API_KEY (you create this; do not commit)
└── README.md
```

## How it fits together

- **`langgraph_backend.py`** compiles the graph with `SqliteSaver` and exposes `chatbot` and `retreiveAllThreads()`.
- **`streamlit_frontend.py`** keeps `thread_id` in session state, streams `chatbot.stream(..., stream_mode="messages")`, and shows tool use in a `st.status` block when a `ToolMessage` appears.

## Alpha Vantage (stock tool)

`get_stock_price` in `langgraph_backend.py` calls Alpha Vantage. The URL in code must use a **real** API key from [Alpha Vantage](https://www.alphavantage.co/support/#api-key); a placeholder string will not return live data. For production, prefer reading the key from an environment variable instead of hardcoding it.


---
