# Create Terraform Deployer service account 

resource "google_service_account" "tf_deployer" {
  project      = var.project_id
  account_id   = "terraform-deployer"
  display_name = "Terraform Deployer"
}

# Assign required IAM roles to Terraform Deployer service account

resource "google_project_iam_member" "service_usage_admin" {
  project = var.project_id
  role    = "roles/serviceusage.serviceUsageAdmin"
  member  = "serviceAccount:${google_service_account.tf_deployer.email}"
}

resource "google_project_iam_member" "project_iam_admin" {
  project = var.project_id
  role    = "roles/resourcemanager.projectIamAdmin"
  member  = "serviceAccount:${google_service_account.tf_deployer.email}"
}

resource "google_project_iam_member" "sa_admin" {
  project = var.project_id
  role    = "roles/iam.serviceAccountAdmin"
  member  = "serviceAccount:${google_service_account.tf_deployer.email}"
}

resource "google_project_iam_member" "network_admin" {
  project = var.project_id
  role    = "roles/compute.networkAdmin"
  member  = "serviceAccount:${google_service_account.tf_deployer.email}"
}

resource "google_project_iam_member" "storage_admin" {
  project = var.project_id
  role    = "roles/storage.admin"
  member  = "serviceAccount:${google_service_account.tf_deployer.email}"
}

resource "google_project_iam_member" "bq_data_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.tf_deployer.email}"
}

resource "google_project_iam_member" "dataflow_admin" {
  project = var.project_id
  role    = "roles/dataflow.admin"
  member  = "serviceAccount:${google_service_account.tf_deployer.email}"
}

resource "google_project_iam_member" "gar_admin" {
  project = var.project_id
  role    = "roles/artifactregistry.admin"
  member  = "serviceAccount:${google_service_account.tf_deployer.email}"
}

resource "google_project_iam_member" "cloudscheduler_admin" {
  project = var.project_id
  role    = "roles/cloudscheduler.admin"
  member  = "serviceAccount:${google_service_account.tf_deployer.email}"
}

# Assign Google group of users who can impersonate Terraform Deployer service account

resource "google_service_account_iam_member" "tf_sa_impersonators" {
  service_account_id = google_service_account.tf_deployer.name
  role               = "roles/iam.serviceAccountTokenCreator"
  member             = "group:${var.terraform_deployer_impersonators}"
}
