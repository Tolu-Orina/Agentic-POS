/**
 * TypeScript type definitions matching DynamoDB schema
 */

export interface Product {
  sku: string;
  name: string;
  description?: string;
  category: string;
  price: number; // In cents
  cost: number; // In cents
  stock_quantity: number;
  reorder_threshold: number;
  unit: string;
  supplier_name?: string;
  supplier_contact?: string;
  image_url?: string;
  created_at: string;
  updated_at: string;
  is_active: boolean;
}

export interface CartItem {
  sku: string;
  name: string;
  quantity: number;
  unit_price: number; // In cents
  line_total: number; // In cents
  discount_applied?: number; // In cents
}

export interface TransactionItem {
  sku: string;
  name: string;
  quantity: number;
  unit_price: number; // In cents
  line_total: number; // In cents
  discount_applied?: number; // In cents
}

export interface Transaction {
  transaction_id: string;
  timestamp: string; // ISO 8601
  user_id: string;
  cashier_name?: string;
  items: TransactionItem[];
  subtotal: number; // In cents
  tax: number; // In cents
  discount_total: number; // In cents
  total: number; // In cents
  payment_method: string;
  status: 'completed' | 'cancelled' | 'refunded';
  agent_reasoning_trace?: string;
  receipt_url?: string;
}

export interface AgentStatus {
  status: 'idle' | 'processing' | 'success' | 'error';
  message?: string;
}

export interface DailySalesSummary {
  date: string;
  total_revenue: number; // In cents
  transaction_count: number;
  average_transaction_value: number; // In cents
  top_selling_items: Array<{
    sku: string;
    name: string;
    quantity_sold: number;
    revenue: number; // In cents
  }>;
}

