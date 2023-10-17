from calendar_event import create_calendar_event
from mail_processor import (
    fetch_unread_emails,
    extract_attachments_from_message,
    mark_email_as_read,
)
from pdf_reader import extract_text_from_pdf, parse_email
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

messages = fetch_unread_emails()

for message in messages:
    pdf_path = extract_attachments_from_message(message["id"])
    
    if pdf_path:
        try:
            pdf_text = extract_text_from_pdf(pdf_path)
            details = parse_email(pdf_text)

            create_calendar_event(details)

            mark_email_as_read("me", message["id"])
        except Exception as e:
            print(f"Error processing PDF from message ID {message['id']}: {e}")
