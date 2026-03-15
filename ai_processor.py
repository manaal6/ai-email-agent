import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_reply(email_text):

    prompt = f"""
A customer sent this email:

{email_text}

Write a short professional reply from a business.
"""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a professional customer support assistant."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant"
    )

    return response.choices[0].message.content