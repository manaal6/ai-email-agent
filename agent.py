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

        print("Processing email from:", sender)

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

            # Mark email as read AFTER everything
            service.users().messages().modify(
                userId="me",
                id=email["id"],
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