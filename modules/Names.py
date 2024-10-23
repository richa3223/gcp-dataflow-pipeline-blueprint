# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Defines constants to support data parsing and dataset management
"""

__all__ = ["Names"]

class Names(object):
    """Defines constants for parsing and dataset management"""

    # Pipeline options argument names
    GCP_PROJ_KEY = 'project'
    GCP_REGION_KEY = 'region'

    # Row data parsing tags
    PARSE_ERRORS = 'parse_errors'

    # Filter keys
    COUNTRY_UK = 'GBR'
    COUNTRY_IRELAND = 'IRL'

    # BigQuery destination table
    BQ_DATASET = 'df_blueprint_internal'
    BQ_TABLE = 'df_processed_data'

    # Common metadata fields for BigQuery tables
    UTC_TS = 'created_ts'
    VALID_FROM = 'valid_from'
    CORRELATION_ID = 'correlation_id'
    RECORD_STATUS = 'record_status'

    # Record status values
    RECORD_STATUS_ACTIVE = 'ACTIVE'

# fmt: on