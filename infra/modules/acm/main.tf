# ACM Module - SSL/TLS Certificate for CloudFront
# Note: This module requires a provider alias for us-east-1
# The provider should be defined in the calling module

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = "~> 5.0"
      configuration_aliases = [aws.us_east_1]
    }
  }
}

resource "aws_acm_certificate" "cloudfront" {
  provider = aws.us_east_1

  domain_name       = var.domain_name
  validation_method = "DNS"

  subject_alternative_names = var.subject_alternative_names

  lifecycle {
    create_before_destroy = true
  }

  tags = merge(
    var.tags,
    {
      Name = var.domain_name
    }
  )
}

resource "aws_acm_certificate_validation" "cloudfront" {
  count = var.wait_for_validation && var.hosted_zone_id != "" ? 1 : 0

  provider = aws.us_east_1

  certificate_arn         = aws_acm_certificate.cloudfront.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}

# Route53 validation records (if hosted zone ID provided)
# Note: Route53 records are created in the default provider region, not us-east-1
# This follows the AWS Terraform provider documentation pattern
# Note: This requires a two-phase apply - first apply creates the certificate,
# second apply creates the validation records once domain_validation_options is available
resource "aws_route53_record" "cert_validation" {
  for_each = var.hosted_zone_id != "" ? {
    for dvo in aws_acm_certificate.cloudfront.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  } : {}

  zone_id = var.hosted_zone_id
  name    = each.value.name
  type    = each.value.type
  records = [each.value.record]
  ttl     = 60

  # Allow overwrite for validation records
  allow_overwrite = true
}

