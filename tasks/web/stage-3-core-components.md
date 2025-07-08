# Stage 3: Core Components and Routing

## Overview
This stage focuses on building the core UI components, routing system, and main layout structure. We'll create the navigation, layout components, and set up the main pages for the application.

## Goals
- Set up TanStack Router with all required routes
- Create main layout components with navigation
- Build core UI components using ShadCN UI
- Implement search functionality for tickers
- Create timeframe toggle (daily/weekly)
- Build responsive layout structure
- Create loading and error states

## Files to Create/Modify

### 1. ShadCN UI Components Setup
**File: `web/src/components/ui/button.tsx`** (New file)
```typescript
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "../../lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
```

### 2. Input Component
**File: `web/src/components/ui/input.tsx`** (New file)
```typescript
import * as React from "react"
import { cn } from "../../lib/utils"

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={ref}
        {...props}
      />
    )
  }
)
Input.displayName = "Input"

export { Input }
```

### 3. Card Component
**File: `web/src/components/ui/card.tsx`** (New file)
```typescript
import * as React from "react"
import { cn } from "../../lib/utils"

const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "rounded-lg border bg-card text-card-foreground shadow-sm",
      className
    )}
    {...props}
  />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props}
  />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn(
      "text-2xl font-semibold leading-none tracking-tight",
      className
    )}
    {...props}
  />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props}
  />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props}
  />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }
```

### 4. Tabs Component
**File: `web/src/components/ui/tabs.tsx`** (New file)
```typescript
import * as React from "react"
import * as TabsPrimitive from "@radix-ui/react-tabs"
import { cn } from "../../lib/utils"

const Tabs = TabsPrimitive.Root

const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex h-10 items-center justify-center rounded-md bg-muted p-1 text-muted-foreground",
      className
    )}
    {...props}
  />
))
TabsList.displayName = TabsPrimitive.List.displayName

const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-sm px-3 py-1.5 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow-sm",
      className
    )}
    {...props}
  />
))
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName

const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
      className
    )}
    {...props}
  />
))
TabsContent.displayName = TabsPrimitive.Content.displayName

export { Tabs, TabsList, TabsTrigger, TabsContent }
```

### 5. Updated Router Configuration
**File: `web/src/router.tsx`** (Replace existing content)
```typescript
import { 
  createRouter, 
  createRoute, 
  createRootRoute,
  Link,
  Outlet
} from '@tanstack/react-router'
import { TanStackRouterDevtools } from '@tanstack/router-devtools'
import { Layout } from './components/Layout'
import { HomePage } from './pages/HomePage'
import { TickerPage } from './pages/TickerPage'
import { PlanPage } from './pages/PlanPage'
import { VPAPage } from './pages/VPAPage'
import { ReportPage } from './pages/ReportPage'
import { LeaderPage } from './pages/LeaderPage'
import { GroupPage } from './pages/GroupPage'
import { ImpactPage } from './pages/ImpactPage'
import { FundsPage } from './pages/FundsPage'
import { HoldPage } from './pages/HoldPage'
import { NotFound } from './pages/NotFound'

// Create a root route
const rootRoute = createRootRoute({
  component: () => (
    <Layout>
      <Outlet />
      <TanStackRouterDevtools />
    </Layout>
  ),
})

// Create routes
const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: HomePage,
})

const planRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/plan',
  component: PlanPage,
})

const vpaRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/vpa',
  component: VPAPage,
})

const reportRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/report',
  component: ReportPage,
})

const leaderRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/leader',
  component: LeaderPage,
})

const groupRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/group',
  component: GroupPage,
})

const impactRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/impact',
  component: ImpactPage,
})

const fundsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/funds',
  component: FundsPage,
})

const tickerRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/ticker/$ticker',
  component: TickerPage,
})

// Secret route for hold.md - non-trivial URL
const holdRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/private/portfolio/analysis/hold',
  component: HoldPage,
})

// Create the route tree
const routeTree = rootRoute.addChildren([
  indexRoute,
  planRoute,
  vpaRoute,
  reportRoute,
  leaderRoute,
  groupRoute,
  impactRoute,
  fundsRoute,
  tickerRoute,
  holdRoute,
])

// Create the router instance
export const router = createRouter({ 
  routeTree,
  defaultNotFoundComponent: NotFound,
})

// Register the router instance for type safety
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}
```

### 6. Main Layout Component
**File: `web/src/components/Layout.tsx`** (New file)
```typescript
import React from 'react';
import { Link, useLocation } from '@tanstack/react-router';
import { 
  Home, 
  Target, 
  TrendingUp, 
  FileText, 
  Users, 
  Building, 
  Impact, 
  Wallet,
  Menu,
  X,
  Search,
  Calendar,
  CalendarDays
} from 'lucide-react';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Card } from './ui/card';
import { Tabs, TabsList, TabsTrigger } from './ui/tabs';
import { useAppStore } from '../stores/appStore';

interface LayoutProps {
  children: React.ReactNode;
}

const navItems = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/plan', label: 'Plan', icon: Target },
  { path: '/vpa', label: 'VPA Analysis', icon: TrendingUp },
  { path: '/report', label: 'Reports', icon: FileText },
  { path: '/leader', label: 'Leaders', icon: Users },
  { path: '/group', label: 'Groups', icon: Building },
  { path: '/impact', label: 'Impact', icon: Impact },
  { path: '/funds', label: 'Funds', icon: Wallet },
];

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);
  const { searchQuery, setSearchQuery, timeframe, setTimeframe } = useAppStore();
  const location = useLocation();

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Mobile menu backdrop */}
      {isMobileMenuOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Header */}
      <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container mx-auto px-4">
          <div className="flex h-16 items-center justify-between">
            {/* Logo and title */}
            <div className="flex items-center space-x-4">
              <Button
                variant="ghost"
                size="icon"
                className="lg:hidden"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              >
                {isMobileMenuOpen ? (
                  <X className="h-5 w-5" />
                ) : (
                  <Menu className="h-5 w-5" />
                )}
              </Button>
              <Link to="/" className="flex items-center space-x-2">
                <TrendingUp className="h-6 w-6 text-primary" />
                <span className="font-bold text-xl">AI Price Action</span>
              </Link>
            </div>

            {/* Search and Controls */}
            <div className="flex items-center space-x-4">
              {/* Search */}
              <div className="relative hidden md:block">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Search tickers..."
                  className="pl-10 w-64"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>

              {/* Timeframe Toggle */}
              <Tabs value={timeframe} onValueChange={(value) => setTimeframe(value as 'daily' | 'weekly')}>
                <TabsList className="grid w-full grid-cols-2">
                  <TabsTrigger value="daily" className="flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    Daily
                  </TabsTrigger>
                  <TabsTrigger value="weekly" className="flex items-center gap-2">
                    <CalendarDays className="h-4 w-4" />
                    Weekly
                  </TabsTrigger>
                </TabsList>
              </Tabs>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar Navigation */}
        <nav className={`
          fixed inset-y-0 left-0 z-50 w-64 bg-background border-r transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
          ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:block
        `}>
          <div className="flex h-full flex-col">
            <div className="flex-1 overflow-y-auto p-4">
              <div className="space-y-2">
                {navItems.map(({ path, label, icon: Icon }) => (
                  <Link
                    key={path}
                    to={path}
                    className={`
                      flex items-center space-x-3 px-3 py-2 rounded-md text-sm font-medium transition-colors
                      ${isActive(path) 
                        ? 'bg-primary text-primary-foreground' 
                        : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground'
                      }
                    `}
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{label}</span>
                  </Link>
                ))}
              </div>
            </div>

            {/* Mobile Search */}
            <div className="p-4 border-t lg:hidden">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <Input
                  placeholder="Search tickers..."
                  className="pl-10"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1 lg:ml-0">
          <div className="container mx-auto px-4 py-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
```

### 7. App State Management
**File: `web/src/stores/appStore.ts`** (New file)
```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AppState {
  // UI State
  searchQuery: string
  timeframe: 'daily' | 'weekly'
  selectedTicker?: string
  favorites: string[]
  
  // Chart Settings
  chartConfig: {
    showVolume: boolean
    showMovingAverages: boolean
    chartType: 'candlestick' | 'line' | 'area'
    timeRange: '1M' | '3M' | '6M' | '1Y' | 'ALL'
  }
  
  // Actions
  setSearchQuery: (query: string) => void
  setTimeframe: (timeframe: 'daily' | 'weekly') => void
  setSelectedTicker: (ticker: string) => void
  toggleFavorite: (ticker: string) => void
  updateChartConfig: (config: Partial<AppState['chartConfig']>) => void
  clearSearch: () => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set) => ({
      // Initial state
      searchQuery: '',
      timeframe: 'daily',
      selectedTicker: undefined,
      favorites: [],
      chartConfig: {
        showVolume: true,
        showMovingAverages: true,
        chartType: 'candlestick',
        timeRange: '3M',
      },

      // Actions
      setSearchQuery: (query) => set({ searchQuery: query }),
      setTimeframe: (timeframe) => set({ timeframe }),
      setSelectedTicker: (ticker) => set({ selectedTicker: ticker }),
      
      toggleFavorite: (ticker) => set((state) => ({
        favorites: state.favorites.includes(ticker)
          ? state.favorites.filter(t => t !== ticker)
          : [...state.favorites, ticker]
      })),
      
      updateChartConfig: (config) => set((state) => ({
        chartConfig: { ...state.chartConfig, ...config }
      })),
      
      clearSearch: () => set({ searchQuery: '' }),
    }),
    {
      name: 'aipriceaction-app-state',
      partialize: (state) => ({
        favorites: state.favorites,
        chartConfig: state.chartConfig,
        timeframe: state.timeframe,
      }),
    }
  )
)
```

### 8. Loading Component
**File: `web/src/components/Loading.tsx`** (New file)
```typescript
import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingProps {
  message?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const Loading: React.FC<LoadingProps> = ({ 
  message = 'Loading...', 
  size = 'md' 
}) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8'
  };

  return (
    <div className="flex flex-col items-center justify-center p-8">
      <Loader2 className={`animate-spin text-primary ${sizeClasses[size]}`} />
      <p className="mt-2 text-sm text-muted-foreground">{message}</p>
    </div>
  );
};
```

### 9. Ticker Search Component
**File: `web/src/components/TickerSearch.tsx`** (New file)
```typescript
import React from 'react';
import { Link } from '@tanstack/react-router';
import { Search, Star, TrendingUp, TrendingDown } from 'lucide-react';
import { Input } from './ui/input';
import { Card, CardContent } from './ui/card';
import { Button } from './ui/button';
import { useAllTickers } from '../hooks/useMarketData';
import { useAppStore } from '../stores/appStore';
import { Loading } from './Loading';

interface TickerSearchProps {
  onTickerSelect?: (ticker: string) => void;
  showFavorites?: boolean;
  maxResults?: number;
}

export const TickerSearch: React.FC<TickerSearchProps> = ({
  onTickerSelect,
  showFavorites = true,
  maxResults = 10
}) => {
  const { data: allTickers, isLoading, error } = useAllTickers();
  const { searchQuery, setSearchQuery, favorites, toggleFavorite } = useAppStore();
  const [localQuery, setLocalQuery] = React.useState(searchQuery);
  
  // Debounce search
  React.useEffect(() => {
    const timer = setTimeout(() => {
      setSearchQuery(localQuery);
    }, 300);
    
    return () => clearTimeout(timer);
  }, [localQuery, setSearchQuery]);

  const filteredTickers = React.useMemo(() => {
    if (!allTickers) return [];
    
    const query = searchQuery.toLowerCase();
    return allTickers
      .filter(ticker => ticker.toLowerCase().includes(query))
      .slice(0, maxResults);
  }, [allTickers, searchQuery, maxResults]);

  const favoriteTickers = React.useMemo(() => {
    if (!allTickers || !showFavorites) return [];
    return allTickers.filter(ticker => favorites.includes(ticker));
  }, [allTickers, favorites, showFavorites]);

  if (isLoading) {
    return <Loading message="Loading tickers..." />;
  }

  if (error) {
    return (
      <Card className="p-4">
        <p className="text-red-600">Error loading tickers: {error.message}</p>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          placeholder="Search tickers (e.g., VCB, HPG, FPT...)"
          className="pl-10"
          value={localQuery}
          onChange={(e) => setLocalQuery(e.target.value)}
        />
      </div>

      {/* Favorites Section */}
      {showFavorites && favoriteTickers.length > 0 && (
        <Card>
          <CardContent className="p-4">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <Star className="h-4 w-4 text-yellow-500" />
              Favorites
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
              {favoriteTickers.map(ticker => (
                <TickerCard
                  key={ticker}
                  ticker={ticker}
                  isFavorite={true}
                  onToggleFavorite={toggleFavorite}
                  onSelect={onTickerSelect}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Search Results */}
      {searchQuery && (
        <Card>
          <CardContent className="p-4">
            <h3 className="font-semibold mb-3">
              Search Results ({filteredTickers.length})
            </h3>
            {filteredTickers.length === 0 ? (
              <p className="text-muted-foreground text-center py-4">
                No tickers found matching "{searchQuery}"
              </p>
            ) : (
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
                {filteredTickers.map(ticker => (
                  <TickerCard
                    key={ticker}
                    ticker={ticker}
                    isFavorite={favorites.includes(ticker)}
                    onToggleFavorite={toggleFavorite}
                    onSelect={onTickerSelect}
                  />
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Popular Tickers */}
      {!searchQuery && allTickers && (
        <Card>
          <CardContent className="p-4">
            <h3 className="font-semibold mb-3">Popular Tickers</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2">
              {['VCB', 'HPG', 'FPT', 'VHM', 'VIC', 'MWG', 'GAS', 'MSN']
                .filter(ticker => allTickers.includes(ticker))
                .map(ticker => (
                  <TickerCard
                    key={ticker}
                    ticker={ticker}
                    isFavorite={favorites.includes(ticker)}
                    onToggleFavorite={toggleFavorite}
                    onSelect={onTickerSelect}
                  />
                ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Info Note */}
      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="p-4">
          <p className="text-sm text-blue-700">
            📈 This is a curated subset of Vietnamese stocks. Total tickers available: {allTickers?.length || 0}
          </p>
        </CardContent>
      </Card>
    </div>
  );
};

interface TickerCardProps {
  ticker: string;
  isFavorite: boolean;
  onToggleFavorite: (ticker: string) => void;
  onSelect?: (ticker: string) => void;
}

const TickerCard: React.FC<TickerCardProps> = ({
  ticker,
  isFavorite,
  onToggleFavorite,
  onSelect
}) => {
  const handleClick = () => {
    if (onSelect) {
      onSelect(ticker);
    }
  };

  return (
    <div className="group relative">
      <Link
        to="/ticker/$ticker"
        params={{ ticker }}
        className="block p-3 border rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors"
        onClick={handleClick}
      >
        <div className="flex items-center justify-between">
          <span className="font-medium">{ticker}</span>
          <div className="flex items-center space-x-1">
            <Button
              variant="ghost"
              size="icon"
              className="h-6 w-6 opacity-0 group-hover:opacity-100 transition-opacity"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                onToggleFavorite(ticker);
              }}
            >
              <Star 
                className={`h-3 w-3 ${isFavorite ? 'fill-yellow-400 text-yellow-400' : 'text-gray-400'}`} 
              />
            </Button>
          </div>
        </div>
      </Link>
    </div>
  );
};
```

### 10. NotFound Page
**File: `web/src/pages/NotFound.tsx`** (New file)
```typescript
import React from 'react';
import { Link } from '@tanstack/react-router';
import { Home, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent } from '../components/ui/card';

export const NotFound: React.FC = () => {
  return (
    <div className="min-h-[60vh] flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardContent className="p-8 text-center">
          <div className="text-6xl font-bold text-muted-foreground mb-4">404</div>
          <h1 className="text-2xl font-semibold mb-2">Page Not Found</h1>
          <p className="text-muted-foreground mb-6">
            The page you're looking for doesn't exist or has been moved.
          </p>
          <div className="flex flex-col sm:flex-row gap-2 justify-center">
            <Button asChild variant="outline">
              <Link to="/" className="flex items-center gap-2">
                <ArrowLeft className="h-4 w-4" />
                Go Back
              </Link>
            </Button>
            <Button asChild>
              <Link to="/" className="flex items-center gap-2">
                <Home className="h-4 w-4" />
                Home
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
```

## Installation Steps

1. **Install additional dependencies:**
   ```bash
   cd web
   npm install zustand @tanstack/react-router@latest
   ```

2. **Create UI components:**
   ```bash
   mkdir -p web/src/components/ui
   # Add button.tsx, input.tsx, card.tsx, tabs.tsx
   ```

3. **Set up routing:**
   ```bash
   # Update router.tsx with new routes
   ```

4. **Create layout and stores:**
   ```bash
   mkdir -p web/src/stores
   # Add appStore.ts, Layout.tsx
   ```

5. **Test the routing:**
   ```bash
   npm run dev
   # Navigate to different routes
   ```

## Expected Outcome
- Complete navigation system with sidebar and header
- Responsive design that works on mobile and desktop
- Search functionality for tickers
- Timeframe toggle (daily/weekly)
- State management for app-wide settings
- All main routes configured and working
- Loading states and error handling

## Testing Strategy
- Test navigation between all routes
- Verify search functionality works
- Test responsive design on different screen sizes
- Verify state persistence across page reloads
- Test error boundaries and loading states

## Troubleshooting

### Common Issues:
1. **Route not found**: Check route paths in router.tsx
2. **Component not rendering**: Verify import paths and component exports
3. **State not persisting**: Check Zustand persist configuration
4. **Styling issues**: Verify Tailwind classes and ShadCN setup

### Fallback Options:
- Use React Router DOM if TanStack Router has issues
- Implement simple state management with React Context if Zustand fails
- Use CSS modules if Tailwind is problematic

## Next Steps
After completing this stage, you should have:
- Fully functional navigation and routing
- Responsive layout with search capabilities
- State management system
- Core UI components ready for use
- Foundation for building individual page components

The next stage will focus on building the individual page components and advanced features.