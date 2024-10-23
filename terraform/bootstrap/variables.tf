variable "project_id" {
  type        = string
  description = "GCP project ID"
}

variable "terraform_deployer_impersonators" {
  type        = string
  description = "Group email ID for users who can impersonate Terraform Deployer service account"
}
