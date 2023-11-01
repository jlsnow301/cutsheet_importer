import json
import os

from auth_service import get_calendar_service


def get_delivery_person_email(name):
    delivery_persons = json.loads(os.environ.get("DELIVERY_PERSONS", "{}"))
    return delivery_persons.get(name)


def create_calendar_event(details):
    delivery_person_email = get_delivery_person_email(details.get("Delivery Person"))

    calendar_service = get_calendar_service()

    event = {
        "summary": details["event_name"],
        "description": f"Client: {details.get('Client/Organization', '')}. Headcount: {details.get('Actual', '')}.",
        "location": details["Site Address"],
        "start": {
            "dateTime": details["ready_by_time"],
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": details["start_time"],
            "timeZone": "America/Los_Angeles",
        },
        "attendees": [{"email": delivery_person_email}],
        "visibility": "private",
    }

    event = calendar_service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {event['htmlLink']}")
