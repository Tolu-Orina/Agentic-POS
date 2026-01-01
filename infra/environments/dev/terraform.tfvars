# Development Environment Configuration

aws_region               = "us-east-1"
environment              = "dev"
web_bucket_name          = "agentic-retail-os-web-dev"
images_bucket_name       = "agentic-retail-os-images-dev"
web_distribution_name    = "agentic-retail-os-web-dev"
images_distribution_name = "agentic-retail-os-images-dev"
log_bucket_name          = "agentic-retail-os-logs-dev"
base_domain              = "agentic-pos.conquerorfoundation.com"
hosted_zone_id           = "Z052058934LNMXLJISF94"
create_certificate       = true

tags = {
  Environment = "dev"
  Team        = "platform"
  Project     = "AgenticRetailOS"
}

