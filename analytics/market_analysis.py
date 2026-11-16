
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "AtmoSync_Raw_Dataset"
OUTPUT_DIR = BASE_DIR / "reports" / "project_reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def market_analysis():

    file_path = DATA_DIR / "commodity_market_prices_raw.csv"

    market = pd.read_csv(file_path)

    market["price_timestamp"] = pd.to_datetime(
        market["price_timestamp"],
        errors="coerce"
    )

    # Average price by commodity and market
    market_summary = market.groupby(
        ["commodity_name", "market_name", "market_location"],
        as_index=False
    ).agg(
        average_price=("price", "mean"),
        minimum_price=("price", "min"),
        maximum_price=("price", "max")
    )

    # Cheapest market for each commodity
    cheapest_market = market_summary.loc[
        market_summary.groupby("commodity_name")[
            "average_price"
        ].idxmin()
    ]

    # Most expensive market for each commodity
    expensive_market = market_summary.loc[
        market_summary.groupby("commodity_name")[
            "average_price"
        ].idxmax()
    ]

    # Compare cheapest and most expensive markets
    comparison = cheapest_market.merge(
        expensive_market,
        on="commodity_name",
        suffixes=("_cheapest", "_expensive")
    )

    comparison["price_difference"] = (
        comparison["average_price_expensive"]
        - comparison["average_price_cheapest"]
    )

    comparison["price_difference_percentage"] = (
        comparison["price_difference"]
        / comparison["average_price_cheapest"].replace(0, pd.NA)
    ) * 100

    # Save reports
    market_summary.to_csv(
        OUTPUT_DIR / "market_price_summary.csv",
        index=False
    )

    cheapest_market.to_csv(
        OUTPUT_DIR / "cheapest_markets.csv",
        index=False
    )

    comparison.to_csv(
        OUTPUT_DIR / "market_price_comparison.csv",
        index=False
    )

    print("\nMarket Analysis Completed!")

    print("\nCheapest Markets:")
    print(cheapest_market)

    print("\nMarket Price Differences:")
    print(comparison)


if __name__ == "__main__":
    market_analysis()
