import json
import requests
from collections import defaultdict

from src.services.location_client import LocationClient
from src.services.police_client import PoliceClient
from collections import defaultdict


def convert_police_data(data):
    d = defaultdict(int)
    for item in data:
        d[item['category']] += 1

    results_list = [{'label': key, 'value': value} for key, value in d.items()]
    return results_list


def get_data(location):
    location_client = LocationClient(location)
    latitude, longitude = location_client.postcode_to_coordinates()

    police_client = PoliceClient()
    data = police_client.get_data_for_coordinates(latitude, longitude)

    return convert_police_data(data)