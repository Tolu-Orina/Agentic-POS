/**
 * Product Catalog Component
 * Browse and search products with visual cards
 */

import { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  Chip,
  CircularProgress,
  InputAdornment,
  Stack,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import type { Product } from '../../types';
import { productService } from '../../services/mockData';
import { formatPrice } from '../../utils/formatters';

interface ProductCatalogProps {
  onAddToCart: (sku: string, quantity: number) => void;
}

export default function ProductCatalog({ onAddToCart }: ProductCatalogProps) {
  const [products, setProducts] = useState<Product[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadProducts();
  }, []);

  useEffect(() => {
    const timeoutId = setTimeout(() => {
      if (searchQuery.trim()) {
        searchProducts(searchQuery);
      } else {
        loadProducts();
      }
    }, 300); // Debounce search

    return () => clearTimeout(timeoutId);
  }, [searchQuery]);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const data = await productService.getAll();
      setProducts(data);
    } catch (error) {
      console.error('Failed to load products:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchProducts = async (query: string) => {
    setLoading(true);
    try {
      const results = await productService.search(query);
      setProducts(results);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box>
      <TextField
        fullWidth
        placeholder="Search by name, SKU, or category..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
        sx={{ mb: 3 }}
      />

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
          <CircularProgress />
        </Box>
      ) : products.length === 0 ? (
        <Typography color="text.secondary" sx={{ textAlign: 'center', p: 4 }}>
          {searchQuery ? 'No products found matching your search.' : 'No products available.'}
        </Typography>
      ) : (
        <Box
          sx={{
            display: 'grid',
            gridTemplateColumns: {
              xs: 'repeat(2, 1fr)',
              sm: 'repeat(3, 1fr)',
              md: 'repeat(4, 1fr)',
            },
            gap: 2,
            maxHeight: '70vh',
            overflowY: 'auto',
            pr: 1,
          }}
        >
          {products.map((product) => (
            <Card
              key={product.sku}
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'box-shadow 0.2s',
                '&:hover': {
                  boxShadow: 4,
                },
              }}
            >
              <CardMedia
                component="img"
                height="140"
                image={product.image_url || '/placeholder.png'}
                alt={product.name}
                sx={{
                  objectFit: 'contain',
                  bgcolor: 'grey.100',
                  p: 1,
                }}
                onError={(e) => {
                  // Fallback if image fails to load
                  const target = e.target as HTMLImageElement;
                  target.src = '/placeholder.png';
                }}
              />
              <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', p: 2 }}>
                <Typography variant="caption" color="text.secondary" gutterBottom>
                  {product.category}
                </Typography>
                <Typography
                  variant="body2"
                  fontWeight={600}
                  gutterBottom
                  sx={{
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    display: '-webkit-box',
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: 'vertical',
                    minHeight: '2.5em',
                  }}
                >
                  {product.name}
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ mb: 1 }}>
                  SKU: {product.sku}
                </Typography>
                <Box sx={{ mt: 'auto', pt: 1 }}>
                  <Stack direction="row" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                    <Typography variant="h6" color="primary" sx={{ fontWeight: 700 }}>
                      {formatPrice(product.price)}
                    </Typography>
                    <Chip
                      label={product.stock_quantity > 0 ? 'In Stock' : 'Out of Stock'}
                      color={product.stock_quantity > 0 ? 'success' : 'error'}
                      size="small"
                    />
                  </Stack>
                  <Button
                    fullWidth
                    variant="contained"
                    size="small"
                    startIcon={<AddShoppingCartIcon />}
                    onClick={() => onAddToCart(product.sku, 1)}
                    disabled={product.stock_quantity === 0 || !product.is_active}
                  >
                    Add to Cart
                  </Button>
                </Box>
              </CardContent>
            </Card>
          ))}
        </Box>
      )}
    </Box>
  );
}

