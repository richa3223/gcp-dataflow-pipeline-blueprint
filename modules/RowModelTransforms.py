# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Transforms that map ingested data rows to custom row models
"""

__all__ = [
    "DecorateCustomerId",
    "MapToProductModel",
    "MapToSampleRowModel",
    "MapToStoreModel",
    "SampleRowModelToDict",
]

import apache_beam as beam
from modules.RowModels import (
    PipelineError,
    SampleRowModel,
)
from modules.Mappers import Mappers
from modules.Names import Names

class DecorateCustomerId(beam.DoFn):
    """Applies mapper transform to SampleRowModel instance"""

    def process(self, element, *args, **kwargs):
        try:
            row: SampleRowModel = element
            yield Mappers.decorate_customer_id(row)
        except Exception as err:
            error = PipelineError(
                pipeline_step='DecorateCustomerId',
                input_element=element,
                exception=err
            )
            yield beam.pvalue.TaggedOutput(Names.PARSE_ERRORS, error)     

class MapToProductModel(beam.DoFn):
    """Transforms ingested data row to custom data model"""
    
    def process(self, element, *args, **kwargs):
        try:
            data: dict = element
            yield Mappers.map_to_product_row_model(data)
        except Exception as err:
            error = PipelineError(
                pipeline_step='MapToProductModel',
                input_element=element,
                exception=err
            )
            yield beam.pvalue.TaggedOutput(Names.PARSE_ERRORS, error) 

class MapToRowModel(beam.DoFn):
    """Transforms ingested data row to custom data model"""

    def __init__(self, mapper: str, step_label: str):
        beam.DoFn.__init__(self)
        self._mapper = mapper
        self._label = step_label

    def process(self, element, *args, **kwargs):
        try:
            data: dict = element
            yield self._mapper(data)
        except Exception as err:
            error = PipelineError(
                pipeline_step=self._label,
                input_element=element,
                exception=err
            )
            yield beam.pvalue.TaggedOutput(Names.PARSE_ERRORS, error)

class MapToSampleRowModel(beam.DoFn):
    """Transforms ingested data row to custom data model"""
    
    def process(self, element, *args, **kwargs):
        try:
            data: dict = element
            yield Mappers.map_to_sample_row_model(data)
        except Exception as err:
            error = PipelineError(
                pipeline_step='MapToSampleRowModel',
                input_element=element,
                exception=err
            )
            yield beam.pvalue.TaggedOutput(Names.PARSE_ERRORS, error)

class MapToStoreModel(beam.PTransform):
    """Transforms ingested data row to Store custom data model"""

    def expand(self, pcoll):
        return (
            pcoll
            | 'Stores to Model'
            >> beam.ParDo(
                MapToRowModel(Mappers.map_to_store_row_model, 'MapToStoreModel')
            ).with_outputs(Names.PARSE_ERRORS, main="outputs")
        )

class SampleRowModelToDict(beam.DoFn):
    """Transforms SampleRowModel to python dictionary"""

    def __init__(self, metadata: dict):
        beam.DoFn.__init__(self)
        self._metadata = metadata

    def process(self, element, *args, **kwargs):
        try:
            row: SampleRowModel = element
            yield row.bigquery_dict(self._metadata)
        except Exception as err:
            error = PipelineError(
                pipeline_step='SampleRowModelToDict',
                input_element=element,
                exception=err
            )
            yield beam.pvalue.TaggedOutput(Names.PARSE_ERRORS, error)  
# fmt: on