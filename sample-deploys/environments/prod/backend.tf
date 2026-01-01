# Backend configuration for Production environment
# Uses environment-specific state file key to separate state per environment

terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    bucket         = "umcp-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "umcp-terraform-locks"
  }
}

