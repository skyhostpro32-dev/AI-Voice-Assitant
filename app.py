import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
from datetime import datetime

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Advanced AI Voice Assistant",
    layout="centered"
)

# ---------------- TITLE ----------------

st.title("🎤 Advanced AI Voice Assistant")

st.write("Upload WAV audio and get smart AI responses")

# ---------------- SIDEBAR ----------------

st.sidebar.header("⚙️ Settings")

language_option = st.sidebar.selectbox(
    "Translate Response To",
    [
        "English",
        "Tamil",
        "Hindi",
        "French"
    ]
)

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

# ---------------- AI RESPONSE ----------------

def generate_response(user_text):

    if "hello" in user_text:
        return "Hello! How can I help you today?"

    elif "your name" in user_text:
        return "I am your Advanced AI Voice Assistant."

    elif "time" in user_text:

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}"

    elif "date" in user_text:

        current_date = datetime.now().strftime("%d %B %Y")

        return f"Today's date is {current_date}"

    elif "motivate" in user_text:
        return "Believe in yourself. Every expert was once a beginner."

    elif "weather" in user_text:
        return "Weather feature will be added in the next version."

    elif "bye" in user_text:
        return "Goodbye! Have a wonderful day."

    else:
        return "Sorry, I could not understand your request."

# ---------------- SIMPLE TRANSLATION ----------------

def translate_text(text, language):

    translations = {

        "Tamil": "வணக்கம்! இது தமிழில் மாற்றப்பட்ட பதில்.",

        "Hindi": "नमस्ते! यह हिंदी में अनुवादित उत्तर है।",

        "French": "Bonjour! Ceci est une réponse traduite en français.",

        "English": text
    }

    return translations.get(language, text)

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

    # Convert speech to text

    user_text = speech_to_text(audio_path)

    # Display user speech

    st.subheader("🗣 You Said")

    st.write(user_text)

    # Generate AI response

    ai_reply = generate_response(user_text)

    # Translate response

    translated_reply = translate_text(
        ai_reply,
        language_option
    )

    # Show response

    st.subheader("🤖 Assistant Response")

    st.write(translated_reply)

    # Voice output

    response_audio = text_to_speech(translated_reply)

    # Play audio

    st.subheader("🔊 Voice Response")

    st.audio(response_audio)

# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("Built with Streamlit + SpeechRecognition + gTTS")
