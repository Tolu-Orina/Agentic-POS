/**
 * Material UI Theme Configuration
 * Based on UI/UX Design Document
 */

import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976D2', // Retail Blue - Trust, professionalism
      light: '#42A5F5',
      dark: '#1565C0',
      contrastText: '#FFFFFF',
    },
    secondary: {
      main: '#4CAF50', // Success Green - Stock available, positive actions
      light: '#81C784',
      dark: '#388E3C',
      contrastText: '#FFFFFF',
    },
    error: {
      main: '#F44336', // Alert Red - Low stock, errors
      light: '#E57373',
      dark: '#D32F2F',
    },
    warning: {
      main: '#FF9800', // Warning Orange - Reorder alerts
      light: '#FFB74D',
      dark: '#F57C00',
    },
    info: {
      main: '#2196F3', // Info Blue - Agent status, information
      light: '#64B5F6',
      dark: '#1976C0',
    },
    success: {
      main: '#4CAF50', // Success Green
    },
    background: {
      default: '#F5F5F5', // Light grey background
      paper: '#FFFFFF', // White cards/panels
    },
    text: {
      primary: '#212121', // Dark grey for primary text
      secondary: '#757575', // Medium grey for secondary text
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
      textTransform: 'none', // Keep button text as-is (no uppercase)
    },
  },
  spacing: 8, // 8px base spacing unit
  shape: {
    borderRadius: 8, // Consistent rounded corners
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

