import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BUSINESS_NAME = os.getenv("BUSINESS_NAME", "Our Company")
BUSINESS_TONE = os.getenv("BUSINESS_TONE", "professional, warm, and concise")


def generate_reply(email_text):
    """
    Generate a professional reply to an incoming customer email.
    """
    prompt = f"""A customer sent this email:

{email_text}

Write a short reply on behalf of {BUSINESS_NAME}.
- Keep it under 100 words
- Do not repeat the customer's question back to them
- End with a clear next step or offer to help further
"""

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    f"You are a customer support representative for {BUSINESS_NAME}. "
                    f"Your tone is {BUSINESS_TONE}. "
                    "Never use filler phrases like 'Great question!' or 'Absolutely!'. "
                    "Be direct, helpful, and human."
                )
            },
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant"
    )

    return response.choices[0].message.content


def extract_sender_name(email_body, sender_raw):
    """
    Try to extract the sender's real name from the email body or the raw From header.
    Falls back to "Unknown" if no name is found.
    """
    prompt = f"""Extract the sender's first and last name from this email.

From header: {sender_raw}
Email body:
{email_body[:500]}

Reply with ONLY the person's name (e.g. "John Smith").
If you cannot find a name, reply with "Unknown".
"""

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You extract names from emails. Reply with only the name, nothing else."
                },
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            max_tokens=20
        )
        name = response.choices[0].message.content.strip()
        # Sanity check — reject if response looks like junk
        if len(name) > 50 or "\n" in name:
            return "Unknown"
        return name
    except Exception as e:
        print("Name extraction failed:", e)
        return "Unknown"