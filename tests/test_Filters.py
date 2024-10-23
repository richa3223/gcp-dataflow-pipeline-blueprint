# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

import pytest
from pytest import FixtureRequest, mark
from modules.Filters import Filters

class TestFilters:
    """Unit tests for the Filters class"""

    @pytest.mark.parametrize(
        "input_data, countries, skip_filter, expected",
        [
            (
                'sample_row_model',
                ["EST","IRL"],
                False,
                True
            ),
            (
                'sample_row_model',
                ["EST","IRL"],
                True,
                True
            )
        ]
    )

    def test_filter_by_country_matches(self, input_data, countries: list[str], skip_filter: bool, expected: bool, request: FixtureRequest):
        """Test the filter_by_country method"""
        input_data = request.getfixturevalue(input_data)
        assert Filters.filter_by_country(input_data, countries, skip_filter) == expected

    @pytest.mark.parametrize(
        "input_data, countries, skip_filter, expected",
        [
            (
                'sample_row_model',
                ["DEU","ITA"],
                False,
                False
            ),
            (
                'sample_row_model',
                ["DEU","ITA"],
                True,
                True
            )            
        ]
    )


    def test_filter_by_country_no_matches(self, input_data, countries: list[str], skip_filter: bool, expected: bool,request: FixtureRequest):
        """Test the filter_by_country method with no matches"""
        input_data = request.getfixturevalue(input_data)
        assert Filters.filter_by_country(input_data, countries, skip_filter) == expected


    @pytest.mark.parametrize(
        "input_data, countries, skip_filter, expected",
        [
            (
                'sample_row_model',
                [],
                False,
                False
            ),
            (
                'sample_row_model',
                [],
                True,
                True
            )
        ]
    )        

    def test_filter_by_country_empty_list(self, input_data, countries: list[str], skip_filter: bool, expected: bool, request: FixtureRequest):
        """Test the filter_by_country method with an empty countries list"""
        input_data = request.getfixturevalue(input_data)
        assert Filters.filter_by_country(input_data, countries, skip_filter) == expected
        
# fmt: on