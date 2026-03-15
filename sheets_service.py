import os
import gspread
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

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
    sheet = client.open_by_key("1Ge2AG1piFHXbiA6_LAwK2zkEmUkJavoJ8az9i9c7qPc").sheet1
    return sheet


def save_lead(name, email, request, date):

    try:

        sheet = get_sheet()
        sheet.append_row([name, email, request, date])
        print("Lead saved to Google Sheets")

    except Exception as e:
        print("Error saving lead:", e)