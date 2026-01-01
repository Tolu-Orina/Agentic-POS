variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "enable_versioning" {
  description = "Enable versioning on the bucket"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Enable encryption on the bucket"
  type        = bool
  default     = true
}

variable "enable_logging" {
  description = "Enable access logging"
  type        = bool
  default     = true
}

variable "log_bucket_name" {
  description = "Name of the bucket for access logs (used for count condition - must be known at plan time)"
  type        = string
  default     = ""
}

variable "log_bucket_id" {
  description = "ID of the bucket for access logs (can use module output - used for target_bucket)"
  type        = string
  default     = ""
}

variable "tags" {
  description = "Tags to apply to resources"
  type        = map(string)
  default     = {}
}

