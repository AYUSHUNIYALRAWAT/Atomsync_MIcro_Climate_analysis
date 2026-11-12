
import pandas as pd
from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


def ingest_sensor_data(source_file):

    source_file = Path(source_file)

    if not source_file.exists():
        raise FileNotFoundError(f"File not found: {source_file}")

    # Read Excel or CSV
    if source_file.suffix.lower() in [".xlsx", ".xls"]:
        df = pd.read_excel(source_file)
    elif source_file.suffix.lower() == ".csv":
        df = pd.read_csv(source_file)
    else:
        raise ValueError("Only CSV and Excel files are supported")

    if df.empty:
        raise ValueError("Sensor dataset is empty")

    # Save original sensor data
    sensor_path = RAW_DIR / "sensor_events_raw.csv"
    df.to_csv(sensor_path, index=False)

    print(f"Sensor data ingested: {len(df)} records")

    # Generate shipment reference data
    if "shipment_id" in df.columns:

        containers = (
            df[["shipment_id"]]
            .dropna()
            .drop_duplicates()
            .reset_index(drop=True)
        )

        containers.to_csv(
            RAW_DIR / "containers_raw.csv",
            index=False
        )

        print(f"Shipment records: {len(containers)}")

    print("Sensor ingestion completed successfully!")


if __name__ == "__main__":

    source = BASE_DIR / "ALL_benchmark_W60.xlsx"

    ingest_sensor_data(source)
