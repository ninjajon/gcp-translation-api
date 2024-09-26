resource "google_compute_region_network_endpoint_group" "default" {
  project               = var.project
  name                  = "${var.prefix}-run-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = var.cloud_run_service
  }
}

data "google_project" "project" {
  project_id = var.project
}

# resource "google_iap_brand" "project_brand" {
#   support_email     = var.support_email
#   application_title = title(var.cloud_run_service)
#   project           = data.google_project.project.number
# }

# resource "google_iap_client" "project_client" {
#   display_name = var.cloud_run_service
#   brand        =  google_iap_brand.project_brand.name
#   # external users

# }

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
        #oauth2_client_id     = google_iap_client.project_client.client_id
        #oauth2_client_secret = google_iap_client.project_client.secret
        oauth2_client_id     = "589130920841-2pgd7agluvjit2rjm0guoa1s3a5fovtk.apps.googleusercontent.com"
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

resource "google_iap_web_iam_binding" "iap_web_user" {
  project    = var.project
  role       = "roles/iap.httpsResourceAccessor"  # This is the IAP Web App User role
  members    = ["group:${var.iap_group_name}"]
}
