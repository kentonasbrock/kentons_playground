"""Weather module for fetching NOAA 7-day forecast data for Cincinnati, OH."""
from __future__ import annotations

import json
import urllib.request
from dataclasses import dataclass

CINCINNATI_LAT = 39.1031
CINCINNATI_LON = -84.5120
NOAA_API_BASE = "https://api.weather.gov"
USER_AGENT = "python_package/weather (kentons-playground)"
FORECAST_PERIODS = 14  # 14 half-day periods = 7 full days


@dataclass
class ForecastPeriod:
    """A single forecast period (roughly 12 hours: day or night)."""

    name: str
    temperature: int
    temperature_unit: str
    wind_speed: str
    wind_direction: str
    short_forecast: str
    detailed_forecast: str


def _fetch_json(url: str) -> dict:
    """Fetch JSON from a NOAA API URL."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "application/geo+json"},
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def get_forecast_url() -> str:
    """Return the NOAA gridpoint forecast URL for Cincinnati, OH."""
    data = _fetch_json(f"{NOAA_API_BASE}/points/{CINCINNATI_LAT},{CINCINNATI_LON}")
    return data["properties"]["forecast"]


def get_7day_forecast() -> list[ForecastPeriod]:
    """Fetch the 7-day forecast for Cincinnati, OH from NOAA.

    Returns up to 14 ForecastPeriod objects (day + night for each of 7 days).
    """
    data = _fetch_json(get_forecast_url())
    periods = data["properties"]["periods"][:FORECAST_PERIODS]
    return [
        ForecastPeriod(
            name=p["name"],
            temperature=p["temperature"],
            temperature_unit=p["temperatureUnit"],
            wind_speed=p["windSpeed"],
            wind_direction=p["windDirection"],
            short_forecast=p["shortForecast"],
            detailed_forecast=p["detailedForecast"],
        )
        for p in periods
    ]
