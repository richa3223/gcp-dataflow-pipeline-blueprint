# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Transforms that write data to local disk, Cloud Storage or BigQuery
"""

__all__ = [
    "LoadIntoBigQuery"
]

import apache_beam as beam
from apache_beam.io.gcp.bigquery import WriteToBigQuery, BigQueryDisposition

class LoadIntoBigQuery(beam.PTransform):
    """Composite transform to write data to BigQuery"""

    def __init__(self, project: str, dataset: str, table: str):
        beam.PTransform.__init__(self)
        self._project = project
        self._dataset = dataset
        self._table = table

    def expand(self, pcoll):
        return (
            pcoll
            | 'Write to {}.{}'.format(self._dataset, self._table)
            >> WriteToBigQuery(table=self._table,
                               dataset=self._dataset,
                               project=self._project,
                               method=WriteToBigQuery.Method.FILE_LOADS,                                                                 
                               create_disposition=BigQueryDisposition.CREATE_NEVER,
                               write_disposition=BigQueryDisposition.WRITE_APPEND
            )
        )

# fmt: on