import pytest
from project import get_route, geocode, track
from geopy.exc import GeocoderTimedOut, GeocoderServiceError, GeocoderQueryError, GeocoderUnavailable
from unittest.mock import patch, mock_open

def main():
    test_get_route()
    test_geocode()
    test_track()


def test_get_route():
    cities = get_route("uscities.csv")
    assert cities != None

    for city in cities:
        assert "city_name" in city
        assert "longitude" in city
        assert "delivery_time" in city
        assert city["city_name"] != None
        assert float(city["latitude"]) == city["latitude"]
        assert int(city["population"]) == city["population"]
        assert city["population"] > 0
        assert city["latitude"] != city["longitude"]

        with pytest.raises(ValueError):
            assert int(city["state"])

def test_geocode():
    coded = geocode("Boston", "MA")
    assert coded.address == "Boston, Suffolk County, Massachusetts, United States"
    coded = geocode("New York", "NY")
    assert coded.address == "City of New York, New York, United States"
    coded = geocode("Woodbury", "MN")
    assert coded.address == "Woodbury, Washington County, Minnesota, United States"
    assert geocode("Kansas", "Kansas") == None
    assert geocode("Paris", "France") == None
    assert geocode("Harry", "Potter") == None

def test_track():
    data = "San Juan,Puerto Rico,1809800,18.3985,-66.061,12.065"
    with patch("builtins.open", mock_open(read_data=data)) as visited:
        city = track()
        assert "state" in city
        assert "population" in city
        assert "longitude" in city
        assert float(city["delivery_time"]) == 12.065
        assert city["city_name"] == "San Juan"
        assert float(city["latitude"]) == 18.3985


if __name__ == "__main__":
    main()

