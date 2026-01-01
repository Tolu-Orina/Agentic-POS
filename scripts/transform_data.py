"""
Data Transformation Script for Agentic Retail OS
Transforms UCI Online Retail dataset into DynamoDB-ready format.

Steps:
1. Convert Excel to CSV
2. Extract unique products → Product Catalog
3. Group transactions → Transaction History
4. Simulate inventory → Add stock levels
5. Normalize data → Clean, format, validate
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
import uuid
import re
from collections import defaultdict
import os

# Get script directory and set paths relative to project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

# Configuration
INPUT_FILE = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail', 'Online Retail.xlsx')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'datasets', 'uci-retail')
TAX_RATE = 0.08  # 8% UK VAT approximation
DATE_SHIFT_DAYS = 0  # Shift dates to recent (0 = keep original, 365 = shift 1 year forward)

# Category inference keywords
CATEGORY_KEYWORDS = {
    'Home Decor': ['t-light', 'lantern', 'light', 'holder', 'hanging', 'decorative', 'ornament'],
    'Kitchen': ['mug', 'tea', 'kitchen', 'spoon', 'towel', 'bottle', 'cup', 'coaster'],
    'Toys & Games': ['jigsaw', 'doll', 'blocks', 'game', 'puzzle', 'toy', 'playhouse'],
    'Gifts & Accessories': ['bag', 'gift', 'sticker', 'tape', 'wrapping', 'card'],
    'Seasonal': ['christmas', 'valentine', 'easter', 'halloween'],
    'Office Supplies': ['pen', 'pencil', 'notebook', 'folder', 'file'],
    'Personal Care': ['soap', 'shampoo', 'toothpaste', 'cream', 'lotion']
}

# Supplier names for assignment
SUPPLIERS = [
    {'name': 'UK Home Supplies', 'contact': 'supplier1@example.com'},
    {'name': 'European Retail Partners', 'contact': 'supplier2@example.com'},
    {'name': 'Global Home Goods', 'contact': 'supplier3@example.com'},
    {'name': 'Premium Decor Co', 'contact': 'supplier4@example.com'}
]


def normalize_product_name(description):
    """Convert ALL CAPS to Title Case, clean up description."""
    if pd.isna(description) or description == '':
        return ''
    
    # Convert to title case
    name = description.title()
    
    # Fix common issues
    name = re.sub(r'\s+', ' ', name)  # Multiple spaces to single
    name = name.strip()
    
    return name


def infer_category(description):
    """Infer product category from description keywords."""
    if pd.isna(description) or description == '':
        return 'General'
    
    description_lower = description.lower()
    
    # Check each category
    for category, keywords in CATEGORY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category
    
    return 'General'


def convert_price_to_cents(price):
    """Convert decimal price to cents."""
    if pd.isna(price):
        return 0
    return int(round(float(price) * 100))


def parse_date(date_str):
    """Parse date string to ISO 8601 format."""
    if pd.isna(date_str):
        return None
    
    try:
        # Handle format: "12/1/2010 8:26"
        dt = pd.to_datetime(date_str, format='%m/%d/%Y %H:%M', errors='coerce')
        if pd.isna(dt):
            # Try alternative format
            dt = pd.to_datetime(date_str, errors='coerce')
        
        if pd.isna(dt):
            return None
        
        # Shift date if needed (for demo purposes)
        if DATE_SHIFT_DAYS > 0:
            dt = dt + timedelta(days=DATE_SHIFT_DAYS)
        
        return dt.isoformat() + 'Z'
    except:
        return None


def calculate_stock_level(sales_frequency, total_quantity_sold, is_low_stock):
    """Calculate realistic stock level based on sales frequency."""
    # If marked as low stock, force low stock levels
    if is_low_stock:
        # Force low stock: 2-15 units
        return np.random.randint(2, 16)
    
    # Base stock on sales frequency
    # High frequency (appears in many transactions) = higher stock
    # Low frequency = lower stock
    if sales_frequency >= 50:  # Very popular
        base_stock = 80 + np.random.randint(0, 40)
    elif sales_frequency >= 20:  # Popular
        base_stock = 40 + np.random.randint(0, 30)
    elif sales_frequency >= 10:  # Moderate
        base_stock = 20 + np.random.randint(0, 25)
    elif sales_frequency >= 5:  # Less common
        base_stock = 10 + np.random.randint(0, 15)
    else:  # Rare
        base_stock = 5 + np.random.randint(0, 10)
    
    return base_stock


def calculate_reorder_threshold(stock_quantity, sales_frequency, is_low_stock=False):
    """Calculate reorder threshold based on stock and sales frequency."""
    # For low stock items, threshold should be higher than current stock
    if is_low_stock:
        # Set threshold to be 1.5-2x the stock quantity (ensures it's below threshold)
        return int(stock_quantity * 1.8)
    
    # For normal stock, threshold should be 20-30% of stock quantity
    if sales_frequency >= 20:
        threshold = int(stock_quantity * 0.25)
    elif sales_frequency >= 10:
        threshold = int(stock_quantity * 0.30)
    else:
        threshold = int(stock_quantity * 0.35)
    
    return max(5, threshold)  # Minimum threshold of 5


def assign_supplier(sku, category):
    """Assign supplier based on SKU hash (consistent assignment)."""
    # Use hash of SKU for consistent assignment
    hash_val = hash(sku) % len(SUPPLIERS)
    supplier = SUPPLIERS[hash_val]
    return supplier['name'], supplier['contact']


def step1_convert_excel_to_csv():
    """Step 1: Convert Excel to CSV."""
    print("Step 1: Converting Excel to CSV...")
    
    try:
        df = pd.read_excel(INPUT_FILE)
        output_csv = os.path.join(OUTPUT_DIR, 'Online_Retail_Raw.csv')
        df.to_csv(output_csv, index=False)
        print(f"✓ Converted to: {output_csv}")
        print(f"  Rows: {len(df)}")
        return df
    except Exception as e:
        print(f"✗ Error converting Excel: {e}")
        raise


def step2_extract_products(df):
    """Step 2: Extract unique products and create product catalog."""
    print("\nStep 2: Extracting unique products...")
    
    # Filter out POST items and invalid data
    df_clean = df[
        (df['StockCode'].notna()) &
        (df['Description'].notna()) &
        (df['UnitPrice'] > 0) &
        (~df['StockCode'].str.upper().str.contains('POST', na=False))
    ].copy()
    
    # Group by StockCode to get unique products
    product_stats = df_clean.groupby('StockCode').agg({
        'Description': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],  # Most common description
        'UnitPrice': 'mean',  # Average price
        'Quantity': ['sum', 'count'],  # Total sold, frequency
    }).reset_index()
    
    product_stats.columns = ['sku', 'description', 'avg_price', 'total_quantity_sold', 'sales_frequency']
    
    # Normalize product names
    product_stats['name'] = product_stats['description'].apply(normalize_product_name)
    
    # Infer categories
    product_stats['category'] = product_stats['description'].apply(infer_category)
    
    # Convert prices to cents
    product_stats['price'] = product_stats['avg_price'].apply(convert_price_to_cents)
    
    # Calculate cost (60% of price, simulated)
    product_stats['cost'] = (product_stats['price'] * 0.6).astype(int)
    
    # Initial stock levels (will be recalculated after sorting)
    product_stats['stock_quantity'] = product_stats.apply(
        lambda row: calculate_stock_level(
            row['sales_frequency'], 
            row['total_quantity_sold'],
            False  # Will be recalculated after sorting
        ),
        axis=1
    )
    
    # Initial reorder thresholds (will be recalculated after sorting)
    product_stats['reorder_threshold'] = product_stats.apply(
        lambda row: calculate_reorder_threshold(
            row['stock_quantity'], 
            row['sales_frequency'],
            False  # Will be recalculated after sorting
        ),
        axis=1
    )
    
    # Assign suppliers
    supplier_data = product_stats.apply(
        lambda row: assign_supplier(row['sku'], row['category']),
        axis=1,
        result_type='expand'
    )
    supplier_data.columns = ['supplier_name', 'supplier_contact']
    product_stats = pd.concat([product_stats, supplier_data], axis=1)
    
    # Add metadata
    current_time = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    product_stats['created_at'] = current_time
    product_stats['updated_at'] = current_time
    product_stats['is_active'] = True
    product_stats['unit'] = 'each'
    product_stats['image_url'] = ''  # Will be populated after image generation
    
    # Select top products for MVP (most frequently sold)
    # Sort by sales frequency and take top 50
    product_stats = product_stats.sort_values('sales_frequency', ascending=False).head(50).reset_index(drop=True)
    
    # NOW determine which products should be low stock (after sorting and selecting)
    # Select every 5th product from the top 50 to be low stock
    total_products = len(product_stats)
    low_stock_indices = set(range(0, total_products, max(1, total_products // 5)))
    product_stats['is_low_stock'] = product_stats.index.isin(low_stock_indices)
    
    # Recalculate stock levels with correct low stock flags
    product_stats['stock_quantity'] = product_stats.apply(
        lambda row: calculate_stock_level(
            row['sales_frequency'], 
            row['total_quantity_sold'],
            row['is_low_stock']
        ),
        axis=1
    )
    
    # Recalculate thresholds with correct low stock flags
    product_stats['reorder_threshold'] = product_stats.apply(
        lambda row: calculate_reorder_threshold(
            row['stock_quantity'], 
            row['sales_frequency'],
            row['is_low_stock']
        ),
        axis=1
    )
    
    # Drop temporary column
    product_stats = product_stats.drop('is_low_stock', axis=1)
    
    # Reorder columns to match DynamoDB schema
    products_df = product_stats[[
        'sku', 'name', 'description', 'category', 'price', 'cost',
        'stock_quantity', 'reorder_threshold', 'unit',
        'supplier_name', 'supplier_contact', 'image_url',
        'created_at', 'updated_at', 'is_active'
    ]]
    
    # Save to CSV
    output_file = os.path.join(OUTPUT_DIR, 'products_catalog.csv')
    products_df.to_csv(output_file, index=False)
    
    print(f"✓ Extracted {len(products_df)} unique products")
    print(f"  Saved to: {output_file}")
    print(f"  Categories: {products_df['category'].value_counts().to_dict()}")
    print(f"  Low stock items (< threshold): {len(products_df[products_df['stock_quantity'] < products_df['reorder_threshold']])}")
    
    return products_df, df_clean


def step3_group_transactions(df_clean, products_df):
    """Step 3: Group transactions and create transaction history."""
    print("\nStep 3: Grouping transactions...")
    
    # Filter to only include products in our catalog
    valid_skus = set(products_df['sku'].values)
    df_clean = df_clean[df_clean['StockCode'].isin(valid_skus)].copy()
    
    # Create product name lookup
    product_lookup = dict(zip(products_df['sku'], products_df['name']))
    price_lookup = dict(zip(products_df['sku'], products_df['price']))
    
    # Group by InvoiceNo
    transactions = []
    
    for invoice_no, group in df_clean.groupby('InvoiceNo'):
        # Skip if invoice has negative quantities (returns/cancellations)
        if (group['Quantity'] < 0).any():
            continue
        
        # Get transaction date (use first row's date)
        invoice_date = group['InvoiceDate'].iloc[0]
        timestamp = parse_date(invoice_date)
        
        if not timestamp:
            continue
        
        # Build items array
        items = []
        subtotal = 0
        
        for _, row in group.iterrows():
            sku = row['StockCode']
            quantity = int(row['Quantity'])
            unit_price = price_lookup.get(sku, convert_price_to_cents(row['UnitPrice']))
            line_total = quantity * unit_price
            
            items.append({
                'sku': sku,
                'name': product_lookup.get(sku, normalize_product_name(row['Description'])),
                'quantity': quantity,
                'unit_price': unit_price,
                'line_total': line_total
            })
            
            subtotal += line_total
        
        # Calculate tax and total
        tax = int(subtotal * TAX_RATE)
        total = subtotal + tax
        
        # Generate transaction ID (use InvoiceNo or UUID)
        transaction_id = str(invoice_no)
        
        transactions.append({
            'transaction_id': transaction_id,
            'timestamp': timestamp,
            'user_id': f"cashier_{np.random.randint(1, 4):03d}",  # Simulated cashier
            'cashier_name': f"Cashier {np.random.randint(1, 4)}",
            'items': items,
            'subtotal': subtotal,
            'tax': tax,
            'discount_total': 0,
            'total': total,
            'payment_method': 'mock',
            'status': 'completed'
        })
    
    # Select diverse transactions for MVP (mix of sizes)
    # Sort by item count and select diverse set
    transactions.sort(key=lambda x: len(x['items']))
    
    # Select: 5 small (2-3 items), 10 medium (4-8 items), 10 large (9+ items)
    small = [t for t in transactions if 2 <= len(t['items']) <= 3][:5]
    medium = [t for t in transactions if 4 <= len(t['items']) <= 8][:10]
    large = [t for t in transactions if len(t['items']) >= 9][:10]
    
    selected_transactions = small + medium + large
    
    print(f"✓ Processed {len(transactions)} total transactions")
    print(f"  Selected {len(selected_transactions)} transactions for MVP")
    print(f"    Small (2-3 items): {len(small)}")
    print(f"    Medium (4-8 items): {len(medium)}")
    print(f"    Large (9+ items): {len(large)}")
    
    return selected_transactions


def step4_normalize_data(products_df, transactions):
    """Step 4: Final data normalization and validation."""
    print("\nStep 4: Normalizing and validating data...")
    
    # Validate products
    products_df['name'] = products_df['name'].fillna('')
    products_df['description'] = products_df['description'].fillna('')
    products_df['category'] = products_df['category'].fillna('General')
    
    # Ensure all required fields are present
    required_product_fields = ['sku', 'name', 'category', 'price', 'stock_quantity', 'reorder_threshold']
    missing = [field for field in required_product_fields if field not in products_df.columns]
    if missing:
        print(f"⚠ Warning: Missing product fields: {missing}")
    
    # Validate transactions
    for txn in transactions:
        if not txn.get('transaction_id'):
            txn['transaction_id'] = str(uuid.uuid4())
        if not txn.get('timestamp'):
            txn['timestamp'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        if not txn.get('items') or len(txn['items']) == 0:
            continue
    
    print("✓ Data validation complete")
    
    return products_df, transactions


def step5_save_outputs(products_df, transactions):
    """Step 5: Save final CSV files."""
    print("\nStep 5: Saving output files...")
    
    # Save products catalog
    products_file = os.path.join(OUTPUT_DIR, 'products_catalog.csv')
    products_df.to_csv(products_file, index=False)
    print(f"✓ Products catalog: {products_file}")
    print(f"  Products: {len(products_df)}")
    
    # Save transactions (handle complex items structure)
    # For CSV, we'll need to convert items list to JSON string
    transactions_for_csv = []
    for txn in transactions:
        txn_copy = txn.copy()
        # Convert items list to JSON string for CSV
        import json
        txn_copy['items'] = json.dumps(txn['items'])
        transactions_for_csv.append(txn_copy)
    
    transactions_df = pd.DataFrame(transactions_for_csv)
    transactions_file = os.path.join(OUTPUT_DIR, 'transactions_history.csv')
    transactions_df.to_csv(transactions_file, index=False)
    print(f"✓ Transactions history: {transactions_file}")
    print(f"  Transactions: {len(transactions)}")
    
    # Summary
    print("\n" + "="*60)
    print("TRANSFORMATION SUMMARY")
    print("="*60)
    print(f"Products extracted: {len(products_df)}")
    print(f"Transactions processed: {len(transactions)}")
    print(f"\nProduct categories:")
    for cat, count in products_df['category'].value_counts().items():
        print(f"  {cat}: {count}")
    print(f"\nStock status:")
    low_stock = len(products_df[products_df['stock_quantity'] < products_df['reorder_threshold']])
    healthy_stock = len(products_df[products_df['stock_quantity'] >= products_df['reorder_threshold']])
    print(f"  Low stock (needs restock): {low_stock}")
    print(f"  Healthy stock: {healthy_stock}")
    print(f"\nOutput files:")
    print(f"  {products_file}")
    print(f"  {transactions_file}")
    print("="*60)


def main():
    """Main execution function."""
    print("="*60)
    print("AGENTIC RETAIL OS - DATA TRANSFORMATION")
    print("="*60)
    print(f"Input file: {INPUT_FILE}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()
    
    try:
        # Step 1: Convert Excel to CSV
        df = step1_convert_excel_to_csv()
        
        # Step 2: Extract products
        products_df, df_clean = step2_extract_products(df)
        
        # Step 3: Group transactions
        transactions = step3_group_transactions(df_clean, products_df)
        
        # Step 4: Normalize data
        products_df, transactions = step4_normalize_data(products_df, transactions)
        
        # Step 5: Save outputs
        step5_save_outputs(products_df, transactions)
        
        print("\n✓ Transformation complete!")
        print("\nNext steps:")
        print("  1. Review products_catalog.csv")
        print("  2. Review transactions_history.csv")
        print("  3. Run image generation script")
        print("  4. Import to DynamoDB via NoSQL Workbench")
        
    except Exception as e:
        print(f"\n✗ Error during transformation: {e}")
        import traceback
        traceback.print_exc()
        raise


if __name__ == '__main__':
    main()

