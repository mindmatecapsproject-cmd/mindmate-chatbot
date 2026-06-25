import google.generativeai as genai
import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-1.5-flash")

def get_response(user_message):

    prompt = f"""
    You are MindMate, a supportive school wellbeing chatbot.

    Student says:
    {user_message}

    Give:
    - empathy
    - practical advice
    - short response
    """

    response = model.generate_content(prompt)

    return response.text
