# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

import pytest
from pytest import fixture
from datetime import date
from modules.RowModels import SampleRowModel

"""Defines reusable fixtures for unit tests"""

@pytest.fixture
def sample_row_model():
    return SampleRowModel(
        record_date=date(2023, 2, 15),
        store_id='282704',
        product_id='h5ORkG7X',
        customer_id='670550',
        country_id='EST',
        order_id='xgJ9qVo8',
        quantity=20,
        value=629.99,
        promotion_id=None,
        fingerprint='d29eb28684d2f9d843a8343ac0830c426fac730c5c98a2c4b000fe39baecc7f2'
    )

@pytest.fixture
def sample_row_model_with_region():
    return SampleRowModel(
        record_date=date(2023, 2, 15),
        store_id='282704',
        product_id='h5ORkG7X',
        customer_id='670550',
        country_id='EST',
        order_id='xgJ9qVo8',
        quantity=20,
        value=629.99,
        promotion_id=None,
        country='Estonia',
        region='Baltic States',
        fingerprint='d29eb28684d2f9d843a8343ac0830c426fac730c5c98a2c4b000fe39baecc7f2'
    )

@pytest.fixture
def sample_row_model_with_store():
    return SampleRowModel(
        record_date=date(2023, 2, 15),
        store_id='282704',
        product_id='h5ORkG7X',
        customer_id='670550',
        country_id='EST',
        order_id='xgJ9qVo8',
        quantity=20,
        value=629.99,
        promotion_id=None,
        store_name='Rimi Tallinn',
        fingerprint='d29eb28684d2f9d843a8343ac0830c426fac730c5c98a2c4b000fe39baecc7f2'
    )

@pytest.fixture
def sample_row_model_decorated_order_id():
    return SampleRowModel(
        record_date=date(2023, 2, 15),
        store_id='282704',
        product_id='h5ORkG7X',
        customer_id='60670550',
        country_id='EST',
        order_id='xgJ9qVo8',
        quantity=20,
        value=629.99,
        promotion_id=None,
        fingerprint='d29eb28684d2f9d843a8343ac0830c426fac730c5c98a2c4b000fe39baecc7f2'
    )

@pytest.fixture
def sample_row_model_with_promotion():
    return SampleRowModel(
        record_date=date(2023, 11, 20),
        store_id='355677',
        product_id='Vqbbu572',
        customer_id='239827',
        country_id='ITA',
        order_id='dQknbEKq',
        quantity=6,
        value=72.00,
        promotion_id='FLASH50',
        fingerprint='12b59850b5d2259179cdd52f0f880e6cec8387c958c69e6de1557c00bcafa774'
    )

@pytest.fixture
def sample_row_model_dict():
    return {
        'txn_date': '15/02/2023',
        'store_id': '282704',   
        'sku': 'h5ORkG7X',
        'customer': '670550',
        'territory': 'EST',
        'txn_id': 'xgJ9qVo8',
        'qty': '20',
        'value': '629.99',
        'promotion_code': None
    }

@pytest.fixture
def sample_row_model_with_promotion_dict():
    return {
        'txn_date': '20/11/2023',
        'store_id': '355677',   
        'sku': 'Vqbbu572',
        'customer': '239827',
        'territory': 'ITA',
        'txn_id': 'dQknbEKq',
        'qty': '6',
        'value': '72.00',
        'promotion_code': 'FLASH50'
    }

# fmt: on