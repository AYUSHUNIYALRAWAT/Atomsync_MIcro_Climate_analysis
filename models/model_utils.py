
from pathlib import Path
import pandas as pd

# Main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "AtmoSync_Raw_Dataset"
PROCESSED_DIR = DATA_DIR / "processed"
CURATED_DIR = DATA_DIR / "curated"
MODEL_DIR = BASE_DIR / "models"

CURATED_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def load_csv(filename):

    file_path = PROCESSED_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    return pd.read_csv(file_path)

def normalize_columns(df):

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )

    return df

def prepare_sensor_features(sensor_df):

    sensor_df = normalize_columns(sensor_df)

    required_columns = ["container_id"]

    for col in required_columns:
        if col not in sensor_df.columns:
            raise ValueError(f"Missing column: {col}")

    temperature_col = next(
        (c for c in ["temperature", "temp", "temperature_c"]
         if c in sensor_df.columns),
        None
    )

    humidity_col = next(
        (c for c in ["humidity", "relative_humidity"]
         if c in sensor_df.columns),
        None
    )

    if temperature_col is None or humidity_col is None:
        raise ValueError(
            "Temperature and humidity columns are required."
        )

    sensor_df[temperature_col] = pd.to_numeric(
        sensor_df[temperature_col],
        errors="coerce"
    )

    sensor_df[humidity_col] = pd.to_numeric(
        sensor_df[humidity_col],
        errors="coerce"
    )

    sensor_df = sensor_df.dropna(
        subset=[
            "container_id",
            temperature_col,
            humidity_col
        ]
    )

    features = sensor_df.groupby("container_id").agg(
        avg_temperature=(temperature_col, "mean"),
        max_temperature=(temperature_col, "max"),
        min_temperature=(temperature_col, "min"),
        avg_humidity=(humidity_col, "mean"),
        max_humidity=(humidity_col, "max"),
        min_humidity=(humidity_col, "min"),
        temperature_std=(temperature_col, "std"),
        humidity_std=(humidity_col, "std"),
        sensor_readings=(temperature_col, "count")
    ).reset_index()

    return features.fillna(0)