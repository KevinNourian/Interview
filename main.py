"""AI Interview Coach - A Streamlit application for interview practice."""

import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI


# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=OPENAI_API_KEY)


# Page configuration
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minimalist clean styling
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main app background */
    .stApp {
        background-color: #fafafa;
    }
    
    /* Main title styling */
    .main-title {
        font-size: 2.8rem;
        font-weight: 600;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.3rem;
        letter-spacing: -0.5px;
    }
    
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1rem;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Section dividers */
    .section-divider {
        height: 1px;
        background-color: #e0e0e0;
        margin: 2.5rem 0;
    }
    
    /* Card containers */
    .config-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        margin-bottom: 1.5rem;
    }
    
    /* Labels */
    .stSelectbox label, .stSlider label, .stTextArea label {
        color: #2c3e50 !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: white;
        border: 1.5px solid #e0e0e0;
        border-radius: 8px;
        transition: all 0.2s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #3498db;
    }
    
    /* Slider styling */
    .stSlider > div > div > div {
        background-color: #3498db;
    }
    
    /* AI Message styling */
    .ai-message {
        background: white;
        border: 1.5px solid #e8f4f8;
        border-left: 4px solid #3498db;
        color: #2c3e50;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 6px rgba(52, 152, 219, 0.08);
    }
    
    .ai-message strong {
        color: #3498db;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* User Message styling */
    .user-message {
        background: white;
        border: 1.5px solid #e8f8f5;
        border-left: 4px solid #27ae60;
        color: #2c3e50;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 2px 6px rgba(39, 174, 96, 0.08);
    }
    
    .user-message strong {
        color: #27ae60;
        font-weight: 600;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.7rem 2rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
    }
    
    .stButton>button:hover {
        background-color: #2980b9;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(52, 152, 219, 0.3);
    }
    
    /* Text area styling */
    .stTextArea>div>div>textarea {
        background-color: white;
        border-radius: 8px;
        border: 1.5px solid #e0e0e0;
        padding: 1rem;
        color: #2c3e50;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }
    
    /* Success message */
    .stSuccess {
        background-color: #d5f4e6;
        border-left: 4px solid #27ae60;
        color: #27ae60;
        padding: 1rem;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Error message */
    .stError {
        background-color: #fadbd8;
        border-left: 4px solid #e74c3c;
        color: #c0392b;
        padding: 1rem;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Column spacing */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown(
    '<h1 class="main-title">✨ AI Interview Coach</h1>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="subtitle">Practice and perfect your interview skills</p>',
    unsafe_allow_html=True
)

# Initialize all session state variables
SESSION_VARS = [
    "interview_type",
    "difficulty_level",
    "interviewer_type",
    "temperature",
    "top_p",
    "messages",
    "session_over",
    "user_input",
    "first_question_asked",
    "input_counter"
]

for var in SESSION_VARS:
    if var not in st.session_state:
        if var == "temperature":
            st.session_state.temperature = 0.7
        elif var == "top_p":
            st.session_state.top_p = 0.5
        elif var == "messages":
            st.session_state.messages = []
        elif var == "session_over":
            st.session_state.session_over = False
        elif var == "first_question_asked":
            st.session_state.first_question_asked = False
        elif var == "input_counter":
            st.session_state.input_counter = 0
        else:
            st.session_state[var] = None

# Interview Configuration Section
col1, col2, col3 = st.columns(3)

INTERVIEW_TYPES = [
    "Select an option",
    "Data Science",
    "Education",
    "Ecommerce",
    "Healthcare",
    "Finance",
    "Technology",
    "Marketing"
]

DIFFICULTY_LEVELS = ["Select an option", "Easy", "Medium", "Hard"]

INTERVIEWER_STYLES = ["Select an option", "Friendly", "Neutral", "Strict"]

with col1:
    current_index = 0
    if (st.session_state.interview_type is not None and
            st.session_state.interview_type in INTERVIEW_TYPES):
        current_index = INTERVIEW_TYPES.index(
            st.session_state.interview_type
        )
    
    interview_type = st.selectbox(
        "Interview Type",
        INTERVIEW_TYPES,
        index=current_index
    )

with col2:
    current_index = 0
    if (st.session_state.difficulty_level is not None and
            st.session_state.difficulty_level in DIFFICULTY_LEVELS):
        current_index = DIFFICULTY_LEVELS.index(
            st.session_state.difficulty_level
        )
    
    difficulty_level = st.selectbox(
        "Difficulty Level",
        DIFFICULTY_LEVELS,
        index=current_index
    )

with col3:
    current_index = 0
    if (st.session_state.interviewer_type is not None and
            st.session_state.interviewer_type in INTERVIEWER_STYLES):
        current_index = INTERVIEWER_STYLES.index(
            st.session_state.interviewer_type
        )
    
    interviewer_type = st.selectbox(
        "Interviewer Style",
        INTERVIEWER_STYLES,
        index=current_index
    )

# AI Settings Section
st.session_state.temperature = st.slider(
    "AI Creativity",
    min_value=0.0,
    max_value=2.0,
    value=st.session_state.temperature,
    step=0.05,
    help="Adjust how creative the AI responses are"
)

st.session_state.top_p = st.slider(
    "Top P (Nucleus Sampling)",
    min_value=0.0,
    max_value=1.0,
    value=st.session_state.top_p,
    step=0.05,
    help="Controls diversity via nucleus sampling (lower = more focused)"
)

st.markdown(
    '<div class="section-divider"></div>',
    unsafe_allow_html=True
)

# Difficulty level instructions
DIFFICULTY_INSTRUCTIONS = {
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

# Interviewer type instructions
INTERVIEWER_INSTRUCTIONS = {
    "Strict": """
- Maintain a formal, professional tone at all times
- Set high expectations and hold the candidate accountable
- Point out weaknesses and mistakes directly
- Provide critical feedback without sugarcoating
- Be demanding and challenge vague or incomplete answers
- Show limited warmth or encouragement""",
    "Neutral": """
- Maintain a balanced, professional demeanor
- Provide objective feedback that is neither overly critical nor overly encouraging
- Be fair and impartial in your assessment
- Focus on facts and concrete observations
- Keep emotions and personal opinions minimal""",
    "Friendly": """
- Be warm, encouraging, and supportive throughout
- Create a comfortable, low-pressure atmosphere
- Celebrate strengths and progress enthusiastically
- Frame constructive feedback gently and positively
- Use encouraging language and show genuine interest
- Help the candidate feel at ease and confident"""
}

# Initialize session after user selects type, difficulty, and interviewer
if (st.session_state.interview_type is None and
        interview_type != "Select an option" and
        difficulty_level != "Select an option" and
        interviewer_type != "Select an option"):
    
    st.session_state.interview_type = interview_type
    st.session_state.difficulty_level = difficulty_level
    st.session_state.interviewer_type = interviewer_type
    
    system_prompt = f"""
You are an expert interview coach conducting a \
{st.session_state.interview_type} interview practice session at a \
{st.session_state.difficulty_level} difficulty level with a \
{st.session_state.interviewer_type} interviewing style.

Your responsibilities:
- Ask one question at a time, strictly related to \
{st.session_state.interview_type}
- After each user answer, provide concise, constructive feedback
- Then ask the next relevant question
- Keep your responses concise

Difficulty Level - {st.session_state.difficulty_level}:
{DIFFICULTY_INSTRUCTIONS[st.session_state.difficulty_level]}

Interviewer Type - {st.session_state.interviewer_type}:
{INTERVIEWER_INSTRUCTIONS[st.session_state.interviewer_type]}

Deciding when to end the interview:
- You have full control over when the interview concludes
- Typically conduct 4-6 questions covering different aspects of \
{st.session_state.interview_type}
- Assess the user's responses for depth, quality, and engagement
- End the interview when you feel you've covered sufficient ground or if \
the user seems to be struggling
- When concluding, say "This concludes our interview session" and provide \
final comprehensive feedback
- After concluding, do NOT ask another question

Remember: You decide when the interview is complete based on the \
conversation flow and coverage of key topics.
"""
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]
    st.session_state.first_question_asked = False
    st.session_state.session_over = False
    st.session_state.user_input = ""


def moderate_content(text):
    """Check content using OpenAI's moderation API.
    
    Args:
        text: The text content to moderate
        
    Returns:
        tuple: (is_safe: bool, error_message: str)
    """
    try:
        response = openai_client.moderations.create(input=text)
        result = response.results[0]
        
        if result.flagged:
            flagged_categories = [
                cat for cat, flagged in result.categories.__dict__.items()
                if flagged
            ]
            error_msg = (
                f"Content violates usage policies "
                f"({', '.join(flagged_categories)}). "
                f"Please provide appropriate responses."
            )
            return False, error_msg
        return True, ""
    except Exception as e:
        st.warning(f"Moderation check temporarily unavailable: {str(e)}")
        return True, ""


def get_ai_response():
    """Get AI response from OpenAI and update session state."""
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=st.session_state.temperature,
        max_tokens=300,
        top_p=st.session_state.top_p,
        frequency_penalty=0,
        presence_penalty=0,
    )
    ai_message = response.choices[0].message.content
    
    # Check if AI has concluded the session BEFORE adding to messages
    conclusion_phrases = [
        "this concludes our interview",
        "this concludes the interview",
        "that concludes our interview",
        "that concludes the interview",
        "interview session complete",
        "interview is now complete",
        "concludes our interview session",
        "that wraps up our interview"
    ]
    
    if any(phrase in ai_message.lower() for phrase in conclusion_phrases):
        st.session_state.session_over = True
    
    st.session_state.messages.append(
        {"role": "assistant", "content": ai_message}
    )


# Generate first AI question if not yet asked
if (st.session_state.interview_type and
        not st.session_state.first_question_asked):
    get_ai_response()
    st.session_state.first_question_asked = True

# Display conversation history
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        st.markdown(
            f'<div class="ai-message"><strong>AI Coach</strong><br><br>'
            f'{msg["content"]}</div>',
            unsafe_allow_html=True
        )
    elif msg["role"] == "user":
        st.markdown(
            f'<div class="user-message"><strong>You</strong><br><br>'
            f'{msg["content"]}</div>',
            unsafe_allow_html=True
        )

# Session ended message and Reset button
if st.session_state.session_over:
    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True
    )
    st.success("Interview session complete. Great job!")
    
    if st.button(
        "Start New Interview",
        type="primary",
        use_container_width=True
    ):
        # Clear all session state variables to reset to original state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Input box and submit button: only if session NOT over
elif (st.session_state.first_question_asked and
        not st.session_state.session_over):
    user_input = st.text_area(
        "Your Answer",
        value="",
        key=f"user_input_{st.session_state.input_counter}",
        placeholder="Type your answer here...",
        height=120
    )
    
    if st.button("Submit Answer", use_container_width=True):
        if user_input.strip():
            # Moderate user input before processing
            is_safe, error_message = moderate_content(user_input.strip())
            
            if not is_safe:
                st.error(error_message)
            else:
                st.session_state.messages.append(
                    {"role": "user", "content": user_input.strip()}
                )
                get_ai_response()
                st.session_state.input_counter += 1
                st.rerun()