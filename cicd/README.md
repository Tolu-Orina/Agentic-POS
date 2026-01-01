# CI/CD Pipeline for Agentic Retail OS

This directory contains the CI/CD pipeline configuration for deploying the Agentic Retail OS infrastructure and web application.

## Files

- `pipeline.yaml` - CloudFormation template for CodePipeline and CodeBuild projects
- `buildspec-validate.yml` - Terraform validation buildspec
- `buildspec-plan.yml` - Terraform plan buildspec
- `buildspec-deploy.yml` - Terraform deploy buildspec

## Setup

1. **Create GitHub Connection** (one-time):
   - Go to AWS CodeStar Connections console
   - Create a new connection to GitHub
   - Note the connection ARN

2. **Deploy Pipeline**:
   ```bash
   aws cloudformation create-stack \
     --stack-name agentic-retail-os-pipeline \
     --template-body file://cicd/pipeline.yaml \
     --parameters \
       ParameterKey=GitHubOwner,ParameterValue=your-github-username \
       ParameterKey=GitHubRepo,ParameterValue=agentic-retail-os \
       ParameterKey=GitHubConnectionArn,ParameterValue=arn:aws:codestar-connections:...
     --capabilities CAPABILITY_NAMED_IAM
   ```

3. **Update Variables**:
   - Edit `pipeline.yaml` parameters as needed
   - Update buildspec paths if your directory structure differs

## Pipeline Stages

1. **Source** - Pulls code from GitHub `develop` branch
2. **Terraform Validate** - Runs `terraform fmt`, `validate`, and `tflint`
3. **Terraform Plan** - Creates Terraform execution plan
4. **Terraform Deploy** - Applies infrastructure changes
5. **Web App Build** - Builds and deploys React app to S3

## Buildspecs

Buildspecs are located in the `infra/` directory and referenced by the pipeline:
- `infra/buildspec-validate.yml`
- `infra/buildspec-plan.yml`
- `infra/buildspec-deploy.yml`

## Notes

- The pipeline uses environment-specific Terraform state files
- Backend configuration is in `infra/environments/{env}/backend.tf`
- Environment variables are set via `TF_VAR_environment` in CodeBuild

