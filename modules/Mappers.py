# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Mappers module
"""

__all__ = ["Mappers"]

from modules.Parsers import Parsers
from modules.RowModels import (
    ProductModel,
    SampleRowModel,
    StoreModel,
)

class Mappers(object):
    """Functions used in Apache Beam Map() transforms"""

    @classmethod
    def add_product_ref_data(cls, element: SampleRowModel, products: dict):
        """Adds product reference data fields using product ID as join key"""
        row = element
        product_data: ProductModel = products.get(row.product_id)
        if bool(product_data):
            row.product_name = product_data.product_name
            row.product_category = product_data.product_category
        return row
    
    @classmethod
    def add_region_ref_data(cls, element: SampleRowModel, regions: dict):
        """Adds region reference data fields using country code as join key"""
        row = element
        region_data: dict = regions.get(row.country_id)
        if bool(region_data):
            row.country = region_data.get('country_name')
            row.region = region_data.get('region')
        return row    
    
    @classmethod
    def add_store_ref_data(cls, element: SampleRowModel, stores: dict):
        """Adds store reference data fields using store ID as join key"""
        row = element
        store_data: StoreModel = stores.get(row.store_id)
        if bool(store_data):
            row.store_name = store_data.store_name
        return row
    
    @classmethod
    def decorate_customer_id(cls, row: SampleRowModel):
        """Transforms customer ID to 8 digit value"""
        d = row
        customer_id = str(int(row.customer_id) + 60000000)
        d.customer_id = customer_id
        return d

    @classmethod
    def map_to_product_row_model(cls, data) -> ProductModel:
        """Creates a ProductModel instance from ingested row data"""
        return ProductModel(
            product_id=data.get('sku'),
            product_name=data.get('description'),
            product_category=data.get('category')
        )
    
    @classmethod
    def map_to_sample_row_model(cls, data) -> SampleRowModel:
        """Creates a SampleRowModel instance from ingested row data"""
        row = SampleRowModel(
            record_date=Parsers.str_to_date(data.get('txn_date'),"%d/%m/%Y"),
            store_id=data.get('store_id'),
            product_id=data.get('sku'),
            customer_id=data.get('customer'),
            country_id=data.get('territory'),
            order_id=data.get('txn_id'),
            quantity=Parsers.str_to_int(data.get('qty')),
            value=Parsers.str_to_float(data.get('value')),
            promotion_id=data.get('promotion_code')
        )
        row.fingerprint = row.generate_fingerprint()
        return row
    
    @classmethod
    def map_to_store_row_model(cls, data) -> StoreModel:
        """Creates a StoreModel instance from ingested row data"""
        return StoreModel(
            store_id=Parsers.safe_str(data.get('store_id')),
            store_name=data.get('store_name'),
            country_id=data.get('country_code')
        )


# fmt: on

# fmt: on