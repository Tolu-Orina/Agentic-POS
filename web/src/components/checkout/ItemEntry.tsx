/**
 * Item Entry Component
 * Allows cashier to enter SKU and quantity
 */

import { useState } from 'react';
import type { KeyboardEvent } from 'react';
import {
  Card,
  TextField,
  Button,
  Typography,
} from '@mui/material';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';

interface ItemEntryProps {
  onAddItem: (sku: string, quantity: number) => void;
  disabled?: boolean;
}

export default function ItemEntry({ onAddItem, disabled = false }: ItemEntryProps) {
  const [skuInput, setSkuInput] = useState('');
  const [quantity, setQuantity] = useState(1);

  const handleAddItem = () => {
    if (skuInput.trim() && quantity > 0) {
      onAddItem(skuInput.trim().toUpperCase(), quantity);
      setSkuInput('');
      setQuantity(1);
    }
  };

  const handleKeyPress = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Enter' && skuInput.trim()) {
      handleAddItem();
    }
  };

  return (
    <Card sx={{ p: 3, mb: 2 }}>
      <Typography variant="h6" gutterBottom>
        Add Item
      </Typography>
      <TextField
        label="SKU or Barcode"
        fullWidth
        value={skuInput}
        onChange={(e) => setSkuInput(e.target.value)}
        onKeyPress={handleKeyPress}
        disabled={disabled}
        autoFocus
        sx={{ mb: 2 }}
        placeholder="Enter SKU (e.g., 85123A)"
      />
      <TextField
        label="Quantity"
        type="number"
        fullWidth
        value={quantity}
        onChange={(e) => {
          const val = parseInt(e.target.value) || 1;
          setQuantity(Math.max(1, val));
        }}
        disabled={disabled}
        inputProps={{ min: 1 }}
        sx={{ mb: 2 }}
      />
      <Button
        variant="contained"
        fullWidth
        onClick={handleAddItem}
        disabled={!skuInput.trim() || disabled}
        startIcon={<AddShoppingCartIcon />}
      >
        Add to Cart
      </Button>
    </Card>
  );
}

