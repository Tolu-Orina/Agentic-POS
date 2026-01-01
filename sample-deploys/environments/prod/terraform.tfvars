# Production Environment Configuration

aws_region         = "us-east-1"
environment        = "prod"
web_bucket_name    = "umcp-web-prod"
log_bucket_name    = "umcp-logs-prod"
distribution_name  = "umcp-web-prod"
base_domain        = "umcp.conquerorfoundation.com"
hosted_zone_id     = "Z052058934LNMXLJISF94"
create_certificate = true

tags = {
  Environment = "prod"
  Team        = "platform"
}

