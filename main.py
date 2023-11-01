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
# if no messages print no messages
if not messages:
    print("No messages found.")

for message in messages:
    csv_path = extract_attachments_from_message(message["id"])
    if csv_path:
        try:
            raw_events = extract_events_from_csv_bytes(csv_path)

            parsed_events = [parse_event(event) for event in raw_events]

            total_events_in_csv = len(raw_events)
            matched_delivery_persons = 0
            created_events_count = 0

            for event in parsed_events:
                if event["Delivery Person"] in DELIVERY_PERSONS:
                    matched_delivery_persons += 1
                    create_calendar_event(event)
                    created_events_count += 1

            mark_email_as_read("me", message["id"])
            print(f"Total events found in CSV: {total_events_in_csv}")
            print(f"Matched delivery persons: {matched_delivery_persons}")
            print(f"Total events created: {created_events_count}")

        except Exception as e:
            print(f"Error processing CSV from message ID {message['id']}: {e}")
    else:
        print(f"No CSV found in message ID {message['id']}")
