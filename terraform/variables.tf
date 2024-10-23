variable "df_worker_impersonators" {
  type        = string
  description = "Group email ID for users who can impersonate Dataflow Worker service account"
}

variable "gar_writer_group" {
  type        = string
  description = "Google group of users able to write to Google Artifact Registry"
}

variable "gcs_name_prefix" {
  type        = string
  description = "Name prefix of GCS bucket for Terraform remote state"
  default     = "df-blueprint"
}

variable "org_id" {
  type        = string
  description = "Organization ID"
}

variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "region" {
  type        = string
  description = "Google Cloud region for resources"
  default     = "europe-west2"
}

variable "required_apis" {
  type        = list(string)
  description = "List of GCP APIs to enable"
  default = [
    "artifactregistry.googleapis.com",
    "bigquery.googleapis.com",
    "cloudapis.googleapis.com",
    "cloudscheduler.googleapis.com",
    "compute.googleapis.com",
    "dataflow.googleapis.com",
    "datapipelines.googleapis.com",
    "datastudio.googleapis.com",
    "iam.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com",
    "storage.googleapis.com",
  ]
}

variable "subnet_name_prefix" {
  type        = string
  description = "Name prefix of subnet"
  default     = "df-blueprint-eur-west2"
}

variable "terraform_deployer_sa" {
  type        = string
  description = "Email address of Terraform Deployer service account"
}

variable "vpc_name_prefix" {
  type        = string
  description = "Name prefix of VPC"
  default     = "df-blueprint"
}
