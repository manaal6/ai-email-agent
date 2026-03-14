from gmail_service import get_new_emails, send_reply
from ai_processor import generate_reply
from sheets_service import save_lead
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

        # generate AI reply
        reply = generate_reply(email)

        # send reply
        send_reply(sender, subject, reply)

        # save lead to Google Sheets
        save_lead(
            "Unknown",
            sender,
            body,
            datetime.now().strftime("%Y-%m-%d")
        )

        print("Email processed successfully\n")


if __name__ == "__main__":
    main()