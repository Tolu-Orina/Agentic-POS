/**
 * Main App Component
 * Sets up routing and theme provider
 */

import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './theme/theme';
import Layout from './components/common/Layout';
import CheckoutScreen from './components/checkout/CheckoutScreen';
import TransactionHistory from './components/receipts/TransactionHistory';
import BasicReporting from './components/analytics/BasicReporting';

// Placeholder component for inventory (Article 2)
const InventoryScreen = () => (
  <div style={{ padding: '20px' }}>
    <h2>Inventory Management</h2>
    <p>Coming in Article 2 - Multi-Agent System</p>
  </div>
);

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<CheckoutScreen />} />
            <Route path="checkout" element={<CheckoutScreen />} />
            <Route path="inventory" element={<InventoryScreen />} />
            <Route path="analytics" element={<BasicReporting />} />
            <Route path="history" element={<TransactionHistory />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
