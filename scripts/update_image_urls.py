"""
Update image URLs in products JSON to use local paths
"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PRODUCTS_JSON = os.path.join(PROJECT_ROOT, 'web', 'src', 'data', 'products.json')

def update_image_urls():
    """Update image URLs to use local paths"""
    with open(PRODUCTS_JSON, 'r') as f:
        products = json.load(f)
    
    for product in products:
        # Extract SKU and update image URL
        sku = product['sku']
        # Update to local path: /images/{sku}.png
        product['image_url'] = f'/images/{sku}.png'
    
    with open(PRODUCTS_JSON, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"✓ Updated image URLs for {len(products)} products")

if __name__ == '__main__':
    update_image_urls()

