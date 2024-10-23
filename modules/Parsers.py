# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Parsing utility class
"""

__all__ = ["Parsers"]

from datetime import datetime, date
import time
from time import mktime
import logging

class Parsers(object):
    """Provides a number of reusable data value parsing functions"""

    BOOL_MAP = {"TRUE": True, "FALSE": False, "YES": True, "NO": False, "Y": True, "N": False}

    @classmethod
    def safe_str(cls, str_val) -> str | None:
        """Safe handling of nullable string values"""
        return str(str_val) if bool(str_val) else None

    @classmethod
    def str_to_bool(cls, str_val) -> bool | None:
        """Decodes TRUE|True|FALSE|False string values to bool"""
        val_str = str_val.upper() if isinstance(str_val, str) else None
        return cls.BOOL_MAP.get(val_str, None)
    
    @classmethod
    def str_to_date(cls, date_str: str, fmt: str = "%d/%m/%Y") -> date | None:
        """Converts string with default format dd/mm/yyyy to date"""
        if bool(date_str):
            try:
                time_struct = time.strptime(date_str, fmt)
                return datetime.fromtimestamp(mktime(time_struct)).date()
            except ValueError as err:
                logging.info(f'Incorrect date format : {err}')
        return None
    
    @classmethod
    def str_to_float(cls, float_str: str) -> int:
        """Converts string to int with null and empty string checks"""
        try:
            if not bool(float_str):
                return 0
            return float(float_str)
        except ValueError as err:
            print(f'Parser error : {err}. Defaulting value to 0')
            return 0      
          
    @classmethod
    def str_to_int(cls, int_str: str) -> int:
        """Converts string to int with null and empty string checks"""
        try:
            if not bool(int_str):
                return 0
            return int(int_str)
        except ValueError as err:
            print(f'Parser error : {err}. Defaulting value to 0')
            return 0
        
    
# fmt: on