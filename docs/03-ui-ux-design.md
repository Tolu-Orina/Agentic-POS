# UI/UX Design: Agentic Retail OS

## 1. Design System Overview

### Material UI (MUI) v5 Foundation

The Agentic Retail OS uses Material UI v5 as its design system foundation, providing a consistent, accessible, and customizable component library. We leverage MUI's theming system to create a retail-focused visual identity.

---

## 2. Theme Configuration

### Color Palette

```typescript
// theme.ts
import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976D2',        // Retail Blue - Trust, professionalism
      light: '#42A5F5',
      dark: '#1565C0',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#4CAF50',        // Success Green - Stock available, positive actions
      light: '#81C784',
      dark: '#388E3C',
      contrastText: '#FFFFFF',
    },
    error: {
      main: '#F44336',         // Alert Red - Low stock, errors
      light: '#E57373',
      dark: '#D32F2F',
    },
    warning: {
      main: '#FF9800',         // Warning Orange - Reorder alerts
      light: '#FFB74D',
      dark: '#F57C00',
    },
    info: {
      main: '#2196F3',         // Info Blue - Agent status, information
      light: '#64B5F6',
      dark: '#1976C0',
    },
    success: {
      main: '#4CAF50',         // Success Green
    },
    background: {
      default: '#F5F5F5',      // Light grey background
      paper: '#FFFFFF',         // White cards/panels
    },
    text: {
      primary: '#212121',       // Dark grey for primary text
      secondary: '#757575',     // Medium grey for secondary text
    },
  },
  typography: {
    fontFamily: [
      'Inter',
      'Roboto',
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontFamily: 'Roboto',
      fontWeight: 600,
      fontSize: '2.5rem',
    },
    h2: {
      fontFamily: 'Roboto',
      fontWeight: 600,
      fontSize: '2rem',
    },
    h3: {
      fontFamily: 'Roboto',
      fontWeight: 600,
      fontSize: '1.75rem',
    },
    h4: {
      fontFamily: 'Roboto',
      fontWeight: 600,
      fontSize: '1.5rem',
    },
    body1: {
      fontFamily: 'Inter',
      fontSize: '1rem',
      lineHeight: 1.5,
    },
    body2: {
      fontFamily: 'Inter',
      fontSize: '0.875rem',
      lineHeight: 1.5,
    },
    button: {
      fontFamily: 'Inter',
      fontWeight: 600,
      textTransform: 'none',    // Keep button text as-is (no uppercase)
    },
  },
  spacing: 8,                   // 8px base spacing unit
  shape: {
    borderRadius: 8,            // Consistent rounded corners
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '10px 24px',
          fontSize: '0.9375rem',
        },
        contained: {
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          '&:hover': {
            boxShadow: '0 4px 8px rgba(0,0,0,0.15)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
          },
        },
      },
    },
  },
});

export default theme;
```

### Typography Scale

- **H1**: 2.5rem (40px) - Page titles
- **H2**: 2rem (32px) - Section headers
- **H3**: 1.75rem (28px) - Subsection headers
- **H4**: 1.5rem (24px) - Card titles
- **Body1**: 1rem (16px) - Primary body text
- **Body2**: 0.875rem (14px) - Secondary text, captions
- **Button**: 0.9375rem (15px) - Button text
- **Caption**: 0.75rem (12px) - Small labels, timestamps

### Spacing System

8px base unit grid system:
- **xs**: 4px (0.5 units)
- **sm**: 8px (1 unit)
- **md**: 16px (2 units)
- **lg**: 24px (3 units)
- **xl**: 32px (4 units)
- **xxl**: 48px (6 units)

---

## 3. Application Layout

### Main Layout Structure

```
┌─────────────────────────────────────────────────────────┐
│  AppBar (Top Navigation)                                │
│  [Logo] [Store Name]              [User Menu] [Logout] │
├──────────┬──────────────────────────────────────────────┤
│          │                                               │
│ Sidebar  │  Main Content Area                           │
│ Nav      │                                               │
│          │  [Dynamic content based on route]             │
│ [Checkout│                                               │
│  Inventory│                                              │
│  Analytics│                                              │
│  History] │                                              │
│          │                                               │
└──────────┴──────────────────────────────────────────────┘
```

### AppBar Component

```typescript
// AppBar.tsx
<AppBar position="static" elevation={1}>
  <Toolbar>
    <Typography variant="h6" sx={{ flexGrow: 1 }}>
      Agentic Retail OS
    </Typography>
    <Typography variant="body2" sx={{ mr: 2 }}>
      {storeName}
    </Typography>
    <IconButton>
      <AccountCircle />
    </IconButton>
  </Toolbar>
</AppBar>
```

**Features**:
- Fixed at top of screen
- Store name display
- User menu with profile/logout
- Responsive: collapses on mobile

---

### Sidebar Navigation

```typescript
// Navigation.tsx
const navigationItems = [
  { label: 'Checkout', icon: <PointOfSale />, path: '/checkout' },
  { label: 'Inventory', icon: <Inventory />, path: '/inventory' },
  { label: 'Analytics', icon: <Analytics />, path: '/analytics' },
  { label: 'History', icon: <History />, path: '/history' },
];
```

**Features**:
- Persistent navigation on all screens
- Active route highlighting
- Icon + label for each item
- Collapsible on mobile (drawer)

---

### Responsive Breakpoints

```typescript
// Material UI breakpoints
xs: 0px      // Mobile (portrait)
sm: 600px    // Mobile (landscape) / Tablet (portrait)
md: 960px    // Tablet (landscape) / Small desktop
lg: 1280px   // Desktop
xl: 1920px   // Large desktop
```

**Layout Adaptations**:
- **Mobile (< 600px)**: Sidebar becomes drawer, AppBar simplified
- **Tablet (600-960px)**: Sidebar collapsible, content adapts
- **Desktop (> 960px)**: Full sidebar, multi-column layouts

---

## 4. Key Screens & Components

### Checkout Screen (Article 1)

**Purpose**: Primary interface for processing sales transactions

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  Checkout                                    [Agent Status]│
├──────────────────┬───────────────────────────────────────┤
│                  │                                       │
│  Item Entry      │  Cart Display                        │
│                  │                                       │
│  [SKU Input]     │  ┌─────────────────────────────────┐ │
│  [Quantity]      │  │ Item 1        $19.99            │ │
│  [Add to Cart]   │  │ Item 2        $29.99            │ │
│                  │  │ ...                              │ │
│  [Quick Add]     │  └─────────────────────────────────┘ │
│                  │                                       │
│                  │  Totals:                              │
│                  │  Subtotal: $49.98                    │
│                  │  Tax: $4.00                          │
│                  │  Total: $53.98                       │
│                  │                                       │
│                  │  [Complete Sale] [Clear Cart]        │
└──────────────────┴───────────────────────────────────────┘
```

**Components**:

#### ItemEntry.tsx
```typescript
<Card sx={{ p: 3, mb: 2 }}>
  <Typography variant="h6" gutterBottom>Add Item</Typography>
  <TextField
    label="SKU or Barcode"
    fullWidth
    value={skuInput}
    onChange={handleSkuChange}
    onKeyPress={handleKeyPress}
    autoFocus
    sx={{ mb: 2 }}
  />
  <TextField
    label="Quantity"
    type="number"
    value={quantity}
    onChange={handleQuantityChange}
    sx={{ mb: 2 }}
  />
  <Button
    variant="contained"
    fullWidth
    onClick={handleAddItem}
    disabled={!skuInput || agentLoading}
  >
    Add to Cart
  </Button>
</Card>
```

**Features**:
- SKU input with barcode scanner simulation
- Quantity selector (default: 1)
- Real-time agent inventory verification
- Loading state during agent processing
- Error handling for invalid SKUs

---

#### CartDisplay.tsx
```typescript
<Card sx={{ p: 3 }}>
  <Typography variant="h6" gutterBottom>Cart</Typography>
  {cartItems.length === 0 ? (
    <Typography color="text.secondary" align="center" sx={{ py: 4 }}>
      Cart is empty
    </Typography>
  ) : (
    <>
      <List>
        {cartItems.map((item) => (
          <ListItem key={item.sku}>
            <ListItemText
              primary={item.name}
              secondary={`SKU: ${item.sku} | Qty: ${item.quantity}`}
            />
            <Typography variant="body1" sx={{ fontWeight: 600 }}>
              ${formatPrice(item.lineTotal)}
            </Typography>
            <IconButton onClick={() => removeItem(item.sku)}>
              <Delete />
            </IconButton>
          </ListItem>
        ))}
      </List>
      <Divider sx={{ my: 2 }} />
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
        <Typography>Subtotal:</Typography>
        <Typography>${formatPrice(subtotal)}</Typography>
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
        <Typography>Tax:</Typography>
        <Typography>${formatPrice(tax)}</Typography>
      </Box>
      <Divider sx={{ my: 2 }} />
      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h6">Total:</Typography>
        <Typography variant="h6" color="primary">
          ${formatPrice(total)}
        </Typography>
      </Box>
    </>
  )}
</Card>
```

**Features**:
- Itemized list with remove functionality
- Real-time total calculation
- Tax calculation display
- Empty state messaging

---

#### AgentStatusIndicator.tsx
```typescript
<Chip
  icon={agentLoading ? <CircularProgress size={16} /> : <CheckCircle />}
  label={
    agentLoading
      ? 'Agent processing...'
      : agentStatus === 'success'
      ? 'Ready'
      : agentStatus === 'error'
      ? 'Error - Check connection'
      : 'Idle'
  }
  color={
    agentLoading
      ? 'info'
      : agentStatus === 'success'
      ? 'success'
      : agentStatus === 'error'
      ? 'error'
      : 'default'
  }
  sx={{ position: 'absolute', top: 16, right: 16 }}
/>
```

**Features**:
- Visual indicator of agent status
- Loading, success, error states
- Non-intrusive placement

---

#### ReceiptPreview.tsx
```typescript
<Dialog open={receiptOpen} onClose={handleCloseReceipt} maxWidth="sm" fullWidth>
  <DialogTitle>Receipt</DialogTitle>
  <DialogContent>
    <Box sx={{ fontFamily: 'monospace', p: 2 }}>
      {/* Receipt content */}
      <Typography variant="h6" align="center" gutterBottom>
        AGENTIC RETAIL OS
      </Typography>
      <Typography variant="body2" align="center" gutterBottom>
        123 Main Street
      </Typography>
      <Divider sx={{ my: 2 }} />
      {transaction.items.map((item) => (
        <Box key={item.sku} sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
          <Typography>{item.quantity}x {item.name}</Typography>
          <Typography>${formatPrice(item.lineTotal)}</Typography>
        </Box>
      ))}
      <Divider sx={{ my: 2 }} />
      <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
        <Typography variant="h6">Total:</Typography>
        <Typography variant="h6">${formatPrice(transaction.total)}</Typography>
      </Box>
    </Box>
  </DialogContent>
  <DialogActions>
    <Button onClick={handlePrint}>Print</Button>
    <Button onClick={handleDownloadPDF}>Download PDF</Button>
    <Button onClick={handleCloseReceipt}>Close</Button>
  </DialogActions>
</Dialog>
```

**Features**:
- Modal dialog for receipt display
- Print-optimized formatting
- Print and PDF download actions
- Monospace font for receipt-like appearance

---

### Inventory Management Screen (Article 2)

**Purpose**: Manage product catalog, monitor stock levels, handle restock requests

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  Inventory Management                                   │
├─────────────────────────────────────────────────────────┤
│  [Search] [Filter] [Add Product]                        │
├─────────────────────────────────────────────────────────┤
│  Product Catalog                                        │
│  ┌──────────┬──────────┬──────────┬──────────┐        │
│  │ SKU      │ Name     │ Stock    │ Status   │        │
│  ├──────────┼──────────┼──────────┼──────────┤        │
│  │ ABC123   │ Product 1│ 45       │ [Green]  │        │
│  │ DEF456   │ Product 2│ 8        │ [Yellow] │        │
│  │ GHI789   │ Product 3│ 2        │ [Red]    │        │
│  └──────────┴──────────┴──────────┴──────────┘        │
├─────────────────────────────────────────────────────────┤
│  Restock Requests                                       │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Product 3 - Low Stock (2 units)                  │  │
│  │ Recommended: 50 units                            │  │
│  │ [Generate Invoice] [Dismiss]                     │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Components**:

#### ProductCatalog.tsx
```typescript
<DataGrid
  rows={products}
  columns={[
    { field: 'sku', headerName: 'SKU', width: 150 },
    { field: 'name', headerName: 'Product Name', width: 200 },
    { field: 'category', headerName: 'Category', width: 150 },
    { field: 'price', headerName: 'Price', width: 100, renderCell: (params) => `$${formatPrice(params.value)}` },
    {
      field: 'stock_quantity',
      headerName: 'Stock',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={
            params.value > params.row.reorder_threshold * 2
              ? 'success'
              : params.value > params.row.reorder_threshold
              ? 'warning'
              : 'error'
          }
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <>
          <IconButton size="small" onClick={() => handleEdit(params.row)}>
            <Edit />
          </IconButton>
          <IconButton size="small" onClick={() => handleAdjustStock(params.row)}>
            <Inventory />
          </IconButton>
        </>
      ),
    },
  ]}
  pageSize={25}
  rowsPerPageOptions={[10, 25, 50]}
  disableSelectionOnClick
/>
```

**Features**:
- Searchable, filterable product table
- Color-coded stock levels
- Quick actions (edit, adjust stock)
- Pagination for large catalogs

---

#### StockLevelIndicator.tsx
```typescript
const getStockColor = (current: number, threshold: number) => {
  if (current > threshold * 2) return 'success';  // Green
  if (current > threshold) return 'warning';      // Yellow
  return 'error';                                  // Red
};

<Chip
  label={`${stockQuantity} units`}
  color={getStockColor(stockQuantity, reorderThreshold)}
  size="small"
/>
```

**Features**:
- Visual color coding (green/yellow/red)
- Threshold-based logic
- Clear stock level display

---

#### RestockRequestCard.tsx
```typescript
<Alert severity="warning" sx={{ mb: 2 }}>
  <AlertTitle>Low Stock Alert</AlertTitle>
  <Typography variant="body2">
    <strong>{productName}</strong> (SKU: {sku}) has {currentStock} units remaining.
    Recommended restock: {recommendedQuantity} units.
  </Typography>
  <Box sx={{ mt: 2, display: 'flex', gap: 1 }}>
    <Button
      variant="contained"
      size="small"
      onClick={handleGenerateInvoice}
      startIcon={<Receipt />}
    >
      Generate Invoice
    </Button>
    <Button
      variant="outlined"
      size="small"
      onClick={handleDismiss}
    >
      Dismiss
    </Button>
  </Box>
</Alert>
```

**Features**:
- Alert-style card for visibility
- Product details and recommendations
- Quick actions (generate invoice, dismiss)
- Auto-generated by inventory agent

---

#### InvoiceGenerator.tsx
```typescript
<Dialog open={invoiceOpen} onClose={handleCloseInvoice} maxWidth="md" fullWidth>
  <DialogTitle>Inventory Invoice</DialogTitle>
  <DialogContent>
    <Box sx={{ fontFamily: 'sans-serif', p: 2 }}>
      <Typography variant="h5" gutterBottom>INVOICE</Typography>
      <Typography variant="body2" gutterBottom>Invoice #: {invoiceNumber}</Typography>
      <Typography variant="body2" gutterBottom>Date: {formatDate(invoiceDate)}</Typography>
      
      <Box sx={{ my: 3 }}>
        <Typography variant="subtitle2" gutterBottom>Bill To:</Typography>
        <Typography>{supplierName}</Typography>
        <Typography variant="body2">{supplierAddress}</Typography>
      </Box>
      
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Item</TableCell>
            <TableCell align="right">Quantity</TableCell>
            <TableCell align="right">Unit Price</TableCell>
            <TableCell align="right">Total</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {invoiceItems.map((item) => (
            <TableRow key={item.sku}>
              <TableCell>{item.name}</TableCell>
              <TableCell align="right">{item.quantity}</TableCell>
              <TableCell align="right">${formatPrice(item.unitPrice)}</TableCell>
              <TableCell align="right">${formatPrice(item.lineTotal)}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      
      <Box sx={{ mt: 3, textAlign: 'right' }}>
        <Typography variant="h6">Total: ${formatPrice(invoiceTotal)}</Typography>
      </Box>
    </Box>
  </DialogContent>
  <DialogActions>
    <Button onClick={handlePrintInvoice}>Print</Button>
    <Button onClick={handleDownloadInvoicePDF}>Download PDF</Button>
    <Button onClick={handleCloseInvoice}>Close</Button>
  </DialogActions>
</Dialog>
```

**Features**:
- Professional invoice layout
- Supplier information display
- Itemized product list
- Print and PDF download

---

### Analytics Dashboard (Article 2)

**Purpose**: Natural language analytics queries and visual data representation

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  Analytics Dashboard                                     │
├─────────────────────────────────────────────────────────┤
│  Natural Language Query                                  │
│  ┌──────────────────────────────────────────────────┐  │
│  │ What was our top seller today?                    │  │
│  │                                    [Ask Agent]    │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Agent Response                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Based on today's sales data, the top seller is   │  │
│  │ "Product X" with 45 units sold, generating       │  │
│  │ $899.55 in revenue.                              │  │
│  └──────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  Visualizations                                          │
│  ┌──────────────────┬──────────────────────────────┐  │
│  │ Sales Trend      │ Top Products                 │  │
│  │ [Line Chart]     │ [Bar Chart]                  │  │
│  └──────────────────┴──────────────────────────────┘  │
│  [Time Range: Today | This Week | This Month]          │
└─────────────────────────────────────────────────────────┘
```

**Components**:

#### NLQueryInput.tsx
```typescript
<Card sx={{ p: 3, mb: 3 }}>
  <Typography variant="h6" gutterBottom>Ask a Question</Typography>
  <TextField
    fullWidth
    multiline
    rows={3}
    placeholder="e.g., What was our most profitable item this morning?"
    value={query}
    onChange={handleQueryChange}
    disabled={agentProcessing}
    sx={{ mb: 2 }}
  />
  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
    <FormControl>
      <Select value={timeRange} onChange={handleTimeRangeChange}>
        <MenuItem value="today">Today</MenuItem>
        <MenuItem value="week">This Week</MenuItem>
        <MenuItem value="month">This Month</MenuItem>
      </Select>
    </FormControl>
    <Button
      variant="contained"
      onClick={handleSubmitQuery}
      disabled={!query || agentProcessing}
      startIcon={agentProcessing ? <CircularProgress size={20} /> : <Send />}
    >
      {agentProcessing ? 'Processing...' : 'Ask Agent'}
    </Button>
  </Box>
</Card>
```

**Features**:
- Natural language input field
- Time range selector
- Loading state during agent processing
- Clear, conversational interface

---

#### AgentResponseDisplay.tsx
```typescript
<Card sx={{ p: 3, mb: 3, bgcolor: 'background.paper' }}>
  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
    <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
      <SmartToy />
    </Avatar>
    <Typography variant="h6">Agent Response</Typography>
  </Box>
  {response ? (
    <>
      <Typography variant="body1" paragraph>
        {response.answer}
      </Typography>
      {response.supportingData && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="subtitle2" gutterBottom>Supporting Data:</Typography>
          <Table size="small">
            <TableBody>
              {Object.entries(response.supportingData).map(([key, value]) => (
                <TableRow key={key}>
                  <TableCell><strong>{key}:</strong></TableCell>
                  <TableCell>{String(value)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      )}
    </>
  ) : (
    <Typography color="text.secondary" align="center" sx={{ py: 4 }}>
      Ask a question to get insights
    </Typography>
  )}
</Card>
```

**Features**:
- Formatted agent response display
- Supporting data table
- Empty state when no query submitted
- Visual agent indicator

---

#### SalesChart.tsx
```typescript
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

<Card sx={{ p: 3 }}>
  <Typography variant="h6" gutterBottom>Sales Trend</Typography>
  <ResponsiveContainer width="100%" height={300}>
    <LineChart data={salesData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="revenue" stroke="#1976D2" name="Revenue" />
      <Line type="monotone" dataKey="transactions" stroke="#4CAF50" name="Transactions" />
    </LineChart>
  </ResponsiveContainer>
</Card>
```

**Features**:
- Interactive charts (Recharts library)
- Multiple data series
- Tooltips and legends
- Responsive sizing

---

### Transaction History Screen

**Purpose**: View past transactions, access receipts

**Layout**:
```
┌─────────────────────────────────────────────────────────┐
│  Transaction History                                     │
├─────────────────────────────────────────────────────────┤
│  [Search] [Date Range] [Filter]                         │
├─────────────────────────────────────────────────────────┤
│  Transactions                                            │
│  ┌──────────┬──────────┬──────────┬──────────┐        │
│  │ Date     │ ID       │ Items    │ Total    │        │
│  ├──────────┼──────────┼──────────┼──────────┤        │
│  │ 2025-01-15│ TXN-001 │ 3 items │ $53.98   │        │
│  │ 2025-01-15│ TXN-002 │ 5 items │ $127.50  │        │
│  └──────────┴──────────┴──────────┴──────────┘        │
└─────────────────────────────────────────────────────────┘
```

**Components**:

#### ReceiptList.tsx
```typescript
<DataGrid
  rows={transactions}
  columns={[
    { field: 'timestamp', headerName: 'Date & Time', width: 180, renderCell: (params) => formatDateTime(params.value) },
    { field: 'transaction_id', headerName: 'Transaction ID', width: 200 },
    { field: 'items', headerName: 'Items', width: 100, renderCell: (params) => `${params.value.length} items` },
    { field: 'total', headerName: 'Total', width: 120, renderCell: (params) => `$${formatPrice(params.value)}` },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 150,
      renderCell: (params) => (
        <Button
          size="small"
          onClick={() => handleViewReceipt(params.row)}
          startIcon={<Receipt />}
        >
          View Receipt
        </Button>
      ),
    },
  ]}
  pageSize={25}
  rowsPerPageOptions={[10, 25, 50]}
/>
```

**Features**:
- Searchable transaction list
- Date range filtering
- Quick receipt access
- Pagination

---

## 5. User Flows

### Flow 1: Complete Sale

```
1. Cashier opens Checkout screen
   ↓
2. Enters SKU in input field (or simulates barcode scan)
   ↓
3. Agent automatically verifies inventory (loading indicator shown)
   ↓
4. If available: Item added to cart with price
   If unavailable: Error message displayed
   ↓
5. Cashier enters quantity (default: 1)
   ↓
6. Clicks "Add to Cart"
   ↓
7. Cart updates with itemized list and running total
   ↓
8. Agent applies any applicable discounts automatically
   ↓
9. Cashier reviews cart and totals
   ↓
10. Clicks "Complete Sale"
    ↓
11. Agent processes transaction and updates inventory
    ↓
12. Receipt generated and displayed in modal
    ↓
13. Cashier can:
    - Print receipt (browser print dialog)
    - Download PDF
    - Close and start new transaction
```

**UI States**:
- **Idle**: Ready for input
- **Processing**: Agent checking inventory (loading spinner)
- **Cart Updated**: Item added, totals recalculated
- **Completing**: Transaction processing (loading state)
- **Complete**: Receipt displayed, success message

---

### Flow 2: Inventory Restock

```
1. Background inventory agent detects low stock
   ↓
2. Restock request card appears in Inventory screen
   ↓
3. Manager reviews request (product, current stock, recommended quantity)
   ↓
4. Manager clicks "Generate Invoice"
   ↓
5. Inventory agent generates invoice with supplier details
   ↓
6. Invoice displayed in modal dialog
   ↓
7. Manager reviews invoice (items, quantities, totals)
   ↓
8. Manager can:
    - Print invoice (browser print dialog)
    - Download PDF for email
    - Close invoice
   ↓
9. After restocking, manager updates stock levels manually
   ↓
10. System syncs updated quantities
```

**UI States**:
- **Alert**: Restock request card visible
- **Generating**: Invoice generation in progress
- **Invoice Ready**: Invoice displayed with print/download options
- **Stock Updated**: Confirmation message, request dismissed

---

### Flow 3: Analytics Query

```
1. Manager opens Analytics Dashboard
   ↓
2. Types natural language query in input field
   (e.g., "What was our top seller today?")
   ↓
3. Selects time range (Today/This Week/This Month)
   ↓
4. Clicks "Ask Agent"
   ↓
5. Analytics agent processes query (loading indicator)
   ↓
6. Agent retrieves relevant data from DynamoDB
   ↓
7. Agent analyzes data and generates insights
   ↓
8. Response displayed with:
    - Natural language answer
    - Supporting data table
    - Relevant charts/graphs
   ↓
9. Manager can:
    - Ask follow-up questions
    - Export report as PDF/CSV
    - Adjust time range and re-query
```

**UI States**:
- **Ready**: Query input available
- **Processing**: Agent analyzing (loading spinner, "Processing..." message)
- **Response**: Answer displayed with data and charts
- **Error**: Error message if query fails or data unavailable

---

## 6. Accessibility & UX Principles

### WCAG 2.1 AA Compliance

**Color Contrast**:
- Text meets 4.5:1 contrast ratio minimum
- Interactive elements meet 3:1 contrast ratio
- Color not sole indicator (icons + text)

**Keyboard Navigation**:
- All interactive elements keyboard accessible
- Tab order follows visual flow
- Focus indicators visible
- Skip links for main content

**Screen Reader Support**:
- Semantic HTML elements
- ARIA labels for icons and buttons
- Alt text for images
- Form labels associated with inputs
- Status announcements for agent actions

**Example**:
```typescript
<Button
  aria-label="Add item to cart"
  onClick={handleAddItem}
>
  <AddShoppingCart aria-hidden="true" />
  Add to Cart
</Button>
```

---

### Loading States

**Agent Processing Indicators**:
```typescript
{agentLoading && (
  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 2 }}>
    <CircularProgress size={24} />
    <Typography variant="body2">Agent is processing your request...</Typography>
  </Box>
)}
```

**Skeleton Loaders** (for data tables):
```typescript
<Skeleton variant="rectangular" width="100%" height={200} />
```

---

### Error Handling

**User-Friendly Error Messages**:
```typescript
<Alert severity="error" sx={{ mb: 2 }}>
  <AlertTitle>Unable to Process Transaction</AlertTitle>
  <Typography variant="body2">
    The item you're trying to add is out of stock. 
    Please check with the inventory manager or try a different item.
  </Typography>
</Alert>
```

**Error States**:
- Network errors: "Connection issue. Please check your internet and try again."
- Agent errors: "Agent is temporarily unavailable. Please try again in a moment."
- Validation errors: Inline field errors with specific guidance
- 404 errors: "Page not found" with navigation back to home

---

### Confirmation Dialogs

**Critical Actions**:
```typescript
<Dialog open={confirmOpen} onClose={handleCloseConfirm}>
  <DialogTitle>Confirm Action</DialogTitle>
  <DialogContent>
    <Typography>Are you sure you want to clear the cart? This action cannot be undone.</Typography>
  </DialogContent>
  <DialogActions>
    <Button onClick={handleCloseConfirm}>Cancel</Button>
    <Button onClick={handleConfirm} color="error" variant="contained">
      Clear Cart
    </Button>
  </DialogActions>
</Dialog>
```

**Actions Requiring Confirmation**:
- Clear cart
- Delete product
- Cancel transaction
- Dismiss restock request

---

## 7. Print-Ready Components

### Receipt Print Stylesheet

```css
@media print {
  body {
    margin: 0;
    padding: 0;
    font-family: 'Courier New', monospace;
  }
  
  .no-print {
    display: none !important;
  }
  
  .receipt-content {
    width: 80mm; /* Standard thermal printer width */
    margin: 0 auto;
    padding: 10px;
  }
  
  .receipt-header {
    text-align: center;
    margin-bottom: 10px;
  }
  
  .receipt-items {
    border-top: 1px dashed #000;
    border-bottom: 1px dashed #000;
    padding: 10px 0;
    margin: 10px 0;
  }
  
  .receipt-totals {
    text-align: right;
    margin-top: 10px;
  }
  
  .receipt-footer {
    text-align: center;
    margin-top: 20px;
    font-size: 10px;
  }
}
```

### Invoice Print Stylesheet

```css
@media print {
  .invoice-content {
    width: 8.5in;
    margin: 0 auto;
    padding: 0.5in;
  }
  
  .invoice-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
  }
  
  .invoice-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
  }
  
  .invoice-table th,
  .invoice-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
  }
  
  .invoice-totals {
    text-align: right;
    margin-top: 20px;
  }
}
```

---

## 8. Mobile Responsiveness

### Mobile Adaptations (< 600px)

**Layout Changes**:
- Sidebar becomes drawer (hamburger menu)
- AppBar simplified (logo + menu icon)
- Single-column layouts
- Stacked form fields
- Full-width buttons

**Touch Optimizations**:
- Larger tap targets (min 44x44px)
- Swipe gestures for navigation
- Bottom sheet for actions
- Simplified cart display

**Example Mobile Checkout**:
```typescript
{isMobile && (
  <BottomSheet open={cartOpen} onClose={handleCloseCart}>
    <Box sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>Cart</Typography>
      {/* Cart content */}
      <Button variant="contained" fullWidth sx={{ mt: 2 }}>
        Complete Sale
      </Button>
    </Box>
  </BottomSheet>
)}
```

---

## 9. Component Library Usage

### Material UI Components Used

**Navigation**:
- `AppBar`, `Toolbar`, `Drawer`, `List`, `ListItem`, `ListItemButton`

**Layout**:
- `Container`, `Grid`, `Box`, `Stack`, `Paper`, `Card`

**Input**:
- `TextField`, `Select`, `MenuItem`, `Checkbox`, `Radio`, `Switch`

**Feedback**:
- `Button`, `IconButton`, `Chip`, `Alert`, `Snackbar`, `Dialog`, `CircularProgress`, `Skeleton`

**Data Display**:
- `Typography`, `Table`, `DataGrid`, `List`, `Avatar`, `Badge`

**Navigation**:
- `Tabs`, `Stepper`, `Breadcrumbs`

---

## 10. Design Tokens

### Spacing Scale
```typescript
const spacing = {
  xs: 4,   // 0.5 units
  sm: 8,   // 1 unit
  md: 16,  // 2 units
  lg: 24,  // 3 units
  xl: 32,  // 4 units
  xxl: 48, // 6 units
};
```

### Elevation (Shadows)
```typescript
const elevations = {
  card: 2,      // Cards, panels
  dialog: 8,    // Modals, dialogs
  appBar: 4,    // Top navigation
  floating: 6, // Floating action buttons
};
```

### Border Radius
```typescript
const borderRadius = {
  small: 4,   // Buttons, chips
  medium: 8, // Cards, inputs
  large: 12, // Large cards, dialogs
};
```

---

## 11. Animation & Transitions

### Page Transitions
```typescript
// React Router with Framer Motion
<AnimatePresence mode="wait">
  <Routes location={location} key={location.pathname}>
    <Route path="/checkout" element={<CheckoutScreen />} />
    {/* ... */}
  </Routes>
</AnimatePresence>
```

### Loading Animations
- Skeleton loaders for data tables
- Circular progress for agent processing
- Pulse animation for active agent status

### Micro-interactions
- Button hover effects
- Card elevation on hover
- Smooth scroll to sections
- Toast notifications slide-in

---

## 12. Conclusion

This UI/UX design provides a comprehensive, accessible, and user-friendly interface for the Agentic Retail OS platform. The Material UI foundation ensures consistency and accessibility, while the component designs address real-world retail workflows.

The design balances functionality with simplicity, providing clear visual feedback for agent actions while maintaining an intuitive user experience. Responsive design ensures the platform works seamlessly across devices, from desktop POS terminals to mobile manager dashboards.

