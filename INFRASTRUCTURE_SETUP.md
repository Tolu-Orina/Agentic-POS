# Infrastructure Setup Summary

## ✅ Created Structure

### 1. CI/CD Pipeline (`cicd/`)
- **pipeline.yaml** - CloudFormation template for CodePipeline
  - Dev pipeline (develop branch)
  - CodeBuild projects for Terraform (validate, plan, deploy)
  - CodeBuild project for web app deployment
  - IAM roles and permissions

- **buildspec-validate.yml** - Terraform validation (fmt, validate, tflint)
- **buildspec-plan.yml** - Terraform plan generation
- **buildspec-deploy.yml** - Terraform apply and CloudFront invalidation

### 2. Infrastructure (`infra/`)

#### Main Configuration
- **main.tf** - Orchestrates all modules
- **variables.tf** - Input variables
- **outputs.tf** - Output values

#### Modules Created
1. **dynamodb/** - All DynamoDB tables:
   - Products (with category-index GSI)
   - Transactions (with user-date-index and date-index GSIs)
   - Inventory_Logs (with product-time-index GSI)
   - Restock_Requests (with status-index and product-index GSIs)
   - Invoices

2. **s3/** - S3 buckets (copied from sample-deploys):
   - Web application bucket
   - Product images bucket
   - Versioning, encryption, logging

3. **cloudfront/** - CloudFront distributions (copied from sample-deploys):
   - Web application CDN
   - Product images CDN
   - Origin Access Control (OAC)

4. **api-gateway/** - HTTP API Gateway:
   - REST API with CORS
   - Default stage
   - CloudWatch logging

5. **lambda/** - Lambda functions:
   - Inventory service (Python 3.11)
   - Auth service (Node.js 20.x)
   - IAM roles with DynamoDB permissions
   - CloudWatch log groups

6. **iam/** - IAM roles and policies (copied from sample-deploys)

#### Environments
- **dev/** - Development environment
- **test/** - Test environment  
- **prod/** - Production environment

Each environment has:
- `backend.tf` - Terraform state backend configuration
- `terraform.tfvars` - Environment-specific variables

## 📋 Next Steps

### 1. Create Terraform Backend Resources (One-time)
Before running Terraform, create the S3 bucket and DynamoDB table for state:

```bash
# Create S3 bucket for Terraform state
aws s3 mb s3://agentic-retail-os-terraform-state --region us-east-1

# Create DynamoDB table for state locking
aws dynamodb create-table \
  --table-name agentic-retail-os-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### 2. Initialize Terraform
```bash
cd infra/environments/dev
terraform init
```

### 3. Plan Infrastructure
```bash
terraform plan
```

### 4. Deploy Infrastructure
```bash
terraform apply
```

### 5. Deploy CI/CD Pipeline
```bash
aws cloudformation create-stack \
  --stack-name agentic-retail-os-pipeline \
  --template-body file://cicd/pipeline.yaml \
  --parameters \
    ParameterKey=GitHubOwner,ParameterValue=YOUR_GITHUB_USERNAME \
    ParameterKey=GitHubRepo,ParameterValue=YOUR_REPO_NAME \
    ParameterKey=GitHubConnectionArn,ParameterValue=YOUR_CONNECTION_ARN \
  --capabilities CAPABILITY_NAMED_IAM
```

## 🔧 Configuration Notes

### Backend State
- **Bucket**: `agentic-retail-os-terraform-state`
- **Lock Table**: `agentic-retail-os-terraform-locks`
- **State Keys**: `{environment}/terraform.tfstate`

### S3 Buckets
- **Web**: `agentic-retail-os-web-{env}`
- **Images**: `agentic-retail-os-images-{env}`
- **Logs**: `agentic-retail-os-logs-{env}` (optional)

### CloudFront Distributions
- **Web**: `agentic-retail-os-web-{env}`
- **Images**: `agentic-retail-os-images-{env}`

### DynamoDB Tables
- All tables use **PAY_PER_REQUEST** billing
- Table names: `{environment}-{TableName}`

### Lambda Functions
- **Inventory Service**: `{environment}-inventory-service`
- **Auth Service**: `{environment}-auth-service`
- Functions use placeholder code (deploy via CI/CD)

## ⚠️ Important Notes

1. **Clerk Agent**: Infrastructure for the clerk agent (Lambda Container/ECR) is **NOT** included - you'll handle that separately.

2. **API Gateway Integration**: Lambda functions are created but not yet integrated with API Gateway routes. You'll need to:
   - Create API routes in `infra/modules/api-gateway/main.tf`
   - Add Lambda integrations
   - Configure CORS properly

3. **Environment Variables**: Update `terraform.tfvars` files with your actual values:
   - Domain names (if using Route53)
   - Bucket names (must be globally unique)
   - Region settings

4. **CI/CD Setup**: 
   - Create GitHub connection in AWS CodeStar Connections first
   - Update pipeline.yaml with your GitHub details
   - Buildspecs reference `cicd/` directory

## 📚 Documentation

- `cicd/README.md` - CI/CD pipeline documentation
- `infra/README.md` - Infrastructure documentation
- `docs/02-technical-architecture-design.md` - Architecture details

