# Langgraph-Chatbot

A **tool-enabled AI chatbot built with LangGraph, LangChain, and Streamlit**.
The chatbot supports **multiple conversation threads, tool calling, persistent memory using SQLite, and streaming responses**.

The system allows the AI to dynamically use tools such as:

* Web search
* Stock price lookup
* Calculator

All conversations are **persisted in a SQLite checkpoint database**, so chat history is retained across sessions.

---

# Features

* **LangGraph agent workflow**
* **Tool calling support**
* **Web search using DuckDuckGo**
* **Stock price lookup using Alpha Vantage API**
* **Calculator tool**
* **Streaming AI responses**
* **Persistent chat memory with SQLite**
* **Multiple conversation threads**
* **Streamlit UI**

---

# Project Structure

```
.
├── langgraph_backend.py      # LangGraph agent + tools + SQLite checkpoint
├── streamlit_frontend.py     # Streamlit UI for the chatbot
├── chatbot.db                # SQLite database for storing conversation states
├── .env                      # Environment variables
├── requirements.txt          # Project dependencies
└── README.md
```

---

# Architecture

The system is built using a **LangGraph state machine**.

### Chat State

The conversation state contains a list of messages.

```python
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

Messages automatically accumulate across turns.

---

### Graph Flow

```
START
  │
  ▼
chatNode (LLM)
  │
  ├── If tool required ───► tools
  │                         │
  │                         ▼
  └────────────────────── chatNode
                            │
                            ▼
                           END
```

* The **LLM node decides whether a tool is required**
* If needed, execution moves to the **ToolNode**
* The result is sent back to the LLM
* The cycle continues until the final answer is produced

---

# Tools Available

### Web Search

Uses DuckDuckGo search.

```
DuckDuckGoSearchRun
```

---

### Calculator Tool

Supports arithmetic operations:

* add
* sub
* mul
* div

Example input:

```
first_num = 5
second_num = 3
operation = "mul"
```

---

### Stock Price Tool

Fetches the latest stock data from **Alpha Vantage API**.

Example:

```
get_stock_price("AAPL")
```

---

# Memory & Persistence

Conversation memory is stored using **LangGraph checkpointing with SQLite**.

```python
checkpointer = SqliteSaver(conn=connection)
```

Benefits:

* Conversations persist across restarts
* Multiple chat threads supported
* Conversation history can be loaded anytime

The Streamlit UI retrieves past conversations using:

```
retreiveAllThreads()
```

which scans the SQLite checkpoints. 

---

# Frontend (Streamlit)

The frontend provides:

* Chat interface
* Sidebar conversation list
* New chat creation
* Streaming responses
* Tool usage status indicators

When the AI calls a tool, the UI shows a **status indicator** while the tool runs. 

---

# Installation

## 1 Create Virtual Environment

```bash
python3 -m venv myenv
```

Activate it:

Mac/Linux

```bash
source myenv/bin/activate
```

Windows

```bash
myenv\Scripts\activate
```

---

## 2 Install Dependencies

Create `requirements.txt`

```
streamlit
langchain
langgraph
langchain-google-genai
langchain-community
duckduckgo-search
python-dotenv
requests
```

Install:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```
GOOGLE_API_KEY=your_google_api_key
```

For stock price tool, replace the API key inside:

```
Alpha_Vantage_API_KEY
```

with your Alpha Vantage key.

---

# Running the Application

Start the Streamlit app:

```bash
streamlit run streamlit_frontend.py
```

Then open:

```
http://localhost:8501
```

---

# Example Queries

Try asking:

```
What is the stock price of Tesla?
```

```
Search latest news about AI
```

```
Calculate 45 * 23
```

The AI will automatically decide whether to call a tool.

---

# Conversation Threads

The chatbot supports **multiple chat sessions**.

Features:

* New chat button
* Sidebar conversation history
* Switching between threads
* SQLite-backed persistent storage

---

# Key Technologies

* **LangGraph** – agent workflow and state management
* **LangChain** – tool integration
* **Google Gemini** – LLM
* **Streamlit** – UI
* **SQLite** – persistent memory

---

# Future Improvements

Possible extensions:

* Add RAG with vector database
* Add file upload support
* Add conversation summarization
* Add authentication
* Add more tools (weather, finance APIs)
