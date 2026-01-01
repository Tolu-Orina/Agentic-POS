/**
 * Checkout Screen Component
 * Main interface for processing sales transactions
 */

import { useState } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  Typography,
  Stack,
} from '@mui/material';
import ProductCatalog from './ProductCatalog';
import CartDisplay from './CartDisplay';
import AgentStatusIndicator from '../common/AgentStatusIndicator';
import ReceiptPreview from './ReceiptPreview';
import type { CartItem, AgentStatus, Transaction } from '../../types';
import { agentService } from '../../services/mockData';

const TAX_RATE = 0.08; // 8% tax

export default function CheckoutScreen() {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [agentStatus, setAgentStatus] = useState<AgentStatus>({ status: 'idle' });
  const [processing, setProcessing] = useState(false);
  const [completedTransaction, setCompletedTransaction] = useState<Transaction | null>(null);
  const [receiptOpen, setReceiptOpen] = useState(false);

  const handleAddItem = async (sku: string, quantity: number) => {
    setAgentStatus({ status: 'processing', message: 'Checking inventory...' });
    
    try {
      const result = await agentService.lookupInventory(sku, quantity);
      
      if (!result.available || !result.product) {
        setAgentStatus({
          status: 'error',
          message: result.product
            ? `Insufficient stock. Available: ${result.product.stock_quantity}`
            : 'Product not found',
        });
        return;
      }

      const unitPrice = result.product.price;
      const lineTotal = unitPrice * quantity;

      const newItem: CartItem = {
        sku: result.product.sku,
        name: result.product.name,
        quantity,
        unit_price: unitPrice,
        line_total: lineTotal,
      };

      // Check if item already in cart
      const existingIndex = cartItems.findIndex(item => item.sku === sku);
      if (existingIndex >= 0) {
        // Update quantity
        const updatedItems = [...cartItems];
        updatedItems[existingIndex].quantity += quantity;
        updatedItems[existingIndex].line_total = updatedItems[existingIndex].unit_price * updatedItems[existingIndex].quantity;
        setCartItems(updatedItems);
      } else {
        // Add new item
        setCartItems([...cartItems, newItem]);
      }

      setAgentStatus({ status: 'success', message: 'Item added to cart' });
      
      // Reset status after 2 seconds
      setTimeout(() => {
        setAgentStatus({ status: 'idle' });
      }, 2000);
    } catch (error) {
      setAgentStatus({
        status: 'error',
        message: 'Failed to check inventory. Please try again.',
      });
    }
  };

  const handleRemoveItem = (sku: string) => {
    setCartItems(cartItems.filter(item => item.sku !== sku));
  };

  const handleUpdateQuantity = (sku: string, newQuantity: number) => {
    if (newQuantity <= 0) {
      handleRemoveItem(sku);
      return;
    }
    
    const updatedItems = cartItems.map(item => {
      if (item.sku === sku) {
        return {
          ...item,
          quantity: newQuantity,
          line_total: item.unit_price * newQuantity,
        };
      }
      return item;
    });
    setCartItems(updatedItems);
  };

  const handleCompleteSale = async () => {
    if (cartItems.length === 0) return;

    setProcessing(true);
    setAgentStatus({ status: 'processing', message: 'Processing transaction...' });

    try {
      const items = cartItems.map(item => ({
        sku: item.sku,
        quantity: item.quantity,
      }));

      const transaction = await agentService.processTransaction(items);
      
      setAgentStatus({ status: 'success', message: 'Transaction completed!' });
      
      // Clear cart
      setCartItems([]);
      
      // Show receipt
      setCompletedTransaction(transaction);
      setReceiptOpen(true);
      
      // Reset status after showing receipt
      setTimeout(() => {
        setAgentStatus({ status: 'idle' });
        setProcessing(false);
      }, 1000);
    } catch (error) {
      setAgentStatus({
        status: 'error',
        message: 'Transaction failed. Please try again.',
      });
      setProcessing(false);
    }
  };

  // Calculate totals
  const subtotal = cartItems.reduce((sum, item) => sum + item.line_total, 0);
  const tax = Math.round(subtotal * TAX_RATE);
  const total = subtotal + tax;

  return (
    <Box sx={{ position: 'relative' }}>
      <Typography variant="h4" gutterBottom>
        Checkout
      </Typography>
      
      <AgentStatusIndicator status={agentStatus} />

      <Box
        sx={{
          mt: 2,
          display: 'flex',
          flexDirection: { xs: 'column', md: 'row' },
          gap: 3,
          height: { md: 'calc(100vh - 180px)' },
        }}
      >
        {/* Products Section - 65% width */}
        <Box
          sx={{
            flex: { xs: '1', md: '0 0 65%' },
            display: 'flex',
            flexDirection: 'column',
            overflow: 'hidden',
          }}
        >
          <Box sx={{ flex: 1, overflow: 'auto', pr: 1 }}>
            <ProductCatalog onAddToCart={handleAddItem} />
          </Box>
        </Box>

        {/* Cart Section - 35% width, sticky */}
        <Box
          sx={{
            flex: { xs: '1', md: '0 0 35%' },
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <Box
            sx={{
              position: { md: 'sticky' },
              top: { md: 80 },
              maxHeight: { md: 'calc(100vh - 100px)' },
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <CartDisplay
              items={cartItems}
              subtotal={subtotal}
              tax={tax}
              total={total}
              onRemoveItem={handleRemoveItem}
              onUpdateQuantity={handleUpdateQuantity}
            />
            <Stack direction="column" spacing={2} sx={{ mt: 2 }}>
              <Button
                variant="contained"
                size="large"
                fullWidth
                onClick={handleCompleteSale}
                disabled={cartItems.length === 0 || processing}
                sx={{ py: 2, fontSize: '1.1rem', fontWeight: 700 }}
              >
                {processing ? (
                  <>
                    <CircularProgress size={20} sx={{ mr: 1 }} />
                    Processing...
                  </>
                ) : (
                  'Complete Sale'
                )}
              </Button>
              <Button
                variant="outlined"
                size="large"
                fullWidth
                onClick={() => {
                  setCartItems([]);
                  setAgentStatus({ status: 'idle' });
                }}
                disabled={cartItems.length === 0 || processing}
              >
                Clear Cart
              </Button>
            </Stack>
          </Box>
        </Box>
      </Box>

      <ReceiptPreview
        open={receiptOpen}
        transaction={completedTransaction}
        onClose={() => {
          setReceiptOpen(false);
          setCompletedTransaction(null);
        }}
      />
    </Box>
  );
}

