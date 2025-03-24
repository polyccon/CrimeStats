import json
import logging
import requests


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOGGER = logging.getLogger(__name__)


class LocationClient:
    def __init__(self, location):
        self.location = location

    def postcode_to_coordinates(self):
        url = f"http://api.postcodes.io/postcodes/{self.location}"
        response = requests.get(url=url)
        LOGGER.info(f"location client: {response.status_code}")
        try:
            data = response.json().get("result")
            latitude = data["latitude"]
            longitude = data["longitude"]
            return latitude, longitude
        except Exception as e:
            LOGGER.error(f"police client: {str(e)}")
            return {"error": f"police client: {str(e)}"}
