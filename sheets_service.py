import os
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_sheet():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
    client = gspread.authorize(creds)
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID is not set in environment variables")
    sheet = client.open_by_key(sheet_id).sheet1
    return sheet


def save_lead(name, email, request, date, category="general"):
    try:
        sheet = get_sheet()
        sheet.append_row([name, email, request, date, category])
        print(f"Lead saved to Google Sheets | {email} | {category}")
    except Exception as e:
        print("Error saving lead:", e)