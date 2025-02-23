import json
import logging

from src.data.convert_data import CrimeDataProcessor

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.ERROR)


def lambda_handler(event, context):
    LOGGER.debug("event", event)

    location = event.get("location", None)
    if not location:
        location = event.get("pathParameters", {}).get("location", None)
    LOGGER.debug("location", location)

    processor = CrimeDataProcessor(location)
    data = processor.get_crime_categories()
    LOGGER.info(f"Successfully obtained data for location: {location}")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"data": data}),
    }
