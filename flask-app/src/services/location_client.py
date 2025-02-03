import json
import requests


class LocationClient:
    def __init__(self, location):
        self.location = location

    def location_to_coordinates(self):
        url = f"http://api.postcodes.io/postcodes/{self.location}"
        resp_postcode = requests.get(url=url)
        data = json.loads(resp_postcode.text)['result']
        latitude = data['latitude']
        longitude = data['longitude']
        return latitude, longitude