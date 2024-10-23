# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

import pytest
from pytest import FixtureRequest, mark
from modules.Mappers import Mappers
from modules.RowModels import StoreModel

class TestMappers:
    """Unit tests for the Mappers class"""

    @pytest.mark.parametrize(
            "input_data, expected",
            [
                (
                    'sample_row_model_dict',
                    'sample_row_model'
                ),
                (
                    'sample_row_model_with_promotion_dict',
                    'sample_row_model_with_promotion'
                )
            ]
    )

    def test_map_to_sample_row_model(self, input_data, expected, request: FixtureRequest):
        """Test the map_to_sample_row_model method"""
        input_data = request.getfixturevalue(input_data)
        expected = request.getfixturevalue(expected)
        assert Mappers.map_to_sample_row_model(input_data) == expected


    @pytest.mark.parametrize(
            "input_data, region_data, expected",
            [
                (
                    'sample_row_model',
                    {'EST': {'country_code': 'EST', 'country_name': 'Estonia', 'region': 'Baltic States'}},
                    'sample_row_model_with_region'
                )
            ]
    )

    def test_add_region_ref_data(self, input_data, region_data, expected, request: FixtureRequest):
        """Test the add_region_ref_data mapper method"""
        input_data = request.getfixturevalue(input_data)
        expected = request.getfixturevalue(expected)
        assert Mappers.add_region_ref_data(input_data, region_data) == expected        

    @pytest.mark.parametrize(
            "input_data, store_data, expected",
            [
                (
                    'sample_row_model',
                    {'282704': StoreModel(store_id='282704', store_name='Rimi Tallinn', country_id='EST')},
                    'sample_row_model_with_store'
                ),
                (
                    'sample_row_model',
                    {'999999': StoreModel(store_id='999999', store_name='Dummy Store', country_id='AUT')},
                    'sample_row_model'                    
                )
            ]
    )

    def test_add_store_ref_data(self, input_data, store_data, expected, request: FixtureRequest):
        """Test the add_store_ref_data mapper method"""
        input_data = request.getfixturevalue(input_data)
        expected = request.getfixturevalue(expected)
        assert Mappers.add_store_ref_data(input_data, store_data) == expected       


    @pytest.mark.parametrize(
        "input_data, expected",
        [
            (
                'sample_row_model',
                'sample_row_model_decorated_order_id'
            )
        ]
    )     

    def test_decorate_customer_id(self, input_data, expected, request: FixtureRequest):
        """Test the decorate_customer_id mapper method"""
        input_data = request.getfixturevalue(input_data)
        expected = request.getfixturevalue(expected)
        assert Mappers.decorate_customer_id(input_data) == expected        
    
# fmt: on