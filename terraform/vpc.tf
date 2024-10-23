# Create custom VPC

resource "google_compute_network" "custom_vpc" {
  project                 = var.project_id
  name                    = local.vpc_name
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

# Create private subnet in specified region (default is europe-west2)

resource "google_compute_subnetwork" "custom_subnet" {
  name                     = local.subnet_name
  network                  = google_compute_network.custom_vpc.id
  region                   = var.region
  project                  = var.project_id
  ip_cidr_range            = "10.240.0.0/22"
  private_ip_google_access = true

  secondary_ip_range {
    ip_cidr_range = "10.0.0.0/14"
    range_name    = "secondary-pods-range"
  }

  secondary_ip_range {
    ip_cidr_range = "172.16.0.0/20"
    range_name    = "secondary-svc-range"
  }
}
