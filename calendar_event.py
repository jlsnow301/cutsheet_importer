from auth_service import get_calendar_service


def create_calendar_event(details):
    calendar_service = get_calendar_service()

    event = {
        "summary": details["event_name"],
        "location": details["site_address"],
        "description": f"Headcount: {details['headcount']}. Contact Phone: {details['site_telephone']}",
        "start": {
            "dateTime": details["ready_by_time"],
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": details["start_time"],
            "timeZone": "America/Los_Angeles",
        },
    }

    event = calendar_service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created: {event['htmlLink']}")
