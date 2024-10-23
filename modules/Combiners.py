# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Transforms to return PCollections of models as look-up dictionaries
"""

__all__ = [
    "CollectionAsDecodeDict",
]

import apache_beam as beam

class CollectionAsDecodeDict(beam.CombineFn):
    """Transforms reference data PCollection into a dictionary of dictionaries"""    

    def __init__(self, key: str = None):
        beam.CombineFn.__init__(self) 
        self._key = key

    def create_accumulator(self):
        return {}

    def add_input(self, accumulator, element):
        key = element.get(self._key) if bool(self._key) else element.dict_key()
        accumulator[key] = element
        return accumulator

    def merge_accumulators(self, accumulators):
        merged = {}
        for a in accumulators:
            for k,v in a.items():
                merged[k] = v
        return merged

    def extract_output(self, accumulator):
        return accumulator
    
    def compact(self, accumulator):
        return accumulator  
    
# fmt: on