import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import tempfile
from datetime import datetime
import random

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Multilingual AI Voice Assistant",
    page_icon="🤖",
    layout="wide"
)

# ---------------- SESSION ----------------

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
    font-size: 55px;
}

.stMarkdown {
    color: white;
}

.stButton button {
    width: 100%;
    height: 55px;
    border-radius: 12px;
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

</style>
""", unsafe_allow_html=True)

# ---------------- TRANSLATOR ----------------

translator = Translator()

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("⚙️ AI Settings")

    personality = st.selectbox(
        "Assistant Personality",
        [
            "Professional",
            "Funny",
            "Motivational"
        ]
    )

    languages = {
        "English": "en",
        "Tamil": "ta",
        "Hindi": "hi",
        "French": "fr",
        "German": "de"
    }

    source_lang = st.selectbox(
        "🎤 Input Language",
        list(languages.keys())
    )

    target_lang = st.selectbox(
        "🌍 Translate To",
        list(languages.keys())
    )

    source_code = languages[source_lang]
    target_code = languages[target_lang]

    st.divider()

    st.markdown("### 🚀 Features")

    st.write("✅ Voice Recognition")
    st.write("✅ AI Translation")
    st.write("✅ Voice Reply")
    st.write("✅ Multi Language")
    st.write("✅ Chat History")

# ---------------- TITLE ----------------

st.title("🤖 Multilingual AI Voice Assistant")

st.markdown(
    "<h4 style='text-align:center;color:lightgray;'>Speech Translation + AI Reply System</h4>",
    unsafe_allow_html=True
)

st.divider()

# ---------------- FILE UPLOADER ----------------

audio_file = st.file_uploader(
    "📤 Upload WAV Audio File",
    type=["wav"]
)

# ---------------- SPEECH TO TEXT ----------------

def speech_to_text(audio_path):

    recognizer = sr.Recognizer()

    try:

        with sr.AudioFile(audio_path) as source:

            audio = recognizer.record(source)

        text = recognizer.recognize_google(
            audio,
            language=source_code
        )

        return text.lower()

    except Exception as e:

        return f"Error: {e}"

# ---------------- AI RESPONSE ----------------

def generate_response(user_text, personality):

    greetings = [
        "Hello! How can I help you?",
        "Hi there!",
        "Welcome back!"
    ]

    jokes = [
        "AI is becoming smarter every day.",
        "Python developers love coffee.",
        "Debugging is like detective work."
    ]

    motivational = [
        "Success comes from consistency.",
        "Keep learning every day.",
        "You can achieve anything."
    ]

    if "hello" in user_text:

        return random.choice(greetings)

    elif "your name" in user_text:

        return "I am your AI Voice Assistant."

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

    elif "bye" in user_text:

        return "Goodbye! Have a great day."

    else:

        if personality == "Funny":

            return f"Interesting question: {user_text}"

        elif personality == "Motivational":

            return f"You can definitely do it: {user_text}"

        else:

            return f"I understood: {user_text}"

# ---------------- TEXT TO SPEECH ----------------

def text_to_speech(text, lang):

    tts = gTTS(
        text=text,
        lang=lang
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

        # Save uploaded WAV file

        temp_wav = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        )

        temp_wav.write(audio_file.read())

        audio_path = temp_wav.name

        # Speech Recognition

        user_text = speech_to_text(audio_path)

        # Translation

        translated = translator.translate(
            user_text,
            src=source_code,
            dest=target_code
        )

        translated_text = translated.text

        # AI Response

        ai_reply = generate_response(
            translated_text,
            personality
        )

        # Voice Output

        response_audio = text_to_speech(
            ai_reply,
            target_code
        )

        # Save History

        st.session_state.history.append({
            "input": user_text,
            "translated": translated_text,
            "reply": ai_reply
        })

    st.success("✅ Audio Processed Successfully")

    # ---------------- ORIGINAL SPEECH ----------------

    st.subheader("🧑 Original Speech")

    st.markdown(
        f"""
        <div class="user-box">
        {user_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- TRANSLATED TEXT ----------------

    st.subheader("🌍 Translated Text")

    st.markdown(
        f"""
        <div class="response-box">
        {translated_text}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------- AI RESPONSE ----------------

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

    st.subheader("🔊 Voice Reply")

    st.audio(response_audio)

    # ---------------- DOWNLOAD ----------------

    with open(response_audio, "rb") as file:

        st.download_button(
            "⬇️ Download Voice Reply",
            file,
            file_name="ai_reply.mp3"
        )

# ---------------- CHAT HISTORY ----------------

if st.session_state.history:

    st.divider()

    st.subheader("💬 Chat History")

    for item in reversed(st.session_state.history):

        st.markdown(
            f"""
            <div class="user-box">
            🎤 {item['input']}
            </div>

            <br>

            <div class="response-box">
            🌍 {item['translated']}
            </div>

            <br>

            <div class="response-box">
            🤖 {item['reply']}
            </div>

            <br>
            """,
            unsafe_allow_html=True
        )

# ---------------- FOOTER ----------------

st.divider()

st.caption("🚀 Built using Streamlit + SpeechRecognition + GoogleTrans + gTTS")
