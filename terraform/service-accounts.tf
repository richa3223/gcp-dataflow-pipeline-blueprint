# Custom Dataflow Worker Service Account

resource "google_service_account" "df_worker" {
  project      = var.project_id
  account_id   = "df-worker"
  display_name = "Custom Dataflow Worker"
}

# Add required IAM roles for Dataflow Worker for BigQuery and GCS

resource "google_project_iam_member" "df_worker" {
  project = var.project_id
  role    = "roles/dataflow.worker"
  member  = "serviceAccount:${google_service_account.df_worker.email}"
}

resource "google_project_iam_member" "df_developer" {
  project = var.project_id
  role    = "roles/dataflow.developer"
  member  = "serviceAccount:${google_service_account.df_worker.email}"
}

resource "google_project_iam_member" "df_worker_bq_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.df_worker.email}"
}

resource "google_storage_bucket_iam_member" "df_worker" {
  bucket = google_storage_bucket.df_blueprint.name
  role   = "roles/storage.objectUser"
  member = "serviceAccount:${google_service_account.df_worker.email}"
}

resource "google_bigquery_dataset_access" "df_worker" {
  project       = var.project_id
  dataset_id    = google_bigquery_dataset.internal.dataset_id
  role          = "roles/bigquery.dataEditor"
  user_by_email = google_service_account.df_worker.email
}

resource "google_service_account_iam_member" "df_worker_impersonators" {
  service_account_id = google_service_account.df_worker.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "group:${var.df_worker_impersonators}"
}

# Looker Studio Read-Only Service Account

resource "google_service_account" "looker_studio_readonly" {
  project      = var.project_id
  account_id   = "looker-studio-readonly"
  display_name = "Looker Studio Read-only"
}

# Add required IAM roles for Looker Studio account read-only access to BigQuery

resource "google_project_iam_member" "looker_studio_bq_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.looker_studio_readonly.email}"
}

resource "google_bigquery_dataset_access" "looker_studio_readonly" {
  project       = var.project_id
  dataset_id    = google_bigquery_dataset.reporting.dataset_id
  role          = "roles/bigquery.dataViewer"
  user_by_email = google_service_account.looker_studio_readonly.email
}

# Enable org-level Looker Studio Service Agent to impersonate Looker Studio read-only account

resource "google_service_account_iam_member" "looker_studio_agent" {
  service_account_id = google_service_account.looker_studio_readonly.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "serviceAccount:${local.looker_studio_agent}"
}
