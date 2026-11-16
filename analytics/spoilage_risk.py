
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "AtmoSync_Raw_Dataset"
OUTPUT_DIR = BASE_DIR / "reports" / "project_reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def calculate_spoilage_risk():

    sensor_file = DATA_DIR / "sensor_events_raw.csv"
    container_file = DATA_DIR / "containers_raw.csv"

    sensors = pd.read_csv(sensor_file)
    containers = pd.read_csv(container_file)

    # Aggregate sensor readings for each container
    risk_data = sensors.groupby("container_id").agg(
        average_temperature=("temperature", "mean"),
        maximum_temperature=("temperature", "max"),
        average_humidity=("humidity", "mean"),
        maximum_humidity=("humidity", "max"),
        reading_count=("event_id", "count")
    ).reset_index()

    # Merge with container information
    risk_data = risk_data.merge(
        containers,
        on="container_id",
        how="left"
    )

    # Temperature risk score (0-50)
    risk_data["temperature_score"] = (
        (risk_data["maximum_temperature"] - 8)
        .clip(lower=0, upper=10) * 5
    )

    # Humidity risk score (0-30)
    risk_data["humidity_score"] = (
        (risk_data["maximum_humidity"] - 80)
        .clip(lower=0, upper=20) * 1.5
    )

    # Average temperature risk (0-20)
    risk_data["average_temp_score"] = (
        (risk_data["average_temperature"] - 5)
        .clip(lower=0, upper=10) * 2
    )

    # Overall spoilage risk
    risk_data["spoilage_risk_score"] = (
        risk_data["temperature_score"]
        + risk_data["humidity_score"]
        + risk_data["average_temp_score"]
    ).clip(0, 100)

    # Risk classification
    def classify_risk(score):

        if score <= 30:
            return "Low"

        elif score <= 60:
            return "Medium"

        return "High"

    risk_data["risk_category"] = (
        risk_data["spoilage_risk_score"].apply(classify_risk)
    )

    # Sort by highest risk
    risk_data = risk_data.sort_values(
        by="spoilage_risk_score",
        ascending=False
    )

    risk_data.to_csv(
        OUTPUT_DIR / "container_spoilage_risk.csv",
        index=False
    )

    print("\nSpoilage Risk Analysis Completed!")
    print(
        risk_data[
            ["container_id", "spoilage_risk_score", "risk_category"]
        ].head(10)
    )

    print("\nRisk Distribution:")
    print(risk_data["risk_category"].value_counts())


if __name__ == "__main__":
    calculate_spoilage_risk()
