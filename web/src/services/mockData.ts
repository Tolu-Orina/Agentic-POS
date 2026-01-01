/**
 * Mock data service for local development
 * Loads data from JSON files
 */

import productsData from '../data/products.json';
import transactionsData from '../data/transactions.json';
import type { Product, Transaction } from '../types';

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

export const mockProducts = productsData as Product[];
export const mockTransactions = transactionsData as Transaction[];

/**
 * Mock API service for products
 */
export const productService = {
  /**
   * Get all products
   */
  async getAll(): Promise<Product[]> {
    await delay(300); // Simulate network delay
    return [...mockProducts];
  },

  /**
   * Get product by SKU
   */
  async getBySku(sku: string): Promise<Product | null> {
    await delay(200);
    return mockProducts.find(p => p.sku === sku) || null;
  },

  /**
   * Search products
   */
  async search(query: string): Promise<Product[]> {
    await delay(300);
    const lowerQuery = query.toLowerCase();
    return mockProducts.filter(
      p =>
        p.name.toLowerCase().includes(lowerQuery) ||
        p.sku.toLowerCase().includes(lowerQuery) ||
        p.category.toLowerCase().includes(lowerQuery)
    );
  },
};

/**
 * Mock API service for transactions
 */
export const transactionService = {
  /**
   * Get all transactions
   */
  async getAll(): Promise<Transaction[]> {
    await delay(300);
    return [...mockTransactions].sort((a, b) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    );
  },

  /**
   * Get transaction by ID
   */
  async getById(transactionId: string): Promise<Transaction | null> {
    await delay(200);
    return mockTransactions.find(t => t.transaction_id === transactionId) || null;
  },

  /**
   * Create new transaction (mock)
   */
  async create(transaction: Omit<Transaction, 'transaction_id' | 'timestamp'>): Promise<Transaction> {
    await delay(500); // Simulate agent processing time
    const newTransaction: Transaction = {
      ...transaction,
      transaction_id: `TXN-${Date.now()}`,
      timestamp: new Date().toISOString(),
    };
    mockTransactions.unshift(newTransaction);
    return newTransaction;
  },
};

/**
 * Mock agent service
 */
export const agentService = {
  /**
   * Mock inventory lookup
   */
  async lookupInventory(sku: string, quantity: number): Promise<{ available: boolean; product: Product | null }> {
    await delay(800); // Simulate agent processing
    const product = mockProducts.find(p => p.sku === sku);
    if (!product) {
      return { available: false, product: null };
    }
    return {
      available: product.stock_quantity >= quantity,
      product,
    };
  },

  /**
   * Mock transaction processing
   */
  async processTransaction(items: Array<{ sku: string; quantity: number }>): Promise<Transaction> {
    await delay(1500); // Simulate agent processing
    
    // Calculate totals
    let subtotal = 0;
    const transactionItems = items.map(item => {
      const product = mockProducts.find(p => p.sku === item.sku);
      if (!product) throw new Error(`Product not found: ${item.sku}`);
      
      const unitPrice = product.price;
      const lineTotal = unitPrice * item.quantity;
      subtotal += lineTotal;
      
      return {
        sku: product.sku,
        name: product.name,
        quantity: item.quantity,
        unit_price: unitPrice,
        line_total: lineTotal,
      };
    });
    
    const tax = Math.round(subtotal * 0.08); // 8% tax
    const total = subtotal + tax;
    
    const transaction: Transaction = {
      transaction_id: `TXN-${Date.now()}`,
      timestamp: new Date().toISOString(),
      user_id: 'cashier_001',
      cashier_name: 'Cashier 1',
      items: transactionItems,
      subtotal,
      tax,
      discount_total: 0,
      total,
      payment_method: 'mock',
      status: 'completed',
    };
    
    mockTransactions.unshift(transaction);
    return transaction;
  },
};

