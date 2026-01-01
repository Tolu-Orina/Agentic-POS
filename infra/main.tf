# Agentic Retail OS - Main Terraform Configuration

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Local variables
locals {
  environment = var.environment
  common_tags = merge(
    var.tags,
    {
      Project     = "AgenticRetailOS"
      Environment = local.environment
      ManagedBy   = "Terraform"
    }
  )
}

# DynamoDB Module
module "dynamodb" {
  source = "./modules/dynamodb"

  environment = local.environment
  tags        = local.common_tags
}

# S3 Module - Web Application
module "s3_web" {
  source = "./modules/s3"

  bucket_name       = var.web_bucket_name
  enable_versioning = true
  enable_encryption  = true
  enable_logging    = var.log_bucket_name != "" ? true : false
  log_bucket_name   = var.log_bucket_name
  tags              = local.common_tags
}

# S3 Module - Product Images
module "s3_images" {
  source = "./modules/s3"

  bucket_name       = var.images_bucket_name
  enable_versioning = false
  enable_encryption  = true
  enable_logging    = var.log_bucket_name != "" ? true : false
  log_bucket_name   = var.log_bucket_name
  tags              = local.common_tags
}

# CloudFront Module - Web Application
module "cloudfront_web" {
  source = "./modules/cloudfront"

  distribution_name = var.web_distribution_name
  bucket_id         = module.s3_web.bucket_id
  bucket_arn        = module.s3_web.bucket_arn
  bucket_domain     = module.s3_web.bucket_regional_domain_name
  tags              = local.common_tags
}

# CloudFront Module - Product Images
module "cloudfront_images" {
  source = "./modules/cloudfront"

  distribution_name = var.images_distribution_name
  bucket_id         = module.s3_images.bucket_id
  bucket_arn        = module.s3_images.bucket_arn
  bucket_domain     = module.s3_images.bucket_regional_domain_name
  tags              = local.common_tags
}

# API Gateway Module
module "api_gateway" {
  source = "./modules/api-gateway"

  environment = local.environment
  tags        = local.common_tags
}

# Lambda Module - Inventory Service
module "lambda_inventory" {
  source = "./modules/lambda"

  function_name = "${var.environment}-inventory-service"
  handler       = "index.handler"
  runtime       = "python3.11"
  environment   = local.environment
  tags          = local.common_tags

  # DynamoDB permissions
  dynamodb_table_arns = [
    module.dynamodb.products_table_arn,
    module.dynamodb.transactions_table_arn,
    module.dynamodb.inventory_logs_table_arn
  ]
}

# Lambda Module - Auth Service
module "lambda_auth" {
  source = "./modules/lambda"

  function_name = "${var.environment}-auth-service"
  handler       = "index.handler"
  runtime       = "nodejs20.x"
  environment   = local.environment
  tags          = local.common_tags
}

# IAM Module
module "iam" {
  source = "./modules/iam"

  environment = local.environment
  tags        = local.common_tags
}

