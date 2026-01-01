# Data Transformation Scripts

## Overview
Scripts for transforming the UCI Online Retail dataset into DynamoDB-ready format for the Agentic Retail OS.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Scripts

### transform_data.py
Transforms the raw Excel file into normalized CSV files ready for DynamoDB import.

**Usage:**
```bash
cd scripts
python transform_data.py
```

**Input:**
- `../datasets/uci-retail/Online Retail.xlsx`

**Output:**
- `../datasets/uci-retail/Online_Retail_Raw.csv` - Raw CSV conversion
- `../datasets/uci-retail/products_catalog.csv` - Product catalog (ready for DynamoDB)
- `../datasets/uci-retail/transactions_history.csv` - Transaction history (ready for DynamoDB)

**What it does:**
1. Converts Excel to CSV
2. Extracts unique products (top 50 by sales frequency)
3. Normalizes product names (Title Case)
4. Infers categories from descriptions
5. Simulates stock levels and reorder thresholds
6. Groups transactions by InvoiceNo
7. Calculates totals, tax, and line items
8. Validates and normalizes all data

**Configuration:**
Edit the script to adjust:
- `TAX_RATE` - Tax percentage (default: 0.08 = 8%)
- `DATE_SHIFT_DAYS` - Shift dates forward (default: 0 = keep original)
- Number of products selected (currently top 50)

### generate_images.py
Generates product images using AWS Bedrock Nova Canvas API with automatic throttling handling.

**Prerequisites:**
- AWS credentials configured (via `~/.aws/credentials` or environment variables)
- AWS Bedrock access enabled in your AWS account
- Nova Canvas model available in your region

**Usage:**
```bash
cd scripts
python generate_images.py
```

**Configuration:**
Edit the script to adjust:
- `BEDROCK_REGION` - AWS region (default: 'us-east-1')
- `BASE_DELAY_SECONDS` - Delay between requests (default: 2.5)
- `THUMBNAIL_WIDTH/HEIGHT` - Image dimensions (default: 512x512)
- `IMAGE_QUALITY` - JPEG quality (default: 85)

**Input:**
- `../datasets/uci-retail/products_catalog.csv`

**Output:**
- `../datasets/uci-retail/product_images/{sku}.jpg` - Generated thumbnail images
- `../datasets/uci-retail/products_catalog_with_images.csv` - Updated CSV with image paths
- `../datasets/uci-retail/image_generation.log` - Generation log
- `../datasets/uci-retail/failed_images.txt` - Failed SKUs for retry

**Features:**
- Sequential API calls with rate limiting
- Exponential backoff with jitter for throttling
- Thumbnail generation (512x512 by default)
- Resume capability (skips existing images)
- Progress tracking and error handling

**Throttling Handling:**
- Automatic retry with exponential backoff (1s → 2s → 4s → 8s → 16s)
- Jitter added to prevent synchronized retries
- Client-side rate limiting (2.5s delay between requests)
- Logs all throttling events for monitoring

## Next Steps

After running `transform_data.py`:
1. Review the generated CSV files
2. Run `generate_images.py` to create product images
3. Upload images to S3 bucket
4. Update CSV with S3 URLs (or use local paths)
5. Import to DynamoDB using NoSQL Workbench

