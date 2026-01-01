# Test Environment Configuration

aws_region               = "us-east-1"
environment              = "test"
web_bucket_name          = "agentic-retail-os-web-test"
images_bucket_name       = "agentic-retail-os-images-test"
web_distribution_name    = "agentic-retail-os-web-test"
images_distribution_name = "agentic-retail-os-images-test"
log_bucket_name          = "agentic-retail-os-logs-test"
base_domain              = "agentic-pos.conquerorfoundation.com"
hosted_zone_id           = "Z052058934LNMXLJISF94"
create_certificate       = true

tags = {
  Environment = "test"
  Team        = "platform"
  Project     = "AgenticRetailOS"
}

