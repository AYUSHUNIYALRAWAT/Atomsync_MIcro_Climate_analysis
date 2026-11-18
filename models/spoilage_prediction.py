
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report
)
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from model_utils import (
    load_csv,
    normalize_columns,
    prepare_sensor_features,
    CURATED_DIR,
    MODEL_DIR
)

FEATURE_COLUMNS = [
    "avg_temperature",
    "max_temperature",
    "min_temperature",
    "avg_humidity",
    "max_humidity",
    "min_humidity",
    "temperature_std",
    "humidity_std",
    "sensor_readings"
]

def prepare_target(target):

    if target.dtype == "object":

        mapping = {
            "yes": 1,
            "no": 0,
            "true": 1,
            "false": 0,
            "spoiled": 1,
            "not spoiled": 0,
            "1": 1,
            "0": 0
        }

        target = target.astype(str).str.lower().str.strip()
        target = target.map(mapping)

    else:
        target = pd.to_numeric(target, errors="coerce")

    return target

def create_model():

    model = Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median")
        ),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                random_state=42,
                class_weight="balanced"
            )
        )
    ])

    return model

def run_spoilage_prediction():

    print("Starting Spoilage Prediction Model...")

    # Load sensor data
    sensor_df = load_csv(
        "sensor_events_processed.csv"
    )

    features = prepare_sensor_features(sensor_df)

    # Load container data
    containers = normalize_columns(
        load_csv("containers_processed.csv")
    )

    # Find historical spoilage label
    target_candidates = [
        "spoilage",
        "spoiled",
        "spoilage_status",
        "is_spoiled",
        "spoilage_label"
    ]

    target_column = next(
        (
            col for col in target_candidates
            if col in containers.columns
        ),
        None
    )

    if target_column is None:
        print(
            "ERROR: No historical spoilage labels found."
        )
        print(
            "Add a labelled spoilage column before training."
        )
        return

    if "container_id" not in containers.columns:
        raise ValueError("container_id is missing.")

    # Merge sensor features and labels
    data = features.merge(
        containers[["container_id", target_column]],
        on="container_id",
        how="inner"
    )

    data[target_column] = prepare_target(
        data[target_column]
    )

    data = data.dropna(subset=[target_column])

    data[target_column] = data[target_column].astype(int)

    if not data[target_column].isin([0, 1]).all():
        raise ValueError("Labels must be 0 or 1.")

    if data[target_column].nunique() != 2:
        raise ValueError(
            "Both spoiled and not-spoiled classes are required."
        )

    if data[target_column].value_counts().min() < 2:
        raise ValueError(
            "At least two examples per class are required."
        )

    X = data[FEATURE_COLUMNS]
    y = data[target_column]

    # Training and testing split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    # Train model
    model = create_model()

    model.fit(X_train, y_train)

    # Evaluate model
    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    # Save model
    model_path = MODEL_DIR / "spoilage_model.pkl"

    joblib.dump(model, model_path)

    # Predict all containers
    all_predictions = model.predict(
        features[FEATURE_COLUMNS]
    )

    probabilities = model.predict_proba(
        features[FEATURE_COLUMNS]
    )[:, list(model.classes_).index(1)]

    results = features[["container_id"]].copy()

    results["spoilage_prediction"] = all_predictions

    results["spoilage_probability"] = probabilities

    results["prediction_status"] = (
        results["spoilage_prediction"].map({
            1: "Likely Spoilage",
            0: "Unlikely Spoilage"
        })
    )

    output_file = (
        CURATED_DIR / "spoilage_predictions.csv"
    )

    results.to_csv(output_file, index=False)

    print("\nSpoilage Prediction Completed!")

    print(results.head())

    print(f"\nModel saved: {model_path}")
    print(f"Predictions saved: {output_file}")

if __name__ == "__main__":
    run_spoilage_prediction()