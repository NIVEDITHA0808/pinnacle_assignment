import re
import tempfile
from gtts import gTTS
import streamlit as st
import speech_recognition as sr

from groq_client import chat_with_groq
from rag import search_retrieval_data
from booking import get_availability,create_session,book_appointment

st.set_page_config(page_title="Stevens Creek Chevrolet Voice Assistant", layout="wide")
st.title("🚗 Stevens Creek Chevrolet Voice Assistant")

user_query=""
st.markdown("""
Upload a voice file or type your question, and the assistant will reply **in text and speech**.
""")

# -----------------------------
# 1️⃣ Voice Input
# -----------------------------
# ---------------- Session state for chat history ----------------
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi! 👋 How can I help you today?"}
    ]

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])
    else:
        st.chat_message("user").write(msg["content"])

# ---------------- Speech-to-text ----------------
def listen_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening... Speak now!")
        audio = recognizer.listen(source, timeout=10)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn’t understand that."
        except sr.RequestError:
            return "Speech service unavailable."

# ---------------- Text cleanup for TTS ----------------
def clean_for_tts(text: str) -> str:
    text = re.sub(r"\*+", "", text)          # remove *bold*
    text = re.sub(r"#", "", text)            # remove headers
    text = re.sub(r"-{2,}", " ", text)       # replace -- with space
    text = re.sub(r"[^\w\s.,!?']", "", text) # remove emojis/symbols
    text = re.sub(r"\s+", " ", text).strip() # collapse spaces
    return text

# ---------------- Text-to-speech ----------------
def speak_text(text):
    tts = gTTS(text, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# ---------------- Input options ----------------
if st.button("🎤 Speak"):
    user_query = listen_microphone()
    
# -----------------------------
# 2️⃣ Conversational AI + RAG
# -----------------------------
if user_query:
     # Save user message
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    if "booking" in user_query or "book" in user_query or "schedule" in user_query:
        agent_name = st.text_input("Provide the agent name")
        create_session(agent_name)
        if agent_name:
            slots = get_availability(agent_name)
            st.session_state["messages"].append({"role": "assistant", "content": slots})
            st.chat_message("assistant").write(slots)
        if "service" in user_query.lower():
            agent_type = "Service"
        else:
            agent_type="Sales"
        book_appointment(agent_type, agent_name,slots[0])
    else:
        
        # Retrieve relevant dealership info
        context = search_retrieval_data(user_query)
        
        with st.spinner("Thinking...", show_time=True):
            # Stream response token by token
            reply = chat_with_groq(user_query)

        # Convert token to speech
        with st.spinner("Generating...", show_time=True):
            re_reply = clean_for_tts(reply)
            print(reply)
            speak_text(re_reply)

        st.session_state["messages"].append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
