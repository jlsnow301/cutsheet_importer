import os
import json
from calendar_event import create_calendar_event
from mail_processor import (
    fetch_unread_emails,
    extract_attachments_from_message,
    mark_email_as_read,
)
from csv_reader import extract_events_from_csv_bytes, parse_event

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

DELIVERY_PERSONS = json.loads(os.environ.get("DELIVERY_PERSONS", "{}"))

messages = fetch_unread_emails()

for message in messages:
    csv_path = extract_attachments_from_message(message["id"])

    if csv_path:
        try:
            raw_events = extract_events_from_csv_bytes(csv_path)

            parsed_events = [parse_event(event) for event in raw_events]

            for event in parsed_events:
                if event["Delivery Person"] in DELIVERY_PERSONS:
                    create_calendar_event(event)

            mark_email_as_read("me", message["id"])
        except Exception as e:
            print(f"Error processing CSV from message ID {message['id']}: {e}")
