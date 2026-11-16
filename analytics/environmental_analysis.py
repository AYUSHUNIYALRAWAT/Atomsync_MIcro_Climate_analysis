
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "AtmoSync_Raw_Dataset"
OUTPUT_DIR = BASE_DIR / "reports" / "project_reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def environmental_analysis():

    sensor_file = DATA_DIR / "sensor_events_raw.csv"
    weather_file = DATA_DIR / "weather_raw.csv"

    sensors = pd.read_csv(sensor_file)
    weather = pd.read_csv(weather_file)

    # Convert timestamp columns
    sensors["event_timestamp"] = pd.to_datetime(
        sensors["event_timestamp"], errors="coerce"
    )

    weather["observation_time"] = pd.to_datetime(
        weather["observation_time"], errors="coerce"
    )

    # Sensor environmental analysis
    sensor_summary = sensors.groupby("container_id").agg(
        average_temperature=("temperature", "mean"),
        maximum_temperature=("temperature", "max"),
        minimum_temperature=("temperature", "min"),
        average_humidity=("humidity", "mean"),
        maximum_humidity=("humidity", "max")
    ).reset_index()

    # Environmental threshold detection
    sensor_summary["high_temperature"] = (
        sensor_summary["maximum_temperature"] > 8
    )

    sensor_summary["high_humidity"] = (
        sensor_summary["maximum_humidity"] > 80
    )

    sensor_summary["environment_status"] = "Normal"

    sensor_summary.loc[
        sensor_summary["high_temperature"] |
        sensor_summary["high_humidity"],
        "environment_status"
    ] = "Warning"

    # Weather analysis by location
    weather_summary = weather.groupby("location").agg(
        average_temperature=("temperature", "mean"),
        maximum_temperature=("temperature", "max"),
        average_humidity=("humidity", "mean"),
        average_rainfall=("rainfall", "mean"),
        average_wind_speed=("wind_speed", "mean")
    ).reset_index()

    sensor_summary.to_csv(
        OUTPUT_DIR / "environmental_sensor_analysis.csv",
        index=False
    )

    weather_summary.to_csv(
        OUTPUT_DIR / "weather_location_analysis.csv",
        index=False
    )

    print("Environmental analysis completed!")
    print(sensor_summary.head())
    print(weather_summary.head())


if __name__ == "__main__":
    environmental_analysis()
