from collections import defaultdict
from typing import List

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
            self.crime_data = self.police_client.get_data_for_coordinates(latitude, longitude)

    def extract_specific_data(self, key: str) -> List:
        """Helper function to count occurrences of a given key in crime data."""
        self.fetch_crime_data()

        d = defaultdict(int)
        for item in self.crime_data:
            if key == "outcome_status":
                outcome = item.get("outcome_status")
                if outcome:
                    outcome_category = outcome.get("category", "Unknown")
                else:
                    outcome_category = "Unknown"
                d[outcome_category] += 1
            elif key == "category":
                category = item.get(key, "Unknown")
                d[category] += 1

        return [{'label': k, 'value': v} for k, v in d.items()]

    def get_crime_categories(self) -> List:
        """Extracts crime categories."""
        return self.extract_specific_data("category")

    def get_crime_outcomes(self) -> List:
        """Extracts crime outcomes."""
        return self.extract_specific_data("outcome_status")