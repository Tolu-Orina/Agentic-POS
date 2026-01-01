"""
Our Simple Clerk agent with several capabilities/tools which helps it autonomously perform tasks. 
These tools include:

- Inventory lookup and verification
- Transaction processing
- Receipt generation
- Transaction queries
"""

# Import the Necessary Libraries
from strands import Agent, tool
from strands.models import BedrockModel
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os

# Initialize the agent with a Bedrock model
model = BedrockModel(model_id="nova-pro")

# Initialize the DynamoDB client
dynamodb = boto3.client('dynamodb')


#Use the @tool decorator to create a tool for the agent to use
@tool
def inventory_lookup(sku: str) -> dict:
    """Look up product information and stock level by SKU."""


    # Query DynamoDB for product
    product = dynamodb.get_item(TableName='Products', Key={'sku': sku})
    return {
        "sku": product['sku'],
        "name": product['name'],
        "price": product['price'],
        "stock_quantity": product['stock_quantity'],
        "available": product['stock_quantity'] > 0
    }


@tool
def transaction_processing(items: list) -> dict:
    """
    Process a transaction by calculating the total price and stock level.
    It does the following:
    - Calculates the total price of the items
    - Calculates the stock level of the items
    - Updates the stock level of the items
    - Returns the total price and stock level of the transaction
    
    Args:
        items: A list of items in the transaction
    Returns:
        A dictionary containing the total price and stock level of the transaction
        {
            "total_price": total_price,
            "stock_level": stock_level
        }
    """

    # Calculate the total price of the items
    total_price = sum(item['price'] * item['quantity'] for item in items)
    # Calculate the stock level of the items
    stock_level = sum(item['stock_quantity'] for item in items)

    # Update the stock level of the items
    for item in items:
        dynamodb.update_item(
            TableName='Products',
            Key={'sku': item['sku']},
            UpdateExpression='SET stock_quantity = stock_quantity - :quantity',
            ExpressionAttributeValues={':quantity': item['quantity']}
        )
    return {
        "total_price": total_price,
        "stock_level": stock_level
    }

@tool
def receipt_generation(transaction: dict) -> dict:
    """
    Generate a receipt for a transaction, including the:
    Store header (name, address, phone number)
    Transaction details (transaction ID, date, time, cashier name)
    Item details (name, quantity, price, total)
    Totals (subtotal, tax, discount, total)
    Footer (thank you message)

    The receipt should be printable, in a properly structured format
    with the header, transaction details, item details, totals, and footer.
    It can be downloaded as a PDF.
    """ 
    
    
    # Extract transaction data
    transaction_id = transaction.get('transaction_id', 'N/A')
    timestamp = transaction.get('timestamp', datetime.now().isoformat())
    cashier_name = transaction.get('cashier_name', 'N/A')
    items = transaction.get('items', [])
    subtotal = transaction.get('subtotal', 0)
    tax = transaction.get('tax', 0)
    discount_total = transaction.get('discount_total', 0)
    total = transaction.get('total', 0)
    
    # Parse timestamp
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        date_str = dt.strftime('%B %d, %Y')
        time_str = dt.strftime('%I:%M %p')
    except:
        date_str = timestamp
        time_str = ''
    
    # Format price helper
    def format_price(cents):
        return f"${cents / 100:.2f}"
    
    # Create PDF
    filename = f"receipt-{transaction_id}.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    margin = 0.75 * inch
    y_position = height - margin
    
    # Store Header
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y_position, "AGENTIC RETAIL OS")
    y_position -= 25
    
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, y_position, "Demo Store")
    y_position -= 15
    c.drawCentredString(width / 2, y_position, "123 Main Street")
    y_position -= 15
    c.drawCentredString(width / 2, y_position, "City, State 12345")
    y_position -= 15
    c.drawCentredString(width / 2, y_position, "Phone: 123-456-7890")
    y_position -= 30
    
    # Divider line
    c.line(margin, y_position, width - margin, y_position)
    y_position -= 20
    
    # Transaction Details
    c.setFont("Helvetica", 10)
    c.drawString(margin, y_position, f"Transaction ID: {transaction_id}")
    y_position -= 15
    c.drawString(margin, y_position, f"Date: {date_str}")
    y_position -= 15
    if time_str:
        c.drawString(margin, y_position, f"Time: {time_str}")
        y_position -= 15
    c.drawString(margin, y_position, f"Cashier: {cashier_name}")
    y_position -= 20
    
    # Divider line
    c.line(margin, y_position, width - margin, y_position)
    y_position -= 20
    
    # Items Header
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y_position, "Item")
    c.drawString(margin + 3.5 * inch, y_position, "Qty")
    c.drawString(margin + 4.2 * inch, y_position, "Price")
    c.drawRightString(width - margin, y_position, "Total")
    y_position -= 20
    
    # Divider line
    c.line(margin, y_position, width - margin, y_position)
    y_position -= 15
    
    # Items List
    c.setFont("Helvetica", 9)
    for item in items:
        name = item.get('name', 'Unknown Item')
        quantity = item.get('quantity', 0)
        unit_price = item.get('unit_price', 0)
        line_total = item.get('line_total', 0)
        sku = item.get('sku', '')
        
        # Truncate long names
        display_name = name[:35] + "..." if len(name) > 35 else name
        
        # Item name and SKU
        c.drawString(margin, y_position, display_name)
        y_position -= 12
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(margin + 0.2 * inch, y_position, f"SKU: {sku}")
        y_position -= 3
        
        # Quantity, unit price, and line total
        c.setFont("Helvetica", 9)
        c.drawString(margin + 3.5 * inch, y_position, str(quantity))
        c.drawString(margin + 4.2 * inch, y_position, format_price(unit_price))
        c.drawRightString(width - margin, y_position, format_price(line_total))
        y_position -= 18
        
        # Add spacing between items
        if y_position < margin + 100:
            c.showPage()
            y_position = height - margin
    
    # Divider line before totals
    y_position -= 10
    c.line(margin, y_position, width - margin, y_position)
    y_position -= 20
    
    # Totals Section
    c.setFont("Helvetica", 10)
    c.drawString(margin, y_position, "Subtotal:")
    c.drawRightString(width - margin, y_position, format_price(subtotal))
    y_position -= 18
    
    if discount_total > 0:
        c.drawString(margin, y_position, "Discount:")
        c.drawRightString(width - margin, y_position, f"-{format_price(discount_total)}")
        y_position -= 18
    
    c.drawString(margin, y_position, "Tax (8%):")
    c.drawRightString(width - margin, y_position, format_price(tax))
    y_position -= 20
    
    # Divider line
    c.line(margin, y_position, width - margin, y_position)
    y_position -= 20
    
    # Total (bold and larger)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y_position, "TOTAL:")
    c.drawRightString(width - margin, y_position, format_price(total))
    y_position -= 40
    
    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width / 2, y_position, "Thank you for your business!")
    y_position -= 15
    c.setFont("Helvetica", 8)
    c.drawCentredString(width / 2, y_position, "Returns accepted within 30 days with receipt")
    
    # Save PDF
    c.save()
    
    # Return receipt data and file path
    # In production, upload to S3 and return URL
    return {
        "receipt_url": filename,  # In production: S3 URL
        "transaction_id": transaction_id
    }

@tool
def transaction_queries(transaction_type: str) -> any:
    """
    Support for different transaction queries including:
    
    - Retrieve transaction history
    - Get transaction details by ID
    - Support transaction search by date (for reporting)

    Args:
        example:
            transaction_type: 'history'
            transaction_id: '1234567890'
            start_date: '2024-01-01'
            end_date: '2024-01-31'
    Returns:
        A dictionary containing the transaction history, details, or search results
        {
            "transaction_history": transaction_history,
            "transaction_details": transaction_details,
            "transaction_search": transaction_search
        }
        If the transaction type is invalid, return an error message
        {
            "error": "Invalid transaction type"
        }
    """

    # Retrieve transaction history
    if transaction_type == 'history':
        # Get all transactions - expensive operation, use with caution
        return dynamodb.scan(TableName='Transactions')
    
    # Get transaction details by ID
    elif transaction_type == 'details':
        return dynamodb.get_item(TableName='Transactions', Key={'transaction_id': transaction_id})
    
    # Support transaction search by date (for reporting)
    elif transaction_type == 'search':
        return dynamodb.scan(TableName='Transactions', FilterExpression='timestamp >= :start_date AND timestamp <= :end_date', ExpressionAttributeValues={':start_date': start_date, ':end_date': end_date})
    
    else:
        return "Invalid transaction type"


# Now we can add our model and the tools to the agent
clerk_agent = Agent(
    name="clerk_agent",
    model=model,
    tools=[inventory_lookup, transaction_processing,
     receipt_generation, transaction_queries],
    system_prompt=
    """
    You are a helpful retail clerk assistant. You are responsible for helping the user with their tasks.
    
    You have the following tools at your disposal:
    - inventory_lookup: Look up products in the inventory
    - transaction_processing: Process transactions
    - receipt_generation: Generate receipts
    - transaction_queries: Query transaction history
    - Return the results of the tasks to the user

    You should use the tools to help the user with their tasks.
    You should not make up information, only use the tools to get the information you need.
    You should not make up information, only use the tools to get the information you need.
    """
)

# Now we can run the agent
response = clerk_agent("Look up the product with the SKU 1234567890")
print(response)