# Test Environment Configuration

aws_region         = "us-east-1"
environment        = "test"
web_bucket_name    = "umcp-web-test"
log_bucket_name    = "umcp-logs-test"
distribution_name  = "umcp-web-test"
base_domain        = "umcp.conquerorfoundation.com"
hosted_zone_id     = "Z052058934LNMXLJISF94"
create_certificate = true

tags = {
  Environment = "test"
  Team        = "platform"
}

