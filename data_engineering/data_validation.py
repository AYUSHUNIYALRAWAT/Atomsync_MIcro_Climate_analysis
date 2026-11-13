
import pandas as pd


def validate_dataset(df, dataset_name="Dataset"):

    print("\n" + "=" * 50)
    print(f"VALIDATING: {dataset_name}")
    print("=" * 50)

    errors = []
    warnings = []

    # Check empty dataset
    if df.empty:
        errors.append("Dataset is empty")

    # Check duplicate records
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        warnings.append(
            f"{duplicate_count} duplicate records found"
        )

    # Check missing values
    missing_values = df.isnull().sum()

    for column, count in missing_values.items():
        if count > 0:
            percentage = (count / len(df)) * 100 if len(df) else 0

            warnings.append(
                f"{column}: {count} missing values ({percentage:.2f}%)"
            )

    # Check duplicate column names
    if not df.columns.is_unique:
        errors.append("Duplicate column names found")

    # Display results
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Duplicate records: {duplicate_count}")

    print("\nData Types:")
    print(df.dtypes)

    if errors:
        print("\nVALIDATION ERRORS:")
        for error in errors:
            print("-", error)

    if warnings:
        print("\nVALIDATION WARNINGS:")
        for warning in warnings:
            print("-", warning)

    if not errors and not warnings:
        print("\nDataset passed validation.")

    return {
        "dataset": dataset_name,
        "rows": len(df),
        "columns": len(df.columns),
        "duplicates": int(duplicate_count),
        "missing_cells": int(df.isnull().sum().sum()),
        "status": "FAILED" if errors else "PASSED",
        "errors": errors,
        "warnings": warnings
    }


def save_validation_report(results, output_path):

    report = []

    for result in results:
        report.append({
            "dataset": result["dataset"],
            "rows": result["rows"],
            "columns": result["columns"],
            "duplicates": result["duplicates"],
            "missing_cells": result["missing_cells"],
            "status": result["status"],
            "errors": "; ".join(result["errors"]),
            "warnings": "; ".join(result["warnings"])
        })

    pd.DataFrame(report).to_csv(output_path, index=False)

    print(f"\nValidation report saved: {output_path}")
