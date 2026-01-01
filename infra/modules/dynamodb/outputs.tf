output "products_table_name" {
  description = "Name of the Products table"
  value       = aws_dynamodb_table.products.name
}

output "products_table_arn" {
  description = "ARN of the Products table"
  value       = aws_dynamodb_table.products.arn
}

output "transactions_table_name" {
  description = "Name of the Transactions table"
  value       = aws_dynamodb_table.transactions.name
}

output "transactions_table_arn" {
  description = "ARN of the Transactions table"
  value       = aws_dynamodb_table.transactions.arn
}

output "inventory_logs_table_name" {
  description = "Name of the Inventory_Logs table"
  value       = aws_dynamodb_table.inventory_logs.name
}

output "inventory_logs_table_arn" {
  description = "ARN of the Inventory_Logs table"
  value       = aws_dynamodb_table.inventory_logs.arn
}

output "restock_requests_table_name" {
  description = "Name of the Restock_Requests table"
  value       = aws_dynamodb_table.restock_requests.name
}

output "restock_requests_table_arn" {
  description = "ARN of the Restock_Requests table"
  value       = aws_dynamodb_table.restock_requests.arn
}

output "invoices_table_name" {
  description = "Name of the Invoices table"
  value       = aws_dynamodb_table.invoices.name
}

output "invoices_table_arn" {
  description = "ARN of the Invoices table"
  value       = aws_dynamodb_table.invoices.arn
}

