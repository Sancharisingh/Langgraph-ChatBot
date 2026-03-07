# AI Chatbot

A conversational chatbot built with **LangGraph**, **LangChain**, and **Google's Gemini** (gemini-2.5-flash). The bot keeps conversation history per thread using in-memory checkpoints so it can remember context within a session.

## Features

- **LangGraph** – State-graph workflow with a single chat node
- **Gemini** – Google’s `gemini-2.5-flash` model for responses
- **Thread memory** – `MemorySaver` checkpointer so each thread keeps its own message history
- **Simple CLI** – Type in the notebook; type `exit`, `bye`, or `quit` to stop

## Prerequisites

- Python 3.13+ (project uses a venv named `myenv`)
- A [Google AI API key](https://aistudio.google.com/apikey) for Gemini

## Setup

1. **Clone or open the project**
   ```bash
   cd /path/to/AI
   ```

2. **Create and activate the virtual environment**
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate   # macOS/Linux
   # or: myenv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install langgraph langchain-core langchain-google-genai python-dotenv
   ```

4. **Configure the API key**  
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   Do not commit `.env` or share your API key.

## How to Run

1. Activate the venv (if not already):
   ```bash
   source myenv/bin/activate
   ```

2. Start Jupyter and open the notebook:
   ```bash
   jupyter notebook chatbot.ipynb
   ```
   Or open `chatbot.ipynb` in VS Code / Cursor and run the cells.

3. **Run all cells in order** (they load env, define the graph, and compile the chatbot).

4. When you reach the cell with the `while True:` loop, type in the box and press Enter to chat. Type `exit`, `bye`, or `quit` to stop.

## Project Structure

```
AI/
├── chatbot.ipynb    # Main notebook: graph definition + chat loop
├── .env             # GOOGLE_API_KEY (create this, do not commit)
├── myenv/           # Python virtual environment
└── README.md        # This file
```

## Dependencies (summary)

| Package                | Purpose                    |
|------------------------|----------------------------|
| `langgraph`           | State graph and checkpointer |
| `langchain-core`      | Messages and base types    |
| `langchain-google-genai` | Gemini chat model       |
| `python-dotenv`       | Load `GOOGLE_API_KEY` from `.env` |

## Notes

- The chatbot uses a fixed `thread_id` (`'1'`) in the notebook, so all messages in that run share one conversation history.
- For production, use a persistent checkpointer (e.g. database) instead of `MemorySaver` so state survives restarts.
