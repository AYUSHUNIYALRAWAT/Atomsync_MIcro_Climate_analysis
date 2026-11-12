
import pandas as pd
from pathlib import Path

# ============================================
# ATMOSYNC - DATA INGESTION PIPELINE
# ============================================

# Automatically identify project root
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "AtmoSync_Raw_Dataset"

# Existing raw datasets
DATASETS = {
    "containers": "containers_raw.csv",
    "sensor_events": "sensor_events_raw.csv",
    "weather": "weather_raw.csv",
    "commodity_market_prices": "commodity_market_prices_raw.csv",
    "market_routes": "market_routes_raw.csv"
}


# ============================================
# 1. INGESTION / DATASET LOADING
# ============================================

def ingest_dataset(dataset_name, filename):

    file_path = RAW_DIR / filename

    print(f"\nProcessing: {filename}")

    if not file_path.exists():
        print("ERROR: File not found!")
        return None

    try:
        df = pd.read_csv(file_path)

        if df.empty:
            print("WARNING: Dataset is empty!")
            return None

        print("Status: Successfully loaded")
        print("Total records:", len(df))
        print("Total columns:", len(df.columns))
        print("Columns:", list(df.columns))

        return df

    except Exception as error:
        print("ERROR:", error)
        return None


# ============================================
# 2. INGEST ALL RAW DATASETS
# ============================================

def run_ingestion():

    print("\n====================================")
    print(" ATMOSYNC DATA INGESTION PIPELINE")
    print("====================================")

    datasets = {}

    for name, filename in DATASETS.items():

        df = ingest_dataset(name, filename)

        if df is not None:
            datasets[name] = df

    return datasets


# ============================================
# 3. INGESTION SUMMARY
# ============================================

def ingestion_summary(datasets):

    print("\n====================================")
    print("       INGESTION SUMMARY")
    print("====================================")

    for name, df in datasets.items():

        print(f"{name}: {len(df)} records loaded")

    missing = [
        filename
        for filename in DATASETS.values()
        if not (RAW_DIR / filename).exists()
    ]

    if missing:
        print("\nMissing datasets:")
        for filename in missing:
            print("-", filename)
    else:
        print("\nAll five raw datasets are available.")

    print("\nProject directory:", BASE_DIR)
    print("Raw data location:", RAW_DIR)


# ============================================
# 4. MAIN EXECUTION
# ============================================

def main():

    datasets = run_ingestion()

    ingestion_summary(datasets)

    print("\n====================================")
    print(" INGESTION PIPELINE COMPLETED")
    print("====================================")


if __name__ == "__main__":
    main()
