provider "google" {
  alias = "impersonate_terraform_service_account"
  scopes = [
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/drive.readonly",
  ]
}

# Generate short-lived access token for Terraform service account

data "google_service_account_access_token" "tf_sa" {
  provider               = google.impersonate_terraform_service_account
  target_service_account = var.terraform_deployer_sa
  scopes                 = ["userinfo-email", "cloud-platform"]
  lifetime               = "3600s"
}

# Provide service account access token to Terraform Google providers

provider "google" {
  access_token = data.google_service_account_access_token.tf_sa.access_token
}

provider "google-beta" {
  access_token = data.google_service_account_access_token.tf_sa.access_token
}
