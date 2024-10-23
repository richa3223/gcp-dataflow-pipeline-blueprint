# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
BigQuery utility class
"""

__all__ = ["BigQueryUtils"]

from datetime import datetime, timezone
import uuid
from modules.Names import Names

class BigQueryUtils(object):
    """BigQuery utility class"""

    @classmethod
    def utc_ts(cls) -> datetime:
        """UTC datetime"""
        return datetime.now(timezone.utc)
    
    @classmethod
    def correlation_id(cls) -> str:
        """Generates a UUID4 string value"""
        return uuid.uuid4().hex
    
    @classmethod
    def metadata_fields(cls) -> dict:
        """Generates a common set of metadata fields for each table"""
        timestamp = cls.utc_ts()
        return {
            Names.UTC_TS: timestamp,
            Names.CORRELATION_ID: cls.correlation_id(),
            Names.RECORD_STATUS: Names.RECORD_STATUS_ACTIVE,
            Names.VALID_FROM: timestamp.replace(second=0,microsecond=0)
        }   
    
# fmt: on