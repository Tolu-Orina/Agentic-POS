# Agentic Retail OS - Main Terraform Configuration

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = "~> 5.0"
      configuration_aliases = [aws.us_east_1]
    }
  }

  # Backend configuration - values are overridden by -backend-config flags in buildspecs
  # This allows the same configuration to work across different environments
  backend "s3" {
    # These values will be overridden by -backend-config flags:
    # -backend-config="bucket=agentic-retail-os-terraform-state"
    # -backend-config="key=${TF_VAR_environment}/terraform.tfstate"
    # -backend-config="region=us-east-1"
    # -backend-config="encrypt=true"
    # -backend-config="dynamodb_table=agentic-retail-os-terraform-locks"
  }
}

# Default provider (uses aws_region variable)
provider "aws" {
  region = var.aws_region
}

# Provider alias for us-east-1 (required for ACM certificates used by CloudFront)
provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
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

# S3 Module - Log Bucket (if logging is enabled)
module "s3_logs" {
  source = "./modules/s3"

  count = var.log_bucket_name != "" ? 1 : 0

  bucket_name       = var.log_bucket_name
  enable_versioning = false
  enable_encryption = true
  enable_logging    = false # Log bucket doesn't log to itself
  log_bucket_name   = ""
  tags              = local.common_tags
}

# S3 Module - Web Application
module "s3_web" {
  source = "./modules/s3"

  bucket_name       = var.web_bucket_name
  enable_versioning = true
  enable_encryption = true
  enable_logging    = var.log_bucket_name != "" ? true : false
  log_bucket_name   = var.log_bucket_name # Use input variable for count, module output will be used in resource
  log_bucket_id     = var.log_bucket_name != "" && length(module.s3_logs) > 0 ? module.s3_logs[0].bucket_id : var.log_bucket_name
  tags              = local.common_tags

  depends_on = [module.s3_logs]
}

# S3 Module - Product Images
module "s3_images" {
  source = "./modules/s3"

  bucket_name       = var.images_bucket_name
  enable_versioning = false
  enable_encryption = true
  enable_logging    = var.log_bucket_name != "" ? true : false
  log_bucket_name   = var.log_bucket_name # Use input variable for count, module output will be used in resource
  log_bucket_id     = var.log_bucket_name != "" && length(module.s3_logs) > 0 ? module.s3_logs[0].bucket_id : var.log_bucket_name
  tags              = local.common_tags

  depends_on = [module.s3_logs]
}

# ACM Module - SSL Certificate for Web Application (if domain provided)
module "acm_web" {
  source = "./modules/acm"
  providers = {
    aws.us_east_1 = aws.us_east_1
  }

  count = var.base_domain != "" && var.create_certificate ? 1 : 0

  domain_name               = var.base_domain != "" ? (var.environment == "prod" ? var.base_domain : "${var.environment}.${var.base_domain}") : ""
  subject_alternative_names = []
  hosted_zone_id            = var.hosted_zone_id
  wait_for_validation       = true
  tags                      = local.common_tags
}

# CloudFront Module - Web Application
module "cloudfront_web" {
  source = "./modules/cloudfront"

  distribution_name     = var.web_distribution_name
  s3_bucket_id          = module.s3_web.bucket_id
  s3_bucket_domain_name = module.s3_web.bucket_regional_domain_name
  domain_name           = var.base_domain != "" ? (var.environment == "prod" ? var.base_domain : "${var.environment}.${var.base_domain}") : ""
  certificate_arn       = var.base_domain != "" && var.create_certificate && length(module.acm_web) > 0 ? module.acm_web[0].certificate_arn : ""
  environment           = local.environment
  tags                  = local.common_tags
}

# CloudFront Module - Product Images
module "cloudfront_images" {
  source = "./modules/cloudfront"

  distribution_name     = var.images_distribution_name
  s3_bucket_id          = module.s3_images.bucket_id
  s3_bucket_domain_name = module.s3_images.bucket_regional_domain_name
  domain_name           = "" # Images don't need custom domain
  certificate_arn       = ""
  environment           = local.environment
  tags                  = local.common_tags
}

# Route53 Module - DNS Records for Web Application
module "route53_web" {
  source = "./modules/route53"

  count = var.base_domain != "" && var.hosted_zone_id != "" ? 1 : 0

  domain_name               = var.environment == "prod" ? var.base_domain : "${var.environment}.${var.base_domain}"
  hosted_zone_id            = var.hosted_zone_id
  cloudfront_domain_name    = module.cloudfront_web.distribution_domain_name
  cloudfront_hosted_zone_id = "Z2FDTNDATAQYW2" # CloudFront's global hosted zone ID
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

  function_name  = "${var.environment}-inventory-service"
  code_directory = "inventory"
  handler        = "lambda_function.handler"
  runtime        = "python3.13"
  environment    = local.environment
  tags           = local.common_tags

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

  function_name  = "${var.environment}-auth-service"
  code_directory = "auth"
  handler        = "lambda_function.handler"
  runtime        = "python3.13"
  environment    = local.environment
  tags           = local.common_tags
}

# IAM Module
module "iam" {
  source = "./modules/iam"

  name_prefix                 = "agentic-retail-os-${local.environment}"
  s3_bucket_arn               = module.s3_web.bucket_arn
  cloudfront_distribution_id  = module.cloudfront_web.distribution_id
  cloudfront_distribution_arn = module.cloudfront_web.distribution_arn
  tags                        = local.common_tags
}

