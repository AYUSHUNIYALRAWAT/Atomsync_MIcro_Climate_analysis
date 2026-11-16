
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "AtmoSync_Raw_Dataset"
OUTPUT_DIR = BASE_DIR / "reports" / "project_reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "containers": "containers_raw.csv",
    "sensors": "sensor_events_raw.csv",
    "weather": "weather_raw.csv",
    "market_prices": "commodity_market_prices_raw.csv",
    "routes": "market_routes_raw.csv"
}


def load_datasets():
    datasets = {}

    for name, filename in FILES.items():
        path = DATA_DIR / filename

        if not path.exists():
            print(f"Missing file: {path}")
            continue

        datasets[name] = pd.read_csv(path)

    return datasets


def perform_eda():
    datasets = load_datasets()
    summary = []

    for name, df in datasets.items():

        print(f"\n{'=' * 50}")
        print(f"DATASET: {name.upper()}")
        print("=" * 50)

        print("\nShape:", df.shape)
        print("\nColumns:")
        print(df.columns.tolist())

        print("\nData Types:")
        print(df.dtypes)

        print("\nMissing Values:")
        print(df.isnull().sum())

        print("\nDuplicate Rows:", df.duplicated().sum())

        print("\nStatistical Summary:")
        print(df.describe(include="all").to_string())

        summary.append({
            "dataset": name,
            "rows": len(df),
            "columns": len(df.columns),
            "missing_values": int(df.isnull().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum())
        })

    report = pd.DataFrame(summary)

    report.to_csv(
        OUTPUT_DIR / "eda_summary.csv",
        index=False
    )

    print("\nEDA summary saved successfully!")


if __name__ == "__main__":
    perform_eda()
