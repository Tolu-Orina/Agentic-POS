variable "function_name" {
  description = "Name of the Lambda function"
  type        = string
}

variable "code_directory" {
  description = "Subdirectory name under code/ containing the Lambda function code (e.g., 'inventory', 'auth')"
  type        = string
  default     = ""
}

variable "handler" {
  description = "Lambda handler"
  type        = string
}

variable "runtime" {
  description = "Lambda runtime"
  type        = string
}

variable "timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 30
}

variable "memory_size" {
  description = "Lambda memory size in MB"
  type        = number
  default     = 128
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "environment_variables" {
  description = "Environment variables for Lambda"
  type        = map(string)
  default     = {}
}

variable "dynamodb_table_arns" {
  description = "List of DynamoDB table ARNs for IAM permissions"
  type        = list(string)
  default     = []
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

