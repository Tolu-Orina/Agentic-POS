# Route53 Module - DNS Configuration

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

data "aws_route53_zone" "main" {
  count   = var.domain_name != "" ? 1 : 0
  zone_id = var.hosted_zone_id != "" ? var.hosted_zone_id : null
  name    = var.hosted_zone_id == "" ? var.domain_name : null
}

locals {
  zone_id = var.domain_name != "" ? (
    var.hosted_zone_id != "" ? var.hosted_zone_id : (
      length(data.aws_route53_zone.main) > 0 ? data.aws_route53_zone.main[0].zone_id : ""
    )
  ) : ""
  cloudfront_hosted_zone_id = var.cloudfront_hosted_zone_id != "" ? var.cloudfront_hosted_zone_id : "Z2FDTNDATAQYW2" # CloudFront's hosted zone ID
}

resource "aws_route53_record" "root" {
  count   = var.domain_name != "" ? 1 : 0
  zone_id = local.zone_id
  name    = var.domain_name
  type    = "A"

  allow_overwrite = true # Allow overwriting existing records

  alias {
    name                   = var.cloudfront_domain_name
    zone_id                = local.cloudfront_hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_record" "www" {
  count   = var.domain_name != "" ? 1 : 0
  zone_id = local.zone_id
  name    = "www.${var.domain_name}"
  type    = "A"

  allow_overwrite = true # Allow overwriting existing records

  alias {
    name                   = var.cloudfront_domain_name
    zone_id                = local.cloudfront_hosted_zone_id
    evaluate_target_health = false
  }
}

