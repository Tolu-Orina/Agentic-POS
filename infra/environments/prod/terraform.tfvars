# Production Environment Configuration

aws_region              = "us-east-1"
environment             = "prod"
web_bucket_name         = "agentic-retail-os-web-prod"
images_bucket_name      = "agentic-retail-os-images-prod"
web_distribution_name   = "agentic-retail-os-web-prod"
images_distribution_name = "agentic-retail-os-images-prod"
log_bucket_name         = "agentic-retail-os-logs-prod"
base_domain             = ""
hosted_zone_id          = ""
create_certificate      = false

tags = {
  Environment = "prod"
  Team        = "platform"
  Project     = "AgenticRetailOS"
}

