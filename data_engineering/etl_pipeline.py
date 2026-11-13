
from pathlib import Path
import pandas as pd

from .data_cleaning import clean_dataset
from .data_validation import (
    validate_dataset,
    save_validation_report
)
from .data_transformation import transform_dataset


# ==========================================
# ATMOSYNC PROJECT PATHS
# ==========================================

# Main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Raw datasets are directly inside this folder
DATASET_DIR = BASE_DIR / "AtmoSync_Raw_Dataset"

# Output directories
RAW_DIR = DATASET_DIR
PROCESSED_DIR = DATASET_DIR / "processed"
CURATED_DIR = DATASET_DIR / "curated"


# Create output directories if missing
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
CURATED_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# DATASET CONFIGURATION
# ==========================================

DATASETS = [
    "containers_raw.csv",
    "sensor_events_raw.csv",
    "weather_raw.csv",
    "commodity_market_prices_raw.csv",
    "market_routes_raw.csv"
]


# ==========================================
# MAIN ETL PIPELINE
# ==========================================

def run_etl_pipeline():

    print("\n" + "=" * 60)
    print("       ATMOSYNC DATA ENGINEERING PIPELINE")
    print("=" * 60)

    print(f"\nProject directory: {BASE_DIR}")
    print(f"Dataset directory: {DATASET_DIR}")

    validation_results = []

    for filename in DATASETS:

        print("\n" + "-" * 60)
        print(f"Processing: {filename}")
        print("-" * 60)

        raw_path = RAW_DIR / filename

        processed_name = filename.replace(
            "_raw.csv", "_processed.csv"
        )

        curated_name = filename.replace(
            "_raw.csv", "_curated.csv"
        )

        processed_path = PROCESSED_DIR / processed_name
        curated_path = CURATED_DIR / curated_name

        try:

            # STEP 1: CHECK RAW FILE
            if not raw_path.exists():
                raise FileNotFoundError(
                    f"File not found: {raw_path}"
                )

            # STEP 2: LOAD RAW DATA
            raw_df = pd.read_csv(raw_path)

            print("Raw data loaded successfully")
            print("Shape:", raw_df.shape)

            # STEP 3: CLEAN DATA
            cleaned_df = clean_dataset(raw_df)

            cleaned_df.to_csv(
                processed_path,
                index=False
            )

            print("Data cleaning completed")
            print("Processed shape:", cleaned_df.shape)

            # STEP 4: VALIDATE DATA
            validation = validate_dataset(
                cleaned_df,
                filename
            )

            validation_results.append(validation)

            if validation["status"] == "FAILED":

                print("Validation failed.")
                print("Skipping transformation.")

                continue

            # STEP 5: TRANSFORM DATA
            transformed_df = transform_dataset(
                cleaned_df
            )

            transformed_df.to_csv(
                curated_path,
                index=False
            )

            print("Data transformation completed")

            # STEP 6: DISPLAY OUTPUT
            print("\nGenerated files:")
            print("Processed:", processed_path)
            print("Curated:", curated_path)

            print("\nDataset processing successful!")

        except Exception as error:

            print(f"\nERROR: {error}")

            validation_results.append({
                "dataset": filename,
                "rows": 0,
                "columns": 0,
                "duplicates": 0,
                "missing_cells": 0,
                "status": "FAILED",
                "errors": [str(error)],
                "warnings": []
            })

    # ======================================
    # STEP 7: SAVE VALIDATION REPORT
    # ======================================

    report_path = CURATED_DIR / "validation_report.csv"

    save_validation_report(
        validation_results,
        report_path
    )

    # ======================================
    # STEP 8: PIPELINE SUMMARY
    # ======================================

    successful = sum(
        result["status"] == "PASSED"
        for result in validation_results
    )

    failed = len(validation_results) - successful

    print("\n" + "=" * 60)
    print("             ATMOSYNC ETL SUMMARY")
    print("=" * 60)

    print(f"Total datasets: {len(DATASETS)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    print("\nValidation report:", report_path)

    print("\nETL PIPELINE EXECUTION COMPLETED")
    print("=" * 60)


# ==========================================
# EXECUTION
# ==========================================

if __name__ == "__main__":
    run_etl_pipeline()
