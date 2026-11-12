
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)


def ingest_market_data(source_file):

    source_file = Path(source_file)

    if not source_file.exists():
        raise FileNotFoundError(
            f"Market data file not found: {source_file}"
        )

    df = pd.read_csv(source_file)

    if df.empty:
        raise ValueError("Market dataset is empty")

    output_file = RAW_DIR / "commodity_market_prices_raw.csv"

    df.to_csv(output_file, index=False)

    print("Market data ingestion completed!")
    print("Total records:", len(df))
    print("Saved to:", output_file)


if __name__ == "__main__":

    source = BASE_DIR / "commodity_market_prices_raw.csv"

    ingest_market_data(source)
