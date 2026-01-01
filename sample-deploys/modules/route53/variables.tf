variable "domain_name" {
  description = "Domain name for Route53"
  type        = string
  default     = ""
}

variable "hosted_zone_id" {
  description = "Existing Route53 hosted zone ID (optional, will lookup by domain if not provided)"
  type        = string
  default     = ""
}

variable "cloudfront_domain_name" {
  description = "Domain name of the CloudFront distribution"
  type        = string
}

variable "cloudfront_hosted_zone_id" {
  description = "Hosted zone ID of the CloudFront distribution (defaults to CloudFront's global hosted zone ID)"
  type        = string
  default     = "Z2FDTNDATAQYW2" # CloudFront's hosted zone ID
}


