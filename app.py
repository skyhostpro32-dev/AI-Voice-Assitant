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

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

/* ---------------- MAIN APP ---------------- */

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* ---------------- TITLE ---------------- */

h1 {
    text-align: center;
    font-size: 3rem !important;
    color: #38bdf8 !important;
    font-weight: 700;
    margin-bottom: 10px;
    animation: glow 3s infinite;
}

p {
    color: #d1d5db;
    font-size: 1rem;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #334155;
}

/* ---------------- FILE UPLOADER ---------------- */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    border: 2px dashed #38bdf8;
}

/* ---------------- BUTTON ---------------- */

.stButton > button {
    width: 100%;
    background: linear-gradient(
        90deg,
        #06b6d4,
        #3b82f6
    );
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-size: 18px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.03);
}

/* ---------------- AUDIO PLAYER ---------------- */

audio {
    width: 100%;
    margin-top: 10px;
    border-radius: 12px;
}

/* ---------------- SUBHEADERS ---------------- */

h2, h3 {
    color: #f8fafc !important;
    margin-top: 20px;
}

/* ---------------- SELECTBOX ---------------- */

.stSelectbox div[data-baseweb="select"] {
    background: #1e293b;
    border-radius: 10px;
    color: white;
}

/* ---------------- ANIMATION ---------------- */

@keyframes glow {

    0% {
        text-shadow: 0 0 5px #38bdf8;
    }

    50% {
        text-shadow: 0 0 20px #38bdf8;
    }

    100% {
        text-shadow: 0 0 5px #38bdf8;
    }
}

/* ---------------- FOOTER ---------------- */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

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

# ---------------- TRANSLATION ----------------

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
# ---------------- SPEECH STYLE OPTION ----------------

speech_style = st.sidebar.selectbox(
    "🎭 Response Style",
    [
        "Professional",
        "Funny",
        "Friendly",
        "Motivational"
    ]
)

# ---------------- AI RESPONSE ----------------

def generate_response(user_text, style):

    # PROFESSIONAL STYLE

    if style == "Professional":

        if "hello" in user_text:
            return "Hello. How may I assist you today?"

        elif "time" in user_text:

            current_time = datetime.now().strftime("%I:%M %p")

            return f"The current time is {current_time}"

        elif "date" in user_text:

            current_date = datetime.now().strftime("%d %B %Y")

            return f"Today's date is {current_date}"

        else:
            return "I am processing your request professionally."

    # FUNNY STYLE

    elif style == "Funny":

        if "hello" in user_text:
            return "Hey there! Ready to talk with the smartest assistant alive?"

        elif "time" in user_text:

            current_time = datetime.now().strftime("%I:%M %p")

            return f"It is {current_time}. Time flies faster than WiFi speed."

        elif "date" in user_text:

            current_date = datetime.now().strftime("%d %B %Y")

            return f"Today is {current_date}. Another beautiful day to avoid homework."

        else:
            return "Oops! My AI brain needs more coffee to understand that."

    # FRIENDLY STYLE

    elif style == "Friendly":

        return "Hi friend! I'm happy to help you today."

    # MOTIVATIONAL STYLE

    elif style == "Motivational":

        return "Keep pushing forward. Great things take time."

# ---------------- GENERATE RESPONSE ----------------

ai_reply = generate_response(
    user_text,
    speech_style
)
# ---------------- MAIN APP ----------------
# ---------------- MAIN APP ----------------

if audio_file is not None:

    # Save WAV File

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

    # Generate AI Response

    ai_reply = generate_response(
        user_text,
        speech_style
    )

    # Translate Response

    translated_reply = translate_text(
        ai_reply,
        language_option
    )

    # Show AI Response

    st.subheader("🤖 Assistant Response")

    st.write(translated_reply)

    # Generate Voice

    response_audio = text_to_speech(
        translated_reply,
        voice_gender
    )

    # Play Voice

    st.subheader("🔊 Voice Response")

    st.audio(response_audio)
# ---------------- FOOTER ----------------

st.markdown("---")
st.caption("Built with Streamlit + SpeechRecognition + gTTS")
