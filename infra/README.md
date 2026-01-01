# Infrastructure as Code - Agentic Retail OS

Terraform modules and configurations for deploying the Agentic Retail OS infrastructure.

## Structure

```
infra/
├── main.tf                 # Main Terraform configuration
├── variables.tf            # Input variables
├── outputs.tf             # Output values
├── modules/               # Reusable Terraform modules
│   ├── dynamodb/          # DynamoDB tables
│   ├── s3/                # S3 buckets (web + images)
│   ├── cloudfront/         # CloudFront distributions
│   ├── api-gateway/       # API Gateway REST API
│   ├── lambda/            # Lambda functions
│   └── iam/               # IAM roles and policies
└── environments/          # Environment-specific configs
    ├── dev/
    ├── test/
    └── prod/
```

## Modules

### DynamoDB
Creates all required tables:
- `Products` - Product catalog
- `Transactions` - Transaction history
- `Inventory_Logs` - Inventory change logs
- `Restock_Requests` - Restock requests (Article 2)
- `Invoices` - Invoices (Article 2)

### S3
Creates S3 buckets for:
- Web application static hosting
- Product images storage

### CloudFront
Creates CDN distributions for:
- Web application
- Product images

### API Gateway
Creates HTTP API with:
- CORS configuration
- CloudWatch logging
- Default stage

### Lambda
Creates Lambda functions with:
- IAM roles and permissions
- DynamoDB access (if configured)
- CloudWatch log groups

## Usage

### Initialize Terraform

```bash
cd infra/environments/dev
terraform init
```

### Plan Changes

```bash
terraform plan
```

### Apply Changes

```bash
terraform apply
```

### Environment Variables

Set via `terraform.tfvars` in each environment directory:
- `dev/terraform.tfvars`
- `test/terraform.tfvars`
- `prod/terraform.tfvars`

## Backend Configuration

Each environment has its own backend configuration in `backend.tf`:
- State bucket: `agentic-retail-os-terraform-state`
- State key: `{environment}/terraform.tfstate`
- Lock table: `agentic-retail-os-terraform-locks`

## Notes

- All tables use **PAY_PER_REQUEST** billing mode
- Lambda functions use placeholder code (deployed via CI/CD)
- API Gateway endpoints need to be configured with Lambda integrations
- Clerk agent infrastructure is handled separately (not in this repo)

