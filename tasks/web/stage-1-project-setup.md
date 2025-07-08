# Stage 1: Project Setup and Infrastructure

## Overview
This stage sets up the React web frontend infrastructure with the specified tech stack: React + TanStack Router + TanStack Query + Tailwind CSS 4 + ShadCN UI. The project will be client-side only and deployed on Vercel.

## Goals
- Initialize React project in `web/` folder
- Configure TanStack Router for routing
- Set up TanStack Query for data fetching
- Configure Tailwind CSS 4
- Install and configure ShadCN UI
- Set up Vercel deployment configuration
- Create basic project structure

## Files to Create/Modify

### 1. Create React Project Structure
```bash
# Run from project root
cd web
npx create-react-app . --template typescript
# or use Vite for better performance
npm create vite@latest . -- --template react-ts
```

### 2. Package.json Configuration
**File: `web/package.json`** (New file)
```json
{
  "name": "aipriceaction-web",
  "version": "0.1.0",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@tanstack/react-router": "^1.58.3",
    "@tanstack/router-devtools": "^1.58.3",
    "@tanstack/react-query": "^5.56.2",
    "@tanstack/react-query-devtools": "^5.56.2",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-navigation-menu": "^1.1.4",
    "@radix-ui/react-tabs": "^1.0.4",
    "@radix-ui/react-accordion": "^1.1.2",
    "@radix-ui/react-scroll-area": "^1.0.5",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.5.2",
    "lucide-react": "^0.441.0",
    "react-markdown": "^9.0.1",
    "remark-gfm": "^4.0.0",
    "csv-parse": "^5.5.6",
    "recharts": "^2.12.7",
    "date-fns": "^3.6.0",
    "papaparse": "^5.4.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.2.2",
    "vite": "^5.0.8",
    "@types/papaparse": "^5.3.14"
  }
}
```

### 3. Vite Configuration
**File: `web/vite.config.ts`** (New file)
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
  },
  server: {
    port: 3000,
  },
})
```

### 4. TypeScript Configuration
**File: `web/tsconfig.json`** (New file)
```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### 5. Tailwind CSS Configuration
**File: `web/tailwind.config.js`** (New file)
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ['class'],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: '',
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      colors: {
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },
      },
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}
```

### 6. PostCSS Configuration
**File: `web/postcss.config.js`** (New file)
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### 7. Global CSS with ShadCN Variables
**File: `web/src/index.css`** (New file)
```css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222.2 84% 4.9%;
    --muted: 210 40% 96%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96%;
    --accent-foreground: 222.2 84% 4.9%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 84% 4.9%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 224.3 76.3% 94.1%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

### 8. Utility Functions for ShadCN
**File: `web/src/lib/utils.ts`** (New file)
```typescript
import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### 9. TanStack Router Configuration
**File: `web/src/routeTree.gen.ts`** (New file - will be auto-generated)
```typescript
// This file is auto-generated by TanStack Router
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/')({
  component: () => <div>Hello World!</div>,
})
```

### 10. Router Setup
**File: `web/src/router.tsx`** (New file)
```typescript
import { createRouter, createRoute, createRootRoute } from '@tanstack/react-router'
import { QueryClient } from '@tanstack/react-query'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'

// Create a root route
const rootRoute = createRootRoute({
  component: () => (
    <>
      <div id="app">
        {/* Router outlet will be here */}
      </div>
      <TanStackRouterDevtools />
    </>
  ),
})

// Create an index route
const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: function Index() {
    return (
      <div className="p-8">
        <h1 className="text-3xl font-bold">AI Price Action Dashboard</h1>
        <p className="mt-4 text-muted-foreground">
          Welcome to the Vietnamese Stock Market Analysis Dashboard
        </p>
      </div>
    )
  },
})

// Create the route tree
const routeTree = rootRoute.addChildren([indexRoute])

// Create the router instance
export const router = createRouter({ routeTree })

// Register the router instance for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
```

### 11. Query Client Setup
**File: `web/src/lib/queryClient.ts`** (New file)
```typescript
import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutes
      cacheTime: 1000 * 60 * 10, // 10 minutes
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})
```

### 12. Main App Component
**File: `web/src/App.tsx`** (New file)
```typescript
import { RouterProvider } from '@tanstack/react-router'
import { QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { router } from './router'
import { queryClient } from './lib/queryClient'

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  )
}

export default App
```

### 13. Entry Point
**File: `web/src/main.tsx`** (New file)
```typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

### 14. HTML Template
**File: `web/index.html`** (New file)
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>AI Price Action Dashboard</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### 15. Vercel Configuration
**File: `vercel.json`** (New file in project root)
```json
{
  "builds": [
    {
      "src": "web/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "web/dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/web/dist/$1"
    }
  ],
  "buildCommand": "cd web && npm run build",
  "outputDirectory": "web/dist",
  "installCommand": "cd web && npm install"
}
```

### 16. Environment Variables
**File: `web/.env`** (New file)
```
VITE_GITHUB_REPO_URL=https://raw.githubusercontent.com/quanhua92/aipriceaction/main
VITE_APP_TITLE=AI Price Action Dashboard
VITE_CHART_LIBRARY=recharts
```

### 17. GitHub Actions Workflow (Optional)
**File: `.github/workflows/deploy.yml`** (New file)
```yaml
name: Deploy to Vercel

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: web/package-lock.json
      
      - name: Install dependencies
        run: cd web && npm ci
      
      - name: Build project
        run: cd web && npm run build
      
      - name: Deploy to Vercel
        uses: vercel/action@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID }}
          vercel-project-id: ${{ secrets.PROJECT_ID }}
```

## Implementation Steps

1. **Create web directory:**
   ```bash
   mkdir web
   cd web
   ```

2. **Initialize with Vite:**
   ```bash
   npm create vite@latest . -- --template react-ts
   ```

3. **Install dependencies:**
   ```bash
   npm install @tanstack/react-router @tanstack/router-devtools @tanstack/react-query @tanstack/react-query-devtools
   npm install @radix-ui/react-slot @radix-ui/react-dialog @radix-ui/react-select @radix-ui/react-navigation-menu @radix-ui/react-tabs @radix-ui/react-accordion @radix-ui/react-scroll-area
   npm install class-variance-authority clsx tailwind-merge lucide-react react-markdown remark-gfm csv-parse
   npm install recharts date-fns papaparse
   npm install -D tailwindcss postcss autoprefixer tailwindcss-animate @types/papaparse
   ```

4. **Initialize Tailwind:**
   ```bash
   npx tailwindcss init -p
   ```

5. **Test the setup:**
   ```bash
   npm run dev
   ```

## Expected Outcome
- Working React + TypeScript application with Vite
- TanStack Router configured for client-side routing
- TanStack Query ready for data fetching
- Tailwind CSS 4 with ShadCN UI foundation
- Vercel deployment configuration
- Development server running on localhost:3000

## Troubleshooting

### Common Issues:
1. **Module resolution errors**: Ensure `@` alias is properly configured in both `vite.config.ts` and `tsconfig.json`
2. **Tailwind classes not working**: Check that `tailwind.config.js` content paths include all relevant files
3. **Router not working**: Verify that `RouterProvider` is properly configured in `App.tsx`
4. **Query client errors**: Ensure `QueryClientProvider` wraps the entire app

### Fallback Options:
- If Vite has issues, fall back to Create React App: `npx create-react-app . --template typescript`
- If TanStack Router is problematic, temporarily use React Router DOM for initial setup
- If Tailwind 4 is unstable, use Tailwind CSS 3.4

## Next Steps
After completing this stage, you should have a fully functional React application with:
- Modern development tooling (Vite, TypeScript, ESLint)
- Routing capability (TanStack Router)
- Data fetching foundation (TanStack Query)
- UI styling system (Tailwind CSS + ShadCN UI)
- Deployment configuration (Vercel)

The application should successfully start with `npm run dev` and display a basic welcome page.

## Testing
Run the following commands to verify the setup:
```bash
cd web
npm install
npm run build
npm run dev
```

All commands should complete without errors, and the development server should start successfully.