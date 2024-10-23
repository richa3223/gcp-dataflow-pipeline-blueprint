# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Serializes a CSV file to Parquet binary format
"""

from modules.Converters import (
    ParquetSerializer
)

def csv_to_parquet(csv_file_path, parquet_file_path):
    """Loads CSV file and serializes content to Parquet binary file"""

    serializer = ParquetSerializer(
        csv_file_path,
        parquet_file_path
    )

    serializer.csv_to_parquet()


if __name__ == "__main__":
    csv_file_path = "./sample-input-data/parquet_data.csv"
    parquet_file_path = "./sample-input-data/parquet/sample_parquet_data.parquet"

    csv_to_parquet(csv_file_path, parquet_file_path)

# fmt: on