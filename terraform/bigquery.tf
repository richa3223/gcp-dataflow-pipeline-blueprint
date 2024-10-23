# Create a BQ dataset for internal use

resource "google_bigquery_dataset" "internal" {
  project                    = var.project_id
  dataset_id                 = "df_blueprint_internal"
  friendly_name              = "Dataflow Blueprint Internal"
  location                   = var.region
  max_time_travel_hours      = 168 # 7 days
  delete_contents_on_destroy = true
  lifecycle {
    ignore_changes = [access]
  }
}

# Create a BQ dataset for reporting use

resource "google_bigquery_dataset" "reporting" {
  project                    = var.project_id
  dataset_id                 = "df_blueprint_reporting"
  friendly_name              = "Dataflow Blueprint Reporting"
  location                   = var.region
  delete_contents_on_destroy = true
  lifecycle {
    ignore_changes = [access]
  }
}

# Make the Reporting dataset an Authorized Dataset for the Internal dataset
# This enables SQL views in the Reporting dataset to read from tables in the Internal dataset

resource "google_bigquery_dataset_access" "authorized" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.internal.dataset_id
  dataset {
    dataset {
      project_id = google_bigquery_dataset.reporting.project
      dataset_id = google_bigquery_dataset.reporting.dataset_id
    }
    target_types = ["VIEWS"]
  }
}

# Daily processed input dataset table

resource "google_bigquery_table" "processed_data" {
  project                  = var.project_id
  dataset_id               = google_bigquery_dataset.internal.dataset_id
  table_id                 = "df_processed_data"
  require_partition_filter = false
  deletion_protection      = false

  time_partitioning {
    type  = "DAY"
    field = "created_ts"
  }

  clustering = [
    "record_date",
    "region",
    "country_id",
    "store_id"
  ]

  schema = file("${path.module}/bq-schemas/df_processed_data.json")
}

# Authorized View on processed table 

resource "google_bigquery_table" "processed_view" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.reporting.dataset_id
  table_id   = "df_processed_view"

  view {
    query          = templatefile("${path.module}/bq-views/df_processed_view.tftpl", { proj = var.project_id, dataset = "${google_bigquery_dataset.internal.dataset_id}" })
    use_legacy_sql = false
  }

  depends_on = [
    google_bigquery_table.processed_data,
    google_bigquery_dataset_access.authorized
  ]
}

# Table Valued Function enabling dynamic date range querying across processed table

resource "google_bigquery_routine" "processed_tvf" {
  project         = var.project_id
  dataset_id      = google_bigquery_dataset.reporting.dataset_id
  routine_id      = "df_processed_for_dates"
  routine_type    = "TABLE_VALUED_FUNCTION"
  language        = "SQL"
  definition_body = templatefile("${path.module}/bq-routines/df_processed_for_dates_func.tftpl", { proj = var.project_id, dataset = "${google_bigquery_dataset.reporting.dataset_id}" })

  arguments {
    name          = "start_date"
    argument_kind = "FIXED_TYPE"
    data_type     = jsonencode({ "typeKind" : "DATE" })
  }

  arguments {
    name          = "end_date"
    argument_kind = "FIXED_TYPE"
    data_type     = jsonencode({ "typeKind" : "DATE" })
  }

  depends_on = [
    google_bigquery_table.processed_view
  ]
}

# Table Valued Function as authorized routine on internal dataset

resource "google_bigquery_dataset_access" "authorized_tvf" {
  project    = var.project_id
  dataset_id = google_bigquery_dataset.internal.dataset_id
  routine {
    project_id = google_bigquery_routine.processed_tvf.project
    dataset_id = google_bigquery_dataset.reporting.dataset_id
    routine_id = google_bigquery_routine.processed_tvf.routine_id
  }
}

