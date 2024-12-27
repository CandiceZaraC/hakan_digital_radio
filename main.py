import streamlit as st
import json
import requests
import os
import uuid
from chat import show_chat_room_page  # Import the chat room page function

def apply_custom_styles():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    # Adding transitions and animations
    st.markdown(
        """
        <style>
        body {
            animation: fadeIn 2s;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        a {
            transition: color 0.3s ease;
        }
        a:hover {
            color: orange;
        }
        .stButton button {
            transition: transform 0.2s;
        }
        .stButton button:hover {
            transform: scale(1.1);
        }
        .stSelectbox > div > div {
            transition: background-color 0.3s;
        }
        .stSelectbox:hover {
            background-color: rgba(255, 255, 255, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    apply_custom_styles()

    st.sidebar.title("Hakan Digital Radio")
    page = st.sidebar.radio("Navigate to:", ["Welcome", "Radio", "Chat room", "About Us"])

    if page == "Welcome":
        show_welcome_page()
    elif page == "Radio":
        show_audio_player_page()
    elif page == "Chat room":
        show_chat_room_page()
    elif page == "About Us":
        show_about_contact_page()

def show_welcome_page():
    st.image("images/HD-Radio-logo1.jpeg", use_container_width=True)
    st.title("Welcome to the Hakan Digital Radio!")
    st.write("This app allows you to explore various functionalities including listening to radio streaming.")

def show_audio_player_page():
    st.markdown("<h1 id='radio'>Radio</h1>", unsafe_allow_html=True)
    st.write("Select a radio station below to start streaming:")

    stations = load_stations()

    col1, col2 = st.columns([1, 2], border=True)

    with col1:
        selected_station = st.selectbox("Choose a station", list(stations.keys()))
        
        try:
            response = requests.get(stations[selected_station], stream=True)
            if response.status_code == 200:
                st.audio(stations[selected_station], format="audio/mp3")
            else:
                st.error("Unable to stream the selected station. Please try another one.")
        except requests.exceptions.RequestException as e:
            st.error(f"Error streaming the station: {e}")
        
        st.write("##### Add a new station")
        st.write("Enter Station Name and URL")
        new_station_name = st.text_input("Station name", key="new_station_name", label_visibility="collapsed")
        new_station_url = st.text_input("Station URL", key="new_station_url", label_visibility="collapsed")

        if st.button("Add station"):
            if new_station_name and new_station_url:
                stations[new_station_name] = new_station_url
                save_stations(stations)
                st.success(f"Station '{new_station_name}' added successfully!")
            else:
                st.error("Please provide both a station name and URL.")


        st.write("##### Remove a station")
        station_to_remove = st.selectbox("Select a station to remove", list(stations.keys()))
        if st.button("Remove station"):
            stations.pop(station_to_remove)
            save_stations(stations)
            st.success(f"Station '{station_to_remove}' removed successfully!")
        
        st.write("##### Manage stations")
        if st.button("Reset stations"):
            os.remove("stations.json")
            st.success("All stations reset successfully!")

    with col2:
        # add a chat room to the radio page which changes with the selected station
        st.write("### Chat")
        

def show_about_contact_page():
    st.markdown("<h1 id='about-us'>About Us</h1>", unsafe_allow_html=True)
    st.write("Feel free to reach out to us with any questions or feedback.")
    st.write("### Contact Information")
    st.write("- Email: www.linkedin.com/in/krishnacheedella")
    st.write("- Phone: +123 456 7890")
    st.write("- Address: 123 Zayd Street, Frontier City")

def load_stations():
    try:
        with open("stations.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "BBC World Service": "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
            "NPR News": "https://npr-ice.streamguys1.com/live.mp3",
            "Radio Swiss Jazz": "http://stream.srg-ssr.ch/m/rsj/mp3_128"
        }

def save_stations(stations):
    with open("stations.json", "w") as f:
        json.dump(stations, f)

if __name__ == "__main__":
    main()