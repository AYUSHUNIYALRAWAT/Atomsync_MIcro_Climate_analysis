
import pandas as pd
import numpy as np
import re


def standardize_column_names(df):
    """Convert column names into lowercase snake_case."""
    df.columns = [
        re.sub(
            r"_+",
            "_",
            re.sub(r"[^a-zA-Z0-9]+", "_", str(col).strip().lower())
        ).strip("_")
        for col in df.columns
    ]
    return df


def clean_dataset(df):
    """Perform basic data cleaning."""

    df = df.copy()

    # Standardize column names
    df = standardize_column_names(df)

    # Remove duplicate records
    df = df.drop_duplicates()

    # Replace common missing-value strings
    missing_values = ["", "NA", "N/A", "NULL", "null", "None", "nan"]

    df = df.replace(missing_values, np.nan)

    # Remove unnecessary spaces from text columns
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    # Convert likely date/time columns
    for col in df.columns:
        if any(word in col for word in ["date", "time", "timestamp"]):
            converted = pd.to_datetime(df[col], errors="coerce")
            if converted.notna().any():
                df[col] = converted

    # Convert likely numeric columns
    for col in df.select_dtypes(include=["object"]).columns:
        if not any(word in col for word in ["id", "code", "zip", "postal"]):
            converted = pd.to_numeric(df[col], errors="coerce")

            original_count = df[col].notna().sum()

            if original_count > 0:
                conversion_ratio = converted.notna().sum() / original_count

                if conversion_ratio >= 0.90:
                    df[col] = converted

    return df


def clean_csv(input_path, output_path):
    """Read, clean and save a CSV dataset."""

    df = pd.read_csv(input_path)

    cleaned_df = clean_dataset(df)

    cleaned_df.to_csv(output_path, index=False)

    print(f"Cleaned successfully: {input_path}")
    print(f"Saved to: {output_path}")

    return cleaned_df
