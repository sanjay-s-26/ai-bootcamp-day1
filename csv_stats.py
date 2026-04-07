"""CSV summary statistics using Python standard library only."""

import csv
import math
import os
from typing import Dict

# demio purpose
def get_csv_summary(filepath: str, population_std: bool = False) -> Dict[str, Dict[str, float]]:
    """
    Read a CSV file and return summary statistics for all numeric columns.

    Parameters
    ----------
    filepath : str
        Path to the CSV file to analyse.
    population_std : bool, optional
        Controls how ``std_dev`` is computed from the squared deviations
        about the column mean. Let *N* be the number of numeric values in
        the column.

        * ``False`` (default): **sample** standard deviation — variance uses
          divisor *N* - 1 (Bessel's correction). Use when the rows are a
          sample and you want an unbiased estimate of population spread.
        * ``True``: **population** standard deviation — variance uses divisor
          *N*. Use when the rows are the full population (or you explicitly
          want the population formula on those values).

        For a column with only one row, sample mode would divide by zero, so
        variance and ``std_dev`` are set to ``0.0`` in that case.

    Returns
    -------
    dict
        Mapping of column name -> statistics dict with keys:
        ``count``, ``mean``, ``median``, ``min``, ``max``, ``std_dev``.
        ``mean`` and ``std_dev`` are rounded to 2 decimal places.
        The ``std_dev`` value follows *population_std* (population vs sample
        formula as described above).

    Raises
    ------
    FileNotFoundError
        If *filepath* does not point to an existing file.
    ValueError
        If the CSV file is empty (no header row or no data rows).

    Notes
    -----
    Non-numeric columns are silently skipped.
    Only the Python standard library is used (``csv``, ``math``, ``os``).

    Examples
    --------
    >>> summary = get_csv_summary("sample_sales.csv")
    >>> summary["units_sold"]["mean"]
    148.3
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    with open(filepath, newline="", encoding="utf-8") as file_handle:
        csv_reader = csv.DictReader(file_handle)

        if csv_reader.fieldnames is None:
            raise ValueError(f"CSV file is empty: {filepath}")

        columns: Dict[str, list] = {field_name: [] for field_name in csv_reader.fieldnames}

        row_count = 0
        for row in csv_reader:
            row_count += 1
            for field_name in csv_reader.fieldnames:
                columns[field_name].append(row[field_name])

    if row_count == 0:
        raise ValueError(f"CSV file has no data rows: {filepath}")

    result: Dict[str, Dict[str, float]] = {}

    for column_name, raw_values_list in columns.items():
        # Attempt to parse every value as float; skip the column on any failure.
        numeric_values: list[float] = []
        is_numeric_column = True
        for raw_value in raw_values_list:
            try:
                numeric_values.append(float(raw_value))
            except (ValueError, TypeError):
                is_numeric_column = False
                break

        if not is_numeric_column or not numeric_values:
            continue

        value_count = len(numeric_values)
        total_sum = sum(numeric_values)
        mean_value = total_sum / value_count

        sorted_numeric_values = sorted(numeric_values)
        middle_index = value_count // 2
        median_value = (
            sorted_numeric_values[middle_index]
            if value_count % 2 == 1
            else (sorted_numeric_values[middle_index - 1] + sorted_numeric_values[middle_index]) / 2
        )

        variance_divisor = value_count if population_std else value_count - 1
        variance = (
            sum((value - mean_value) ** 2 for value in numeric_values) / variance_divisor
            if variance_divisor > 0
            else 0.0
        )
        std_deviation = math.sqrt(variance)

        result[column_name] = {
            "count": value_count,
            "mean": round(mean_value, 2),
            "median": median_value,
            "min": min(numeric_values),
            "max": max(numeric_values),
            "std_dev": round(std_deviation, 2),
        }

    return result


def main() -> None:
    """Load sample_sales.csv and print formatted summary statistics."""
    filepath = "sample_sales.csv"
    summary_statistics = get_csv_summary(filepath)

    print(f"CSV Summary — {filepath}\n{'=' * 60}")

    statistic_labels = {
        "count": "Count",
        "mean": "Mean",
        "median": "Median",
        "min": "Min",
        "max": "Max",
        "std_dev": "Std Dev (sample)",
    }

    for column_name, column_stats in summary_statistics.items():
        print(f"\n{column_name}")
        print("-" * 30)
        for statistic_key, label in statistic_labels.items():
            statistic_value = column_stats[statistic_key]
            # Show integers without a decimal point for cleanliness.
            formatted_value = int(statistic_value) if statistic_value == int(statistic_value) else statistic_value
            print(f"  {label:<18} {formatted_value}")


if __name__ == "__main__":
    main()
