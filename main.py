import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


st.title("Interview Coach")


prompt = """
You are an expert behavioral interview coach.
You ask one question at a time.
Keep a professional, friendly, and concise tone.
Begin by asking the user a common behavioral interview question.
Ask questions that are relevant to the user's previous answers.
Ask 3 questions total before concluding the session.
"""


response = openai_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "system", "content": prompt}],
    temperature=0.7,
    max_tokens=256,
    top_p=1.0,
    frequency_penalty=0,
    presence_penalty=0,
)

st.write(response.choices[0].message.content)


user_answer = st.text_area("Your answer:")


if st.button("Submit Answer") and user_answer.strip():
    feedback_prompt = f"""
    You are an expert behavioral interview coach.
    The candidate answered: "{user_answer}".
    Provide concise, professional, and supportive feedback.
    """
    feedback_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": feedback_prompt}],
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0,
    )
    st.write("**Feedback:**")
    st.write(feedback_response.choices[0].message.content.strip())
