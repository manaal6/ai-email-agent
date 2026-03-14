import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_reply(email_text):
    prompt = f"""
    A customer sent this email.
    Email:
    {email_text}
    Write a professional reply for a business.
    """
    response = model.generate_content(prompt)
    return response.text