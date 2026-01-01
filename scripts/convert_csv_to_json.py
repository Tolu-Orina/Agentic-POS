"""
Convert CSV files to JSON for local development
"""

import pandas as pd
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Input files
PRODUCTS_CSV = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail', 'products_catalog_with_images.csv')
TRANSACTIONS_CSV = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail', 'transactions_history.csv')

# Output files
WEB_DATA_DIR = os.path.join(PROJECT_ROOT, 'web', 'src', 'data')
PRODUCTS_JSON = os.path.join(WEB_DATA_DIR, 'products.json')
TRANSACTIONS_JSON = os.path.join(WEB_DATA_DIR, 'transactions.json')

def convert_products():
    """Convert products CSV to JSON"""
    print("Converting products CSV to JSON...")
    df = pd.read_csv(PRODUCTS_CSV)
    
    # Convert to list of objects
    products = []
    for _, row in df.iterrows():
        product = {
            'sku': str(row['sku']),
            'name': str(row['name']),
            'description': str(row.get('description', '')),
            'category': str(row['category']),
            'price': int(row['price']),  # Already in cents
            'cost': int(row['cost']),
            'stock_quantity': int(row['stock_quantity']),
            'reorder_threshold': int(row['reorder_threshold']),
            'unit': str(row['unit']),
            'supplier_name': str(row.get('supplier_name', '')),
            'supplier_contact': str(row.get('supplier_contact', '')),
            'image_url': str(row.get('image_url', '')),
            'created_at': str(row['created_at']),
            'updated_at': str(row['updated_at']),
            'is_active': bool(row['is_active'])
        }
        products.append(product)
    
    # Save to JSON
    os.makedirs(WEB_DATA_DIR, exist_ok=True)
    with open(PRODUCTS_JSON, 'w') as f:
        json.dump(products, f, indent=2)
    
    print(f"✓ Converted {len(products)} products to {PRODUCTS_JSON}")

def convert_transactions():
    """Convert transactions CSV to JSON"""
    print("Converting transactions CSV to JSON...")
    df = pd.read_csv(TRANSACTIONS_CSV)
    
    # Convert to list of objects
    transactions = []
    for _, row in df.iterrows():
        # Parse items JSON string
        import json as json_lib
        items_str = row['items']
        if isinstance(items_str, str):
            try:
                items = json_lib.loads(items_str)
            except:
                items = []
        else:
            items = []
        
        transaction = {
            'transaction_id': str(row['transaction_id']),
            'timestamp': str(row['timestamp']),
            'user_id': str(row['user_id']),
            'cashier_name': str(row.get('cashier_name', '')),
            'items': items,
            'subtotal': int(row['subtotal']),
            'tax': int(row['tax']),
            'discount_total': int(row.get('discount_total', 0)),
            'total': int(row['total']),
            'payment_method': str(row.get('payment_method', 'mock')),
            'status': str(row.get('status', 'completed'))
        }
        transactions.append(transaction)
    
    # Save to JSON
    with open(TRANSACTIONS_JSON, 'w') as f:
        json.dump(transactions, f, indent=2)
    
    print(f"✓ Converted {len(transactions)} transactions to {TRANSACTIONS_JSON}")

def copy_images():
    """Copy product images to web/public/images/"""
    print("Copying product images...")
    import shutil
    
    source_dir = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail', 'product_images')
    target_dir = os.path.join(PROJECT_ROOT, 'web', 'public', 'images')
    
    os.makedirs(target_dir, exist_ok=True)
    
    if os.path.exists(source_dir):
        image_files = [f for f in os.listdir(source_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        for img_file in image_files:
            src = os.path.join(source_dir, img_file)
            dst = os.path.join(target_dir, img_file)
            shutil.copy2(src, dst)
        print(f"✓ Copied {len(image_files)} images to {target_dir}")
    else:
        print(f"⚠ Source directory not found: {source_dir}")

def main():
    print("="*60)
    print("CONVERTING CSV TO JSON FOR LOCAL DEVELOPMENT")
    print("="*60)
    
    convert_products()
    convert_transactions()
    copy_images()
    
    print("\n✓ Conversion complete!")
    print(f"  Products: {PRODUCTS_JSON}")
    print(f"  Transactions: {TRANSACTIONS_JSON}")
    print(f"  Images: web/public/images/")

if __name__ == '__main__':
    main()

