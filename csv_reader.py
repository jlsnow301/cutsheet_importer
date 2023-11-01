from datetime import datetime
import csv

EXPECTED_HEADERS = [
    "Date",
    "Delivery Category",
    "Delivery Person",
    "Client/Organization",
    "Description",
    "Actual",
    "Kitchen Ready by ",
    "Setup By",
    "Site Category",
    "Site Contact",
    "Site Address",
]


def extract_events_from_csv_bytes(csv_bytes):
    events = []
    csv_content = csv_bytes.getvalue().decode("utf-8")
    csv_reader = csv.DictReader(csv_content.splitlines())

    for row in csv_reader:
        if any(value is None for value in row.values()):
            continue

        if not row.get("Delivery Person", "").strip():
            continue

        if csv_reader.line_num == 1 and set(row.keys()) != set(EXPECTED_HEADERS):
            print("CSV headers do not match expected headers. Skipping this row.")
            continue

        events.append(row)

    return events


def parse_event(row):
    data = {}
    event_date = None

    for header in EXPECTED_HEADERS:
        if header in row and row[header]:
            data[header] = row[header].strip()

    if "Date" in data:
        event_date = data["Date"]

    if "Kitchen Ready by " in data and event_date:
        date_str = datetime.strptime(event_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        combined_str = f"{date_str} {data['Kitchen Ready by ']}"
        datetime_obj = datetime.strptime(combined_str, "%Y-%m-%d %I:%M %p")
        data["ready_by_time"] = datetime_obj.isoformat()

    if "Setup By" in data and event_date:
        date_str = datetime.strptime(event_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        combined_str = f"{date_str} {data['Setup By']}"
        datetime_obj = datetime.strptime(combined_str, "%Y-%m-%d %I:%M %p")
        data["start_time"] = datetime_obj.isoformat()

    if "Delivery Category" in data and "Description" in data:
        data["event_name"] = f"{data['Delivery Category']} - {data['Description']}"

    return data
