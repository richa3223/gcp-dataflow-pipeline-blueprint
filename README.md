### Google Cloud Apache Beam ETL Pipeline Blueprint

- This repository contains the source code for a sample Google Cloud Platform (GCP) ETL pipeline, responsible for extracting, transforming, and loading data from a number of data sources into a target BigQuery dataset.
- The pipeline is built as a batch process using the Apache Beam Python SDK <https://beam.apache.org/about/> and is deployed as a Dataflow Flex Template on the Google Cloud Platform Cloud Dataflow service.

#### Repository Structure
The repository is structured as follows:

```
├── docs
|	└── how-to-create-dataflow-job-flex-template
|
├── modules                     (Custom Python data models and transforms)
|
├── terraform                   (IaC for GCP project resource deployment)
│   └── bq-routines             (BigQuery table function SQL)
│   └── bq-schemas              (BigQuery table schema JSON)
│   └── bq-views                (BigQuery data source view SQL)
│   └── looker-studio-sql       (SQL added directly to Looker Studio as a custom SQL data source e.g. for BigQuery routines)
|
├── Dockerfile                  (Dataflow Flex Template container) 
├── metadata.json               (Dataflow Flex Template configuration)
├── requirements.txt            (Python dependencies)
├── sample-pipeline.py          (Apache Beam pipeline)
└── tests                       (Python pytest unit tests directory)
```

#### 1. Docs

- This directory has documentation including a how-to document on the steps needed to build and deploy the pipeline on the Google Cloud Platform Dataflow service as a Dataflow Flex Template job

#### 2. Terraform 

- The `terraform` directory contains Terraform infrastructure as code (Iac) configuration responsible for provisioning the required infrastructure for the pipeline, including:
- __BigQuery__
    -  datasets, tables, views and table functions
    - Also the necessary BigQuery access permissions to enable the reporting dataset to act as an 'Authorized Dataset' viewing data in the internal dataset 
- __Cloud Scheduler Job__
    - This job is configured to trigger the Dataflow Flex Template on a predefined schedule.
    - The Terraform code defines the schedule, request payload, and authentication details for the job.
- __Google Cloud Storage (GCS)__
   - Adds a GCS bucket to provide Apache Beam pipeline with staging and temp directories as well as location for ingest files
   - Note that the bucket has Soft Delete disabled as this will help manage storage costs for the temporary or staging assets created by the pipeline
- __Service Accounts__
   - Defines dedicated service account identities and assigns required IAM roles for Dataflow Worker, BigQuery user and Looker Studio read-only personas

#### 3. Python Modules

- The `modules` directory contains custom Python modules used by the pipeline.
- The modules provide a range of specific functionalities and transformations required by the ETL process such as data parsing helpers, row model mappers, filter logic, ingest, join and, output transforms.
- These modules also include Python `dataclass` models to represent the schemas of ingested data sets as well as a single row model class for the transformed and combined data that is the output of the pipeline

#### 4. Apache Beam Pipeline

- The `sample-pipeline.py` file in the root directory contains the main Apache Beam pipeline code.
- This pipeline defines the steps involved in extracting, transforming, and loading the data.
- The `Dockerfile` is used to build a container image to enable the pipeline and its dependencies to be executed on the GCP Cloud Dataflow service using a Dataflow Flex Template 
The `requirements.txt` file lists the Python dependencies required by the pipeline and the custom modules
- The `pyproject.toml` file defines the Python package structure and metadata for bundling the pipeline, custom modules and dependencies as a Python package for distribution and deployment

#### 5. Pytest Unit Tests 

- Functionality of individual custom modules for filtering, combining, parsing or mapping data used by the Apache Beam pipeline can be tested in isolation using standard pytest unit tests <https://docs.pytest.org/en/stable/>
- Test fixtures can be tailored to the schema of data structures or custom row models appropriate for each business domain or use case that the template is applied to.