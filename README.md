# 🎤 AI Interview Coach

An interactive **AI-powered interview practice application** built with **Streamlit** and **OpenAI**.  
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

- **AI-Controlled Interview Flow**
  - Asks one question at a time
  - Provides concise, constructive feedback after each answer
  - Dynamically decides when the interview is complete (typically 4–6 questions)

- **Creativity Control**
  - Adjustable temperature slider to control AI response style

- **Content Moderation**
  - User inputs are checked via OpenAI’s moderation API for safe and appropriate use

- **Session Management**
  - Conversation memory stored using Streamlit session state
  - Ability to restart interviews cleanly

---

## How It Works

1. The user selects:
   - Interview type
   - Difficulty level
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
- **OpenAI API** – interview logic, feedback, moderation
- **dotenv** – secure environment variable management

