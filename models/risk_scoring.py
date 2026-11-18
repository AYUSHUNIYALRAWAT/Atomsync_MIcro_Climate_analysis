
from model_utils import (
    load_csv,
    prepare_sensor_features,
    CURATED_DIR
)

def calculate_risk(row):

    score = 0

    temperature = row["avg_temperature"]
    humidity = row["avg_humidity"]

    # Temperature risk
    if temperature > 8:
        score += 50

    elif temperature < 2:
        score += 20

    # Humidity risk
    if humidity > 90:
        score += 30

    elif humidity < 60:
        score += 20

    return min(score, 100)

def classify_risk(score):

    if score >= 70:
        return "High Risk"

    elif score >= 40:
        return "Medium Risk"

    return "Low Risk"

def run_risk_scoring():

    print("Starting Risk Scoring Model...")

    sensor_df = load_csv(
        "sensor_events_processed.csv"
    )

    features = prepare_sensor_features(sensor_df)

    features["risk_score"] = features.apply(
        calculate_risk,
        axis=1
    )

    features["risk_category"] = (
        features["risk_score"].apply(classify_risk)
    )

    features["recommended_action"] = (
        features["risk_category"].map({
            "High Risk": "Immediate inspection required",
            "Medium Risk": "Monitor container conditions",
            "Low Risk": "Normal monitoring"
        })
    )

    output_file = (
        CURATED_DIR / "container_risk_scores.csv"
    )

    features.to_csv(output_file, index=False)

    print("\nRisk Scoring Completed!")

    print(features.head())

    print(f"\nSaved to: {output_file}")

if __name__ == "__main__":
    run_risk_scoring()