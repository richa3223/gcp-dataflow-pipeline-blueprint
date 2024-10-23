# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Serializes a CSV file to AVRO binary format using a provided AVRO JSON schema
"""

from modules.Converters import (
    AvroSerializer
)

def csv_to_avro(csv_file_path, avro_file_path, avro_schema):
    """Loads CSV file and serializes content to AVRO binary file using schema"""

    converter = AvroSerializer(
        csv_file_path,
        avro_file_path,
        avro_schema
    )

    converter.csv_to_avro()

if __name__ == "__main__":
    csv_file_path = "./sample-input-data/avro_data.csv"
    avro_file_path = "./sample-input-data/avro/sample_avro_data.avro"
    avro_schema = "./sample-input-data/avro/sample_avro.avsc"

    csv_to_avro(csv_file_path, avro_file_path, avro_schema)

