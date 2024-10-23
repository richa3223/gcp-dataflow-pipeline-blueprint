# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Transforms that join PCollections to enrich with additional data 
"""

__all__ = [
    "AddProductRefData",
    "AddRegionRefData",
    "AddStoreRefData",
]

import apache_beam as beam
from modules.Mappers import Mappers
from modules.RowModels import (
    SampleRowModel
)

class AddProductRefData(beam.DoFn):
    """Joins Product reference data to row model"""

    def process(self, element: SampleRowModel, product_dict: dict):
        enriched_row: SampleRowModel = Mappers.add_product_ref_data(element, product_dict)
        yield enriched_row

class AddRegionRefData(beam.DoFn):
    """Joins Region reference data to row model"""

    def process(self, element: SampleRowModel, region_dict: dict):
        enriched_row: SampleRowModel = Mappers.add_region_ref_data(element, region_dict)
        yield enriched_row

class AddStoreRefData(beam.DoFn):
    """Joins Store reference data to row model"""

    def process(self, element: SampleRowModel, store_dict: dict):
        enriched_row: SampleRowModel = Mappers.add_store_ref_data(element, store_dict)
        yield enriched_row

# fmt: on