# S3 Module - Web Application Bucket

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_s3_bucket" "web" {
  bucket = var.bucket_name

  tags = merge(
    var.tags,
    {
      Name = var.bucket_name
    }
  )
}

resource "aws_s3_bucket_versioning" "web" {
  bucket = aws_s3_bucket.web.id

  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Disabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "web" {
  count = var.enable_encryption ? 1 : 0

  bucket = aws_s3_bucket.web.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_public_access_block" "web" {
  bucket = aws_s3_bucket.web.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_logging" "web" {
  count = var.enable_logging && var.log_bucket_name != "" ? 1 : 0

  bucket = aws_s3_bucket.web.id

  target_bucket = var.log_bucket_name
  target_prefix = "s3-access-logs/${var.bucket_name}/"
}

# S3 bucket policy is created in main.tf after CloudFront distribution is created
# This ensures we can use the specific distribution ARN instead of a wildcard
# The policy is created as a separate resource in main.tf to avoid circular dependencies

