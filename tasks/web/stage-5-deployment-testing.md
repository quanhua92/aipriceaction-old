# Stage 5: Deployment and Testing

## Overview
This final stage focuses on deployment configuration, comprehensive testing, performance optimization, and production readiness. We'll configure Vercel deployment, add testing infrastructure, and ensure the application is robust and performant.

## Goals
- Configure Vercel deployment with proper build settings
- Add comprehensive testing suite
- Implement performance optimizations
- Add SEO and meta tags
- Configure error monitoring and analytics
- Create production environment configurations
- Add CI/CD pipeline
- Implement security best practices

## Files to Create/Modify

### 1. Update Vercel Configuration
**File: `vercel.json`** (Update existing in project root)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "web/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/web/dist/index.html"
    }
  ],
  "buildCommand": "cd web && npm ci && npm run build",
  "outputDirectory": "web/dist",
  "installCommand": "cd web && npm ci",
  "framework": "vite",
  "regions": ["sin1", "hnd1"],
  "functions": {
    "web/dist/**": {
      "headers": {
        "cache-control": "public, max-age=31536000, immutable"
      }
    }
  },
  "headers": [
    {
      "source": "/web/dist/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Permissions-Policy",
          "value": "camera=(), microphone=(), geolocation=()"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/portfolio",
      "destination": "/private/portfolio/analysis/hold",
      "permanent": false
    }
  ]
}
```

### 2. Production Environment Configuration
**File: `web/.env.production`** (New file)
```
VITE_GITHUB_REPO_URL=https://raw.githubusercontent.com/quanhua92/aipriceaction/main
VITE_APP_TITLE=AI Price Action Dashboard
VITE_CHART_LIBRARY=recharts
VITE_ENVIRONMENT=production
VITE_API_CACHE_DURATION=300000
VITE_ENABLE_ANALYTICS=true
VITE_SENTRY_DSN=
```

### 3. Updated Vite Configuration for Production
**File: `web/vite.config.ts`** (Update existing)
```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig(({ mode }) => ({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: mode === 'development',
    minify: 'esbuild',
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['@tanstack/react-router'],
          query: ['@tanstack/react-query'],
          charts: ['recharts'],
          ui: ['@radix-ui/react-tabs', '@radix-ui/react-dialog', '@radix-ui/react-select'],
          markdown: ['react-markdown', 'remark-gfm'],
          utils: ['date-fns', 'papaparse', 'zustand']
        }
      }
    },
    target: 'es2020',
    chunkSizeWarningLimit: 1000
  },
  server: {
    port: 3000,
    host: true
  },
  preview: {
    port: 3000,
    host: true
  },
  define: {
    __BUILD_TIME__: JSON.stringify(new Date().toISOString()),
    __VERSION__: JSON.stringify(process.env.npm_package_version || '1.0.0')
  },
  optimizeDeps: {
    include: [
      'react', 
      'react-dom', 
      '@tanstack/react-router', 
      '@tanstack/react-query',
      'recharts',
      'react-markdown',
      'date-fns'
    ]
  }
}))
```

### 4. SEO and Meta Tags Configuration
**File: `web/src/components/SEO.tsx`** (New file)
```typescript
import { Helmet } from 'react-helmet-async';

interface SEOProps {
  title?: string;
  description?: string;
  keywords?: string;
  image?: string;
  url?: string;
  type?: string;
}

export const SEO: React.FC<SEOProps> = ({
  title = 'AI Price Action Dashboard',
  description = 'Comprehensive Vietnamese stock market analysis with VPA signals, technical reports, and actionable trading insights.',
  keywords = 'Vietnamese stocks, VPA analysis, stock trading, technical analysis, VNINDEX, stock charts',
  image = '/og-image.png',
  url = 'https://aipriceaction.vercel.app',
  type = 'website'
}) => {
  const fullTitle = title === 'AI Price Action Dashboard' ? title : `${title} | AI Price Action Dashboard`;

  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      <meta name="author" content="AI Price Action" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      
      {/* Open Graph Meta Tags */}
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={image} />
      <meta property="og:url" content={url} />
      <meta property="og:type" content={type} />
      <meta property="og:site_name" content="AI Price Action Dashboard" />
      
      {/* Twitter Card Meta Tags */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={image} />
      
      {/* Additional Meta Tags */}
      <meta name="robots" content="index, follow" />
      <meta name="language" content="English" />
      <meta name="revisit-after" content="1 days" />
      
      {/* Canonical URL */}
      <link rel="canonical" href={url} />
      
      {/* Favicon */}
      <link rel="icon" type="image/x-icon" href="/favicon.ico" />
      <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
      <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />
      <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
      
      {/* Preconnect to external domains */}
      <link rel="preconnect" href="https://raw.githubusercontent.com" />
      <link rel="dns-prefetch" href="https://raw.githubusercontent.com" />
    </Helmet>
  );
};
```

### 5. Error Monitoring and Analytics
**File: `web/src/lib/analytics.ts`** (New file)
```typescript
// Simple analytics implementation
interface AnalyticsEvent {
  name: string;
  properties?: Record<string, any>;
}

class Analytics {
  private enabled: boolean;
  private events: AnalyticsEvent[] = [];

  constructor() {
    this.enabled = import.meta.env.VITE_ENABLE_ANALYTICS === 'true';
  }

  track(event: AnalyticsEvent) {
    if (!this.enabled) return;
    
    this.events.push({
      ...event,
      timestamp: new Date().toISOString(),
    });

    // In a real implementation, you would send this to your analytics service
    console.log('Analytics Event:', event);
  }

  trackPageView(path: string) {
    this.track({
      name: 'page_view',
      properties: { path }
    });
  }

  trackTickerView(ticker: string, timeframe: string) {
    this.track({
      name: 'ticker_view',
      properties: { ticker, timeframe }
    });
  }

  trackSearch(query: string, resultsCount: number) {
    this.track({
      name: 'search',
      properties: { query, results_count: resultsCount }
    });
  }

  trackChartInteraction(ticker: string, action: string) {
    this.track({
      name: 'chart_interaction',
      properties: { ticker, action }
    });
  }

  getEvents() {
    return this.events;
  }

  clearEvents() {
    this.events = [];
  }
}

export const analytics = new Analytics();
```

### 6. Performance Monitoring Hook
**File: `web/src/hooks/usePerformanceMonitor.ts`** (New file)
```typescript
import { useEffect } from 'react';

interface PerformanceMetrics {
  pageLoadTime: number;
  domContentLoaded: number;
  firstPaint: number;
  firstContentfulPaint: number;
  largestContentfulPaint: number;
}

export const usePerformanceMonitor = () => {
  useEffect(() => {
    const measurePerformance = () => {
      if (typeof window === 'undefined') return;

      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      const paint = performance.getEntriesByType('paint');
      
      const metrics: Partial<PerformanceMetrics> = {
        pageLoadTime: navigation.loadEventEnd - navigation.loadEventStart,
        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
      };

      paint.forEach((entry) => {
        if (entry.name === 'first-paint') {
          metrics.firstPaint = entry.startTime;
        }
        if (entry.name === 'first-contentful-paint') {
          metrics.firstContentfulPaint = entry.startTime;
        }
      });

      // Measure LCP
      const observer = new PerformanceObserver((list) => {
        const entries = list.getEntries();
        const lastEntry = entries[entries.length - 1];
        metrics.largestContentfulPaint = lastEntry.startTime;
      });

      observer.observe({ entryTypes: ['largest-contentful-paint'] });

      // Log metrics in development
      if (import.meta.env.DEV) {
        console.log('Performance Metrics:', metrics);
      }

      // In production, send to analytics
      if (import.meta.env.PROD) {
        // Send metrics to your analytics service
      }
    };

    // Wait for page to load completely
    if (document.readyState === 'complete') {
      measurePerformance();
    } else {
      window.addEventListener('load', measurePerformance);
      return () => window.removeEventListener('load', measurePerformance);
    }
  }, []);
};
```

### 7. Testing Infrastructure
**File: `web/src/test/test-utils.tsx`** (New file)
```typescript
import React from 'react';
import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { RouterProvider, createRouter, createMemoryHistory } from '@tanstack/react-router';
import { routeTree } from '../router';

// Create a test router
const createTestRouter = (initialEntries: string[] = ['/']) => {
  const history = createMemoryHistory({
    initialEntries,
  });

  return createRouter({
    routeTree,
    history,
  });
};

// Create a test query client
const createTestQueryClient = () => {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        cacheTime: 0,
        staleTime: 0,
      },
    },
  });
};

interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  initialEntries?: string[];
  queryClient?: QueryClient;
}

const customRender = (
  ui: React.ReactElement,
  {
    initialEntries = ['/'],
    queryClient = createTestQueryClient(),
    ...renderOptions
  }: CustomRenderOptions = {}
) => {
  const router = createTestRouter(initialEntries);

  const Wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router}>
        {children}
      </RouterProvider>
    </QueryClientProvider>
  );

  return {
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
    router,
    queryClient,
  };
};

export * from '@testing-library/react';
export { customRender as render };
```

### 8. Component Tests
**File: `web/src/components/__tests__/TickerSearch.test.tsx`** (New file)
```typescript
import { describe, it, expect, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { render } from '../../test/test-utils';
import { TickerSearch } from '../TickerSearch';

// Mock the data hooks
vi.mock('../../hooks/useMarketData', () => ({
  useAllTickers: () => ({
    data: ['VCB', 'HPG', 'FPT', 'VHM'],
    isLoading: false,
    error: null,
  }),
}));

describe('TickerSearch', () => {
  it('renders search input', () => {
    render(<TickerSearch />);
    expect(screen.getByPlaceholderText(/search tickers/i)).toBeInTheDocument();
  });

  it('filters tickers based on search query', async () => {
    const user = userEvent.setup();
    render(<TickerSearch />);
    
    const searchInput = screen.getByPlaceholderText(/search tickers/i);
    await user.type(searchInput, 'VC');

    await waitFor(() => {
      expect(screen.getByText('VCB')).toBeInTheDocument();
      expect(screen.queryByText('HPG')).not.toBeInTheDocument();
    });
  });

  it('displays popular tickers when no search query', () => {
    render(<TickerSearch />);
    
    expect(screen.getByText('Popular Tickers')).toBeInTheDocument();
    expect(screen.getByText('VCB')).toBeInTheDocument();
    expect(screen.getByText('HPG')).toBeInTheDocument();
  });

  it('calls onTickerSelect when ticker is clicked', async () => {
    const mockOnSelect = vi.fn();
    const user = userEvent.setup();
    
    render(<TickerSearch onTickerSelect={mockOnSelect} />);
    
    const tickerCard = screen.getByText('VCB').closest('a');
    if (tickerCard) {
      await user.click(tickerCard);
      expect(mockOnSelect).toHaveBeenCalledWith('VCB');
    }
  });
});
```

### 9. Integration Test
**File: `web/src/__tests__/App.test.tsx`** (New file)
```typescript
import { describe, it, expect, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { render } from '../test/test-utils';
import App from '../App';

// Mock the data services
vi.mock('../services/csvService', () => ({
  CSVService: {
    getAllTickers: () => Promise.resolve(['VCB', 'HPG', 'FPT']),
    getTickerData: () => Promise.resolve({
      ticker: 'VCB',
      data: [
        { date: '2025-01-01', open: 100, high: 105, low: 95, close: 102, volume: 1000000 }
      ],
      lastUpdated: '2025-01-01T00:00:00Z'
    }),
  },
}));

vi.mock('../services/markdownService', () => ({
  MarkdownService: {
    getPlanContent: () => Promise.resolve('# Trading Plan\nThis is a test plan.'),
    getVPAAnalysis: () => Promise.resolve([{
      ticker: 'VCB',
      analysis: 'Strong buy signal',
      signals: ['Volume spike'],
      recommendation: 'BUY'
    }]),
  },
}));

describe('App Integration', () => {
  it('renders the main layout', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('AI Price Action')).toBeInTheDocument();
    });
  });

  it('navigates between pages', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText('AI Price Action Dashboard')).toBeInTheDocument();
    });
  });

  it('loads data and displays content', async () => {
    render(<App />);
    
    await waitFor(() => {
      expect(screen.getByText(/Vietnamese stock market analysis/i)).toBeInTheDocument();
    });
  });
});
```

### 10. Package.json Test Scripts
**File: `web/package.json`** (Update test scripts)
```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "type-check": "tsc --noEmit",
    "build:analyze": "npm run build && npx vite-bundle-analyzer dist/stats.html"
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
    "@types/papaparse": "^5.3.14",
    "vitest": "^1.0.0",
    "@testing-library/react": "^14.0.0",
    "@testing-library/jest-dom": "^6.0.0",
    "@testing-library/user-event": "^14.0.0",
    "jsdom": "^23.0.0",
    "@vitest/ui": "^1.0.0",
    "@vitest/coverage-c8": "^0.33.0",
    "react-helmet-async": "^2.0.4"
  }
}
```

### 11. Test Configuration
**File: `web/vitest.config.ts`** (New file)
```typescript
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        '**/dist/**',
      ],
    },
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### 12. GitHub Actions CI/CD
**File: `.github/workflows/ci.yml`** (New file)
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'
          cache-dependency-path: web/package-lock.json

      - name: Install dependencies
        run: cd web && npm ci

      - name: Run type checking
        run: cd web && npm run type-check

      - name: Run linting
        run: cd web && npm run lint

      - name: Run tests
        run: cd web && npm run test:coverage

      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: web/coverage/coverage-final.json
          fail_ci_if_error: true

      - name: Build application
        run: cd web && npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build-files
          path: web/dist

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: web
```

### 13. Security Headers and CSP
**File: `web/public/_headers`** (New file)
```
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://raw.githubusercontent.com; frame-ancestors 'none';
```

### 14. Production Optimizations
**File: `web/src/lib/optimization.ts`** (New file)
```typescript
// Lazy loading utilities
export const lazyLoad = <T extends React.ComponentType<any>>(
  importFunc: () => Promise<{ default: T }>
) => {
  return React.lazy(importFunc);
};

// Image optimization
export const optimizeImage = (src: string, width?: number, height?: number) => {
  // In a real implementation, you might use a service like Cloudinary
  return src;
};

// Bundle splitting utilities
export const loadChunk = async (chunkName: string) => {
  try {
    const module = await import(/* webpackChunkName: "[request]" */ `../chunks/${chunkName}`);
    return module.default;
  } catch (error) {
    console.error(`Failed to load chunk: ${chunkName}`, error);
    throw error;
  }
};

// Performance utilities
export const measurePerformance = (name: string, fn: () => void) => {
  const start = performance.now();
  fn();
  const end = performance.now();
  console.log(`${name} took ${end - start} milliseconds`);
};

// Memory management
export const createMemoizedSelector = <T, R>(
  selector: (state: T) => R,
  equalityFn?: (a: R, b: R) => boolean
) => {
  let lastResult: R;
  let lastArgs: T;

  return (state: T): R => {
    if (state !== lastArgs) {
      const result = selector(state);
      if (!equalityFn || !equalityFn(result, lastResult)) {
        lastResult = result;
      }
      lastArgs = state;
    }
    return lastResult;
  };
};
```

## Implementation Steps

1. **Update Vercel configuration:**
   ```bash
   # Update vercel.json in project root
   ```

2. **Add production dependencies:**
   ```bash
   cd web
   npm install react-helmet-async
   npm install -D vitest @testing-library/react @testing-library/jest-dom @testing-library/user-event jsdom @vitest/ui @vitest/coverage-c8
   ```

3. **Set up testing:**
   ```bash
   # Add test files and configuration
   npm run test
   ```

4. **Configure CI/CD:**
   ```bash
   # Add GitHub Actions workflow
   ```

5. **Deploy to Vercel:**
   ```bash
   vercel --prod
   ```

## Expected Outcome
- Production-ready application deployed on Vercel
- Comprehensive testing suite with good coverage
- Performance monitoring and optimization
- SEO optimization with proper meta tags
- Security headers and CSP configured
- CI/CD pipeline with automated testing and deployment
- Error monitoring and analytics

## Testing Strategy
- Unit tests for individual components
- Integration tests for data flow
- Performance tests for loading times
- End-to-end tests for user workflows
- Security testing for vulnerabilities
- Accessibility testing for WCAG compliance

## Troubleshooting

### Common Issues:
1. **Build failures**: Check dependencies and build configuration
2. **Test failures**: Verify test setup and mocks
3. **Deployment issues**: Check Vercel configuration and environment variables
4. **Performance issues**: Use bundle analyzer to identify large chunks

### Fallback Options:
- Use alternative deployment platforms (Netlify, AWS S3)
- Implement simpler testing if vitest has issues
- Use basic analytics if advanced monitoring fails

## Security Considerations
- CSP headers to prevent XSS attacks
- Secure headers for HTTPS enforcement
- Input validation and sanitization
- Rate limiting for API calls
- Environment variable security

## Performance Targets
- First Contentful Paint: < 2s
- Largest Contentful Paint: < 3s
- Time to Interactive: < 4s
- Bundle size: < 500KB gzipped
- Lighthouse score: > 90

## Final Verification Checklist
- [ ] All routes load successfully
- [ ] Data fetching works correctly
- [ ] Charts render properly
- [ ] Search functionality works
- [ ] Mobile responsive design
- [ ] Error states display correctly
- [ ] Loading states work
- [ ] SEO meta tags present
- [ ] Security headers configured
- [ ] Performance metrics acceptable
- [ ] Tests pass
- [ ] CI/CD pipeline works
- [ ] Production deployment successful

## Post-Deployment Tasks
1. Monitor application performance
2. Set up error tracking
3. Configure analytics dashboard
4. Monitor API usage and caching
5. Regular security updates
6. Performance optimization based on real usage data

This completes the comprehensive development plan for your React web frontend!