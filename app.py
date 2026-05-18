import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Voice Assistant",
    layout="centered"
)

# ---------------- TITLE ----------------

st.title("🎤 AI Voice Assistant")

st.write("Simple Voice Assistant without API Key")

# ---------------- SPEECH TO TEXT ----------------

def speech_to_text():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        st.info("🎙 Listening... Speak Now")

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        return text.lower()

    except Exception as e:

        return f"Error: {e}"

# ---------------- SIMPLE AI RESPONSE ----------------

def generate_response(user_text):

    if "hello" in user_text:
        return "Hello! How can I help you today?"

    elif "your name" in user_text:
        return "I am your AI Voice Assistant."

    elif "time" in user_text:

        from datetime import datetime

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}"

    elif "date" in user_text:

        from datetime import datetime

        current_date = datetime.now().strftime("%d %B %Y")

        return f"Today's date is {current_date}"

    elif "weather" in user_text:
        return "Weather integration can be added later."

    elif "bye" in user_text:
        return "Goodbye! Have a great day."

    else:
        return "Sorry, I did not understand that."

# ---------------- TEXT TO SPEECH ----------------

def text_to_speech(text):

    tts = gTTS(text=text)

    audio_file = "response.mp3"

    tts.save(audio_file)

    return audio_file

# ---------------- BUTTON ----------------

if st.button("🎤 Start Voice Assistant"):

    # Convert Speech to Text
    user_text = speech_to_text()

    # Show User Speech
    st.subheader("🗣 You Said")

    st.write(user_text)

    # Generate Response
    ai_reply = generate_response(user_text)

    # Show AI Reply
    st.subheader("🤖 Assistant Response")

    st.write(ai_reply)

    # Convert Response to Voice
    audio_path = text_to_speech(ai_reply)

    # Play Audio
    audio_file = open(audio_path, "rb")

    audio_bytes = audio_file.read()

    st.audio(audio_bytes, format="audio/mp3")
