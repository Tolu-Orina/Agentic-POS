/**
 * Transaction History Screen
 * Displays list of past transactions with search and filter
 */

import { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  TextField,
  Card,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Chip,
} from '@mui/material';
import ReceiptIcon from '@mui/icons-material/Receipt';
import SearchIcon from '@mui/icons-material/Search';
import type { Transaction } from '../../types';
import { transactionService } from '../../services/mockData';
import { formatPrice, formatDateTime } from '../../utils/formatters';
import ReceiptPreview from '../checkout/ReceiptPreview';

export default function TransactionHistory() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [filteredTransactions, setFilteredTransactions] = useState<Transaction[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);
  const [receiptOpen, setReceiptOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTransactions();
  }, []);

  useEffect(() => {
    filterTransactions();
  }, [searchQuery, transactions]);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const data = await transactionService.getAll();
      setTransactions(data);
      setFilteredTransactions(data);
    } catch (error) {
      console.error('Failed to load transactions:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterTransactions = () => {
    if (!searchQuery.trim()) {
      setFilteredTransactions(transactions);
      return;
    }

    const query = searchQuery.toLowerCase();
    const filtered = transactions.filter(
      (txn) =>
        txn.transaction_id.toLowerCase().includes(query) ||
        txn.items.some((item) =>
          item.name.toLowerCase().includes(query) ||
          item.sku.toLowerCase().includes(query)
        )
    );
    setFilteredTransactions(filtered);
  };

  const handleViewReceipt = (transaction: Transaction) => {
    setSelectedTransaction(transaction);
    setReceiptOpen(true);
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Transaction History
      </Typography>

      <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
        <TextField
          fullWidth
          placeholder="Search by transaction ID, product name, or SKU..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          InputProps={{
            startAdornment: <SearchIcon sx={{ mr: 1, color: 'text.secondary' }} />,
          }}
        />
      </Box>

      {loading ? (
        <Typography>Loading transactions...</Typography>
      ) : filteredTransactions.length === 0 ? (
        <Card sx={{ p: 4, textAlign: 'center' }}>
          <Typography color="text.secondary">
            {searchQuery ? 'No transactions found matching your search.' : 'No transactions yet.'}
          </Typography>
        </Card>
      ) : (
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Date & Time</TableCell>
                <TableCell>Transaction ID</TableCell>
                <TableCell>Items</TableCell>
                <TableCell>Total</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="right">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredTransactions.map((transaction) => (
                <TableRow key={transaction.transaction_id} hover>
                  <TableCell>{formatDateTime(transaction.timestamp)}</TableCell>
                  <TableCell>
                    <Typography variant="body2" sx={{ fontFamily: 'monospace' }}>
                      {transaction.transaction_id}
                    </Typography>
                  </TableCell>
                  <TableCell>{transaction.items.length} items</TableCell>
                  <TableCell>
                    <Typography variant="body1" sx={{ fontWeight: 600 }}>
                      {formatPrice(transaction.total)}
                    </Typography>
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={transaction.status}
                      color={
                        transaction.status === 'completed'
                          ? 'success'
                          : transaction.status === 'cancelled'
                          ? 'error'
                          : 'warning'
                      }
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="right">
                    <Button
                      size="small"
                      onClick={() => handleViewReceipt(transaction)}
                      startIcon={<ReceiptIcon />}
                    >
                      View Receipt
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      <ReceiptPreview
        open={receiptOpen}
        transaction={selectedTransaction}
        onClose={() => {
          setReceiptOpen(false);
          setSelectedTransaction(null);
        }}
      />
    </Box>
  );
}

