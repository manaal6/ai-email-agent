from gmail_service import get_new_emails, send_reply
from ai_processor import generate_reply
import time

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
            # generate AI reply
            reply = generate_reply(body)
            # send reply
            send_reply(sender, subject, reply)
            print("Reply sent successfully to:", sender)
        except Exception as e:
            print("Error processing email:", e)

if __name__ == "__main__":
    while True:
        main()
        print("Waiting 5 minutes before checking again...")
        time.sleep(300)