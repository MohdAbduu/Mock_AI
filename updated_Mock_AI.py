import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
import os
import uuid
import matplotlib.pyplot as plt
import re
from colorama import init
import time
from threading import Thread
from dotenv import load_dotenv
import pygame
from uuid import uuid4
import plotly.graph_objects as go

# Import custom modules for model interface and UI components
from model_interface import initialize_models
from ui_components import render_tier_toggle, render_model_chooser, display_model_info

init(autoreset=True)
st.set_page_config(layout="wide")
st.markdown("""
    <style>
    .stButton>button {
       display: flex;
       align-items: center;
       font-family: inherit;
       cursor: pointer;
       font-weight: 500;
       font-size: 16px;
       padding: 1.1em 4em 1.1em 3.5em;
       color: white;
       background: #A020F0;
       background: linear-gradient(
           0deg,
           rgba(160, 32, 240, 1) 0%,
           rgba(147, 112, 219, 1) 100%
       );
       border: none;
       box-shadow: 0 0.7em 1.5em -0.5em #A020F098;
       letter-spacing: 0.05em;
       border-radius: 20em;
       margin-top: 0.8em;
    }
    .stButton>button svg {
      margin-right: 6px;
    }
    .stButton>button:hover {
      color: white;
      box-shadow: 0 0.5em 1.5em -0.5em #A020F098;
    }
    .stButton>button:active {
      box-shadow: 0 0.3em 1em -0.5em #A020F098;
    }
    .card {
        background: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .tier-section {
        background: rgba(160, 32, 240, 0.05);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #A020F0;
    }
    </style>
""", unsafe_allow_html=True)
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
static_gif_path = r"D:\projectx\PythoAAAAAAAAAAAAAAA\AI-talking-avatar.png"
animated_gif_path = r"D:\projectx\PythoAAAAAAAAAAAAAAA\AI-talking-avatar.gif"
recognizer = sr.Recognizer()

# Initialize session state variables
for key in ["interview_complete", "transcript", "evaluation_scores", "start_clicked", "paused", "mute", "greeted"]:
    if key not in st.session_state:
        st.session_state[key] = False if key in ["interview_complete", "start_clicked", "paused", "mute",
                                                 "greeted"] else []

# Initialize model registry
if "model_registry" not in st.session_state:
    st.session_state["model_registry"] = initialize_models()

interview_tracks = {
    "Data Scientist": [
        "Explain overfitting in machine learning.",
        "What is the difference between supervised and unsupervised learning?",
        "How do you handle imbalanced datasets?",
        "What is feature engineering?",
        "Explain the bias-variance tradeoff."
    ],
    "Software Engineer": [
        "What is your approach to debugging code?",
        "Explain multithreading vs multiprocessing.",
        "What is the concept of clean code?",
        "How do you ensure code security?",
        "Explain RESTful APIs."
    ],
}


def speak_with_gif(text, gif_placeholder, animated_gif_path, static_gif_path):
    try:
        if st.session_state["mute"]:
            return
        temp_audio_file = f"temp_speech_{uuid4().hex}.mp3"
        tts = gTTS(text=text, lang='en')
        tts.save(temp_audio_file)
        pygame.mixer.init()
        pygame.mixer.music.load(temp_audio_file)
        pygame.mixer.music.play()
        gif_placeholder.image(animated_gif_path, width=850)
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except Exception as e:
        st.error(f"❌ Error during playback: {e}")
    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        gif_placeholder.image(static_gif_path, width=850)
        try:
            os.remove(temp_audio_file)
        except PermissionError:
            time.sleep(1)
            os.remove(temp_audio_file)


def get_speech_input():
    with sr.Microphone() as source:
        st.info("🎙 Listening... Please speak your answer.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            text = recognizer.recognize_google(audio)
            st.success(f"✅ You : {text}")
            return text
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"❌ Error: {e}")
        except sr.WaitTimeoutError:
            st.error("❌ Listening timed out.")
    return ""


def chat_with_gpt(prompt):
    """
    Generate a response using the currently selected model.
    """
    try:
        # Get the current model from the registry
        model = st.session_state["model_registry"].get_model()

        # Generate response using the selected model
        system_message = "You are a professional interviewer. Avoid greetings and keep it focused."
        response = model.generate_response(prompt, system_message)

        return response
    except Exception as e:
        st.error(f"❌ Model Error: {e}")
        return "Error generating response."


def generate_followup_with_feedback(user_response):
    followup_prompt = f"""
    Based on the following interview answer, generate a follow-up question with subtle, natural feedback included.
    Do not explicitly state 'Follow-Up Question:' in your response. Keep it natural and conversational.
    Answer: {user_response}
    """
    return chat_with_gpt(followup_prompt)


def evaluate_answers():
    evaluation_prompt = """
    Evaluate the following interview transcript. Provide structured feedback in the exact format below:

    1. Question: <Question>
       Answer: <User's Answer>
       Score: <Score out of 10>
       Feedback: <Brief one-line feedback>

    (as many questions as we have asked)

    At the end, include:
    Overall Feedback: <Summary of overall performance>
    """
    for i, entry in enumerate(st.session_state["transcript"]):
        match = re.search(r"Q\d+: (.*?)\n🗨 You: (.*?)\n🔄 Follow-Up: (.*?)\n🗨 You: (.*)", entry, re.DOTALL)
        if match:
            question = match.group(1)
            answer = match.group(2) + " " + match.group(4)
            evaluation_prompt += f"\n{i + 1}. Question: {question}\nAnswer: {answer}\n"
    evaluation = chat_with_gpt(evaluation_prompt)
    scores = re.findall(r"Score:\s?(\d+)", evaluation)
    return evaluation, [int(s) for s in scores] if scores else [0] * len(st.session_state["transcript"])


def plot_evaluation_chart(scores):
    fig, ax = plt.subplots(figsize=(5, 3))
    questions = [f"Q{i + 1}" for i in range(len(scores))]
    ax.bar(questions, scores, color="#8F00FF")
    ax.set_title("Interview Evaluation Scores", fontsize=14)
    ax.set_xlabel("Questions", fontsize=12)
    ax.set_ylabel("Score (out of 10)", fontsize=12)
    ax.set_ylim([0, 10])
    plt.tight_layout()
    st.pyplot(fig)


# Main application layout
st.title("🎓 AI Mock Interview Platform")

# Subscription tier and model selection section
with st.expander("🔧 Model Settings", expanded=True):
    st.markdown("<div class='tier-section'>", unsafe_allow_html=True)

    # Render tier toggle
    selected_tier = render_tier_toggle()

    # Get models for the selected tier
    tier_models = st.session_state["model_registry"].get_models_by_tier(selected_tier)

    # Render model chooser
    if tier_models:
        selected_model_name = render_model_chooser(tier_models)

        # Set the current model in the registry
        st.session_state["model_registry"].set_current_model(selected_model_name)

        # Display current model info
        current_model = st.session_state["model_registry"].get_model()
        display_model_info(current_model)
    else:
        st.warning(f"No models available for {selected_tier} tier.")

    st.markdown("</div>", unsafe_allow_html=True)

# Main application UI
gif_placeholder = st.empty()
gif_placeholder.image(static_gif_path, width=850)

cols = st.columns(3)
with cols[0]:
    pause_btn = st.button("⏸ PAUSE", key="pause_btn")
with cols[1]:
    mute_btn = st.button("🔇 MUTE", key="mute_btn")
with cols[2]:
    end_call_btn = st.button("❌ END", key="end_call_btn")

if pause_btn:
    st.session_state["paused"] = not st.session_state["paused"]
    st.info("⏸ Interview paused." if st.session_state["paused"] else "▶ Interview resumed.")
if mute_btn:
    st.session_state["mute"] = not st.session_state["mute"]
    st.info("🔇 Audio muted." if st.session_state["mute"] else "🔊 Audio unmuted.")
if end_call_btn:
    for key in ["interview_complete", "transcript", "evaluation_scores", "start_clicked", "paused", "mute", "greeted"]:
        st.session_state[key] = False if key in ["interview_complete", "start_clicked", "paused", "mute",
                                                 "greeted"] else []
    st.experimental_rerun()

with st.sidebar:
    with st.expander("Chat Conversation", expanded=True):
        st.title("🎓 AI Mock Interview Platform")
        if not st.session_state["start_clicked"]:
            username = st.text_input("Enter Your Name:", "")
            track = st.selectbox("Select Your Interview Track:", list(interview_tracks.keys()))
            if st.button("Start Interview"):
                if username.strip():
                    st.session_state["username"] = username
                    st.session_state["track"] = track
                    st.session_state["start_clicked"] = True
                else:
                    st.error("Please enter your name before starting.")
        else:
            username = st.session_state["username"]
            track = st.session_state["track"]
            questions = interview_tracks[track][:3]
            total_questions = len(questions)
            current_question_index = 0
            if not st.session_state["greeted"]:
                greeting = f"Hi, how are you, {username}? Welcome to the {track} interview."
                st.info(f"🤖 AI : {greeting}")
                speak_with_gif(greeting, gif_placeholder, animated_gif_path, static_gif_path)
                st.session_state["greeted"] = True
            if not st.session_state["interview_complete"]:
                for i, question in enumerate(questions):
                    current_question_index = i
                    progress = (current_question_index + 1) / total_questions
                    st.progress(progress)
                    while st.session_state["paused"]:
                        st.warning("⏸ Interview is paused. Click the pause button to resume.")
                        time.sleep(1)
                    speak_with_gif(question, gif_placeholder, animated_gif_path, static_gif_path)
                    st.markdown(f'<div class="card"><strong>🤖 AI:</strong> {question}</div>', unsafe_allow_html=True)
                    user_response = get_speech_input()
                    if user_response == "" and st.session_state["paused"]:
                        continue
                    followup = generate_followup_with_feedback(user_response)
                    speak_with_gif(followup, gif_placeholder, animated_gif_path, static_gif_path)
                    st.markdown(f'<div class="card"><strong>🤖 AI:</strong> {followup}</div>', unsafe_allow_html=True)
                    followup_response = get_speech_input()
                    if followup_response == "" and st.session_state["paused"]:
                        continue
                    block = (
                        f"Q{i + 1}: {question}\n"
                        f"🗨 You: {user_response}\n"
                        f"🔄 Follow-Up: {followup}\n"
                        f"🗨 You: {followup_response}"
                    )
                    st.session_state["transcript"].append(block)
                farewell = f"It was nice meeting you, {username}. Goodbye!"
                speak_with_gif(farewell, gif_placeholder, animated_gif_path, static_gif_path)
                st.info(f"🤖 AI : {farewell}")
                st.session_state["interview_complete"] = True
            if st.session_state["interview_complete"]:
                st.success("✅ Interview complete! You can now proceed to evaluation.")
                if st.button("Evaluate My Performance"):
                    with st.spinner("🔍 Evaluating your responses..."):
                        evaluation_report, scores = evaluate_answers()
                    st.subheader("📄 Evaluation Report")
                    st.write(evaluation_report)
                    st.subheader("📊 Overall Evaluation")
                    overall_score = sum(scores) / len(scores) if scores else 0


                    def get_color(value):
                        if value <= 5:
                            t = value / 5
                            r = 255
                            g = int(0 + 255 * t)
                            b = 0
                        else:
                            t = (value - 5) / 5
                            r = int(255 - 255 * t)
                            g = 255
                            b = 0
                        return f"#{r:02X}{g:02X}{b:02X}"


                    steps = []
                    if overall_score > 0:
                        delta = overall_score / 50
                        start_val = 0
                        while start_val < overall_score:
                            end_val = min(start_val + delta, overall_score)
                            mid = (start_val + end_val) / 2
                            steps.append({"range": [start_val, end_val], "color": get_color(mid)})
                            start_val = end_val
                    steps.append({"range": [overall_score, 10], "color": "rgba(0,0,0,0)"})
                    gauge_fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=overall_score,
                        gauge={
                            "axis": {"range": [0, 10], "tickmode": "array", "tickvals": [1.5, 5.5, 8.5],
                                     "ticktext": ["Bad", "Average", "Good"]},
                            "bar": {"color": "rgba(0,0,0,0)"},
                            "steps": steps,
                            "bgcolor": "rgba(128, 128, 128, 1)",
                            "borderwidth": 0,
                            "bordercolor": "rgba(0,0,0,0)"
                        }
                    ))
                    gauge_fig.update_layout(width=300, height=250, margin=dict(l=20, r=20, t=50, b=20))
                    st.plotly_chart(gauge_fig, use_container_width=False)
                    st.subheader("📊 Interview Evaluation Scores")
                    plot_evaluation_chart(scores)
