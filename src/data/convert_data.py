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

        # Define crime type to color mapping
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

        # Extract lat/lng and details
        crime_list = []
        for crime in self.crime_data:
            location = crime.get("location", {})
            outcome_status = crime.get("outcome_status", {})
            outcome = outcome_status.get("category", "Unknown") if outcome_status else None
            date = outcome_status.get("date", "Unknown") if outcome_status else None
            crime_info = {
                "latitude": location.get("latitude"),
                "longitude": location.get("longitude"),
                "crime_type": crime.get("category"),
                "crime_date": date,
                "crime_id": crime.get("id"),
                "location_type": location.get("location_type"),
                "outcome": outcome,
                "street_name": location.get("street", {}).get("name"),
            }

            # Remove fields that are None or "Unknown"
            filtered_crime_info = {k: v for k, v in crime_info.items() if v and v != "Unknown"}

            # Ensure latitude and longitude exist before adding to the list
            if "latitude" in filtered_crime_info and "longitude" in filtered_crime_info:
                crime_list.append(filtered_crime_info)


        # Filter out missing locations
        crime_list = [c for c in crime_list if c["latitude"] and c["longitude"]]

        # Create map centered on given location
        m = folium.Map(location=[lat, lng], zoom_start=12)

        # Add heatmap layer
        heat_data = [[float(c["latitude"]), float(c["longitude"])] for c in crime_list]
        HeatMap(heat_data, name="Crime Heatmap").add_to(m)

        # Add crime markers with color-coded icons
        for crime in crime_list:
            crime_type = crime.get("crime_type")
            crime_details = {
                "Crime Type": crime_type,
                "Crime Date": crime.get("crime_date"),
                "Location": crime.get("street_name"),
                "Location Type": crime.get("location_type"),
                "Outcome": crime.get("outcome"),
                "Crime ID": crime.get("crime_id"),
            }

            # Construct popup content dynamically
            popup_info = "<b>Crime Details:</b><br>"
            popup_info += "".join(
                f"<b>{key}:</b> {value}<br>" for key, value in crime_details.items() if value
            )

            icon_color = crime_colors.get(crime_type, "gray")

            folium.Marker(
                location=[float(crime["latitude"]), float(crime["longitude"])],
                popup=folium.Popup(popup_info, max_width=300),
                tooltip="Click for details",
                icon=folium.Icon(color=icon_color, icon="info-sign")
            ).add_to(m)

        # Generate filename based on date
        current_year_month = datetime.now().strftime("%Y-%m")
        save_path = "/code/src/static/heatmaps"
        os.makedirs(save_path, exist_ok=True)

        map_filename = os.path.join(save_path, f"crime_heatmap_{self.location}_{current_year_month}.html")
        m.save(map_filename)

        return map_filename
