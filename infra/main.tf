resource "google_compute_region_network_endpoint_group" "default" {
  project               = var.project
  name                  = "${var.prefix}-run-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = var.cloud_run_service
  }
}

module "lb" {
  source  = "GoogleCloudPlatform/lb-http/google//modules/serverless_negs"
  version = "~> 11.0"

  project = var.project
  name    = "${var.prefix}-run"

  ssl                             = true
  managed_ssl_certificate_domains = [var.dns_name]
  https_redirect                  = true
  backends = {
    default = {
      description            = null
      enable_cdn             = false
      custom_request_headers = null

      log_config = {
        enable      = true
        sample_rate = 1.0
      }

      groups = [
        {
          group = google_compute_region_network_endpoint_group.default.id
        }
      ]

      iap_config = {
        enable               = true
        oauth2_client_id     = "486962734106-hkhtpouo54hl4nvav54cr6htnaoq4f3q.apps.googleusercontent.com"
        oauth2_client_secret = "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"
      }

      security_policy = null
    }
  }
}

resource "google_dns_record_set" "default" {
  name         = "${var.dns_name}."
  type         = "A"
  ttl          = 300
  managed_zone = "ninjajon-com"
  rrdatas      = [module.lb.external_ip]
  depends_on   = [module.lb]
}
