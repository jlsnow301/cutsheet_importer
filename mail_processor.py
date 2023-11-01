from auth_service import get_gmail_service
from datetime import datetime, timedelta
import base64
import io
import os


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

    messages = results.get("messages", [])

    # Fetch details of the messages to verify the sender
    allowed_email_domain = os.environ.get("ALLOWED_EMAIL_DOMAIN")
    personal_email = os.environ.get("PERSONAL_EMAIL")

    filtered_messages = []
    for message in messages:
        msg_detail = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=["From"],
            )
            .execute()
        )
        from_header = next(
            (
                header["value"]
                for header in msg_detail["payload"]["headers"]
                if header["name"] == "From"
            ),
            None,
        )

        if not from_header:
            continue

        # Check if the email is from the allowed domain or specific email
        if from_header.endswith(allowed_email_domain) or personal_email in from_header:
            filtered_messages.append(message)

    return filtered_messages


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

        if not filename.endswith(".csv"):
            continue

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
