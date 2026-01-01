# API Gateway Module - REST API for Agentic Retail OS

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# REST API
resource "aws_apigatewayv2_api" "main" {
  name          = "${var.environment}-agentic-retail-os-api"
  protocol_type = "HTTP"
  description   = "API Gateway for Agentic Retail OS"

  cors_configuration {
    allow_origins = ["*"]  # Configure appropriately for production
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["content-type", "authorization"]
    max_age       = 300
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-agentic-retail-os-api"
    }
  )
}

# Default Stage
resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
    })
  }

  tags = var.tags
}

# CloudWatch Log Group for API Gateway
resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/apigateway/${var.environment}-agentic-retail-os"
  retention_in_days = 7

  tags = var.tags
}

