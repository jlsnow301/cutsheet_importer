import base64
import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

creds = None
if os.path.exists("token.pickle"):
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

# Connect to the Gmail API
service = build("gmail", "v1", credentials=creds)
results = (
    service.users()
    .messages()
    .list(userId="me", labelIds=["INBOX"], q="is:unread")
    .execute()
)
messages = results.get("messages", [])

for message in messages:
    msg = service.users().messages().get(userId="me", id=message["id"]).execute()
    for part in msg["payload"]["parts"]:
        if part["filename"]:
            if "data" in part["body"]:
                data = part["body"]["data"]
            else:
                att_id = part["body"]["attachmentId"]
                att = (
                    service.users()
                    .messages()
                    .attachments()
                    .get(userId="me", messageId=message["id"], id=att_id)
                    .execute()
                )
                data = att["data"]
            file_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
            path = part["filename"]

            with open(path, "wb") as f:
                f.write(file_data)

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
]

# Assuming 'creds' and 'service' are already setup from Gmail part
calendar_service = build("calendar", "v3", credentials=creds)

def add_to_calendar(summary, description, start_time, end_time):
    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "America/Los_Angeles",
        },
    }
    event = calendar_service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {event['htmlLink']}")
