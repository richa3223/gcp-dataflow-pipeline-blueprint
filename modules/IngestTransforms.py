# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Transforms that ingest data as Apache Beam PCollections
"""

__all__ = [
    "AvroIngest",
    "BigQueryDataIngest",
    "CsvIngest",
    "FetchFromBigQuery",
    "ParquetIngest",
]

import apache_beam as beam
from apache_beam.io.gcp.bigquery import ReadFromBigQuery
from apache_beam.io.gcp.internal.clients import bigquery
from apache_beam.io import Read
from apache_beam.io.avroio import ReadFromAvro
from apache_beam.io.parquetio import ReadFromParquet
from modules.BeamUtils import CsvFileSource
from modules.Names import Names

class CsvIngest(beam.PTransform):
    """Reads CSV data and optionally transforms to custom model"""

    def __init__(self, csv_file: str, label: str):
        beam.PTransform().__init__(self)
        self._csv_file = csv_file
        self._label = label

    def expand(self, pcoll):
        return (
            pcoll
            | 'Read {} CSV'.format(self._label)
            >> Read(CsvFileSource(self._csv_file, splittable=False))
        )

class AvroIngest(beam.PTransform):
    """Reads AVRO data and optionally transforms to custom model"""

    def __init__(self, avro_file: str, label: str):
        beam.PTransform().__init__(self)
        self._avro_file = avro_file
        self._label = label

    def expand(self, pcoll):
        return (
            pcoll
            | 'Read {} AVRO'.format(self._label)
            >> ReadFromAvro(
                self._avro_file,
                as_rows=False
            )
        )

class ParquetIngest(beam.PTransform):
    """Reads Parquet data and optionally transforms to custom model"""

    def __init__(self, parquet_file: str, label: str):
        beam.PTransform().__init__(self)
        self._parquet_file = parquet_file
        self._label = label

    def expand(self, pcoll):
        return (
            pcoll
            | 'Read {} Parquet'.format(self._label)
            >> ReadFromParquet(
                self._parquet_file,
                as_rows=False
            )
        )

# Composite transform to read data from BigQuery using export job method
class FetchFromBigQuery(beam.PTransform):
    """Reads data from BigQuery"""

    def __init__(self, project: str, dataset: str,query: str, label: str):
        beam.PTransform().__init__(self)
        self._project = project
        self._dataset = dataset
        self._query = query
        self._label = label

    def expand(self, pcoll):
        return (
            pcoll
            | 'Read {} from BQ'.format(self._label) 
            >> ReadFromBigQuery(
                query=self._query,
                use_standard_sql=True,
                method='EXPORT',
                temp_dataset=bigquery.DatasetReference(projectId=self._project, datasetId=self._dataset)
            )
        )
    
# Composite transform for BigQuery data ingest and mapping to custom row models
class BigQueryDataIngest(beam.PTransform):
    """Fetches data from BigQuery and transforms to custom row model"""

    def __init__(self, project: str, dataset: str, query: str, label: str, mapper: beam.DoFn):
        beam.PTransform().__init__(self)
        self._project = project
        self._dataset = dataset
        self._query = query
        self._label = label
        self._mapper = mapper

    def expand(self, pcoll):
        return (
            pcoll
            | 'Read {}'.format(self._label)
            >> FetchFromBigQuery(self._project, self._dataset, self._query, self._label)
            | '{} model'.format(self._label)
            >> beam.ParDo(self._mapper).with_outputs(Names.PARSE_ERRORS, main='outputs')
        )

# fmt: on