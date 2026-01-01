/**
 * Basic Reporting Dashboard
 * Shows daily sales summary and top-selling items
 */

import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider,
  Stack,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import { transactionService } from '../../services/mockData';
import { formatPrice, formatDate } from '../../utils/formatters';

interface DailyStats {
  totalRevenue: number;
  transactionCount: number;
  averageTransactionValue: number;
  topSellingItems: Array<{
    sku: string;
    name: string;
    quantitySold: number;
    revenue: number;
  }>;
}

export default function BasicReporting() {
  const [stats, setStats] = useState<DailyStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const transactions = await transactionService.getAll();
      
      // Get today's date
      const today = new Date().toISOString().split('T')[0];
      
      // Filter today's transactions
      const todayTransactions = transactions.filter((txn) =>
        txn.timestamp.startsWith(today)
      );
      
      // Calculate stats
      const totalRevenue = todayTransactions.reduce(
        (sum, txn) => sum + txn.total,
        0
      );
      const transactionCount = todayTransactions.length;
      const averageTransactionValue =
        transactionCount > 0 ? Math.round(totalRevenue / transactionCount) : 0;
      
      // Calculate top-selling items
      const itemMap = new Map<string, { name: string; quantity: number; revenue: number }>();
      
      todayTransactions.forEach((txn) => {
        txn.items.forEach((item) => {
          const existing = itemMap.get(item.sku);
          if (existing) {
            existing.quantity += item.quantity;
            existing.revenue += item.line_total;
          } else {
            itemMap.set(item.sku, {
              name: item.name,
              quantity: item.quantity,
              revenue: item.line_total,
            });
          }
        });
      });
      
      const topSellingItems = Array.from(itemMap.entries())
        .map(([sku, data]) => ({
          sku,
          name: data.name,
          quantitySold: data.quantity,
          revenue: data.revenue,
        }))
        .sort((a, b) => b.quantitySold - a.quantitySold)
        .slice(0, 5);
      
      setStats({
        totalRevenue,
        transactionCount,
        averageTransactionValue,
        topSellingItems,
      });
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Typography>Loading statistics...</Typography>;
  }

  if (!stats) {
    return <Typography>No data available</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Daily Sales Summary
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        {formatDate(new Date().toISOString())}
      </Typography>

      <Stack
        direction={{ xs: 'column', sm: 'row' }}
        spacing={3}
        sx={{ mb: 4 }}
      >
        <Box sx={{ flex: 1 }}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <AttachMoneyIcon sx={{ mr: 1, color: 'primary.main' }} />
                <Typography variant="h6">Total Revenue</Typography>
              </Box>
              <Typography variant="h4" color="primary">
                {formatPrice(stats.totalRevenue)}
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: 1 }}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <ShoppingCartIcon sx={{ mr: 1, color: 'secondary.main' }} />
                <Typography variant="h6">Transactions</Typography>
              </Box>
              <Typography variant="h4" color="secondary">
                {stats.transactionCount}
              </Typography>
            </CardContent>
          </Card>
        </Box>
        <Box sx={{ flex: 1 }}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingUpIcon sx={{ mr: 1, color: 'info.main' }} />
                <Typography variant="h6">Avg Transaction</Typography>
              </Box>
              <Typography variant="h4" color="info.main">
                {formatPrice(stats.averageTransactionValue)}
              </Typography>
            </CardContent>
          </Card>
        </Box>
      </Stack>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Top Selling Items Today
          </Typography>
          {stats.topSellingItems.length === 0 ? (
            <Typography color="text.secondary">
              No sales data for today yet.
            </Typography>
          ) : (
            <List>
              {stats.topSellingItems.map((item, index) => (
                <Box key={item.sku}>
                  <ListItem>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                          <Typography variant="body1">
                            {index + 1}. {item.name}
                          </Typography>
                          <Typography variant="body1" sx={{ fontWeight: 600 }}>
                            {formatPrice(item.revenue)}
                          </Typography>
                        </Box>
                      }
                      secondary={`SKU: ${item.sku} | Quantity: ${item.quantitySold}`}
                    />
                  </ListItem>
                  {index < stats.topSellingItems.length - 1 && <Divider />}
                </Box>
              ))}
            </List>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}

