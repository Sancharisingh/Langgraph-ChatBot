from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
import sqlite3
load_dotenv()

from langgraph.graph.message import add_messages
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

def chatNode(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

connection = sqlite3.connect(database='chatbot.db', check_same_thread=False)

checkpointer = SqliteSaver(conn=connection)
graph = StateGraph(ChatState)

graph.add_node('chatNode', chatNode)

graph.add_edge(START, 'chatNode')
graph.add_edge('chatNode', END)

chatbot = graph.compile(checkpointer=checkpointer)

for checkpoint in checkpointer.list(None):
    print(checkpoint)