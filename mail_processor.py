from auth_service import get_gmail_service
from datetime import datetime, timedelta
import base64
import io


def fetch_unread_emails():
    service = get_gmail_service()

    three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

    # Update the search query
    query = f"is:unread after:{three_days_ago} subject:'Catering Schedule'"

    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=["INBOX"], q=query)
        .execute()
    )

    return results.get("messages", [])


def extract_attachments_from_message(message_id):
    service = get_gmail_service()
    msg = service.users().messages().get(userId="me", id=message_id).execute()

    parts = [msg["payload"]]
    file_data = None
    while parts:
        part = parts.pop()
        if part.get("parts"):
            parts.extend(part["parts"])
        filename = part.get("filename", "")
        # Look for attachments that are CSV and start with "Catering Schedule"
        if filename.startswith("Catering-Schedule") and filename.endswith(".csv"):
            if "data" in part["body"]:
                data = part["body"]["data"]
            else:
                att_id = part["body"]["attachmentId"]
                att = (
                    service.users()
                    .messages()
                    .attachments()
                    .get(userId="me", messageId=message_id, id=att_id)
                    .execute()
                )
                data = att["data"]
            file_data = base64.urlsafe_b64decode(data.encode("UTF-8"))
            break

    if file_data:
        return io.BytesIO(file_data)


def mark_email_as_read(user_id, msg_id):
    service = get_gmail_service()

    service.users().messages().modify(
        userId=user_id, id=msg_id, body={"removeLabelIds": ["UNREAD"]}
    ).execute()
