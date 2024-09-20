import os

import streamlit as st
from dotenv import load_dotenv

from database_chatbot import DatabaseChatbot


# Initialize the DatabaseChatbot
@st.cache_resource
def get_chatbot():
    db_url = os.getenv("DB_URL")
    return DatabaseChatbot(db_url)


load_dotenv("./.env")
chatbot = get_chatbot()

# Set up the Streamlit UI
st.title("Database Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is your question?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Analyzing...")

        # Get chatbot response
        analyzed_query_response = chatbot.extract_user_query(st.session_state.messages)
        if (
            analyzed_query_response.is_attack_detected
            or analyzed_query_response.is_toxicity_detected
        ):
            st.session_state.messages.pop()
            response = "Your query has triggered our security protocols due to potentially \
                unsafe or inappropriate content. Please review and modify your input. \
                If you believe this is a mistake, you can try rephrasing or contact support for assistance."
        else:
            message_placeholder.markdown("Processing...")
            response = chatbot.query(analyzed_query_response.extracted_query)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

        message_placeholder.markdown(response)
