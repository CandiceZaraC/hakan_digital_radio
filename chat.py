import streamlit as st
import json
import os
from streamlit_autorefresh import st_autorefresh

# Define file path to store messages
MESSAGE_FILE_PATH = "chat_messages.json"

# Ensure the JSON file exists or create an empty one if it doesn't
if not os.path.exists(MESSAGE_FILE_PATH):
    with open(MESSAGE_FILE_PATH, "w") as f:
        json.dump({}, f)

# Function to get all messages from the file
def get_messages():
    try:
        with open(MESSAGE_FILE_PATH, "r") as f:
            messages = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Return an empty dict if the file is missing, empty, or invalid
        messages = {}
    return messages

# Function to save a new message to the file
def save_message(room, username, message):
    messages = get_messages()
    if room not in messages:
        messages[room] = []
    messages[room].append({"username": username, "message": message})
    with open(MESSAGE_FILE_PATH, "w") as f:
        json.dump(messages, f)

def get_stations():
        try:
            with open("stations.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []

def show_chat_room_page():
    st.title("Radio Chat Rooms")

    # Initialize session state for messages if not already initialized
    if "messages" not in st.session_state:
        st.session_state.messages = get_messages()

    # get the list of stations and add them to rooms
    stations = get_stations()
    for station in stations:
        if station not in st.session_state.messages:
            st.session_state.messages[station] = []
        else:
            try:
                st.session_state.messages[station] = get_messages()[station]
            except KeyError:
                st.session_state.messages[station] = []

    
    # Select or create a chat room
    rooms = list(st.session_state.messages.keys())
    col1, col2 = st.columns([1, 2], border=True)

    with col1:
        selected_room = st.selectbox("Select a chat room", rooms)
        # create a seperator to add a new chat room
        st.markdown("---")
        st.write("###### Create a new chat room")
        new_room = st.text_input("Or create a new chat room", key="new_room", label_visibility="collapsed")

        if st.button("Create room"):
            if new_room:
                selected_room = new_room
                if new_room not in st.session_state.messages:
                    st.session_state.messages[new_room] = []
                st.success(f"Chat room '{new_room}' created successfully!")
            else:
                st.error("Please enter a name for the new chat room.")
        
        # delete a chat room
        st.markdown("---")
        st.write("###### Delete a chat room")
        room_to_delete = st.selectbox("Select a room to delete", rooms)
        if st.button("Delete room"):
            st.session_state.messages.pop(room_to_delete)
            st.success(f"Chat room '{room_to_delete}' deleted successfully!")

    with col2:
        # st.write("##### Chat Room List")
        if selected_room:
            st.subheader(f"Chat Room: {selected_room}")
            st.markdown("---")

            # Auto-refresh every 200 ms (adjust interval as needed)
            st_autorefresh(interval=200, key="refresh")

            # Display chat history
            if st.session_state.messages[selected_room]:
                for msg in st.session_state.messages[selected_room]:
                    st.write(f"**{msg['username']}:** {msg['message']}")
            else:
                st.info("The chat room is currently empty. Start the conversation!")

            # User input for sending a message
            st.markdown("---")
            username = st.text_input("Enter your username:", key="username", value="Enter your username", label_visibility="collapsed")
            message = st.text_area("Enter your message:")

            # Handle sending a message
            if st.button("Send"):
                if username and message:
                    save_message(selected_room, username, message)
                    # Update session state with new messages
                    st.session_state.messages = get_messages()
                else:
                    st.error("Please enter both username and message.")

# Call the chat room page function
# show_chat_room_page()