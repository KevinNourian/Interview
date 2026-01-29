# AI Interview Coach

An interactive **AI-powered interview practice application** built with **Streamlit** and **multiple LLM providers** (OpenAI, Anthropic, Mistral).  
The app simulates realistic interview sessions across multiple professional domains and difficulty levels, providing **dynamic questions, real-time feedback, and structured interview flow**.

![AI Interview Illustration](assets/interview_ai.png)

---

## Features

- **Multiple Interview Domains**
  - Data Science
  - Education
  - Ecommerce
  - Healthcare
  - Finance
  - Technology
  - Marketing

- **Adjustable Difficulty Levels**
  - Easy – entry-level and foundational concepts
  - Medium – scenario-based and practical questions
  - Hard – advanced, expert-level challenges

- **Interviewer Style Options**
  - Friendly – warm, encouraging, and supportive
  - Neutral – balanced and professional
  - Strict – formal with high expectations

- **Multiple LLM Support**
  - OpenAI (GPT-4o-mini)
  - Anthropic (Claude Haiku 4.5)
  - Mistral (Mistral Small)

- **AI-Controlled Interview Flow**
  - Asks one question at a time
  - Provides concise, constructive feedback after each answer
  - Dynamically decides when the interview is complete (typically 4–6 questions)

- **Creativity Control**
  - Adjustable temperature slider to control AI response creativity and style

- **Content Moderation**
  - User inputs are checked via OpenAI's moderation API for safe and appropriate use across all LLM providers

- **Session Management**
  - Conversation memory stored using Streamlit session state
  - Ability to restart interviews cleanly

---

## How It Works

1. The user selects:
   - Interview type
   - Difficulty level
   - Interviewer style
   - Large Language Model (OpenAI, Anthropic, or Mistral)
   - AI creativity (temperature)

2. The AI interviewer:
   - Asks domain-specific questions
   - Evaluates each response
   - Adapts the interview flow based on user performance

3. When the interview concludes:
   - The AI provides comprehensive final feedback
   - The session can be reset for a new interview

---

## Tech Stack

- **Python**
- **Streamlit** – UI and session handling
- **OpenAI API** – GPT-4o-mini model, content moderation
- **Anthropic API** – Claude Haiku 4.5 model
- **Mistral API** – Mistral Small model
- **dotenv** – secure environment variable management

---

## Deployment

The app is deployed on GCP Cloud Run at the following address:
https://interview-app-697563534137.us-central1.run.app/