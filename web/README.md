# Agentic Retail OS - Web Application

React + TypeScript frontend for the Agentic Retail OS POS system.

## Tech Stack

- **React 19** with TypeScript
- **Vite 7** - Fast build tool and dev server
- **Material UI v5** - Component library
- **React Router v6** - Routing
- **Axios** - HTTP client
- **jsPDF** - PDF generation
- **Recharts** - Chart library

## Development

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
web/
  src/
    components/
      checkout/        # Checkout screen components
      inventory/       # Inventory management (Article 2)
      analytics/       # Analytics dashboard (Article 2)
      common/          # Shared components (Layout, Navigation)
    services/          # API clients and mock data
    hooks/             # Custom React hooks
    utils/             # Utility functions
    types/             # TypeScript type definitions
    theme/             # Material UI theme configuration
    data/              # Local JSON data (for development)
  public/
    images/            # Product images
```

## Local Development

The app uses local JSON data files for development:
- `src/data/products.json` - Product catalog
- `src/data/transactions.json` - Transaction history

Product images are served from `public/images/` directory.

## Environment Variables

Create a `.env` file for API configuration:

```env
VITE_API_BASE_URL=http://localhost:3000/api
```

## Features (Article 1)

- ✅ Checkout Screen with item entry
- ✅ Real-time cart display
- ✅ Agent status indicator
- ✅ Transaction processing (mock)
- ✅ Receipt generation (coming soon)
- ✅ Transaction history (coming soon)
- ✅ Basic reporting (coming soon)
