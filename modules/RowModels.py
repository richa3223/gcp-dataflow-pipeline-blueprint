# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Provides custom row models for ingested data
"""

__all__ = [
    "PipelineError",
    "ProductModel",
    "SampleRowModel", 
    "StoreModel",
]

from dataclasses import dataclass, asdict
from datetime import date
import hashlib

def safe_default(value, default: int = 0):
    return value if bool(value) == True else default

# Common parsing error class used with all ingest datasets
@dataclass
class PipelineError:
    pipeline_step: str
    input_element: dict
    exception: str

# Schema for sample product reference data side input type
@dataclass
class ProductModel:
    product_id: str
    product_name: str
    product_category: str

    def dict_key(self):
        return self.product_id
    
# Schema for sample ingest dataset
@dataclass
class SampleRowModel:
    record_date: date
    store_id: str
    product_id : str
    customer_id: str
    country_id: str
    order_id: str
    quantity: int
    value: float
    promotion_id: str | None = None
    country: str | None = None
    region: str | None = None
    product_name: str | None = None
    product_category: str | None = None
    store_name: str | None = None
    fingerprint: str | None = None

    def bigquery_dict(self, metadata_fields: dict) -> dict:
        d = asdict(self)
        metadata_fields.update(d)
        return metadata_fields
    
    def generate_fingerprint(self) -> str:
        """Returns SHA256 hash hex digest fingerprint string"""
        hash_input = (
            f'{self.order_id}'
            f'{self.store_id}'
            f'{self.product_id}'
            f'{self.customer_id}'
            f'{self.country_id}'
            f'{self.promotion_id}'
        )
        return hashlib.sha256(hash_input.encode('utf-8')).hexdigest()
    
# Schema for sample reference data side input type
@dataclass
class StoreModel:
    store_id: str
    store_name: str
    country_id: str

    def dict_key(self):
        return self.store_id
    
# fmt: on