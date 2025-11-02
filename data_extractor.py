# from langgraph.prebuilt import create_react_agent
# from langchain.agents import create_react_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import os
# import json

# # ------------------ Load API Key ------------------
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("❌ GOOGLE_API_KEY not found in .env")

# # ------------------ Create LLM ------------------
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash",
#     google_api_key=api_key
# )

# # ------------------ Custom Prompt ------------------
# prompt = """
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
#   "student_request": {
#     "topic": "...",
#     "difficulty": "..."
#   }
# }

# Do not give explanations.
# Do not add extra text.
# You also need to be able to infer the topic from indirect requests. you should understand what topic exactly the student is referring to for example if i proceed to say "i want to learn about the theory of relativity" you should understand that the topic is "theory of relativity".
# """

# # ------------------ Create Agent ------------------
# agent = create_react_agent(
#     model=llm,
#     prompt=prompt,
#     tools=[]
# )

# # ------------------ Example Run ------------------
# user_input=input("📝 Enter student request: ")
# result = agent.invoke({"messages": [("human", user_input)]})

# print("\n✅ AGENT OUTPUT\n")
# print(result["messages"][-1].content)   # ✅ Correct way

# # Save output to a file so scoring agent can read it
# with open("student_context.json", "w") as f:
#     f.write(result["messages"][-1].content)

# print("\n📦 Saved extracted JSON to student_context.json")

from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json

# ------------------ Load API Key ------------------
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env")

# ------------------ Create LLM ------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key
)

# ------------------ Custom Prompt ------------------
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
