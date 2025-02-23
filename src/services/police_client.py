import json
import requests


class PoliceClient:
    def __init__(self):
        pass

    def get_data_for_coordinates(self, latitude, longitude):
        url = "https://data.police.uk/api/crimes-street/all-crime?"
        params = dict(lat=latitude, lng=longitude)
        resp = requests.get(url=url, params=params)
        return json.loads(resp.text)
