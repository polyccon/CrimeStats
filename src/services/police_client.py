import json
import logging
import requests


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOGGER = logging.getLogger(__name__)


class PoliceClient:
    def __init__(self):
        pass

    def get_data_for_coordinates(self, latitude, longitude):
        try:
            url = f"https://data.police.uk/api/crimes-street/all-crime?"

            params = dict(lat=latitude, lng=longitude)
            resp = requests.get(url=url, params=params)
            LOGGER.info(f"police client: {resp.status_code}")
            return resp.json()
        except Exception as e:
            LOGGER.error(f"police client: {str(e)}")
            return {"error": f"police client: {str(e)}"}
