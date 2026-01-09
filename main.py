import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# System prompt
system_prompt = """
You are an expert interview coach.
You ask one question at a time.
Keep a professional, friendly, and concise tone.
Begin by asking the user a common behavioral interview question.
Provide concise, professional, and supportive feedback.
Ask questions that are relevant to the user's previous answers.
You may ask a maximum of 2 questions in total. 
After the second question, provide final feedback and conclude the session.
"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.question_count = 0
    st.session_state.session_over = False
    st.session_state.user_input = ""
    st.session_state.initial_question_asked = False  # Track first AI question

st.title("AI Interview Coach")

# --- Function to handle submit ---
def submit_answer():
    user_answer = st.session_state.user_input.strip()
    if not user_answer:
        return

    # Add user answer to conversation
    st.session_state.messages.append({"role": "user", "content": user_answer})
    st.session_state.question_count += 1

    # Clear text area
    st.session_state.user_input = ""

    # Get AI response (feedback + next question)
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=0.7,
        max_tokens=300,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0,
    )
    ai_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_message})

    # Check if session should end
    if st.session_state.question_count == 3 or "conclude the session" in ai_message.lower():
        st.session_state.session_over = True
        st.success("Interview session complete. Thank you!")

# --- Generate first AI question ---
if not st.session_state.initial_question_asked and not st.session_state.session_over:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=0.7,
        max_tokens=300,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0,
    )
    ai_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    st.session_state.initial_question_asked = True

# Display conversation history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f"**AI:** {msg['content']}")
    elif msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")

# Only show input if session is not over
if not st.session_state.session_over:
    st.text_area(
        "Your answer:",
        value=st.session_state.user_input,
        key="user_input",
        placeholder="Type your answer here..."
    )
    st.button("Submit Answer", on_click=submit_answer)
else:
    st.info("The interview session has ended. Refresh the page to start a new session.")
