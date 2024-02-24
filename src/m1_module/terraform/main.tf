terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.17.0"
    }
  }
}

provider "google" {
  project     = var.Project
  region      = var.Region
  credentials = var.Credentials
}

resource "google_compute_instance" "zc-nixos" {
  name         = "zc-nixos"
  machine_type = "e2-standard-2"
  zone         = "${var.Region}-${var.Zone}"

  tags = ["terraform"]

  boot_disk {
    initialize_params {
      size  = 20
      image = "projects/${var.Project}/global/images/family/${var.ImageFamily}"
    }
  }

  metadata = {
    ssh-keys = "${var.sshUser}:${file(var.sshPubKeyFile)}"
  }

  network_interface {
    network = "default"
    access_config {
      network_tier = "STANDARD"
    }
  }


  service_account {
    email  = var.RunnerEmail
    scopes = ["cloud-platform"]
  }
}
