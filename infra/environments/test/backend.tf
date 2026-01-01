# Backend configuration for Test environment

terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    bucket         = "agentic-retail-os-terraform-state"
    key            = "test/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "agentic-retail-os-terraform-locks"
  }
}

