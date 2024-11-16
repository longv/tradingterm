provider "google" {
  project = "trading-term"  # Replace with your GCP project ID
  region  = "us-central1"
}

resource "google_bigtable_instance" "dev_instance" {
  name           = "dev-bigtable-instance"
  display_name   = "Dev Bigtable Instance"

  cluster {
    cluster_id   = "dev-cluster"
    zone         = "us-central1-b"
    storage_type = "SSD"
  }
}

resource "google_bigtable_table" "trading_data_table" {
  name           = "trading-data-table"
  instance_name  = google_bigtable_instance.dev_instance.name

  column_family {
    family = "attributes"
  }
}
