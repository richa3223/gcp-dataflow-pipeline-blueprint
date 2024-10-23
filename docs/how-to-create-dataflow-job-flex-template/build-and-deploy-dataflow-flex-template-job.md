### How to build & deploy a Dataflow Flex Template job

#### Overview

- Apache Beam Python pipelines can be developed and tested on your local device initially before deploying the pipeline as a job on the GCP Cloud Dataflow service.
- Google recommend the use of Dataflow Flex Templates <https://cloud.google.com/dataflow/docs/concepts/dataflow-templates#compare-flex-templates-and-classic-templates> as the means of deploying your pipeline and all its dependencies as an immutable Docker image artifact stored in Artifact Registry referenced by a separate template configuration file stored in Google Cloud Storage
- A key advantage of Dataflow Flex Templates is that pipeline jobs can be executed on virtual machine workers running on private IP addresses without the need to download python package dependencies from PyPi repositories on the public Internet
- This provides better software supply chain security as well as minimising issues arising from version drift in python dependencies
- Dataflow Flex Template pipeline jobs can also be scheduled and triggered using Cloud Scheduler jobs that send HTTPS requests to the Dataflow API using service account credentials
- See the following steps outlining how to build the pipeline container image and the Dataflow Flex Template configuration file
- Please also refer to the Google documentation for a full overview of these steps : <https://cloud.google.com/dataflow/docs/guides/templates/using-flex-templates>


#### Bundle Python pipeline & dependencies as a container image

__1. Use GCP Cloud Shell__

- GCP Cloud Shell provides pre-installed tools such as `docker`, `gcloud`, `git` and `python` that make it a convenient option for building a container image for the Dataflow Flex Template
- First ensure that you have added the necessary credentials and `git` configuration to your Cloud Shell home directory in order to connect to the Morrisons Bitbucket organisation to clone the repository pipeline and Dockerfile source code 
- See below for a sample Dockerfile that uses a Google Dataflow Flex Template Launcher base image and adds the pipeline dependencies and the pipeline itself along with any custom python modules provided as a package using the `setup.py` configuration :

```
FROM gcr.io/dataflow-templates-base/python311-template-launcher-base:20240812-rc01

# Define location to store the pipeline artifacts
ARG WORKDIR=/template
RUN mkdir -p ${WORKDIR}

# Set working directory to /template
WORKDIR ${WORKDIR}

# Copy pipeline and package modules to working directory
COPY mdm-interco-etl-pipeline.py .
COPY modules modules
COPY requirements.txt .
COPY setup.py .
COPY __init__.py .
COPY README.rst .

# Set configuration env var for main pipeline file to run
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/mdm-interco-etl-pipeline.py"

# Set configuration env var for pipeline package setup file
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"

ENV PYTHONPATH=${WORKDIR}

# Install python dependencies. Use `--no-cache-dir` to reduce image size
RUN apt-get update
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir 'apache-beam[gcp]==2.54.0'
RUN pip install --no-cache-dir -r requirements.txt
RUN pip check

# Download dependencies to local packages cache to speed up Dataflow worker start-up
RUN pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r requirements.txt

# Install the pipeline package on the container
RUN python setup.py install

# All dependencies already installed, so no need to rebuild
ENV PIP_NO_DEPS=True
```

__2. Build Docker Image__

- Ensure your user account has the necessary permissions to push images to the GCP Artifact Registry instance in your Google Cloud project
- Next, authenticate your `gcloud` session using `gcloud auth login`
- Register `gcloud` as a Docker credential helper to authenticate with the Artifact Registry when pushing or pulling images

```
gcloud auth configure-docker LOCATION-docker.pkg.dev
```

- Set a suitable tag value as an environment variable `$TAG` e.g. `20240916-v1`
- Then run the following command to build an image 

```
docker build . -t ${GAR}/mdm/mdm_test_pipeline:${TAG}
```

__3. Test Docker Image__

- It is important to run a quick smoke test on the container image to ensure that the Apache Beam python pipeline and all of its dependencies have been correctly packaged into the image
- Using Cloud Shell, you can instantiate a container from the image and then run your pipeline from a Bash command line session within the running container
- Use the following command to run the container and connect to it :

```
 docker run --rm -it --entrypoint=/bin/bash $IMG
```

- Next you can run your python pipeline using the Apache Beam __DirectRunner__ i.e. the local VM, passing it the required parameters to test it functions correctly and no dependencies are missing :

```
python ./my-test-pipeline.py \
--setup_file ./setup.py \
--project ${PROJECT} \
--runner DirectRunner \
--job_name test-container-image \
--service_account_email my-service-account@${PROJECT}.iam.gserviceaccount.com \
--temp_location gs://${GCS}/dataflow_temp \
--staging_location gs://${GCS}/dataflow_staging \
--str-date '2024-09-22' \
--bulk True
```

__4. Push Docker Image to Google Artifact Registry__

- Once the build has completed and you have run a successful test of the container image running on the DirectRunner in your Cloud Shell session, you can push the image to the Google Artifact Registry

```
PROJECT=my-gcp-project-id
GAR=europe-west2-docker.pkg.dev/${PROJECT}/my-artifact-registry-name
IMG=${GAR}/my-folder/my-pipeline-name:${TAG}
docker push ${IMG}
```

#### Generate Dataflow Flex Template on GCS

- Still working within Cloud Shell, the next step will generate a Flex Template configuration file and write it to a Google Cloud Storage location
- Note that the Flex Template requires some configuration that defines the parameters for the pipeline job that you provide in a JSON file (usually called `metadata.json`) such as the below example
- Please also refer to this Google sample : <https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/dataflow/flex-templates/getting_started/metadata.json>

```
{
    "name": "my-pipeline-template-name",
    "description": "Sample Flex Template parameter configuration",
    "parameters": [
      {
        "name": "bulk",
        "label": "Bulk run flag",
        "helpText": "Flag indicating whether to run bulk job",
        "defaultValue": "false",
        "isOptional": true        
      },
      {
        "name": "str-date",
        "label": "Sample required string parameter",
        "helpText": "Sample string date parameter in 'yyyy-mm-dd format",
        "isOptional": false
      }
    ]
  }
```

- Next, optionally set some environment variables for legibility
- The `TEMPLATE_FILE` variable should contain the fully qualified Google Cloud Storage (GCS) path to the location where you wish to store your Flex Template file including a unique name for the template. 
- It's useful to include the same `TAG` value you assigned to the container image
- Ensure the file name has a `.json` suffix

```
GCS=my-gcs-bucket-name
TEMPLATE_FILE=gs://${GCS}/dataflow_flex_templates/my-pipeline-template-name-${TAG}.json
```

- Run the following `gcloud dataflow flex-template build` command to create a Flex template file and store in GCS

```
gcloud dataflow flex-template build $TEMPLATE_FILE \
> --image $IMG \
> --sdk-language "PYTHON" \
> --metadata-file=metadata.json \
> --project ${PROJECT}
```

- The Flex Template is a JSON file that should look something like the below example :

```
{
    "defaultEnvironment": {},
    "image": "europe-west2-docker.pkg.dev/my-project/my-artifact-registry-name/my-folder/my-pipeline-name:20240901-v8",
    "metadata": {
        "description": "ample Flex Template parameter configuration",
        "name": "my-pipeline-template-name",
        "parameters": [
            {
                "defaultValue": "false",
                "helpText": "Flag indicating whether to run bulk job",
                "isOptional": true,
                "label": "Bulk run flag",
                "name": "bulk"
            },
            {
                "helpText": "Sample string date parameter in 'yyyy-mm-dd format",
                "isOptional": false,
                "label": "Sample required string parameter",
                "name": "str-date"
            }
        ]
    },
    "sdkInfo": {
        "language": "PYTHON"
    }
}
```

#### Create a Dataflow Job to test the Flex Template 

- Once the Flex Template has been generated you can create a Dataflow job to test it works correctly
- Ensure you add service account impersonation for the service account to your `gcloud` configuration before running this manually :

```
gcloud config set auth/impersonate_service_account my-service-account@finc-insight-dev-manu.iam.gservicaccount.com
```

- Use the `gcloud dataflow flex-template run` command to create and start a new Dataflow pipeline job using the Flex Template stored in GCS

```
gcloud dataflow flex-template run my-pipeline-test \
--template-file-gcs-location=$TEMPLATE_FILE \
--disable-public-ips \
--max-workers=1 \
--network=default \
--region=europe-west1 \
--subnetwork=regions/europe-west1/subnetworks/default \
--service-account-email=my-service-account@$PROJECT.iam.gserviceaccount.com  \
--staging-location=gs://$GCS/dataflow_staging \
--temp-location=gs://$GCS/dataflow_temp \
--worker-region=europe-west1 \
--project $PROJECT \
--worker-machine-type=n2-standard-4 \
--parameters=bulk=True,str-date="2024-09-21" \
--verbosity="debug"
```

- If successful, you should see a the `my-pipeline-test` job running in the Google Cloud Console Dataflow > Jobs page

#### Scheduling Execution of Dataflow Flex Template with Cloud Scheduler

- Dataflow Flex Template jobs can be triggered manually using `gcloud` as shown above or by a request to the Dataflow API from a Cloud Scheduler job

__1. Create a Cloud Scheduler Job using Terraform__

- Terraform is a convenient method for configuring the cron schedule and the HTTP POST request payload that will be sent to the Dataflow API
- Ensure your Terraform deployer service account has the necessary IAM permissions :
   - `cloudscheduler.jobs.enable`
   - `cloudscheduler.jobs.create`
   - `cloudscheduler.jobs.delete` 

- See below for a sample Terraform configuration for Cloud Scheduler job that triggers at 9:30am every day to invoke a Dataflow template
- Note that the Cloud Scheduler job will authenticate the request to the Dataflow API using the credentials of the `my-service-account` service account
- Ensure that this service account has the necessary IAM permissions to be able to create a Dataflow job. The `roles/dataflow.developer` IAM role includes this permission
- Note also that the API request body is a JSON structure and must be Base64 encoded 

```
resource "google_cloud_scheduler_job" "my_test_pipeline" {
  project          = var.project_id
  name             = "my-test-pipeline"
  description      = "Sample scheduler job for Flex Template pipeline"
  region           = "europe-west1"
  schedule         = "30 9 * * *"
  time_zone        = "Europe/London"
  attempt_deadline = "60s"
  paused           = false

  http_target {
    http_method = "POST"
    uri         = "https://dataflow.googleapis.com/v1b3/projects/${var.project_id}/locations/europe-west1/flexTemplates:launch"
    body        = base64encode(local.dataflow_api_request_body)

    oauth_token {
      service_account_email = "my-service-account@${var.project_id}.iam.gserviceaccount.com"
    }
  }
}
``` 

- See below example of JSON API request body payload defined as a Terraform local variable `dataflow_api_request_body`
- Note also that the `serviceAccountEmail` field of the request defines the service account identity that will execute the Dataflow job - __NOT__ the Cloud Scheduler job
- For the purposes of this example, the same `my-service-account` identity has been used but you can provide a separate service account 
- The key thing to ensure is that whichever service account you provide in the API request is the identity that the Dataflow job will use when executing so it must have the necessary IAM permissions to access any resources the pipeline requires such as Cloud Storage buckets, BigQuery datasets, Pub/Sub topics, etc

```
tag 						   = "20240916-v1"
gcs_bucket				   = "my-gcs-bucket-name"
flex_template_gcs_path    = "gs://${local.gcs_bucket}/dataflow_flex_templates/mdm-pipeline-template-name-${local.tag}.json"

dataflow_api_request_body = jsonencode({
    "launchParameter" : {
      "jobName" : "my-test-pipeline",
      "containerSpecGcsPath" : "${local.flex_template_gcs_path_prod}",
      "parameters" : {
        "bulk" : "False",
        "str-date" : "2024-09-21"
      },
      "environment" : {
        "serviceAccountEmail" : "my-service-account@${var.project_id}.iam.gserviceaccount.com",
        "workerRegion" : "europe-west1",
        "network" : "default",
        "subnetwork" : "regions/europe-west1/subnetworks/default",
        "launcherMachineType" : "n2-standard-4",
        "machineType" : "n2-standard-4",
        "ipConfiguration" : "WORKER_IP_PRIVATE",
        "tempLocation" : "${local.gcs_bucket}/dataflow_temp",
        "stagingLocation" : "${local.gcs_bucket}/dataflow_staging",
        "numWorkers" : 1,
        "maxWorkers" : 2
      }
    }
})
```

- Refer to the Google Dataflow API documentation for specific request field names and types : <https://cloud.google.com/dataflow/docs/reference/rest/v1b3/projects.locations.flexTemplates/launch#LaunchFlexTemplateParameter>
