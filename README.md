# AI Mock Interview Platform

## Overview

The **AI Mock Interview Platform** is an interactive web application designed to simulate real interview experiences using advanced AI models. It provides users with realistic interview questions, follow-up feedback, and performance evaluation, making it an ideal tool for job seekers to practice and improve their interview skills.

## Features

- **AI-Powered Interviewer:** Choose from multiple AI models (e.g., GPT-4, Gemini, Llama-3 via Replicate) to conduct your mock interview.
- **Tiered Access:**
  - **Personal Tier:** Access cost-efficient models like Gemini or Llama-3 (via Replicate).
  - **Corporate Tier:** Access high-accuracy models like OpenAI GPT-4 for advanced reasoning and feedback.
- **Speech Recognition:** Answer questions using your microphone for a realistic interview experience.
- **Text-to-Speech Feedback:** Hear the AI's questions and feedback with animated avatars.
- **Dynamic Follow-Up:** The AI provides natural follow-up questions and subtle feedback based on your answers.
- **Performance Evaluation:** Receive structured feedback and scores for each question, plus an overall performance summary with visual charts.
- **Customizable Tracks:** Practice interviews for different roles (e.g., Data Scientist, Software Engineer).

## How It Works

1. **Select Your Tier and Model:** Choose between Personal and Corporate tiers, then select your preferred AI model.
2. **Start the Interview:** Enter your name, select your interview track, and begin the session.
3. **Answer Questions:** Respond to AI-generated questions and follow-ups using your voice.
4. **Get Feedback:** After the interview, receive a detailed evaluation and visual performance charts.

## Tech Stack

- **Frontend/UI:** [Streamlit](https://streamlit.io/)
- **AI Models:** OpenAI GPT-4, Google Gemini, Meta Llama-3 (via Replicate)
- **Speech Recognition:** [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- **Text-to-Speech:** [gTTS](https://pypi.org/project/gTTS/), [pygame](https://www.pygame.org/)
- **Visualization:** Matplotlib, Plotly
- **Environment Management:** python-dotenv

## Setup & Installation

1. **Clone the Repository:**
   ```bash
   git clone <your-repo-url>
   cd <project-directory>
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r updated_requirements.txt
   ```
   - For Llama-3 via Replicate, see `API Integration Guide.md` for extra dependencies.
3. **Configure Environment Variables:**
   - Create a `.env` file and add your API keys (see `API Integration Guide.md` for details).
4. **Run the App:**
   ```bash
   streamlit run updated_Mock_AI.py
   ```

## License

MIT License

---

**Contributors:**
- Abdullah
- Mehar

For questions or support, please open an issue on GitHub.

