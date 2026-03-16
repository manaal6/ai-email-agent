import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

BUSINESS_NAME = os.getenv("BUSINESS_NAME", "Our Company")
BUSINESS_TONE = os.getenv("BUSINESS_TONE", "professional, warm, and concise")


def classify_email(email_text):
    """
    Classify email into one of: pricing, appointment, support, complaint, general
    """
    prompt = f"""Classify this email into exactly ONE of these categories:
pricing, appointment, support, complaint, general

Email:
{email_text}

Reply with only the category word, nothing else.
"""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an email classifier. Reply with only one word."},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
        max_tokens=10
    )

    category = response.choices[0].message.content.strip().lower()

    valid = ["pricing", "appointment", "support", "complaint", "general"]
    if category not in valid:
        category = "general"

    return category


def generate_reply(email_text):
    """
    Classify the email, then generate a professional personalized reply.
    Returns (reply_text, category)
    """

    # Step 1 — classify
    category = classify_email(email_text)
    print(f"Email classified as: {category}")

    # Step 2 — generate reply
    prompt = f"""A customer sent this email:

{email_text}

Write a short reply on behalf of {BUSINESS_NAME}.
- Keep it under 100 words
- Do not repeat the customer's question back to them
- End with a clear next step or offer to help further
- The email is about: {category}
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

    reply = response.choices[0].message.content
    return reply, category


def extract_sender_name(email_body, sender_raw):
    """
    Extract sender's real name from email body or From header.
    Falls back to "Unknown".
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
        if len(name) > 50 or "\n" in name:
            return "Unknown"
        return name
    except Exception as e:
        print("Name extraction failed:", e)
        return "Unknown"