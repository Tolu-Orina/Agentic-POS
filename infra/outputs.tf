# Agentic Retail OS - Outputs

output "web_bucket_id" {
  description = "S3 bucket ID for web application"
  value       = module.s3_web.bucket_id
}

output "web_bucket_arn" {
  description = "S3 bucket ARN for web application"
  value       = module.s3_web.bucket_arn
}

output "images_bucket_id" {
  description = "S3 bucket ID for product images"
  value       = module.s3_images.bucket_id
}

output "images_bucket_arn" {
  description = "S3 bucket ARN for product images"
  value       = module.s3_images.bucket_arn
}

output "cloudfront_web_distribution_id" {
  description = "CloudFront distribution ID for web application"
  value       = module.cloudfront_web.distribution_id
}

output "cloudfront_web_domain_name" {
  description = "CloudFront domain name for web application"
  value       = module.cloudfront_web.distribution_domain_name
}

output "web_domain_name" {
  description = "Custom domain name for web application (if configured)"
  value       = var.base_domain != "" ? (var.environment == "prod" ? var.base_domain : "${var.environment}.${var.base_domain}") : module.cloudfront_web.distribution_domain_name
}

output "cloudfront_images_distribution_id" {
  description = "CloudFront distribution ID for product images"
  value       = module.cloudfront_images.distribution_id
}

output "cloudfront_images_domain_name" {
  description = "CloudFront domain name for product images"
  value       = module.cloudfront_images.distribution_domain_name
}

output "api_gateway_url" {
  description = "API Gateway endpoint URL"
  value       = module.api_gateway.api_url
}

output "api_gateway_id" {
  description = "API Gateway ID"
  value       = module.api_gateway.api_id
}

output "lambda_inventory_function_arn" {
  description = "Lambda inventory service function ARN"
  value       = module.lambda_inventory.function_arn
}

output "lambda_auth_function_arn" {
  description = "Lambda auth service function ARN"
  value       = module.lambda_auth.function_arn
}

output "dynamodb_products_table_name" {
  description = "DynamoDB Products table name"
  value       = module.dynamodb.products_table_name
}

output "dynamodb_transactions_table_name" {
  description = "DynamoDB Transactions table name"
  value       = module.dynamodb.transactions_table_name
}

output "acm_certificate_arn" {
  description = "ACM certificate ARN (if created)"
  value       = var.base_domain != "" && var.create_certificate && length(module.acm_web) > 0 ? module.acm_web[0].certificate_arn : ""
}

