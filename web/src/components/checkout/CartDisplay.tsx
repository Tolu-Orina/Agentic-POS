/**
 * Cart Display Component
 * Shows itemized cart with totals
 */

import {
  Card,
  Typography,
  List,
  ListItem,
  IconButton,
  Divider,
  Box,
  Alert,
  Stack,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import type { CartItem } from '../../types';
import { formatPrice } from '../../utils/formatters';

interface CartDisplayProps {
  items: CartItem[];
  subtotal: number;
  tax: number;
  total: number;
  onRemoveItem: (sku: string) => void;
  onUpdateQuantity: (sku: string, quantity: number) => void;
}

export default function CartDisplay({
  items,
  subtotal,
  tax,
  total,
  onRemoveItem,
  onUpdateQuantity,
}: CartDisplayProps) {
  if (items.length === 0) {
    return (
      <Card sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Cart
        </Typography>
        <Alert severity="info" sx={{ mt: 2 }}>
          Cart is empty. Add items to get started.
        </Alert>
      </Card>
    );
  }

  return (
    <Card sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Cart ({items.length} {items.length === 1 ? 'item' : 'items'})
      </Typography>
      <List sx={{ flex: 1, overflow: 'auto' }}>
        {items.map((item) => (
          <ListItem
            key={item.sku}
            sx={{
              flexDirection: 'column',
              alignItems: 'stretch',
              px: 0,
            }}
          >
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
              <Box sx={{ flex: 1 }}>
                <Typography variant="body1" sx={{ fontWeight: 600, mb: 0.5 }}>
                  {item.name}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  SKU: {item.sku}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                  {formatPrice(item.unit_price)} each
                </Typography>
              </Box>
              <IconButton
                size="small"
                aria-label="remove"
                onClick={() => onRemoveItem(item.sku)}
                sx={{ ml: 1 }}
              >
                <DeleteIcon fontSize="small" />
              </IconButton>
            </Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <Stack direction="row" spacing={1} alignItems="center">
                <IconButton
                  size="small"
                  onClick={() => onUpdateQuantity(item.sku, item.quantity - 1)}
                  sx={{ border: 1, borderColor: 'divider' }}
                >
                  <RemoveIcon fontSize="small" />
                </IconButton>
                <Typography variant="body1" sx={{ minWidth: 30, textAlign: 'center', fontWeight: 600 }}>
                  {item.quantity}
                </Typography>
                <IconButton
                  size="small"
                  onClick={() => onUpdateQuantity(item.sku, item.quantity + 1)}
                  sx={{ border: 1, borderColor: 'divider' }}
                >
                  <AddIcon fontSize="small" />
                </IconButton>
              </Stack>
              <Typography variant="body1" sx={{ fontWeight: 700, fontSize: '1.1rem' }}>
                {formatPrice(item.line_total)}
              </Typography>
            </Box>
          </ListItem>
        ))}
      </List>
      <Divider sx={{ my: 2 }} />
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
        <Typography>Subtotal:</Typography>
        <Typography>{formatPrice(subtotal)}</Typography>
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
        <Typography>Tax (8%):</Typography>
        <Typography>{formatPrice(tax)}</Typography>
      </Box>
      <Divider sx={{ my: 2 }} />
      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h6">Total:</Typography>
        <Typography variant="h6" color="primary" sx={{ fontWeight: 700 }}>
          {formatPrice(total)}
        </Typography>
      </Box>
    </Card>
  );
}

