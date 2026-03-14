from gmail_service import get_new_emails, send_reply
from ai_processor import generate_reply
from sheets_service import save_lead
import time
from datetime import datetime


def main():
    print("Checking for new emails...")

    emails = get_new_emails()

    if not emails:
        print("No new emails found.")
        return

    for email in emails:

        sender = email["sender"]
        subject = email["subject"]
        body = email["body"]

        print("Processing email from:", sender)

        try:
            # Generate AI reply
            reply = generate_reply(body)
            print("AI reply generated")

            # Send email reply
            send_reply(sender, subject, reply)
            print("Reply sent successfully")

            # Save lead to Google Sheets
            save_lead(
                "Unknown",
                sender,
                body,
                datetime.now().strftime("%Y-%m-%d")
            )
            print("Lead saved to Google Sheets")

        except Exception as e:
            print("Error processing email:", e)


if __name__ == "__main__":
    while True:
        main()
        print("Waiting 5 minutes before checking again...")
        time.sleep(300)