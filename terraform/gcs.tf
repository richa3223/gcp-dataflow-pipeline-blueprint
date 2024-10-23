# Create private GCS bucket

resource "google_storage_bucket" "df_blueprint" {
  project                     = var.project_id
  name                        = local.gcs_bucket_name
  location                    = upper(var.region)
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  soft_delete_policy {
    retention_duration_seconds = 0
  }
  versioning {
    enabled = false
  }
  force_destroy = true
}

# Create managed folders within GCS bucket

resource "google_storage_managed_folder" "bootstrap_terraform_state" {
  bucket        = google_storage_bucket.df_blueprint.name
  name          = "terraform_state/bootstrap/"
  force_destroy = false
}

resource "google_storage_managed_folder" "blueprint_terraform_state" {
  bucket        = google_storage_bucket.df_blueprint.name
  name          = "terraform_state/blueprint/"
  force_destroy = false
}

resource "google_storage_managed_folder" "dataflow_input" {
  bucket        = google_storage_bucket.df_blueprint.name
  name          = "dataflow/input_data/"
  force_destroy = false
}

resource "google_storage_managed_folder" "dataflow_staging" {
  bucket        = google_storage_bucket.df_blueprint.name
  name          = "dataflow/staging/"
  force_destroy = false
}

resource "google_storage_managed_folder" "dataflow_temp" {
  bucket        = google_storage_bucket.df_blueprint.name
  name          = "dataflow/temp/"
  force_destroy = false
}

resource "google_storage_managed_folder" "flex_templates" {
  bucket        = google_storage_bucket.df_blueprint.name
  name          = "dataflow/flex_templates/"
  force_destroy = false
}

# Add sample input data files to GCS bucket

resource "google_storage_bucket_object" "sample_csv_data" {
  bucket = google_storage_bucket.df_blueprint.name
  name   = "${google_storage_managed_folder.dataflow_input.name}csv/sample_data.csv"
  source = "${path.module}/sample-input-data/sample_data.csv"
}

resource "google_storage_bucket_object" "csv_ref_data" {
  bucket = google_storage_bucket.df_blueprint.name
  name   = "${google_storage_managed_folder.dataflow_input.name}csv/regions_data.csv"
  source = "${path.module}/sample-input-data/regions_data.csv"
}

resource "google_storage_bucket_object" "sample_avro_data" {
  bucket = google_storage_bucket.df_blueprint.name
  name   = "${google_storage_managed_folder.dataflow_input.name}avro/sample_avro_data.avro"
  source = "${path.module}/sample-input-data/avro/sample_avro_data.avro"
}

resource "google_storage_bucket_object" "sample_parquet_data" {
  bucket = google_storage_bucket.df_blueprint.name
  name   = "${google_storage_managed_folder.dataflow_input.name}parquet/sample_parquet_data.parquet"
  source = "${path.module}/sample-input-data/parquet/sample_parquet_data.parquet"
}
