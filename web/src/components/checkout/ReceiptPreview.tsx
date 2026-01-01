/**
 * Receipt Preview Component
 * Displays receipt in a modal dialog with print and PDF download options
 */

import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Divider,
} from '@mui/material';
import PrintIcon from '@mui/icons-material/Print';
import DownloadIcon from '@mui/icons-material/Download';
import type { Transaction } from '../../types';
import { formatPrice, formatDateTime } from '../../utils/formatters';
import jsPDF from 'jspdf';

interface ReceiptPreviewProps {
  open: boolean;
  transaction: Transaction | null;
  onClose: () => void;
}

export default function ReceiptPreview({
  open,
  transaction,
  onClose,
}: ReceiptPreviewProps) {
  const handlePrint = () => {
    window.print();
  };

  const handleDownloadPDF = () => {
    if (!transaction) return;

    const doc = new jsPDF();
    
    // Store header
    doc.setFontSize(20);
    doc.text('AGENTIC RETAIL OS', 105, 20, { align: 'center' });
    doc.setFontSize(12);
    doc.text('Demo Store', 105, 30, { align: 'center' });
    doc.text('123 Main Street', 105, 36, { align: 'center' });
    doc.text('City, State 12345', 105, 42, { align: 'center' });
    
    // Transaction details
    doc.setFontSize(10);
    doc.text(`Transaction ID: ${transaction.transaction_id}`, 20, 55);
    doc.text(`Date: ${formatDateTime(transaction.timestamp)}`, 20, 61);
    if (transaction.cashier_name) {
      doc.text(`Cashier: ${transaction.cashier_name}`, 20, 67);
    }
    
    // Items table
    let y = 80;
    doc.text('Item', 20, y);
    doc.text('Qty', 100, y);
    doc.text('Price', 130, y);
    doc.text('Total', 170, y);
    y += 8;
    
    transaction.items.forEach(item => {
      doc.text(item.name.substring(0, 30), 20, y);
      doc.text(item.quantity.toString(), 100, y);
      doc.text(formatPrice(item.unit_price), 130, y);
      doc.text(formatPrice(item.line_total), 170, y);
      y += 8;
    });
    
    // Totals
    y += 5;
    doc.text(`Subtotal: ${formatPrice(transaction.subtotal)}`, 20, y);
    doc.text(`Tax: ${formatPrice(transaction.tax)}`, 20, y + 8);
    doc.setFontSize(12);
    doc.text(`Total: ${formatPrice(transaction.total)}`, 20, y + 18);
    
    // Footer
    doc.setFontSize(8);
    doc.text('Thank you for your business!', 105, 280, { align: 'center' });
    
    // Save PDF
    doc.save(`receipt-${transaction.transaction_id}.pdf`);
  };

  if (!transaction) return null;

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="sm"
      fullWidth
      PaperProps={{
        sx: {
          '@media print': {
            boxShadow: 'none',
            margin: 0,
            maxWidth: '100%',
          },
        },
      }}
    >
      <DialogTitle sx={{ textAlign: 'center', pb: 1 }}>
        <Typography variant="h5" component="div">
          AGENTIC RETAIL OS
        </Typography>
        <Typography variant="body2" color="text.secondary">
          Demo Store
        </Typography>
        <Typography variant="body2" color="text.secondary">
          123 Main Street, City, State 12345
        </Typography>
      </DialogTitle>
      <DialogContent>
        <Box
          sx={{
            fontFamily: 'monospace',
            '@media print': {
              fontFamily: 'monospace',
            },
          }}
        >
          <Box sx={{ mb: 2 }}>
            <Typography variant="body2">
              Transaction ID: {transaction.transaction_id}
            </Typography>
            <Typography variant="body2">
              Date: {formatDateTime(transaction.timestamp)}
            </Typography>
            {transaction.cashier_name && (
              <Typography variant="body2">
                Cashier: {transaction.cashier_name}
              </Typography>
            )}
          </Box>
          
          <Divider sx={{ my: 2 }} />
          
          {transaction.items.map((item, index) => (
            <Box
              key={index}
              sx={{
                display: 'flex',
                justifyContent: 'space-between',
                mb: 1,
              }}
            >
              <Box>
                <Typography variant="body2">
                  {item.quantity}x {item.name}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  SKU: {item.sku}
                </Typography>
              </Box>
              <Typography variant="body2" sx={{ fontWeight: 600 }}>
                {formatPrice(item.line_total)}
              </Typography>
            </Box>
          ))}
          
          <Divider sx={{ my: 2 }} />
          
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography>Subtotal:</Typography>
            <Typography>{formatPrice(transaction.subtotal)}</Typography>
          </Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
            <Typography>Tax:</Typography>
            <Typography>{formatPrice(transaction.tax)}</Typography>
          </Box>
          <Divider sx={{ my: 1 }} />
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <Typography variant="h6">Total:</Typography>
            <Typography variant="h6" color="primary">
              {formatPrice(transaction.total)}
            </Typography>
          </Box>
          
          <Box sx={{ mt: 3, textAlign: 'center' }}>
            <Typography variant="caption" color="text.secondary">
              Thank you for your business!
            </Typography>
          </Box>
        </Box>
      </DialogContent>
      <DialogActions sx={{ '@media print': { display: 'none' } }}>
        <Button onClick={onClose}>Close</Button>
        <Button onClick={handlePrint} startIcon={<PrintIcon />}>
          Print
        </Button>
        <Button
          onClick={handleDownloadPDF}
          variant="contained"
          startIcon={<DownloadIcon />}
        >
          Download PDF
        </Button>
      </DialogActions>
    </Dialog>
  );
}

