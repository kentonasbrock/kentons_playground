"""Tests for the weather module."""
from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from python_package.weather import ForecastPeriod, get_7day_forecast

MOCK_POINTS_RESPONSE = {
    "properties": {
        "forecast": "https://api.weather.gov/gridpoints/ILN/36,40/forecast",
    }
}

MOCK_PERIOD = {
    "name": "Today",
    "temperature": 72,
    "temperatureUnit": "F",
    "windSpeed": "10 mph",
    "windDirection": "SW",
    "shortForecast": "Partly Cloudy",
    "detailedForecast": "Partly cloudy with a high near 72.",
}

MOCK_FORECAST_RESPONSE = {
    "properties": {
        "periods": [MOCK_PERIOD] * 14,
    }
}


def _make_mock_response(data: dict) -> MagicMock:
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(data).encode()
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


def test_get_7day_forecast(unit_test_mocks: None, monkeypatch):
    """Unit test: verifies forecast parsing with mocked NOAA responses."""
    responses = iter(
        [
            _make_mock_response(MOCK_POINTS_RESPONSE),
            _make_mock_response(MOCK_FORECAST_RESPONSE),
        ]
    )
    monkeypatch.setattr("urllib.request.urlopen", lambda req: next(responses))

    forecast = get_7day_forecast()

    assert len(forecast) == 14
    assert isinstance(forecast[0], ForecastPeriod)
    assert forecast[0].name == "Today"
    assert forecast[0].temperature == 72
    assert forecast[0].temperature_unit == "F"
    assert forecast[0].wind_speed == "10 mph"
    assert forecast[0].wind_direction == "SW"
    assert forecast[0].short_forecast == "Partly Cloudy"
    assert forecast[0].detailed_forecast == "Partly cloudy with a high near 72."


def test_int_get_7day_forecast():
    """Integration test: calls the live NOAA API."""
    forecast = get_7day_forecast()

    assert len(forecast) >= 1
    assert isinstance(forecast[0], ForecastPeriod)
    assert forecast[0].name != ""
    assert forecast[0].temperature_unit in ("F", "C")
