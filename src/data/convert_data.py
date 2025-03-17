import os
from datetime import datetime
from collections import defaultdict
from typing import List
import folium
from folium.plugins import HeatMap

from src.services.location_client import LocationClient
from src.services.police_client import PoliceClient


class CrimeDataProcessor:
    def __init__(self, location):
        """
        Initializes the processor with a location (postcode).
        """
        self.location = location
        self.location_client = LocationClient(location)
        self.police_client = PoliceClient()
        self.crime_data = None  # Lazy loading

    def fetch_crime_data(self) -> None:
        """Fetch crime data only when needed."""
        if not self.crime_data:
            latitude, longitude = self.location_client.postcode_to_coordinates()
            self.crime_data = self.police_client.get_data_for_coordinates(
                latitude, longitude
            )

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

    def generate_heatmap(self):
        """Generate a heatmap using live Police API data."""
        self.fetch_crime_data()
        lat, lng = self.location_client.postcode_to_coordinates()

        if not self.crime_data:
            return {"error": "No crime data found or API request failed"}

        # Extract lat/lng and details
        crime_list = []
        for crime in self.crime_data:
            location = crime.get("location", {})
            crime_list.append({
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
                "crime_type": crime.get("category"),
                "street_name": location.get("street", {}).get("name", "Unknown")
            })

        # Filter out missing locations
        crime_list = [c for c in crime_list if c["latitude"] and c["longitude"]]

        # Create map centered on given location
        m = folium.Map(location=[lat, lng], zoom_start=12)

        # Add heatmap layer
        heat_data = [[float(c["latitude"]), float(c["longitude"])] for c in crime_list]
        HeatMap(heat_data, name="Crime Heatmap").add_to(m)

        # Add crime markers with popups
        for crime in crime_list:
            popup_info = f"<b>Crime:</b> {crime['crime_type']}<br><b>Location:</b> {crime['street_name']}"
            folium.Marker(
                location=[float(crime["latitude"]), float(crime["longitude"])],
                popup=folium.Popup(popup_info, max_width=300),
                tooltip="Click for details",
                icon=folium.Icon(color="blue", icon="info-sign")
            ).add_to(m)
        current_year_month = datetime.now().strftime("%Y-%m")
        # Save map to an HTML file
        save_path = "/code/src"
        os.makedirs(save_path, exist_ok=True)

        map_filename = os.path.join(save_path, f"crime_heatmap_{self.location}_{current_year_month}.html")
        m.save(map_filename)

        return map_filename
