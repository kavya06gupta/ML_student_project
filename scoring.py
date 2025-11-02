# import os
# import json
# from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langgraph.prebuilt import create_react_agent

# # ✅ Load API Key
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("❌ GOOGLE_API_KEY not found in .env")

# # ✅ Read the file EXACTLY like your extractor setup expects
# with open("student_context.json", "r") as f:
#     student_context_text = f.read().strip()

# # ✅ Create Gemini Model
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=api_key
# )

# # ✅ Build our scoring agent
# agent = create_react_agent(
#     llm,
#     tools=[],  # no tools needed
#     prompt="""
# You are a Quiz & Evaluation Agent.

# You are given student context below. It LOOKS like JSON but may not be valid JSON.
# Extract topic & difficulty from the text using reasoning (NOT parsing errors).

# STUDENT CONTEXT:
# {student_context}

# Tasks:
# 1) Create EXACTLY 5 questions based on topic & difficulty
#    - MCQs types only
# 2) Wait for student's answers (don't score yet)
# 3) After answers are given, score them out of 10 total
# 4) Give friendly feedback to improve (NOT JSON — just text)
# 5) Give it perfectly according to the level (beginer/intermediate/advanced) make the questions such that students actually learn soemthing. format well and makew it super clear
# Output rules:
# - First output ONLY the 5 questions.
# - After answers come, output:
#   Score: X/10
#   Feedback: (write feedback nicely, multi-line allowed)

# DO NOT return JSON at any stage.
# """.format(student_context=student_context_text)
# )

# print("\n📚 STUDENT CONTEXT LOADED")
# print(student_context_text)

# print("\n🤖 Generating quiz questions...\n")

# # ✅ Ask agent for quiz
# quiz = agent.invoke({"messages":[{"role":"user","content":"Generate the quiz questions now."}]})
# print(quiz["messages"][-1].content)

# # ✅ Collect answers from user
# answers = []
# print("\n✍️ Enter your answers:")
# for i in range(1,6):
#     ans = input(f"Answer {i}: ")
#     answers.append(ans)

# print("\n⏳ Scoring your responses...\n")

# # ✅ Ask agent to evaluate
# grading_input = f"""
# Student answers: {answers}
# Now score them & give feedback.
# """
# grade = agent.invoke({"messages":[{"role":"user","content":grading_input}]})

# print("✅ RESULT:\n")
# print(grade["messages"][-1].content)

import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

# ✅ Load API Key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")

# ✅ Read the file EXACTLY like your extractor setup expects
with open("student_context.json", "r") as f:
    student_context_text = f.read().strip()

# ✅ Create Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key
)

# ✅ Build our scoring agent
agent = create_react_agent(
    llm,
    tools=[],  # no tools needed
    prompt="""
You are a Quiz & Evaluation Agent.
You are given student context below. It LOOKS like JSON but may not be valid JSON.
Extract topic & difficulty from the text using reasoning (NOT parsing errors).

STUDENT CONTEXT:

{student_context}

Tasks:

1) Create EXACTLY 5 questions based on topic & difficulty
- MCQs types only
2) Wait for student's answers, don't score yet
3) After answers are given, score them out of 10 total
4) Give friendly feedback to improve
5) Explain which answers were correct/incorrect
6) Provide learning tips based on their performance

Output ONLY the questions or the scored feedback depending on stage.
"""
)
