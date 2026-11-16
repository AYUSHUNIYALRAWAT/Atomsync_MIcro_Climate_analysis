
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "AtmoSync_Raw_Dataset"
OUTPUT_DIR = BASE_DIR / "reports" / "project_reports"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def rerouting_analysis():

    file_path = DATA_DIR / "market_routes_raw.csv"

    routes = pd.read_csv(file_path)

    # Keep available routes
    if "route_status" in routes.columns:
        routes["route_status"] = (
            routes["route_status"].astype(str).str.strip().str.lower()
        )

        available_routes = routes[
            routes["route_status"].isin(
                ["available", "active", "open"]
            )
        ].copy()
    else:
        available_routes = routes.copy()

    # Remove invalid route values
    available_routes = available_routes.dropna(
        subset=[
            "origin",
            "destination",
            "distance_km",
            "estimated_duration_hours",
            "transportation_cost"
        ]
    )

    # Group routes by origin and destination
    route_summary = available_routes.groupby(
        ["origin", "destination"],
        as_index=False
    ).agg(
        distance_km=("distance_km", "min"),
        estimated_duration_hours=(
            "estimated_duration_hours", "min"
        ),
        transportation_cost=("transportation_cost", "min")
    )

    # Normalize values for route ranking
    for column in [
        "distance_km",
        "estimated_duration_hours",
        "transportation_cost"
    ]:
        minimum = route_summary[column].min()
        maximum = route_summary[column].max()

        if maximum == minimum:
            route_summary[column + "_normalized"] = 0
        else:
            route_summary[column + "_normalized"] = (
                (route_summary[column] - minimum)
                / (maximum - minimum)
            )

    # Combined route score
    route_summary["route_score"] = (
        route_summary["distance_km_normalized"] * 0.30
        + route_summary["estimated_duration_hours_normalized"] * 0.30
        + route_summary["transportation_cost_normalized"] * 0.40
    )

    # Lower score indicates a better route
    route_summary = route_summary.sort_values(
        by="route_score",
        ascending=True
    )

    route_summary["route_rank"] = range(
        1, len(route_summary) + 1
    )

    route_summary.to_csv(
        OUTPUT_DIR / "rerouting_recommendations.csv",
        index=False
    )

    print("\nRerouting Analysis Completed!")

    print("\nRecommended Routes:")
    print(
        route_summary[
            [
                "origin",
                "destination",
                "distance_km",
                "estimated_duration_hours",
                "transportation_cost",
                "route_score",
                "route_rank"
            ]
        ].head(10)
    )


if __name__ == "__main__":
    rerouting_analysis()
