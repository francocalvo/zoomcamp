terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.17.0"
    }
  }
}

provider "google" {
  project     = "zc-gcp-2024"
  region      = "us-central1"
  credentials = "../../.zc_creds.json"
}

resource "google_storage_bucket" "nixos-images" {
  name     = "zc-nixos-images"
  location = "us-central1"
}
