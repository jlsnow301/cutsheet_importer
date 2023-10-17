from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import Request
import os
import pickle

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
]


def get_credentials():
    creds = None

    # Determine the path to credentials based on the environment
    cred_path = (
        "/home/runner/work/credentials.json"
        if os.getenv("GITHUB_ACTIONS")
        else "credentials.json"
    )

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

    return creds


def get_gmail_service():
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)


def get_calendar_service():
    creds = get_credentials()
    return build("calendar", "v3", credentials=creds)
