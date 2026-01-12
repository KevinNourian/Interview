import os
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)

st.title("AI Interview Coach")

# --- Initialize all session state variables ---
for var in ["interview_type", "difficulty_level", "temperature", "messages", "session_over",
            "user_input", "first_question_asked"]:
    if var not in st.session_state:
        if var == "temperature":
            st.session_state.temperature = 0.7
        elif var == "messages":
            st.session_state.messages = []
        elif var == "session_over":
            st.session_state.session_over = False
        elif var == "first_question_asked":
            st.session_state.first_question_asked = False
        else:
            st.session_state[var] = None

# --- Dropdown for interview type ---
interview_type = st.selectbox(
    "Choose your interview type:",
    ["Select an option", "Data Science", "Education", "Ecommerce",
     "Healthcare", "Finance", "Technology", "Marketing"]
)

# --- Dropdown for difficulty level ---
difficulty_level = st.selectbox(
    "Choose your difficulty level:",
    ["Select an option", "Easy", "Medium", "Hard"]
)

# --- Slider for temperature ---
st.session_state.temperature = st.slider(
    "Set AI creativity (temperature):",
    min_value=0.0,
    max_value=2.0,
    value=st.session_state.temperature,
    step=0.05
)

# --- Initialize session after user selects type and difficulty ---
if (st.session_state.interview_type is None and 
    interview_type != "Select an option" and 
    difficulty_level != "Select an option"):
    
    st.session_state.interview_type = interview_type
    st.session_state.difficulty_level = difficulty_level
    
    # Customize instructions based on difficulty level
    difficulty_instructions = {
        "Easy": """
- Ask foundational and entry-level questions
- Focus on basic concepts and straightforward scenarios
- Provide encouraging and detailed feedback
- Help build confidence with supportive guidance""",
        "Medium": """
- Ask intermediate-level questions that require some experience
- Include scenario-based questions and practical applications
- Provide balanced feedback highlighting both strengths and areas for improvement
- Challenge the user moderately while remaining supportive""",
        "Hard": """
- Ask advanced, complex questions requiring deep expertise
- Include challenging technical problems, edge cases, and strategic thinking
- Provide critical and detailed feedback with high standards
- Push the user to demonstrate mastery and expert-level reasoning"""
    }
    
    system_prompt = f"""
You are an expert interview coach conducting a {st.session_state.interview_type} interview practice session at a {st.session_state.difficulty_level} difficulty level.

Your responsibilities:
- Ask one question at a time, strictly related to {st.session_state.interview_type}
- After each user answer, provide concise, constructive feedback
- Then ask the next relevant question
- Keep a professional, friendly, and concise tone

Difficulty Level - {st.session_state.difficulty_level}:
{difficulty_instructions[st.session_state.difficulty_level]}

Deciding when to end the interview:
- You have full control over when the interview concludes
- Typically conduct 4-6 questions covering different aspects of {st.session_state.interview_type}
- Assess the user's responses for depth, quality, and engagement
- End the interview when you feel you've covered sufficient ground or if the user seems to be struggling
- When concluding, say "This concludes our interview session" and provide final comprehensive feedback
- After concluding, do NOT ask another question

Remember: You decide when the interview is complete based on the conversation flow and coverage of key topics.
"""
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
    st.session_state.first_question_asked = False
    st.session_state.session_over = False
    st.session_state.user_input = ""

# --- Content Moderation Function ---
def moderate_content(text):
    """Check content using OpenAI's moderation API"""
    try:
        response = openai_client.moderations.create(input=text)
        result = response.results[0]
        
        if result.flagged:
            # Get specific categories that were flagged
            flagged_categories = [cat for cat, flagged in result.categories.__dict__.items() if flagged]
            return False, f"Content violates usage policies ({', '.join(flagged_categories)}). Please provide appropriate responses."
        return True, ""
    except Exception as e:
        # If moderation fails, log error but allow content (fail open)
        st.warning(f"Moderation check temporarily unavailable: {str(e)}")
        return True, ""

# --- Function to get AI response ---
def get_ai_response():
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=st.session_state.temperature,
        max_tokens=300,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0,
    )
    ai_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": ai_message})
    
    # Check if AI has concluded the session
    conclusion_phrases = [
        "this concludes our interview",
        "this concludes the interview",
        "that concludes our interview",
        "that concludes the interview",
        "interview session complete",
        "interview is now complete"
    ]
    
    if any(phrase in ai_message.lower() for phrase in conclusion_phrases):
        st.session_state.session_over = True

# --- Generate first AI question if not yet asked ---
if st.session_state.interview_type and not st.session_state.first_question_asked:
    get_ai_response()
    st.session_state.first_question_asked = True

# --- Display conversation history ---
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(f"**AI:** {msg['content']}")
    elif msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")

# --- Input box and submit button: only if session NOT over ---
if st.session_state.first_question_asked and not st.session_state.session_over:
    # Use a unique key that changes after each submission to clear the text area
    if "input_counter" not in st.session_state:
        st.session_state.input_counter = 0
    
    user_input = st.text_area(
        "Your answer:",
        value="",
        key=f"user_input_{st.session_state.input_counter}",
        placeholder="Type your answer here..."
    )
    
    if st.button("Submit Answer"):
        if user_input.strip():
            # Moderate user input before processing
            is_safe, error_message = moderate_content(user_input.strip())
            
            if not is_safe:
                st.error(error_message)
            else:
                st.session_state.messages.append({"role": "user", "content": user_input.strip()})
                get_ai_response()
                st.session_state.input_counter += 1  # Increment to create new text area
                st.rerun()

# --- Session ended message ---
if st.session_state.session_over:
    st.success("Interview session complete. Thank you!")