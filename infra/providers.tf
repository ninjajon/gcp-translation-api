terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.33.0"
    }
  }

  backend "gcs" {
    bucket = "jo-terraform-states"
    prefix = "trainslator"
  }
}

provider "google" {
  project = "jo-shared-services-lzzo"
  region  = "us-central1"
}

provider "google" {
  alias   = "target"
  project = "jo-trainslator-antl"
  region  = "us-central1"
}