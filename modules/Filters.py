# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Filters module
"""

__all__ = ["Filters"]

from modules.RowModels import SampleRowModel

class Filters(object):
    """Provides filter methods for Apache Beam Transforms"""
    
    @classmethod
    def filter_by_country(cls, row: SampleRowModel, countries: list[str], skip: bool) -> bool:
        """Returns true if row matches one of specified countries"""
        if bool(skip):
            return True
        return row.country_id in countries
    
# fmt: on