
import pandas as pd


def transform_dataset(df):

    df = df.copy()

    # Process datetime columns
    for col in df.select_dtypes(
        include=["datetime64[ns]", "datetimetz"]
    ).columns:

        df[f"{col}_year"] = df[col].dt.year
        df[f"{col}_month"] = df[col].dt.month
        df[f"{col}_day"] = df[col].dt.day
        df[f"{col}_hour"] = df[col].dt.hour

    # Standardize text values
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].str.strip()

    # Replace infinite values
    df = df.replace([float("inf"), float("-inf")], None)

    return df


def transform_csv(input_path, output_path):

    df = pd.read_csv(input_path)

    # Restore datetime columns
    for col in df.columns:
        if any(word in col for word in ["date", "time", "timestamp"]):
            converted = pd.to_datetime(df[col], errors="coerce")

            if converted.notna().any():
                df[col] = converted

    transformed_df = transform_dataset(df)

    transformed_df.to_csv(output_path, index=False)

    print(f"Transformation completed: {output_path}")

    return transformed_df
