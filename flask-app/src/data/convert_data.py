import json
import requests
from collections import defaultdict

from src.services.location_client import LocationClient
from src.services.police_client import PoliceClient


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

    police_client = PoliceClient()
    data = police_client.get_data_for_coordinates(latitude, longitude)

    return convert_police_data(data)