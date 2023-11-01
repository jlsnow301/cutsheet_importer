import json
import os


DELIVERY_PERSONS = json.loads(os.environ.get("DELIVERY_PERSONS", "{}"))


def match_driver(delivery_person_str):
    # List how many delivery persons are loaded from the environment variables
    print(f"Loaded {len(DELIVERY_PERSONS)} delivery persons from environment variables")
    drivers = [name.strip() for name in delivery_person_str.split(",")]

    if len(drivers) > 1:  # If there are multiple drivers, match by first name
        matched_drivers = [
            driver
            for driver in drivers
            if any(driver == name.split()[0] for name in DELIVERY_PERSONS.keys())
        ]
    else:  # If only one driver, match by the full name
        matched_drivers = [driver for driver in drivers if driver in DELIVERY_PERSONS]

    return list(
        set(matched_drivers)
    )  # Convert to set and back to list to remove duplicates
