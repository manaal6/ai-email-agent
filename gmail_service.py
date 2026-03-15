import base64
import os
import time
from email import message_from_bytes
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send"
]


# -----------------------------
# Create credentials.json
# -----------------------------
def create_credentials_file():

    creds_json = os.getenv("GOOGLE_CREDENTIALS")

    if creds_json and not os.path.exists("credentials.json"):

        with open("credentials.json", "w") as f:
            f.write(creds_json)


# -----------------------------
# Create token.json
# -----------------------------
def create_token_file():

    token_json = os.getenv("GMAIL_TOKEN")

    if token_json and not os.path.exists("token.json"):

        with open("token.json", "w") as f:
            f.write(token_json)


# -----------------------------
# Authenticate Gmail
# -----------------------------
def authenticate_gmail():

    create_credentials_file()
    create_token_file()

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    # Refresh token safely
    if creds and creds.expired and creds.refresh_token:

        for attempt in range(3):

            try:
                creds.refresh(Request())

                with open("token.json", "w") as token:
                    token.write(creds.to_json())

                break

            except Exception as e:

                print("Token refresh failed. Retrying...", e)
                time.sleep(10)

    if not creds or not creds.valid:

        raise RuntimeError(
            "Invalid Gmail credentials. Generate token.json locally."
        )

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service


# -----------------------------
# Read unread emails
# -----------------------------
def get_new_emails():

    service = authenticate_gmail()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        q="is:unread"
    ).execute()

    messages = results.get("messages", [])

    emails = []

    for msg in messages:

        try:

            msg_data = service.users().messages().get(
                userId="me",
                id=msg["id"],
                format="raw"
            ).execute()

            raw_msg = base64.urlsafe_b64decode(
                msg_data["raw"]
            )

            email_msg = message_from_bytes(raw_msg)

            sender = email_msg.get("From", "")
            subject = email_msg.get("Subject", "")

            body = ""

            if email_msg.is_multipart():

                for part in email_msg.walk():

                    if part.get_content_type() == "text/plain":

                        body = part.get_payload(
                            decode=True
                        ).decode(errors="ignore")

                        break

            else:

                body = email_msg.get_payload(
                    decode=True
                ).decode(errors="ignore")

            emails.append({

                "id": msg["id"],
                "sender": sender,
                "subject": subject,
                "body": body

            })

        except Exception as e:

            print("Error reading email:", e)

    return emails


# -----------------------------
# Send reply
# -----------------------------
def send_reply(to_email, subject, message):

    service = authenticate_gmail()

    try:

        email_message = MIMEText(message)

        email_message["to"] = to_email
        email_message["subject"] = "Re: " + subject

        raw_message = base64.urlsafe_b64encode(
            email_message.as_bytes()
        ).decode()

        service.users().messages().send(
            userId="me",
            body={"raw": raw_message}
        ).execute()

        print("Reply sent to:", to_email)

    except Exception as e:

        print("Failed to send reply:", e)