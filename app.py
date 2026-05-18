# app.py

import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile
from datetime import datetime
import random

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Jarvis AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SESSION STATE ----------------

if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #020617;
}

h1 {
    color: white;
    text-align: center;
    font-size: 60px;
}

.stMarkdown {
    color: white;
}

.stButton button {
    width: 100%;
    height: 55px;
    border-radius: 14px;
    border: none;
    font-size: 18px;
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color: white;
}

.response-box {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    color: white;
}

.user-box {
    background: #0f172a;
    padding: 20px;
    border-radius: 15px;
    color: #38bdf8;
}

.sidebar .sidebar-content {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("⚙️ Settings")

    personality = st.selectbox(
        "Assistant Personality",
        [
            "Professional",
            "Funny",
            "Motivational"
        ]
    )

    language = st.selectbox(
        "Voice Language",
        [
            "en",
            "ta",
            "hi"
        ]
    )

    st.divider()

    st.markdown("### 🤖 Features")

    st.write("✅ Voice AI")
    st.write("✅ Chat History")
    st.write("✅ AI Personality")
    st.write("✅ Voice Response")

# ---------------- TITLE ----------------

st.title("🤖 Jarvis AI Assistant")

st.markdown(
    "<h4 style='text-align:center;color:lightgray;'>Advanced AI Voice Assistant</h4>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- FILE UPLOADER ----------------

audio_file = st.file_uploader(
    "📤 Upload WAV Audio",
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

def generate_response(user_text, personality):

    greetings = [
        "Hello! Nice to meet you.",
        "Hi there! How can I help you?",
        "Hey! Welcome back."
    ]

    jokes = [
        "Why do programmers hate nature? Too many bugs.",
        "Python developers never sleep. They just wait.",
        "AI is learning faster than humans."
    ]

    motivational = [
        "Believe in yourself.",
        "Success comes from consistency.",
        "Keep learning and building."
    ]

    if "hello" in user_text:

        return random.choice(greetings)

    elif "your name" in user_text:

        return "I am Jarvis, your AI assistant."

    elif "time" in user_text:

        current_time = datetime.now().strftime("%I:%M %p")

        return f"The current time is {current_time}"

    elif "date" in user_text:

        current_date = datetime.now().strftime("%d %B %Y")

        return f"Today's date is {current_date}"

    elif "joke" in user_text:

        return random.choice(jokes)

    elif "motivate" in user_text:

        return random.choice(motivational)

    elif "weather" in user_text:

        return "Weather integration feature coming soon."

    elif "bye" in user_text:

        return "Goodbye! Have a wonderful day."

    else:

        if personality == "Funny":
            return f"That sounds interesting: {user_text}"

        elif personality == "Motivational":
            return f"You can definitely achieve it: {user_text}"

        else:
            return f"I understood: {user_text}"

# ---------------- TEXT TO SPEECH ----------------

def text_to_speech(text, language):

    tts = gTTS(
        text=text,
        lang=language
    )

    temp_audio = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    tts.save(temp_audio.name)

    return temp_audio.name

# ---------------- MAIN APP ----------------

if audio_file is not None:

    with st.spinner("🎧 Processing Audio..."):

        temp_wav = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )

        temp_wav.write(audio_file.read())

        audio_path = temp_wav.name

        # Speech Recognition

        user_text = speech_to_text(audio_path)

        # AI Reply

        ai_reply = generate_response(
            user_text,
            personality
        )

        # Save History

        st.session_state.history.append({
            "user": user_text,
            "ai": ai_reply
        })

        # Voice Output

        response_audio = text_to_speech(
            ai_reply,
            language
        )

    st.success("✅ Audio Processed Successfully")

    # ---------------- USER MESSAGE ----------------

    st.subheader("🧑 You Said")

    st.markdown(
        f"""
        <div class="user-box">
        {user_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🤖 AI Response")

    st.markdown(
        f"""
        <div class="response-box">
        {ai_reply}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- AUDIO ----------------

    st.subheader("🔊 Voice Response")

    st.audio(response_audio)

    # ---------------- DOWNLOAD ----------------

    with open(response_audio, "rb") as file:

        st.download_button(
            "⬇️ Download AI Voice",
            file,
            file_name="jarvis_response.mp3"
        )

# ---------------- CHAT HISTORY ----------------

if st.session_state.history:

    st.divider()

    st.subheader("💬 Chat History")

    for chat in reversed(st.session_state.history):

        st.markdown(
            f"""
            <div class="user-box">
            🧑 {chat['user']}
            </div>
            <br>
            <div class="response-box">
            🤖 {chat['ai']}
            </div>
            <br>
            """,
            unsafe_allow_html=True
        )

# ---------------- FOOTER ----------------

st.divider()

st.caption("🚀 Built with Streamlit + SpeechRecognition + gTTS")
