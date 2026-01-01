# Development Environment Configuration

aws_region              = "us-east-1"
environment             = "dev"
web_bucket_name         = "agentic-retail-os-web-dev"
images_bucket_name      = "agentic-retail-os-images-dev"
web_distribution_name   = "agentic-retail-os-web-dev"
images_distribution_name = "agentic-retail-os-images-dev"
log_bucket_name         = "agentic-retail-os-logs-dev"
base_domain             = ""
hosted_zone_id          = ""
create_certificate      = false

tags = {
  Environment = "dev"
  Team        = "platform"
  Project     = "AgenticRetailOS"
}

