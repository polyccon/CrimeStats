from collections import defaultdict

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

    def fetch_crime_data(self):
        """Fetch crime data only when needed."""
        if self.crime_data is None:  # Avoid redundant API calls
            latitude, longitude = self.location_client.postcode_to_coordinates()
            self.crime_data = self.police_client.get_data_for_coordinates(latitude, longitude)

    def gather_category_data(self):
        """Helper function to count occurrences of a given key in crime data."""
        self.fetch_crime_data()

        d = defaultdict(int)
        for item in self.crime_data:
            d[item['category']] += 1

        return [{'label': key, 'value': value} for key, value in d.items()]

    def get_crime_categories(self):
        """Extracts crime categories."""
        return self.gather_category_data()
