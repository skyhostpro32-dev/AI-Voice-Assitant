

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
