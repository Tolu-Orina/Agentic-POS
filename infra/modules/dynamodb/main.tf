# DynamoDB Module - All Tables for Agentic Retail OS

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Products Table
resource "aws_dynamodb_table" "products" {
  name           = "${var.environment}-Products"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "sku"

  attribute {
    name = "sku"
    type = "S"
  }

  attribute {
    name = "category"
    type = "S"
  }

  global_secondary_index {
    name     = "category-index"
    hash_key = "category"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-Products"
    }
  )
}

# Transactions Table
resource "aws_dynamodb_table" "transactions" {
  name           = "${var.environment}-Transactions"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "transaction_id"
  range_key      = "timestamp"

  attribute {
    name = "transaction_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "date"
    type = "S"
  }

  global_secondary_index {
    name            = "user-date-index"
    hash_key        = "user_id"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "date-index"
    hash_key        = "date"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-Transactions"
    }
  )
}

# Inventory_Logs Table
resource "aws_dynamodb_table" "inventory_logs" {
  name           = "${var.environment}-Inventory_Logs"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "log_id"
  range_key      = "timestamp"

  attribute {
    name = "log_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "product_sku"
    type = "S"
  }

  global_secondary_index {
    name            = "product-time-index"
    hash_key        = "product_sku"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-Inventory_Logs"
    }
  )
}

# Restock_Requests Table
resource "aws_dynamodb_table" "restock_requests" {
  name           = "${var.environment}-Restock_Requests"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "request_id"

  attribute {
    name = "request_id"
    type = "S"
  }

  attribute {
    name = "status"
    type = "S"
  }

  attribute {
    name = "product_sku"
    type = "S"
  }

  global_secondary_index {
    name            = "status-index"
    hash_key        = "status"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "product-index"
    hash_key        = "product_sku"
    projection_type = "ALL"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-Restock_Requests"
    }
  )
}

# Invoices Table (Article 2)
resource "aws_dynamodb_table" "invoices" {
  name           = "${var.environment}-Invoices"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "invoice_id"

  attribute {
    name = "invoice_id"
    type = "S"
  }

  tags = merge(
    var.tags,
    {
      Name = "${var.environment}-Invoices"
    }
  )
}

