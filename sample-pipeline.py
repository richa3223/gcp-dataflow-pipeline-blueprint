# fmt: off
# pylint: disable=abstract-method,unnecessary-dunder-call,expression-not-assigned

"""
Beam data validating pipeline blueprint

This pipeline example implements the following steps:

- Ingest a tabular dataset as a CSV file from local or GCS source
- Validate each row of ingested CSV against an AVRO schema data contract
- Tag malformed or invalid rows to enable side outputs to file or database sink
- Writes result set to BigQuery table
"""

import argparse
import logging
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from modules.BigQueryUtils import BigQueryUtils
from modules.Filters import Filters
from modules.Names import Names
from modules.Parsers import Parsers
from modules.Combiners import (
    CollectionAsDecodeDict
)
from modules.IngestTransforms import (
    AvroIngest,
    CsvIngest,
    ParquetIngest,
)
from modules.JoinTransforms import (
    AddProductRefData,
    AddRegionRefData,
    AddStoreRefData,
)
from modules.OutputTransforms import (
    LoadIntoBigQuery
)
from modules.RowModelTransforms import (
    DecorateCustomerId,
    MapToProductModel,
    MapToSampleRowModel,
    MapToStoreModel,
    SampleRowModelToDict
)

########################################################### 
# 
#              MAIN PIPELINE ROUTINE
# 
###########################################################

def run(argv=None):
    """Executes pipeline"""

    #  Define pipeline arguments
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--input',
        required=True,
        dest='input',
        help='Path to input dataset e.g. local file or GCS path'
    ),
    parser.add_argument(
        '--ref-data',
        required=True,
        dest='ref_data',
        help='Path to reference data file'
    ),
    parser.add_argument(
        '--avro',
        required=True,
        dest='avro_input',
        help='Path to AVRO binary file'
    ),
    parser.add_argument(
        '--parquet',
        required=True,
        dest='parquet_input',
        help='Path to Parquet binary file'
    ),
    parser.add_argument(
        '--skip-filter',
        required=False,
        default=True,
        dest='skip_filter',
        help='Flag to toggle filter transform'
    ),    
    parser.add_argument(
        '--bq-output',
        required=False,
        default=False,
        dest='bq_output',
        help='Flag to enable writing results to BigQuery table'
    )         

    known_args, pipeline_args = parser.parse_known_args(argv)

    # Set pipeline options
    pipeline_options = PipelineOptions(
        pipeline_args,
        save_main_session=True,
        streaming=False,
    )
    pipeline_options_dict = pipeline_options.get_all_options()

    # Define GCP project ID from pipeline options
    gcp_project_id = pipeline_options_dict[Names.GCP_PROJ_KEY]

    # Convert string parameters to bool
    skip_filter = Parsers.str_to_bool(known_args.skip_filter)
    bq_output = Parsers.str_to_bool(known_args.bq_output)

    # Instantiate Pipeline using provided options
    p = beam.Pipeline(options=pipeline_options)

    # Sample CSV data set ingest and transform to custom row model 
    orders, order_parse_errors = (
        p
        | 'Ingest CSV'
        >> CsvIngest(csv_file=known_args.input, label='Orders')
        | 'Orders to Model'
        >> beam.ParDo(MapToSampleRowModel()).with_outputs(Names.PARSE_ERRORS, main="outputs")
    )  

    # Sample reference data ingest as a side input of Python dictionaries
    region_data = (
        p
        | 'Ingest ref data'
        >> CsvIngest(csv_file=known_args.ref_data,label='Ref Data')
        | 'Ref data as side input'
        >> beam.CombineGlobally(CollectionAsDecodeDict(key='country_code'))
    )      

    # Sample AVRO data set ingest and transform to custom row model
    products, product_parse_errors = (
        p
        | 'Ingest AVRO'
        >> AvroIngest(avro_file=known_args.avro_input, label='Products')
        | 'Products to Model'
        >> beam.ParDo(MapToProductModel()).with_outputs(Names.PARSE_ERRORS, main="outputs")
    )

    # Sample product reference data as side input of custom row models
    product_data = (
        products
        | 'Products as side input'
        >> beam.CombineGlobally(CollectionAsDecodeDict())
    )    

    # Sample Parquet data set ingest and transform to custom row model
    stores, store_parse_errors = (
        p
        | 'Ingest Parquet'
        >> ParquetIngest(parquet_file=known_args.parquet_input, label='Stores')
        | 'Stores to Model'
        >> MapToStoreModel()
    )

    # Sample stores reference data as side input of custom row models
    store_data = (
        stores
        | 'Stores as side input'
        >> beam.CombineGlobally(CollectionAsDecodeDict())
    )   

    #####################################################################
    # This section of the pipeline is where you insert your task specific
    # transforms and calculations using the 'valid_records' PCollection
    # as the input.
    # Once your custom steps are completed you can then pass the result 
    # PCollection to the 'Format row for BQ' transform below.
    # Simply update the input PCollection from the 'valid_records' 
    # variable to a name you have defined holding the output
    # PCollection of your last custom transform step.
    #####################################################################

    # Sample enrichment, filter and decorate transforms
    processed_orders = (
        orders
        | 'Enrich region'
        >> beam.ParDo(AddRegionRefData(), beam.pvalue.AsSingleton(region_data))
        | 'Enrich product'
        >> beam.ParDo(AddProductRefData(), beam.pvalue.AsSingleton(product_data))
        | 'Enrich store'
        >> beam.ParDo(AddStoreRefData(), beam.pvalue.AsSingleton(store_data))
        | 'Filter by country'
        >> beam.Filter(
            Filters.filter_by_country,
            countries=[Names.COUNTRY_UK, Names.COUNTRY_IRELAND], 
            skip=skip_filter
        )
        | 'Format customer ID'
        >> beam.ParDo(DecorateCustomerId())
    )

    # Log processed records
    _ = (
        processed_orders
        | 'Count records' >> beam.combiners.Count.Globally()
        | 'Log records' >> beam.Map(lambda num: logging.info(f'Processed records : {num}'))
    )     

    # Log parsing errors
    _ = (
        (order_parse_errors, product_parse_errors, store_parse_errors)
        | 'Flatten errs' >> beam.Flatten()
        | 'Count errs' >> beam.combiners.Count.Globally()
        | 'Log errs' >> beam.Map(lambda num: logging.info(f'Parsing errors : {num}'))
    )         

    # Conditionally insert records into BigQuery table if pipeline parameter set
    if bq_output == True:

        metadata_fields = BigQueryUtils.metadata_fields()

        _ = (
            processed_orders
            | 'Format for BigQuery'
            >> beam.ParDo(SampleRowModelToDict(metadata_fields))
            | 'Write to BigQuery'
            >> LoadIntoBigQuery(
                project=gcp_project_id, 
                dataset=Names.BQ_DATASET, 
                table=Names.BQ_TABLE
            )
        )
        
    # Execute the pipeline
    result = p.run()

    # Wait until pipeline is in a terminal state
    result.wait_until_finish()

    # Log information from PipelineResult
    logging.info(f'Pipeline Info : State={result.state}')
    
  
if __name__ == '__main__':  
    logging.getLogger().setLevel(logging.INFO)
    run()

# fmt: on  