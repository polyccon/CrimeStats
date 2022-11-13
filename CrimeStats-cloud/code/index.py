import json
from collections import defaultdict
import requests
import logging

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.ERROR)


def get_data(location):
    results_list = []
    if location:
        url_postcode = "http://api.postcodes.io/postcodes/" + location
        resp_postcode = requests.get(url=url_postcode)
        ll = json.loads(resp_postcode.text)["result"]
        latitude = ll["latitude"]
        longitude = ll["longitude"]
        url = "https://data.police.uk/api/crimes-street/all-crime?"
        params = dict(lat=latitude, lng=longitude)
        resp = requests.get(url=url, params=params)
        data = json.loads(resp.text)

        d = defaultdict(dict)
        for item in data:
            if not d.get(item["category"]):
                d[item["category"]] = 1
            else:
                d[item["category"]] += 1

        for key, value in d.items():
            result = {"label": key, "value": value}
            results_list.append(result)
    return results_list


def lambda_handler(event, context):
    LOGGER.debug("event", event)

    location = event.get("location", None)
    if not location:
        location = event.get("pathParameters", {}).get("location", None)
    LOGGER.debug("location", location)

    data = get_data(location)
    LOGGER.info(f"Successfully obtained data for location: {location}")

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"data": data}),
    }
