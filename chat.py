import streamlit as st
import json
import os
from streamlit_autorefresh import st_autorefresh

# Define file path to store messages
MESSAGE_FILE_PATH = "chat_messages.json"

# Ensure the JSON file exists or create an empty one if it doesn't
if not os.path.exists(MESSAGE_FILE_PATH):
    with open(MESSAGE_FILE_PATH, "w") as f:
        json.dump([], f)

# Function to get all messages from the file
def get_messages():
    try:
        with open(MESSAGE_FILE_PATH, "r") as f:
            messages = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Return an empty list if the file is missing, empty, or invalid
        messages = []
    return messages

# Function to save a new message to the file
def save_message(username, message):
    messages = get_messages()
    messages.append({"username": username, "message": message})
    with open(MESSAGE_FILE_PATH, "w") as f:
        json.dump(messages, f)

def show_chat_room_page():
    st.title("Public Chat Room")

    # Initialize session state for messages if not already initialized
    if "messages" not in st.session_state:
        st.session_state.messages = get_messages()

    # Auto-refresh every 200 ms (adjust interval as needed)
    st_autorefresh(interval=200, key="refresh")

    # Display chat history
    if st.session_state.messages:
        for msg in st.session_state.messages:
            st.write(f"**{msg['username']}:** {msg['message']}")
    else:
        st.info("The chat room is currently empty. Start the conversation!")

    # User input for sending a message
    username = st.text_input("Enter your username:")
    message = st.text_area("Enter your message:")

    # Handle sending a message
    if st.button("Send"):
        if username and message:
            save_message(username, message)
            # Update session state with new messages
            st.session_state.messages = get_messages()
        else:
            st.error("Please enter both username and message.")

# Call the chat room page function
# show_chat_room_page()
