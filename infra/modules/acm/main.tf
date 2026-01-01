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
# Use static keys (domain names from input variables) to avoid for_each with unknown values
# The domain_validation_options are referenced in resource attributes (can be unknown at plan time)
locals {
  # Create a map of domains that need validation (known at plan time)
  validation_domains = var.hosted_zone_id != "" ? {
    for domain in concat([var.domain_name], var.subject_alternative_names) : domain => true
  } : {}
}

resource "aws_route53_record" "cert_validation" {
  for_each = local.validation_domains

  zone_id = var.hosted_zone_id
  # Reference domain_validation_options in attributes (Terraform handles unknown values here)
  # Find the matching validation option for this domain
  name = [for dvo in aws_acm_certificate.cloudfront.domain_validation_options : dvo.resource_record_name if dvo.domain_name == each.key][0]
  type = [for dvo in aws_acm_certificate.cloudfront.domain_validation_options : dvo.resource_record_type if dvo.domain_name == each.key][0]
  # records expects a list of strings - keep the filtered result as a list (single element)
  records = [for dvo in aws_acm_certificate.cloudfront.domain_validation_options : dvo.resource_record_value if dvo.domain_name == each.key]
  ttl     = 60

  # Allow overwrite for validation records
  allow_overwrite = true
}

