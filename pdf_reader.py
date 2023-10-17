from datetime import datetime
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_buffer):
    reader = PdfReader(pdf_buffer)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def parse_email(text):
    lines = text.split("\n")
    data = {}
    event_date = None

    lines = lines[: lines.index("Ingredients")]

    for line in lines:
        if not data.get("event_name") and line.strip():
            data["event_name"] = line.strip()

        elif any(
            weekday in line
            for weekday in [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        ):
            event_date = line.split(",")[1].strip()

        elif "Ready by:" in line:
            data["ready_by_time"] = line.split("Ready by:")[-1].strip()

        elif "Start Time:" in line:
            data["start_time"] = line.split("Start Time:")[-1].strip()

        elif "Site Address:" in line:
            data["site_address"] = line.split("Site Address:")[-1].strip()

        elif "Headcount:" in line:
            data["headcount"] = line.split("Headcount:")[-1].strip()

        elif "Site Telephone:" in line:
            data["site_telephone"] = line.split("Site Telephone:")[-1].strip()

        elif "Booking Telephone:" in line and not data.get("site_telephone"):
            data["site_telephone"] = line.split("Booking Telephone:")[-1].strip()

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
