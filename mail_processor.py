import base64
from auth_service import get_gmail_service
from datetime import datetime, timedelta
import io


def fetch_unread_emails():
    service = get_gmail_service()

    three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")

    query = f"is:unread after:{three_days_ago} subject:'CUT SHEET for'"

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
    while parts:
        part = parts.pop()
        if part.get("parts"):
            parts.extend(part["parts"])
        if part["filename"] and part["filename"].endswith(".pdf"):
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
            return io.BytesIO(file_data)
