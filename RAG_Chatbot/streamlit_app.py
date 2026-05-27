import streamlit as st
from history_aware_generation import ask_question

# Page config
st.set_page_config(
    page_title="Simple RAG Chat",
    page_icon="🤖",
    layout="centered"
)

# Title
st.title("🤖 Simple RAG Chat UI")
st.markdown("Ask questions based on your ingested documents")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask a question...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = ask_question(user_input)
            st.markdown(response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": response})

