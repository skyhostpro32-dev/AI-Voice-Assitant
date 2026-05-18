import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Voice Assistant",
    layout="centered"
)

# ---------------- TITLE ----------------

st.title("🎤 AI Voice Assistant")

st.write("Upload WAV audio and get AI response")

# ---------------- FILE UPLOADER ----------------

audio_file = st.file_uploader(
    "Upload WAV Audio File",
    type=["wav"]
)

# ---------------- SPEECH TO TEXT ----------------

def speech_to_text(audio_path):

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_path) as source:

            audio = recognizer.record(source)

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

    elif "weather" in user_text:
        return "Weather feature can be added later."

    elif "time" in user_text:

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}"

    elif "date" in user_text:

        current_date = datetime.now().strftime("%d %B %Y")

        return f"Today's date is {current_date}"

    elif "bye" in user_text:
        return "Goodbye! Have a great day."

    else:
        return "Sorry, I could not understand."

# ---------------- TEXT TO SPEECH ----------------

def text_to_speech(text):

    tts = gTTS(text=text)

    temp_audio = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts.save(temp_audio.name)

    return temp_audio.name

# ---------------- MAIN APP ----------------

if audio_file is not None:

    # Save uploaded WAV file

    temp_wav = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    temp_wav.write(audio_file.read())

    audio_path = temp_wav.name

    # Speech Recognition

    user_text = speech_to_text(audio_path)

    # Show User Speech

    st.subheader("🗣 You Said")

    st.write(user_text)

    # Generate AI Reply

    ai_reply = generate_response(user_text)

    # Show AI Response

    st.subheader("🤖 Assistant Response")

    st.write(ai_reply)

    # Convert to Speech

    response_audio = text_to_speech(ai_reply)

    # Play Audio

    st.subheader("🔊 Voice Response")

    st.audio(response_audio)
