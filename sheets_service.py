import os
import gspread
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/spreadsheets",  # no drive scope
]


def get_sheet():
    creds = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )
    print("Token scopes:", creds.scopes)  # add this line
    client = gspread.authorize(creds)
    sheet = client.open("AI Leads").sheet1
    return sheet


def save_lead(name, email, request, date):

    try:

        sheet = get_sheet()

        sheet.append_row([
            name,
            email,
            request,
            date
        ])

        print("Lead saved to Google Sheets")

    except Exception as e:

        print("Error saving lead:", e)