import streamlit as st
from langgraph_backend import chatbot, retreiveAllThreads
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid

def generate_threadId():
    threadId = uuid.uuid4()
    return threadId

def reset_chat():
    threadId = generate_threadId()
    st.session_state['threadId'] = threadId
    addThread(st.session_state['threadId'])
    st.session_state['threadNames'][threadId] = f"Chat {len(st.session_state['chatThreads'])}"
    st.session_state['message_history'] = []


def addThread(threadId):
    if threadId not in st.session_state['chatThreads']:
        st.session_state['chatThreads'].append(threadId)

def loadConversation(threadId):
    state = chatbot.get_state(config={'configurable': {'thread_id': threadId}})
    return state.values.get('messages', [])

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'threadId' not in st.session_state:
    st.session_state['threadId'] = generate_threadId()

if 'chatThreads' not in st.session_state:
    st.session_state['chatThreads'] = retreiveAllThreads()

if 'threadNames' not in st.session_state:
    st.session_state['threadNames'] = {}

addThread(st.session_state['threadId'])

for i, threadId in enumerate(st.session_state['chatThreads']):
    if threadId not in st.session_state['threadNames']:
        st.session_state['threadNames'][threadId] = f"Chat {i+1}"


st.sidebar.title("Langraph Chatbot")

if st.sidebar.button('New chat'):
    reset_chat()

st.sidebar.header('My conversations')

for threadId in st.session_state['chatThreads'][::-1]:
    name = st.session_state['threadNames'].get(threadId, str(threadId))
    if st.sidebar.button(name, key=str(threadId)):
        st.session_state['threadId'] = threadId
        messages = loadConversation(threadId)
        tempMessages = []
        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            tempMessages.append({'role':role, 'content':msg.content})
        st.session_state['message_history'] = tempMessages

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    CONFIG = {
        "configurable": {"thread_id": st.session_state["threadId"]},
        "metadata": {"thread_id": st.session_state["threadId"]},
        "run_name": "chat_turn",}
    

    with st.chat_message("assistant"):
        status_holder = {"box": None}
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})