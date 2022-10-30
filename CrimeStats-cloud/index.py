import json
from collections import defaultdict
import requests


def get_data(location):
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

    results_list = []
    for key, value in d.items():
        result = {"label": key, "value": value}
        results_list.append(result)
    return results_list


def lambda_handler(event, context):
    location = event["location"]
    return json.loads(json.dumps((get_data(location))))
