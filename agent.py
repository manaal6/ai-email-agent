from gmail_service import get_new_emails, send_reply, authenticate_gmail
from ai_processor import generate_reply
from sheets_service import save_lead

import time
from datetime import datetime
import re


def extract_email(sender):
    """
    Extract real email from 'Name <email@domain.com>'
    """
    match = re.search(r"<(.+?)>", sender)
    if match:
        return match.group(1)
    return sender


def is_automated_email(sender):

    sender = sender.lower()

    if "noreply" in sender:
        return True

    if "no-reply" in sender:
        return True

    if "do-not-reply" in sender:
        return True

    if "mailer-daemon" in sender:
        return True

    return False


def already_replied(service, message_id):
    """
    Check if email thread already has replies
    """

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

    messages = thread["messages"]

    # If thread has more than 1 message → skip
    if len(messages) > 1:
        return True

    return False


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

        print("Processing email from:", sender)

        # Skip automated emails
        if is_automated_email(sender):
            print("Skipping automated email")
            continue

        # Thread protection
        if already_replied(service, message_id):
            print("Skipping email (already replied in thread)")
            continue

        try:

            # Generate AI reply
            reply = generate_reply(body)

            print("AI reply generated")

            # Send reply
            send_reply(sender, subject, reply)

            print("Reply sent successfully")

            # Save lead
            save_lead(
                "Unknown",
                sender,
                body,
                datetime.now().strftime("%Y-%m-%d")
            )

            print("Lead saved to Google Sheets")

            # Mark email as read
            service.users().messages().modify(
                userId="me",
                id=message_id,
                body={"removeLabelIds": ["UNREAD"]}
            ).execute()

            print("Email marked as read")

        except Exception as e:

            print("Error processing email:", e)


if __name__ == "__main__":

    while True:

        main()

        print("Waiting 5 minutes before checking again...")

        time.sleep(300)