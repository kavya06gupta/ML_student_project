# import streamlit as st
# import os
# import json
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langgraph.prebuilt import createagent

# # ✅ Set page config
# st.set_page_config(page_title="Study Buddy Quiz Agent", page_icon="📚", layout="centered")

# # ✅ Load API Key
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")
# if not api_key:
#     st.error("❌ GEMINI_API_KEY not found in .env file")
#     st.stop()

# # ✅ Initialize session state
# if 'stage' not in st.session_state:
#     st.session_state.stage = 'input'  # Stages: input, quiz, results, feedback
# if 'student_context' not in st.session_state:
#     st.session_state.student_context = None
# if 'questions' not in st.session_state:
#     st.session_state.questions = []
# if 'current_question' not in st.session_state:
#     st.session_state.current_question = 0
# if 'answers' not in st.session_state:
#     st.session_state.answers = []
# if 'quiz_result' not in st.session_state:
#     st.session_state.quiz_result = None
# if 'chat_messages' not in st.session_state:
#     st.session_state.chat_messages = []

# # ✅ Create LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash-exp",
#     google_api_key=api_key
# )

# # ✅ Data Extraction Agent (from data_extractor.py)
# def extract_student_context(user_input):
#     from langgraph.prebuilt import create_agent

#     prompt = """
# You are STUDY-BUDDY-AGENT 📚
# Your task is to identify what the student wants to study and infer the difficulty level
# based on tone, wording, and intent.

# If student gives direct difficulty level, use it.
# If not, infer:
# - Easy / Beginner / Super simple/ baby level/ new → beginner
# - Intermediate / I know basics/ I have read a bit/ I am trying to reach a better level/medium → intermediate
# - Hard / expert / deep dive/ knowledged/ tough → advanced

# Return ONLY JSON in this structure:

# {
#     "student_request": {
#         "topic": "...",
#         "difficulty": "..."
#     }
# }

# Do not give explanations.
# Do not add extra text.
# You also need to be able to infer the topic from indirect requests. You should understand what topic exactly the student is referring to.
# """

#     agent = create_agent(
#         model=llm,
#         prompt=prompt,
#         tools=[]
#     )

#     result = agent.invoke({"messages": [("human", user_input)]})
#     return result["messages"][-1].content

# # ✅ Quiz Generation & Scoring Agent (from scoring.py)
# def generate_quiz(student_context):
#     agent = create_react_agent(
#         llm,
#         tools=[],
#         prompt=f"""
# You are a Quiz & Evaluation Agent.
# You are given student context below. Extract topic & difficulty from the text.

# STUDENT CONTEXT:
# {student_context}

# Tasks:
# 1) Create EXACTLY 5 multiple-choice questions based on topic & difficulty
# 2) Format each question as:
#    Question X: [question text]
#    A) [option]
#    B) [option]
#    C) [option]
#    D) [option]

# Give it perfectly according to the level (beginner/intermediate/advanced). Make the questions such that students actually learn something. Format well and make it super clear.

# Output ONLY the 5 questions in the format above. DO NOT add any other text.
# """
#     )

#     quiz = agent.invoke({"messages": [{"role": "user", "content": "Generate the quiz questions now."}]})
#     return quiz["messages"][-1].content

# def score_quiz(student_context, answers):
#     agent = create_react_agent(
#         llm,
#         tools=[],
#         prompt=f"""
# You are a Quiz & Evaluation Agent.

# STUDENT CONTEXT:
# {student_context}

# The student has answered 5 questions. Their answers are: {answers}

# Tasks:
# 1) Score them out of 10 total (2 points per question)
# 2) Give friendly, encouraging feedback to improve
# 3) Explain which answers were correct/incorrect and why
# 4) Provide learning tips based on their performance

# Output format:
# Score: X/10

# Feedback:
# [Write detailed, multi-line feedback that helps the student learn and improve]
# """
#     )

#     result = agent.invoke({"messages": [{"role": "user", "content": "Score the student's answers and provide feedback."}]})
#     return result["messages"][-1].content

# # ✅ Parse questions from quiz output
# def parse_questions(quiz_text):
#     questions = []
#     lines = quiz_text.strip().split('\n')
#     current_q = None

#     for line in lines:
#         line = line.strip()
#         if line.startswith('Question '):
#             if current_q:
#                 questions.append(current_q)
#             current_q = {'question': line, 'options': []}
#         elif line and current_q is not None:
#             if line[0] in ['A', 'B', 'C', 'D'] and (len(line) > 1 and line[1] in [')', '.', ']']):
#                 current_q['options'].append(line)

#     if current_q and current_q not in questions:
#         questions.append(current_q)

#     return questions

# # ✅ UI Header
# st.title("📚 Study Buddy Quiz Agent")
# st.markdown("*Your AI-powered learning companion*")
# st.divider()

# # ✅ Stage 1: Initial Input
# if st.session_state.stage == 'input':
#     st.subheader("What would you like to learn today?")
#     st.markdown("Tell me what topic you want to study and at what level (beginner/intermediate/advanced)")

#     user_input = st.text_input(
#         "Your request:",
#         placeholder="e.g., 'I want to learn about quantum physics at beginner level' or 'Teach me machine learning, I'm intermediate'",
#         key="user_input_field"
#     )

#     if st.button("Generate Quiz 🚀", type="primary"):
#         if user_input:
#             with st.spinner("🔍 Understanding your request..."):
#                 # Extract student context
#                 context = extract_student_context(user_input)
#                 st.session_state.student_context = context

#                 # Generate quiz
#                 quiz_text = generate_quiz(context)
#                 questions = parse_questions(quiz_text)

#                 if questions:
#                     st.session_state.questions = questions
#                     st.session_state.stage = 'quiz'
#                     st.session_state.current_question = 0
#                     st.session_state.answers = []
#                     st.rerun()
#                 else:
#                     st.error("Failed to generate questions. Please try again.")
#         else:
#             st.warning("Please enter what you want to learn!")

# # ✅ Stage 2: Quiz Questions (One by One)
# elif st.session_state.stage == 'quiz':
#     # Progress bar
#     progress = st.session_state.current_question / len(st.session_state.questions)
#     st.progress(progress)
#     st.markdown(f"**Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}**")

#     current_q = st.session_state.questions[st.session_state.current_question]

#     st.subheader(current_q['question'])

#     # Display options as radio buttons
#     selected_option = st.radio(
#         "Select your answer:",
#         options=current_q['options'],
#         key=f"q_{st.session_state.current_question}"
#     )

#     col1, col2 = st.columns([1, 1])

#     with col1:
#         if st.session_state.current_question > 0:
#             if st.button("⬅️ Previous"):
#                 st.session_state.current_question -= 1
#                 st.rerun()

#     with col2:
#         if st.button("Next ➡️" if st.session_state.current_question < len(st.session_state.questions) - 1 else "Submit Quiz ✅", type="primary"):
#             # Save answer
#             if len(st.session_state.answers) <= st.session_state.current_question:
#                 st.session_state.answers.append(selected_option)
#             else:
#                 st.session_state.answers[st.session_state.current_question] = selected_option

#             # Move to next question or submit
#             if st.session_state.current_question < len(st.session_state.questions) - 1:
#                 st.session_state.current_question += 1
#                 st.rerun()
#             else:
#                 # All questions answered, move to scoring
#                 with st.spinner("📊 Scoring your quiz..."):
#                     result = score_quiz(st.session_state.student_context, st.session_state.answers)
#                     st.session_state.quiz_result = result
#                     st.session_state.stage = 'results'
#                     st.rerun()

# # ✅ Stage 3: Results & Feedback
# elif st.session_state.stage == 'results':
#     st.success("✅ Quiz Complete!")

#     # Display results
#     st.markdown("### Your Results")
#     st.markdown(st.session_state.quiz_result)

#     st.divider()

#     # Options after quiz
#     col1, col2 = st.columns(2)

#     with col1:
#         if st.button("📝 Take Another Quiz", type="primary"):
#             # Reset to input stage
#             st.session_state.stage = 'input'
#             st.session_state.student_context = None
#             st.session_state.questions = []
#             st.session_state.current_question = 0
#             st.session_state.answers = []
#             st.session_state.quiz_result = None
#             st.rerun()

#     with col2:
#         if st.button("💬 Ask Follow-up Questions"):
#             st.session_state.stage = 'feedback'
#             st.rerun()

# # ✅ Stage 4: Follow-up Chat
# elif st.session_state.stage == 'feedback':
#     st.subheader("💬 Ask Me Anything!")
#     st.markdown("Feel free to ask follow-up questions about the topic or request clarifications.")

#     # Display chat history
#     for msg in st.session_state.chat_messages:
#         with st.chat_message(msg["role"]):
#             st.markdown(msg["content"])

#     # Chat input
#     if user_question := st.chat_input("Ask a follow-up question..."):
#         # Add user message
#         st.session_state.chat_messages.append({"role": "user", "content": user_question})

#         # Generate response
#         with st.spinner("Thinking..."):
#             response = llm.invoke(f"""
# Based on the student context: {st.session_state.student_context}

# Student asks: {user_question}

# Provide a helpful, educational response that helps them understand the topic better.
# """)

#             ai_response = response.content
#             st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})

#         st.rerun()

#     # Option to take new quiz
#     st.divider()
#     if st.button("📝 Take a New Quiz"):
#         # Reset everything
#         st.session_state.stage = 'input'
#         st.session_state.student_context = None
#         st.session_state.questions = []
#         st.session_state.current_question = 0
#         st.session_state.answers = []
#         st.session_state.quiz_result = None
#         st.session_state.chat_messages = []
#         st.rerun()

# # ✅ Sidebar with info
# with st.sidebar:
#     st.header("ℹ️ About")
#     st.markdown("""
#     This Study Buddy Quiz Agent helps you:
#     - 📖 Learn any topic at your pace
#     - 🎯 Test your knowledge with adaptive quizzes
#     - 💡 Get personalized feedback
#     - 💬 Ask follow-up questions

#     **How to use:**
#     1. Tell me what you want to learn
#     2. Answer 5 quiz questions
#     3. Get your score and feedback
#     4. Ask follow-up questions if needed
#     """)

#     st.divider()
#     st.markdown("*Powered by Google Gemini AI*")

import streamlit as st
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# ✅ Set page config
st.set_page_config(page_title="Study Buddy Quiz Agent", page_icon="📚", layout="centered")

# ✅ Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in .env file")
    st.stop()

# ✅ Initialize session state
if 'stage' not in st.session_state:
    st.session_state.stage = 'input'  # Stages: input, quiz, results, feedback
if 'student_context' not in st.session_state:
    st.session_state.student_context = None
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'quiz_result' not in st.session_state:
    st.session_state.quiz_result = None
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

# ✅ Create LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-exp",
    google_api_key=api_key
)

# ✅ Data Extraction Agent
def extract_student_context(user_input):
    prompt = """
You are STUDY-BUDDY-AGENT 📚
Your task is to identify what the student wants to study and infer the difficulty level
based on tone, wording, and intent.

If student gives direct difficulty level, use it.
If not, infer:
- Easy / Beginner / Super simple/ baby level/ new → beginner
- Intermediate / I know basics/ I have read a bit/ I am trying to reach a better level/medium → intermediate
- Hard / expert / deep dive/ knowledged/ tough → advanced

Return ONLY JSON in this structure:

{
    "student_request": {
        "topic": "...",
        "difficulty": "..."
    }
}

Do not give explanations.
Do not add extra text.
You also need to be able to infer the topic from indirect requests. You should understand what topic exactly the student is referring to.
"""
    agent = create_react_agent(
        llm,
        tools=[],
        prompt=prompt
    )
    result = agent.invoke({"messages": [("human", user_input)]})
    return result["messages"][-1].content

# ✅ Quiz Generation & Scoring Agent
def generate_quiz(student_context):
    agent = create_react_agent(
        llm,
        tools=[],
        prompt=f"""
You are a Quiz & Evaluation Agent.
You are given student context below. Extract topic & difficulty from the text.

STUDENT CONTEXT:
{student_context}

Tasks:
1) Create EXACTLY 5 multiple-choice questions based on topic & difficulty
2) Format each question as:
   Question X: [question text]
   A) [option]
   B) [option]
   C) [option]
   D) [option]

Give it perfectly according to the level (beginner/intermediate/advanced). Make the questions such that students actually learn something. Format well and make it super clear.

Output ONLY the 5 questions in the format above. DO NOT add any other text.
"""
    )
    quiz = agent.invoke({"messages": [{"role": "user", "content": "Generate the quiz questions now."}]})
    return quiz["messages"][-1].content

def score_quiz(student_context, answers):
    agent = create_react_agent(
        llm,
        tools=[],
        prompt=f"""
You are a Quiz & Evaluation Agent.

STUDENT CONTEXT:
{student_context}

The student has answered 5 questions. Their answers are: {answers}

Tasks:
1) Score them out of 10 total (2 points per question)
2) Give friendly, encouraging feedback to improve
3) Explain which answers were correct/incorrect and why
4) Provide learning tips based on their performance

Output format:
Score: X/10

Feedback:
[Write detailed, multi-line feedback that helps the student learn and improve]
"""
    )
    result = agent.invoke({"messages": [{"role": "user", "content": "Score the student's answers and provide feedback."}]})
    return result["messages"][-1].content

# ✅ Parse questions from quiz output
def parse_questions(quiz_text):
    questions = []
    lines = quiz_text.strip().split('\n')
    current_q = None

    for line in lines:
        line = line.strip()
        if line.startswith('Question '):
            if current_q:
                questions.append(current_q)
            current_q = {'question': line, 'options': []}
        elif line and current_q is not None:
            if line[0] in ['A', 'B', 'C', 'D'] and (len(line) > 1 and line[1] in [')', '.', ']']):
                current_q['options'].append(line)

    if current_q and current_q not in questions:
        questions.append(current_q)

    return questions

# ✅ UI Header
st.title("📚 Study Buddy Quiz Agent")
st.markdown("*Your AI-powered learning companion*")
st.divider()

# ✅ Stage 1: Initial Input
if st.session_state.stage == 'input':
    st.subheader("What would you like to learn today?")
    st.markdown("Tell me what topic you want to study and at what level (beginner/intermediate/advanced)")

    user_input = st.text_input(
        "Your request:",
        placeholder="e.g., 'I want to learn about quantum physics at beginner level' or 'Teach me machine learning, I'm intermediate'",
        key="user_input_field"
    )

    if st.button("Generate Quiz 🚀", type="primary"):
        if user_input:
            with st.spinner("🔍 Understanding your request..."):
                # Extract student context
                context = extract_student_context(user_input)
                st.session_state.student_context = context

                # Generate quiz
                quiz_text = generate_quiz(context)
                questions = parse_questions(quiz_text)

                if questions:
                    st.session_state.questions = questions
                    st.session_state.stage = 'quiz'
                    st.session_state.current_question = 0
                    st.session_state.answers = []
                    st.rerun()
                else:
                    st.error("Failed to generate questions. Please try again.")
        else:
            st.warning("Please enter what you want to learn!")

# ✅ Stage 2: Quiz Questions (One by One)
elif st.session_state.stage == 'quiz':
    # Progress bar
    progress = st.session_state.current_question / len(st.session_state.questions)
    st.progress(progress)
    st.markdown(f"**Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}**")

    current_q = st.session_state.questions[st.session_state.current_question]

    st.subheader(current_q['question'])

    # Display options as radio buttons
    selected_option = st.radio(
        "Select your answer:",
        options=current_q['options'],
        key=f"q_{st.session_state.current_question}"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.session_state.current_question > 0:
            if st.button("⬅️ Previous"):
                st.session_state.current_question -= 1
                st.rerun()

    with col2:
        if st.button("Next ➡️" if st.session_state.current_question < len(st.session_state.questions) - 1 else "Submit Quiz ✅", type="primary"):
            # Save answer
            if len(st.session_state.answers) <= st.session_state.current_question:
                st.session_state.answers.append(selected_option)
            else:
                st.session_state.answers[st.session_state.current_question] = selected_option

            # Move to next question or submit
            if st.session_state.current_question < len(st.session_state.questions) - 1:
                st.session_state.current_question += 1
                st.rerun()
            else:
                # All questions answered, move to scoring
                with st.spinner("📊 Scoring your quiz..."):
                    result = score_quiz(st.session_state.student_context, st.session_state.answers)
                    st.session_state.quiz_result = result
                    st.session_state.stage = 'results'
                    st.rerun()

# ✅ Stage 3: Results & Feedback
elif st.session_state.stage == 'results':
    st.success("✅ Quiz Complete!")

    # Display results
    st.markdown("### Your Results")
    st.markdown(st.session_state.quiz_result)

    st.divider()

    # Options after quiz
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📝 Take Another Quiz", type="primary"):
            # Reset to input stage
            st.session_state.stage = 'input'
            st.session_state.student_context = None
            st.session_state.questions = []
            st.session_state.current_question = 0
            st.session_state.answers = []
            st.session_state.quiz_result = None
            st.rerun()

    with col2:
        if st.button("💬 Ask Follow-up Questions"):
            st.session_state.stage = 'feedback'
            st.rerun()

# ✅ Stage 4: Follow-up Chat
elif st.session_state.stage == 'feedback':
    st.subheader("💬 Ask Me Anything!")
    st.markdown("Feel free to ask follow-up questions about the topic or request clarifications.")

    # Display chat history
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat input
    if user_question := st.chat_input("Ask a follow-up question..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": user_question})

        # Generate response
        with st.spinner("Thinking..."):
            response = llm.invoke(f"""
Based on the student context: {st.session_state.student_context}

Student asks: {user_question}

Provide a helpful, educational response that helps them understand the topic better.
""")

            ai_response = response.content
            st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})

        st.rerun()

    # Option to take new quiz
    st.divider()
    if st.button("📝 Take a New Quiz"):
        # Reset everything
        st.session_state.stage = 'input'
        st.session_state.student_context = None
        st.session_state.questions = []
        st.session_state.current_question = 0
        st.session_state.answers = []
        st.session_state.quiz_result = None
        st.session_state.chat_messages = []
        st.rerun()

# ✅ Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This Study Buddy Quiz Agent helps you:
    - 📖 Learn any topic at your pace
    - 🎯 Test your knowledge with adaptive quizzes
    - 💡 Get personalized feedback
    - 💬 Ask follow-up questions

    **How to use:**
    1. Tell me what you want to learn
    2. Answer 5 quiz questions
    3. Get your score and feedback
    4. Ask follow-up questions if needed
    """)

    st.divider()
    st.markdown("*Powered by Google Gemini AI*")
