terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.18.1"
    }
  }
}

provider "google" {
  # Configuration options
  project = "inner-fx-449107-t5"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "fashion_retail_sales"
  location      = "US"
  storage_class = "STANDARD"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "training_dataset" {
  dataset_id = "Fashion_retail_sales"
  project = "inner-fx-449107-t5"
  location      = "US"
}