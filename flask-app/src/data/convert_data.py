import json
import requests
from collections import defaultdict
from services.location_client import LocationClient


def convert_police_data(data):
    d = defaultdict(dict)
    for item in data:
        if not d.get(item['category']):
            d[item['category']] = 1
        else:
            d[item['category']] += 1

    results_list = []
    for key, value in d.items():
        result = {
            'label': key, 'value': value
        }
        results_list.append(result)
    return results_list


def get_data(location):
    location_client = LocationClient(location)
    latitude, longitude = location_client.postcode_to_coordinates()

    url = 'https://data.police.uk/api/crimes-street/all-crime?'
    params = dict(
        lat=latitude,
        lng=longitude
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    return convert_police_data(data)