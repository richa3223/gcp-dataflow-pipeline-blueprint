# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Classes to serialize CSV file input as binary AVRO or Parquet files
"""

__all__ = [
    "AvroSerializer",
    "ParquetSerializer",
]

import csv
import fastavro
import pyarrow.csv as pa
import pyarrow.parquet as pq
import logging

class AvroSerializer(object):

    def __init__(self, csv_file_path: str, avro_file_path: str, avro_schema: str):
        self._csv_file_path = csv_file_path
        self._avro_file_path = avro_file_path
        self._avro_schema = avro_schema

    def get_avro_schema(self):
        """Read and parse AVRO schema file"""
        try:
            schema = fastavro.schema.load_schema(self._avro_schema)
            parsed_schema = fastavro.parse_schema(schema)
            return parsed_schema
        except Exception as ex:
            logging.error(f'Error parsing schema {self._avro_schema} : {ex}')

    def csv_to_avro(self):
        """Read CSV file and serialize to AVRO file"""
        try:
            avro_schema = self.get_avro_schema()
            with open(self._csv_file_path, encoding='utf-8', mode='r') as f:
                csv_reader = csv.DictReader(f)  
                with open(self._avro_file_path, mode='a+b') as avro_file:
                    for row in csv_reader:
                        fastavro.writer(
                            avro_file,
                            schema=avro_schema,
                            records=[row]
                        )
        except Exception as ex:
            logging.error(f'Error converting to AVRO: {ex}')


class ParquetSerializer(object):

    def __init__(self, csv_file_path: str, parquet_file_path: str):
        self._csv_file_path = csv_file_path
        self._parquet_file_path = parquet_file_path

    def csv_to_parquet(self):
        """Read CSV file and serialize to Parquet file"""

        try:
            table = pa.read_csv(self._csv_file_path)
            pq.write_table(table, self._parquet_file_path)
        except Exception as ex:
            logging.error(f'Error converting to Parquet: {ex}')

# fmt: on