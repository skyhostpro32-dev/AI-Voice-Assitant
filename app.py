import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="AI Voice Assistant",
    layout="centered"
)

# ---------------- TITLE ----------------

st.title("🎤 AI Voice Assistant")

st.write("Upload WAV audio and get AI voice response")

# ---------------- FILE UPLOAD ----------------

audio_file = st.file_uploader(
    "Upload WAV Audio File",
    type=["wav"]
)

# ---------------- SPEECH TO TEXT ----------------

def speech_to_text(audio_path):

    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:

        audio = recognizer.record(source)

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

    elif "weather" in user_text:
        return "Weather feature can be added later."

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

    # Save Uploaded Audio
    with open("temp.wav", "wb") as f:

        f.write(audio_file.read())

    # Convert Audio to Text
    user_text = speech_to_text("temp.wav")

    # Show User Text
    st.subheader("🗣 You Said")

    st.write(user_text)

    # Generate Assistant Response
    ai_reply = generate_response(user_text)

    # Show AI Response
    st.subheader("🤖 Assistant Response")

    st.write(ai_reply)

    # Convert Response to Voice
    audio_path = text_to_speech(ai_reply)

    # Play Audio
    st.audio(audio_path)
