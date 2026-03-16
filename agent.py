from gmail_service import get_new_emails, send_reply, authenticate_gmail
from ai_processor import generate_reply, extract_sender_name
from sheets_service import save_lead

import time
import urllib.request
from datetime import datetime, timezone, timedelta
import re

PKT = timezone(timedelta(hours=5))  # Pakistan Standard Time


def extract_email(sender):
    match = re.search(r"<(.+?)>", sender)
    if match:
        return match.group(1)
    return sender


def is_automated_email(sender):
    sender = sender.lower()
    return any(x in sender for x in ["noreply", "no-reply", "do-not-reply", "mailer-daemon"])


def already_replied(service, message_id):
    msg = service.users().messages().get(
        userId="me",
        id=message_id,
        format="metadata"
    ).execute()

    thread_id = msg["threadId"]

    thread = service.users().threads().get(
        userId="me",
        id=thread_id
    ).execute()

    return len(thread["messages"]) > 1


def main():

    print("Checking for new emails...")

    emails = get_new_emails()

    if not emails:
        print("No new emails found.")
        return

    service = authenticate_gmail()

    for email in emails:

        sender_raw = email["sender"]
        sender = extract_email(sender_raw)
        subject = email["subject"]
        body = email["body"]
        message_id = email["id"]

        print(f"Processing email from: {sender}")

        if is_automated_email(sender):
            print("Skipping automated email")
            continue

        if already_replied(service, message_id):
            print("Skipping email (already replied in thread)")
            continue

        try:

            # Generate AI reply + category
            reply, category = generate_reply(body)
            print(f"AI reply generated | Category: {category}")

            # Send reply
            send_reply(sender, subject, reply)
            print(f"Reply sent to: {sender}")

            # Extract sender name
            sender_name = extract_sender_name(body, sender_raw)

            # Save lead with category
            save_lead(
                sender_name,
                sender,
                body,
                datetime.now(PKT).strftime("%Y-%m-%d %H:%M:%S"),
                category
            )

            # Mark as read
            service.users().messages().modify(
                userId="me",
                id=message_id,
                body={"removeLabelIds": ["UNREAD"]}
            ).execute()

            print("Email marked as read")

        except Exception as e:
            print(f"Error processing email: {e}")


if __name__ == "__main__":

    while True:
        main()
        print("Waiting 60 seconds before checking again...")
        time.sleep(60)