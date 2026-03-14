import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os
from datetime import datetime

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]


def connect_sheet():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    client = gspread.authorize(creds)

    sheet = client.open("AI Leads").sheet1

    return sheet


def save_lead(name, email, request):

    sheet = connect_sheet()

    date = datetime.now().strftime("%Y-%m-%d")

    sheet.append_row([
        name,
        email,
        request,
        date
    ])

    print("Lead saved:", email)