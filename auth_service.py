from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
]


SERVICE_ACCOUNT_FILE = "credentials.json"


def get_service_account_credentials():
    return Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def get_gmail_service():
    creds = get_service_account_credentials()
    return build("gmail", "v1", credentials=creds)


def get_calendar_service():
    creds = get_service_account_credentials()
    return build("calendar", "v3", credentials=creds)
