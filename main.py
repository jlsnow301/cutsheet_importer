import os
from calendar_event import create_calendar_event
from mail_processor import (
    fetch_unread_emails,
    extract_attachments_from_message,
    mark_email_as_read,
)
from csv_reader import extract_events_from_csv_bytes, parse_event
from match_driver import match_driver

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


messages = fetch_unread_emails()

if not messages:
    print("No messages found.")

for message in messages:
    csv_path = extract_attachments_from_message(message["id"])
    if not csv_path:
        print(f"No CSV found in message ID {message['id']}")
        continue

    try:
        raw_events = extract_events_from_csv_bytes(csv_path)

        parsed_events = [parse_event(event) for event in raw_events]

        total_events_in_csv = len(raw_events)
        matched_delivery_persons = 0
        created_events_count = 0

        for event in parsed_events:
            matched_drivers = match_driver(event["Delivery Person"])
            if not matched_drivers:
                continue

            for driver in matched_drivers:
                matched_delivery_persons += 1
                event[
                    "Delivery Person"
                ] = driver  # Update the event with individual driver
                create_calendar_event(event)
                created_events_count += 1

        mark_email_as_read("me", message["id"])
        print(f"Total events found in CSV: {total_events_in_csv}")
        print(f"Matched delivery persons: {matched_delivery_persons}")
        print(f"Total events created: {created_events_count}")

    except Exception as e:
        print(f"Error processing CSV from message ID {message['id']}: {e}")
