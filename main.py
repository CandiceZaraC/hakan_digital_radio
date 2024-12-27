import streamlit as st

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
    page = st.sidebar.radio("Navigate to:", ["Welcome", "Radio", "About Us"])

    if page == "Welcome":
        show_welcome_page()
    elif page == "Radio":
        show_audio_player_page()
    elif page == "About Us":
        show_about_contact_page()

def show_welcome_page():
    st.image("images/HD-Radio-logo1.jpeg", use_container_width=True)
    st.title("Welcome to the Hakan Digital Radio!")
    st.write("This app allows you to explore various functionalities including listening to radio streaming.")

def show_audio_player_page():
    st.markdown("<h1 id='radio'>Radio</h1>", unsafe_allow_html=True)
    st.write("Select a radio station below to start streaming:")

    stations = {
        "BBC World Service": "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
        "NPR News": "https://npr-ice.streamguys1.com/live.mp3",
        "Classic FM": "http://media-ice.musicradio.com/ClassicFMMP3",
        "Jazz24": "http://live.wostreaming.net/direct/ppm-jazz24mp3-ibc1",
        "Radio Swiss Jazz": "http://stream.srg-ssr.ch/m/rsj/mp3_128"
    }

    selected_station = st.selectbox("Choose a station", list(stations.keys()))
    st.audio(stations[selected_station], format="audio/mp3")

def show_about_contact_page():
    st.markdown("<h1 id='about-us'>About Us</h1>", unsafe_allow_html=True)
    st.write("Feel free to reach out to us with any questions or feedback.")
    st.write("### Contact Information")
    st.write("- Email: www.linkedin.com/in/krishnacheedella")
    st.write("- Phone: +123 456 7890")
    st.write("- Address: 123 Zayd Street, Frontier City")

if __name__ == "__main__":
    main()
