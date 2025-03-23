import os
import logging
import shutil
import tempfile
from datetime import datetime
from collections import defaultdict
from typing import List
import folium
from folium.plugins import HeatMap

from src.services.location_client import LocationClient
from src.services.police_client import PoliceClient


FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
LOGGER = logging.getLogger(__name__)


class CrimeDataProcessor:
    def __init__(self, latitude, longitude, postcode=None):
        """
        Initializes the processor with a location (postcode).
        """
        self.latitude = latitude
        self.longitude = longitude
        self.postcode = postcode
        self.location_client = LocationClient(postcode)
        self.police_client = PoliceClient()
        self.crime_data = None  # Lazy loading

    def fetch_crime_data(self) -> None:
        """Fetch crime data only when needed."""
        if self.postcode:
            LOGGER.info(f"Fetching coordinates for postcode: {self.postcode}")
            latitude, longitude = self.location_client.postcode_to_coordinates()
            self.crime_data = self.police_client.get_data_for_coordinates(
                latitude, longitude
            )
        if not self.crime_data:
            LOGGER.info(f"Fetching crime data for coordinates: {self.latitude}, {self.longitude}")
            self.crime_data = self.police_client.get_data_for_coordinates(
                self.latitude, self.longitude
            )
        return self.crime_data

    def extract_specific_data(self, key: str) -> List:
        """Helper function to count occurrences of a given key in crime data."""
        self.fetch_crime_data()

        d = defaultdict(int)
        for item in self.crime_data:
            topic = item.get(key)
            if key == "outcome_status":
                topic = topic.get("category", "Unknown") if topic else "Unknown"
            d[topic] += 1

        return [{"label": k, "value": v} for k, v in d.items()]

    def get_crime_categories(self) -> List:
        """Extracts crime categories."""
        return self.extract_specific_data("category")

    def get_crime_outcomes(self) -> List:
        """Extracts crime outcomes."""
        return self.extract_specific_data("outcome_status")

    # class CrimeDataProcessor:
    #     def __init__(self, lat, lng, crime_data):
    #         self.lat = lat
    #         self.lng = lng
    #         self.crime_data = crime_data  # Assuming crime data is passed in

    def generate_heatmap(self):
        """Generate and return the HTML for the heatmap with crime info popups."""
        self.fetch_crime_data()
        crime_colors = {
            "violent-crime": "red",
            "burglary": "orange",
            "anti-social-behaviour": "purple",
            "robbery": "darkred",
            "public-order": "blue",
            "drugs": "green",
            "vehicle-crime": "black",
            "criminal-damage-arson": "darkblue",
            "other-theft": "gray",
        }

        crime_list = []
        for crime in self.crime_data:
            location = crime.get("location", {})
            crime_type = crime.get("category", "other-crime")  # Default category if missing
            crime_date = crime.get("date", "Unknown Date")
            crime_id = crime.get("id", "Unknown ID")
            location_type = location.get("location_type", "Unknown Type")
            outcome = crime.get("outcome", "Unknown Outcome")
            street_name = location.get("street", {}).get("name", "Unknown")

            crime_list.append({
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
                "crime_type": crime_type,
                "crime_date": crime_date,
                "crime_id": crime_id,
                "location_type": location_type,
                "outcome": outcome,
                "street_name": street_name
            })

        # Filter out crimes with missing latitude or longitude
        crime_list = [c for c in crime_list if c["latitude"] and c["longitude"]]

        # Create the base map
        m = folium.Map(location=[self.latitude, self.longitude], zoom_start=12)

        # Add the HeatMap layer
        heat_data = [[float(c["latitude"]), float(c["longitude"])] for c in crime_list]
        HeatMap(heat_data, name="Crime Heatmap").add_to(m)

        # Add markers and popups for each crime
        for crime in crime_list:
            crime_type = crime["crime_type"]
            popup_info = f"""
                <b>Crime Type:</b> {crime_type}<br>
                <b>Crime Date:</b> {crime['crime_date']}<br>
                <b>Location:</b> {crime['street_name']}<br>
                <b>Location Type:</b> {crime['location_type']}<br>
                <b>Outcome:</b> {crime['outcome']}<br>
                <b>Crime ID:</b> {crime['crime_id']}
            """

            # Get color based on crime type, default to "gray" if not found
            icon_color = crime_colors.get(crime_type, "gray")

            # Add a marker for each crime with a popup
            folium.Marker(
                location=[float(crime["latitude"]), float(crime["longitude"])],
                popup=folium.Popup(popup_info, max_width=300),
                tooltip="Click for details",
                icon=folium.Icon(color=icon_color, icon="info-sign")
            ).add_to(m)

        # Define the directory to save the heatmap HTML file
        save_dir = "/code/src/static/heatmaps"
        os.makedirs(save_dir, exist_ok=True)

        # Generate a filename with the current year and month
        current_year_month = datetime.now().strftime("%Y-%m")
        file_name = f"crime_heatmap_{self.latitude}_{self.longitude}_{current_year_month}.html"

        # Full path to save the HTML file
        file_path = os.path.join(save_dir, file_name)

        # Save the generated map as an HTML file
        m.save(file_path)

        print(f"✅ Heatmap successfully saved at: {file_path}")

        return file_path
