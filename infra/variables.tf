# Agentic Retail OS - Variables

variable "environment" {
  description = "Environment name (dev, test, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "Environment must be one of: dev, test, prod"
  }
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "web_bucket_name" {
  description = "S3 bucket name for web application"
  type        = string
}

variable "images_bucket_name" {
  description = "S3 bucket name for product images"
  type        = string
}

variable "web_distribution_name" {
  description = "CloudFront distribution name for web application"
  type        = string
}

variable "images_distribution_name" {
  description = "CloudFront distribution name for product images"
  type        = string
}

variable "log_bucket_name" {
  description = "S3 bucket name for access logs (optional)"
  type        = string
  default     = ""
}

variable "base_domain" {
  description = "Base domain name (optional, for Route53)"
  type        = string
  default     = ""
}

variable "hosted_zone_id" {
  description = "Route53 hosted zone ID (optional)"
  type        = string
  default     = ""
}

variable "create_certificate" {
  description = "Create ACM certificate (optional)"
  type        = bool
  default     = false
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

