from datetime import datetime
import csv


def extract_events_from_csv_bytes(csv_bytes):
    events = []
    csv_content = csv_bytes.getvalue().decode("utf-8")
    csv_reader = csv.DictReader(csv_content.splitlines())
    for row in csv_reader:
        events.append(row)

    return events


def parse_event(row):
    data = {}
    event_date = None

    if "Date" in row:
        event_date = row["Date"]

    if "Delivery Person" in row:
        data["Delivery Person"] = row["Delivery Person"].strip()

    if "Kitchen Ready by " in row:
        data["ready_by_time"] = row["Kitchen Ready by "].strip()

    if "Setup By" in row:
        data["start_time"] = row["Setup By"].strip()

    if "Actual" in row:
        data["headcount"] = row["Actual"].strip()

    if "Client/Organization" in row:
        data["client"] = row["Client/Organization"].strip()

    delivery_category = row.get("Delivery Category", "").strip()
    description = row.get("Description", "").strip()
    data["event_name"] = f"{delivery_category} - {description}"

    if event_date:
        date_str = datetime.strptime(event_date, "%m/%d/%Y").strftime("%Y-%m-%d")

        # Combine with time and convert to ISO format for ready_by_time
        if "ready_by_time" in data:
            combined_str = f"{date_str} {data['ready_by_time']}"
            datetime_obj = datetime.strptime(combined_str, "%Y-%m-%d %I:%M %p")
            data["ready_by_time"] = datetime_obj.isoformat()

        # Do the same for start_time if needed
        if "start_time" in data:
            combined_str = f"{date_str} {data['start_time']}"
            datetime_obj = datetime.strptime(combined_str, "%Y-%m-%d %I:%M %p")
            data["start_time"] = datetime_obj.isoformat()

    return data
