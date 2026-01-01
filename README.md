# Agentic Retail OS

An AI-powered Point-of-Sale (POS) system built with AWS Strands agents, providing intelligent checkout, autonomous inventory management, and natural language analytics.

## 🎯 Overview

Agentic Retail OS transforms traditional POS systems into intelligent, autonomous business management tools. The platform leverages AWS Strands agents to provide:

- **Intelligent Checkout**: AI-powered transaction processing with real-time inventory verification
- **Autonomous Operations**: Background agents monitor stock levels and generate restock requests
- **Natural Language Interface**: Query business data using conversational language
- **Multi-Agent Coordination**: Specialized agents work together seamlessly

## 🏗️ Architecture

### Article 1: Smart Clerk (Current)
- Single-agent system for intelligent checkout
- Real-time inventory verification
- Receipt generation
- Transaction management
- Basic reporting

### Article 2: Store Management Team (Planned)
- Multi-agent system with specialized roles
- Autonomous inventory management
- Natural language analytics
- Invoice generation

### Article 3: Enterprise Platform (Planned)
- Production-grade security and observability
- Cross-agent communication
- Advanced compliance and audit

## 📁 Project Structure

```
.
├── docs/                    # Product and technical documentation
├── infra/                   # Terraform infrastructure as code
│   ├── modules/            # Reusable Terraform modules
│   └── environments/       # Environment-specific configs (dev/test/prod)
├── cicd/                    # CI/CD pipeline configuration
├── web/                     # React frontend application
├── Part 1 - Simple Clerk/   # Clerk agent implementation
├── scripts/                 # Data transformation and image generation
└── datasets/                # Sample retail data
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Python 3.11+
- AWS CLI configured
- Terraform 1.6.0+
- AWS Account with appropriate permissions

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd POS-App
   ```

2. **Set up the web application**
   ```bash
   cd web
   npm install
   npm run dev
   ```
   The app will be available at `http://localhost:5173`

3. **Set up Python environment**
   ```bash
   cd scripts
   pip install -r requirements.txt
   ```

4. **Prepare sample data** (optional)
   ```bash
   python scripts/transform_data.py
   python scripts/generate_images.py
   python scripts/convert_csv_to_json.py
   ```

### Infrastructure Deployment

1. **Create Terraform backend** (one-time)
   ```bash
   aws s3 mb s3://agentic-retail-os-terraform-state --region us-east-1
   aws dynamodb create-table \
     --table-name agentic-retail-os-terraform-locks \
     --attribute-definitions AttributeName=LockID,AttributeType=S \
     --key-schema AttributeName=LockID,KeyType=HASH \
     --billing-mode PAY_PER_REQUEST \
     --region us-east-1
   ```

2. **Deploy infrastructure**
   ```bash
   cd infra/environments/dev
   terraform init
   terraform plan
   terraform apply
   ```

3. **Deploy CI/CD pipeline**
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

## 🛠️ Technology Stack

### Frontend
- React 19 + TypeScript
- Vite 7
- Material UI v5
- React Router v6

### Backend
- AWS Lambda (Node.js 20.x / Python 3.11)
- API Gateway (HTTP API)
- DynamoDB
- AWS Strands SDK v1.0

### Infrastructure
- Terraform
- AWS CodePipeline
- AWS CodeBuild
- S3 + CloudFront

### AI/Agents
- AWS Strands SDK
- Amazon Bedrock (Nova, Claude)
- Amazon Bedrock Nova Canvas (image generation)

## 📚 Documentation

- [Product Overview](docs/01-product-overview.md)
- [Technical Architecture](docs/02-technical-architecture-design.md)
- [UI/UX Design](docs/03-ui-ux-design.md)
- [Infrastructure Setup](INFRASTRUCTURE_SETUP.md)
- [CI/CD Pipeline](cicd/README.md)
- [Infrastructure Guide](infra/README.md)

## 🔧 Development

### Web Application
```bash
cd web
npm run dev      # Start dev server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Data Scripts
```bash
cd scripts
python transform_data.py        # Transform raw data to normalized format
python generate_images.py       # Generate product images via Bedrock
python convert_csv_to_json.py  # Convert CSV to JSON for local dev
```

### Infrastructure
```bash
cd infra/environments/dev
terraform init    # Initialize Terraform
terraform plan    # Preview changes
terraform apply   # Deploy infrastructure
```

## 📋 Environment Variables

### Web Application
Create `web/.env`:
```env
VITE_API_BASE_URL=https://your-api-gateway-url.execute-api.us-east-1.amazonaws.com
```

### AWS Configuration
Ensure AWS credentials are configured:
```bash
aws configure
```

## 🧪 Testing

### Local Testing
- Web app uses mock data from `web/src/data/`
- Product images served from `web/public/images/`
- All agent interactions are simulated

### Integration Testing
- Deploy infrastructure to dev environment
- Connect web app to real API endpoints
- Test with actual DynamoDB data

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📞 Support

[Add support information here]

