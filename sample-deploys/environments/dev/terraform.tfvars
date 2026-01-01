# Development Environment Configuration

aws_region         = "us-east-1"
environment        = "dev"
web_bucket_name    = "umcp-web-dev"
log_bucket_name    = "umcp-logs-dev"
distribution_name  = "umcp-web-dev"
base_domain        = "umcp.conquerorfoundation.com"
hosted_zone_id     = "Z052058934LNMXLJISF94"
create_certificate = true

tags = {
  Environment = "dev"
  Team        = "platform"
}

