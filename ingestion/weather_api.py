
import requests
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

API_URL = "https://archive-api.open-meteo.com/v1/archive"


def ingest_weather_data(
    latitude=20.91,
    longitude=77.78,
    start_date="2026-01-01",
    end_date="2026-10-31"
):

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "dew_point_2m",
            "precipitation",
            "wind_speed_10m",
            "wind_direction_10m",
            "cloud_cover",
            "shortwave_radiation"
        ],
        "timezone": "UTC"
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    if "hourly" not in data:
        raise ValueError("Weather API returned no hourly data")

    df = pd.DataFrame(data["hourly"])

    df["latitude"] = latitude
    df["longitude"] = longitude
    df["elevation"] = data.get("elevation")

    output_file = RAW_DIR / "weather_raw.csv"

    df.to_csv(output_file, index=False)

    print("Weather ingestion completed!")
    print("Records:", len(df))
    print("Saved to:", output_file)


if __name__ == "__main__":

    ingest_weather_data()
