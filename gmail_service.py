import base64
import os
from email import message_from_bytes
from email.mime.text import MIMEText

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Permissions
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send"
]


def authenticate_gmail():
    creds = None

    # Load saved token
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # First-time authentication
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


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

        msg_data = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="raw"
        ).execute()

        raw_msg = base64.urlsafe_b64decode(msg_data["raw"])
        email_msg = message_from_bytes(raw_msg)

        sender = email_msg["From"]
        subject = email_msg["Subject"]

        body = ""

        if email_msg.is_multipart():
            for part in email_msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
        else:
            body = email_msg.get_payload(decode=True).decode(errors="ignore")

        emails.append({
            "sender": sender,
            "subject": subject,
            "body": body
        })

        # mark email as read
        service.users().messages().modify(
            userId="me",
            id=msg["id"],
            body={"removeLabelIds": ["UNREAD"]}
        ).execute()

    return emails


def send_reply(to_email, subject, message):

    service = authenticate_gmail()

    email_message = MIMEText(message)

    email_message["to"] = to_email
    email_message["subject"] = "Re: " + subject

    raw_message = base64.urlsafe_b64encode(
        email_message.as_bytes()
    ).decode()

    message_body = {
        "raw": raw_message
    }

    service.users().messages().send(
        userId="me",
        body=message_body
    ).execute()

    print("Reply sent to:", to_email)