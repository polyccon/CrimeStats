import pytest
from unittest.mock import patch, MagicMock

from src.data.convert_data import CrimeDataProcessor

# Mock data
MOCK_COORDINATES = (51.5074, -0.1278)  # London example
MOCK_CRIME_DATA = [
    {"category": "burglary", "outcome_status": {"category": "Under investigation"}},
    {"category": "theft", "outcome_status": {"category": "No further action"}},
    {"category": "burglary", "outcome_status": None},  # No outcome
    {"category": "theft", "outcome_status": {"category": "Under investigation"}},
]

@pytest.fixture
def mock_processor():
    """Fixture to create a CrimeDataProcessor with mocked API calls."""
    with patch("src.data.convert_data.LocationClient") as MockLocationClient, \
         patch("src.data.convert_data.PoliceClient") as MockPoliceClient:

        # Mock LocationClient behavior
        mock_location = MockLocationClient.return_value
        mock_location.postcode_to_coordinates.return_value = MOCK_COORDINATES

        # Mock PoliceClient behavior
        mock_police = MockPoliceClient.return_value
        mock_police.get_data_for_coordinates.return_value = MOCK_CRIME_DATA

        return CrimeDataProcessor("SW1A 1AA")


def test_get_crime_categories(mock_processor):
    """Test if categories are counted correctly."""
    expected_result = [
        {"label": "burglary", "value": 2},
        {"label": "theft", "value": 2}
    ]
    assert mock_processor.get_crime_categories() == expected_result


def test_get_crime_outcomes(mock_processor):
    """Test if outcomes are counted correctly, including 'Unknown' cases."""
    expected_result = [
        {"label": "Under investigation", "value": 2},
        {"label": "No further action", "value": 1},
        {"label": "Unknown", "value": 1},  # One crime had no outcome
    ]

    assert mock_processor.get_crime_outcomes() == expected_result


def test_fetch_crime_data_calls_api_once(mock_processor):
    """Ensure postcode_to_coordinates and get_data_for_coordinates are only called once."""

    with patch.object(mock_processor.location_client, "postcode_to_coordinates", return_value=(51.5074, -0.1278)) as mock_location, \
         patch.object(mock_processor.police_client, "get_data_for_coordinates", return_value=[{"category": "theft"}]) as mock_police:

        mock_processor.get_crime_categories()
        mock_processor.get_crime_outcomes()

        # Assert API methods are only called once
        mock_location.assert_called_once()
        mock_police.assert_called_once()
