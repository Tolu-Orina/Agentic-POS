"""
Image Generation Script for Agentic Retail OS
Generates product images using AWS Bedrock Nova Canvas API.

Features:
- Sequential API calls with rate limiting
- Exponential backoff with jitter for throttling
- Thumbnail generation (configurable dimensions)
- Progress tracking and error handling
- Resume capability (skip existing images)
- CSV update with local file paths
"""

import pandas as pd
import boto3
import json
import base64
import io
import os
import time
import random
import logging
from datetime import datetime
from PIL import Image
from botocore.config import Config
from botocore.exceptions import ClientError

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# AWS Configuration
BEDROCK_REGION = 'us-east-1'  # Change if needed
MODEL_ID = 'amazon.nova-canvas-v1:0'

# Rate Limiting Configuration
BASE_DELAY_SECONDS = 2.5  # Delay between requests
MAX_RETRIES = 5  # Maximum retries for throttling
INITIAL_BACKOFF = 1.0  # Initial backoff in seconds

# Image Configuration
THUMBNAIL_WIDTH = 512
THUMBNAIL_HEIGHT = 512
OUTPUT_FORMAT = 'PNG'  # PNG for better quality and transparency support

# File Paths
INPUT_CSV = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail', 'products_catalog.csv')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail', 'product_images')
OUTPUT_CSV = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail', 'products_catalog_with_images.csv')
LOG_FILE = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail', 'image_generation.log')
FAILED_FILE = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail', 'failed_images.txt')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ImageError(Exception):
    """Custom exception for errors returned by Amazon Nova Canvas"""
    def __init__(self, message):
        self.message = message


def create_output_directory():
    """Create output directory for images if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    logger.info(f"Output directory: {OUTPUT_DIR}")


def generate_prompt(product_name, description=None, category=None):
    """
    Generate a prompt for image generation from product information.
    
    Args:
        product_name: Product name
        description: Product description (optional)
        category: Product category (optional)
    
    Returns:
        str: Generated prompt (max 1024 characters)
    """
    # Base prompt template
    base_prompt = f"Professional product photography of {product_name}"
    
    # Add description if available
    if description and description.strip() and description.upper() != product_name.upper():
        # Clean description (remove ALL CAPS formatting)
        desc_clean = description.strip()
        if len(desc_clean) > 100:
            desc_clean = desc_clean[:100] + "..."
        base_prompt += f", {desc_clean}"
    
    # Add category context if available
    if category:
        base_prompt += f", {category} product"
    
    # Add style instructions
    base_prompt += ", white background, retail product image, high quality, clean lighting, e-commerce style, product photography"
    
    # Ensure prompt doesn't exceed 1024 characters
    if len(base_prompt) > 1024:
        base_prompt = base_prompt[:1020] + "..."
    
    return base_prompt


def generate_image_with_retry(bedrock_client, prompt, max_retries=MAX_RETRIES):
    """
    Generate an image using Amazon Nova Canvas with exponential backoff retry logic.
    
    Args:
        bedrock_client: Boto3 Bedrock runtime client
        prompt: Text prompt for image generation
        max_retries: Maximum number of retry attempts
    
    Returns:
        bytes: Generated image bytes
    
    Raises:
        ImageError: If image generation fails after all retries
    """
    body = json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt
        },
        "imageGenerationConfig": {
            "numberOfImages": 1,
            "height": THUMBNAIL_HEIGHT,
            "width": THUMBNAIL_WIDTH,
            "cfgScale": 8.0,
            "seed": 0
        }
    })
    
    accept = "application/json"
    content_type = "application/json"
    
    for attempt in range(max_retries):
        try:
            logger.debug(f"Attempt {attempt + 1}/{max_retries} - Generating image...")
            
            response = bedrock_client.invoke_model(
                body=body,
                modelId=MODEL_ID,
                accept=accept,
                contentType=content_type
            )
            
            response_body = json.loads(response.get("body").read())
            
            # Check for errors in response
            error = response_body.get("error")
            if error is not None:
                raise ImageError(f"Image generation error: {error}")
            
            # Extract image from response
            images = response_body.get("images")
            if not images or len(images) == 0:
                raise ImageError("No images returned in response")
            
            base64_image = images[0]
            base64_bytes = base64_image.encode('ascii')
            image_bytes = base64.b64decode(base64_bytes)
            
            logger.debug(f"Successfully generated image (size: {len(image_bytes)} bytes)")
            return image_bytes
            
        except ClientError as err:
            error_code = err.response.get("Error", {}).get("Code", "")
            error_message = err.response.get("Error", {}).get("Message", "")
            
            # Handle throttling with exponential backoff
            if error_code == "ThrottlingException" or "throttl" in error_message.lower():
                if attempt < max_retries - 1:
                    # Calculate exponential backoff with jitter
                    backoff_time = INITIAL_BACKOFF * (2 ** attempt)
                    jitter = random.uniform(0, 1)
                    wait_time = backoff_time + jitter
                    
                    logger.warning(
                        f"Throttling error (attempt {attempt + 1}/{max_retries}). "
                        f"Waiting {wait_time:.2f} seconds before retry..."
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    raise ImageError(f"Throttling error after {max_retries} attempts: {error_message}")
            
            # Handle other client errors
            else:
                raise ImageError(f"Client error: {error_code} - {error_message}")
        
        except ImageError:
            # Re-raise ImageError without retry
            raise
        
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Unexpected error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                wait_time = INITIAL_BACKOFF * (2 ** attempt) + random.uniform(0, 1)
                time.sleep(wait_time)
                continue
            else:
                raise ImageError(f"Unexpected error after {max_retries} attempts: {str(e)}")
    
    raise ImageError(f"Failed to generate image after {max_retries} attempts")


def save_image(image_bytes, sku, output_dir):
    """
    Save image bytes to file as thumbnail.
    
    Args:
        image_bytes: Image bytes from API
        sku: Product SKU for filename
        output_dir: Output directory path
    
    Returns:
        str: Path to saved image file
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGBA for PNG (supports transparency)
        if image.mode not in ('RGB', 'RGBA'):
            image = image.convert('RGBA')
        
        # Resize to thumbnail size (in case API returns different size)
        image.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), Image.Resampling.LANCZOS)
        
        # Create square image with white background if needed
        if image.size[0] != image.size[1]:
            # Create square canvas with white background
            square_size = max(image.size)
            square_image = Image.new('RGBA', (square_size, square_size), (255, 255, 255, 255))
            # Center the image
            offset = ((square_size - image.size[0]) // 2, (square_size - image.size[1]) // 2)
            square_image.paste(image, offset, image if image.mode == 'RGBA' else None)
            image = square_image
        
        # Resize to exact thumbnail dimensions
        image = image.resize((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), Image.Resampling.LANCZOS)
        
        # Convert to RGB for saving (PNG can be RGB or RGBA)
        if image.mode == 'RGBA':
            # Create white background and composite
            rgb_image = Image.new('RGB', image.size, (255, 255, 255))
            rgb_image.paste(image, mask=image.split()[3] if len(image.split()) == 4 else None)
            image = rgb_image
        
        # Save as PNG
        filename = f"{sku}.png"
        filepath = os.path.join(output_dir, filename)
        image.save(filepath, OUTPUT_FORMAT, optimize=True)
        
        file_size = os.path.getsize(filepath)
        logger.debug(f"Saved image: {filepath} ({file_size} bytes)")
        
        return filepath
        
    except Exception as e:
        raise ImageError(f"Error saving image: {str(e)}")


def process_products(products_df, bedrock_client, resume=True):
    """
    Process all products and generate images.
    
    Args:
        products_df: DataFrame with product data
        bedrock_client: Boto3 Bedrock runtime client
        resume: If True, skip products that already have images
    
    Returns:
        tuple: (successful_count, failed_count, failed_skus)
    """
    successful_count = 0
    failed_count = 0
    failed_skus = []
    
    total_products = len(products_df)
    logger.info(f"Processing {total_products} products...")
    
    for index, row in products_df.iterrows():
        sku = row['sku']
        product_name = row['name']
        description = row.get('description', '')
        category = row.get('category', '')
        
        # Check if image already exists (resume mode)
        image_path = os.path.join(OUTPUT_DIR, f"{sku}.png")
        if resume and os.path.exists(image_path):
            logger.info(f"[{index + 1}/{total_products}] Skipping {sku} - image already exists")
            continue
        
        logger.info(f"[{index + 1}/{total_products}] Generating image for {sku}: {product_name}")
        
        try:
            # Generate prompt
            prompt = generate_prompt(product_name, description, category)
            logger.debug(f"Prompt: {prompt[:100]}...")
            
            # Generate image with retry logic
            image_bytes = generate_image_with_retry(bedrock_client, prompt)
            
            # Save image
            save_image(image_bytes, sku, OUTPUT_DIR)
            
            # Update CSV with local path
            products_df.at[index, 'image_url'] = f"product_images/{sku}.png"
            
            successful_count += 1
            logger.info(f"[SUCCESS] Successfully generated image for {sku}")
            
            # Rate limiting: wait between requests
            if index < total_products - 1:  # Don't wait after last product
                delay = BASE_DELAY_SECONDS + random.uniform(0, 0.5)  # Add small jitter
                logger.debug(f"Waiting {delay:.2f} seconds before next request...")
                time.sleep(delay)
            
        except ImageError as e:
            failed_count += 1
            failed_skus.append(sku)
            logger.error(f"[FAILED] Failed to generate image for {sku}: {e.message}")
            
            # Continue with next product
            continue
        
        except Exception as e:
            failed_count += 1
            failed_skus.append(sku)
            logger.error(f"✗ Unexpected error for {sku}: {str(e)}")
            continue
    
    return successful_count, failed_count, failed_skus


def save_failed_skus(failed_skus):
    """Save list of failed SKUs to file for manual retry."""
    if failed_skus:
        with open(FAILED_FILE, 'w') as f:
            for sku in failed_skus:
                f.write(f"{sku}\n")
        logger.info(f"Saved {len(failed_skus)} failed SKUs to {FAILED_FILE}")


def main():
    """Main execution function."""
    logger.info("="*60)
    logger.info("AGENTIC RETAIL OS - IMAGE GENERATION")
    logger.info("="*60)
    logger.info(f"Model: {MODEL_ID}")
    logger.info(f"Region: {BEDROCK_REGION}")
    logger.info(f"Thumbnail size: {THUMBNAIL_WIDTH}x{THUMBNAIL_HEIGHT}")
    logger.info(f"Base delay: {BASE_DELAY_SECONDS} seconds")
    logger.info("")
    
    try:
        # Create output directory
        create_output_directory()
        
        # Load products CSV
        logger.info(f"Loading products from: {INPUT_CSV}")
        products_df = pd.read_csv(INPUT_CSV)
        logger.info(f"Loaded {len(products_df)} products")
        
        # Initialize Bedrock client
        logger.info(f"Initializing Bedrock client (region: {BEDROCK_REGION})...")
        bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=BEDROCK_REGION,
            config=Config(read_timeout=300)  # 5 minute timeout for image generation
        )
        
        # Process products
        start_time = time.time()
        successful_count, failed_count, failed_skus = process_products(
            products_df, 
            bedrock_client, 
            resume=True
        )
        elapsed_time = time.time() - start_time
        
        # Save updated CSV
        logger.info(f"\nSaving updated CSV to: {OUTPUT_CSV}")
        products_df.to_csv(OUTPUT_CSV, index=False)
        
        # Save failed SKUs
        if failed_skus:
            save_failed_skus(failed_skus)
        
        # Summary
        logger.info("")
        logger.info("="*60)
        logger.info("IMAGE GENERATION SUMMARY")
        logger.info("="*60)
        logger.info(f"Total products: {len(products_df)}")
        logger.info(f"Successful: {successful_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"Elapsed time: {elapsed_time:.2f} seconds ({elapsed_time/60:.2f} minutes)")
        logger.info("")
        logger.info(f"Images saved to: {OUTPUT_DIR}")
        logger.info(f"Updated CSV: {OUTPUT_CSV}")
        if failed_skus:
            logger.info(f"Failed SKUs: {FAILED_FILE}")
        logger.info("")
        logger.info("Next steps:")
        logger.info("  1. Review generated images")
        logger.info("  2. Upload images to S3 bucket")
        logger.info("  3. Update CSV with S3 URLs (or use S3 paths directly)")
        logger.info("  4. Import to DynamoDB via NoSQL Workbench")
        logger.info("="*60)
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        logger.error(f"Please ensure {INPUT_CSV} exists")
        raise
    
    except Exception as e:
        logger.error(f"Error during image generation: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    main()

