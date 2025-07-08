# Stage 2: Data Services and Chart Integration

## Overview
This stage focuses on creating data services to fetch and parse the various data sources from the GitHub repository, including CSV files, markdown documents, and implementing interactive charts using Recharts.

## Goals
- Create data service layer for fetching GitHub repository data
- Implement CSV parsing for market data (daily and weekly)
- Create markdown parsing utilities for structured content
- Build interactive chart components using Recharts
- Implement data models and TypeScript interfaces
- Create caching and error handling strategies

## Files to Create/Modify

### 1. TypeScript Interfaces and Types
**File: `web/src/types/index.ts`** (New file)
```typescript
// Market Data Types
export interface MarketDataRow {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
  adj_close?: number;
  ticker?: string;
}

export interface TickerData {
  ticker: string;
  data: MarketDataRow[];
  lastUpdated: string;
}

export interface MarketCapData {
  ticker: string;
  marketCap: number;
  shares: number;
  price: number;
}

// Content Types
export interface MarkdownSection {
  title: string;
  content: string;
  level: number;
  ticker?: string;
}

export interface VPAAnalysis {
  ticker: string;
  analysis: string;
  signals: string[];
  recommendation?: 'BUY' | 'SELL' | 'HOLD';
}

export interface ReportData {
  ticker: string;
  summary: string;
  technicalAnalysis: string;
  fundamentals?: string;
  recommendation?: string;
}

// App State Types
export interface AppState {
  selectedTimeframe: 'daily' | 'weekly';
  selectedTicker?: string;
  searchQuery: string;
  favorites: string[];
}

// Chart Types
export interface ChartConfig {
  showVolume: boolean;
  showMovingAverages: boolean;
  chartType: 'candlestick' | 'line' | 'area';
  timeRange: '1M' | '3M' | '6M' | '1Y' | 'ALL';
}

// API Response Types
export interface GitHubRawResponse {
  content: string;
  encoding: 'utf8' | 'base64';
  sha: string;
  size: number;
}

export interface DataServiceError {
  message: string;
  type: 'NETWORK' | 'PARSE' | 'NOT_FOUND' | 'RATE_LIMIT';
  details?: any;
}
```

### 2. Data Service Base Class
**File: `web/src/services/dataService.ts`** (New file)
```typescript
import { DataServiceError } from '../types';

export class DataService {
  private static readonly BASE_URL = import.meta.env.VITE_GITHUB_REPO_URL;
  private static readonly CACHE_DURATION = 5 * 60 * 1000; // 5 minutes
  private static cache = new Map<string, { data: any; timestamp: number }>();

  static async fetchRawContent(path: string): Promise<string> {
    const cacheKey = path;
    const cached = this.cache.get(cacheKey);
    
    if (cached && Date.now() - cached.timestamp < this.CACHE_DURATION) {
      return cached.data;
    }

    try {
      const url = `${this.BASE_URL}/${path}`;
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new DataServiceError({
          message: `Failed to fetch ${path}: ${response.status} ${response.statusText}`,
          type: response.status === 404 ? 'NOT_FOUND' : 'NETWORK',
          details: { status: response.status, path }
        });
      }

      const content = await response.text();
      this.cache.set(cacheKey, { data: content, timestamp: Date.now() });
      return content;
    } catch (error) {
      if (error instanceof DataServiceError) {
        throw error;
      }
      throw new DataServiceError({
        message: `Network error fetching ${path}: ${error.message}`,
        type: 'NETWORK',
        details: error
      });
    }
  }

  static clearCache(): void {
    this.cache.clear();
  }

  static getCacheStats(): { size: number; keys: string[] } {
    return {
      size: this.cache.size,
      keys: Array.from(this.cache.keys())
    };
  }
}
```

### 3. CSV Data Service
**File: `web/src/services/csvService.ts`** (New file)
```typescript
import Papa from 'papaparse';
import { DataService } from './dataService';
import { MarketDataRow, TickerData, MarketCapData } from '../types';

export class CSVService extends DataService {
  
  static async getTickerData(ticker: string, timeframe: 'daily' | 'weekly'): Promise<TickerData> {
    const folder = timeframe === 'daily' ? 'market_data' : 'market_data_week';
    const filename = timeframe === 'daily' 
      ? `${ticker}_2025-01-02_to_2025-07-07.csv`
      : `${ticker}_2025-01-02_to_2025-07-04.csv`;
    
    const path = `${folder}/${filename}`;
    
    try {
      const csvContent = await this.fetchRawContent(path);
      const parsedData = Papa.parse<MarketDataRow>(csvContent, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        transformHeader: (header) => header.toLowerCase().replace(/\s+/g, '_')
      });

      if (parsedData.errors.length > 0) {
        console.warn(`CSV parsing warnings for ${ticker}:`, parsedData.errors);
      }

      const processedData: MarketDataRow[] = parsedData.data.map(row => ({
        date: row.date,
        open: Number(row.open),
        high: Number(row.high),
        low: Number(row.low),
        close: Number(row.close),
        volume: Number(row.volume),
        adj_close: row.adj_close ? Number(row.adj_close) : undefined,
        ticker: ticker
      })).filter(row => row.date && !isNaN(row.close));

      return {
        ticker,
        data: processedData,
        lastUpdated: new Date().toISOString()
      };
    } catch (error) {
      throw new Error(`Failed to fetch data for ${ticker} (${timeframe}): ${error.message}`);
    }
  }

  static async getAllTickers(): Promise<string[]> {
    try {
      const csvContent = await this.fetchRawContent('TICKERS.csv');
      const parsedData = Papa.parse<{ ticker: string }>(csvContent, {
        header: true,
        skipEmptyLines: true
      });

      return parsedData.data.map(row => row.ticker).filter(ticker => ticker);
    } catch (error) {
      throw new Error(`Failed to fetch tickers list: ${error.message}`);
    }
  }

  static async getMarketCapData(): Promise<MarketCapData[]> {
    try {
      const csvContent = await this.fetchRawContent('stock_market_cap.csv');
      const parsedData = Papa.parse<MarketCapData>(csvContent, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        transformHeader: (header) => header.toLowerCase().replace(/\s+/g, '_')
      });

      return parsedData.data.map(row => ({
        ticker: row.ticker,
        marketCap: Number(row.marketCap) || 0,
        shares: Number(row.shares) || 0,
        price: Number(row.price) || 0
      })).filter(row => row.ticker);
    } catch (error) {
      throw new Error(`Failed to fetch market cap data: ${error.message}`);
    }
  }

  static async getFundsTickers(): Promise<string[]> {
    try {
      const csvContent = await this.fetchRawContent('FUNDS.csv');
      const parsedData = Papa.parse<{ ticker: string }>(csvContent, {
        header: true,
        skipEmptyLines: true
      });

      return parsedData.data.map(row => row.ticker).filter(ticker => ticker);
    } catch (error) {
      throw new Error(`Failed to fetch funds list: ${error.message}`);
    }
  }

  // Utility method to get price change data
  static calculatePriceChanges(data: MarketDataRow[]): MarketDataRow[] {
    return data.map((row, index) => {
      const prevRow = data[index - 1];
      const change = prevRow ? row.close - prevRow.close : 0;
      const changePercent = prevRow ? ((row.close - prevRow.close) / prevRow.close) * 100 : 0;
      
      return {
        ...row,
        change,
        changePercent
      };
    });
  }
}
```

### 4. Markdown Service
**File: `web/src/services/markdownService.ts`** (New file)
```typescript
import { DataService } from './dataService';
import { MarkdownSection, VPAAnalysis, ReportData } from '../types';

export class MarkdownService extends DataService {
  
  static parseMarkdownToSections(content: string): MarkdownSection[] {
    const lines = content.split('\n');
    const sections: MarkdownSection[] = [];
    let currentSection: MarkdownSection | null = null;
    
    for (const line of lines) {
      const headerMatch = line.match(/^(#{1,6})\s+(.+)$/);
      
      if (headerMatch) {
        // Save previous section if exists
        if (currentSection) {
          sections.push(currentSection);
        }
        
        const level = headerMatch[1].length;
        const title = headerMatch[2].trim();
        
        currentSection = {
          title,
          level,
          content: '',
          ticker: this.extractTickerFromTitle(title)
        };
      } else if (currentSection) {
        currentSection.content += line + '\n';
      }
    }
    
    // Add last section
    if (currentSection) {
      sections.push(currentSection);
    }
    
    return sections.map(section => ({
      ...section,
      content: section.content.trim()
    }));
  }

  static extractTickerFromTitle(title: string): string | undefined {
    // Try to extract ticker from title (e.g., "# VCB", "## Analysis for HPG")
    const tickerMatch = title.match(/\b([A-Z]{2,5})\b/);
    return tickerMatch ? tickerMatch[1] : undefined;
  }

  static async getVPAAnalysis(timeframe: 'daily' | 'weekly'): Promise<VPAAnalysis[]> {
    const filename = timeframe === 'daily' ? 'VPA.md' : 'VPA_week.md';
    
    try {
      const content = await this.fetchRawContent(filename);
      const sections = this.parseMarkdownToSections(content);
      
      return sections
        .filter(section => section.ticker && section.level <= 2)
        .map(section => ({
          ticker: section.ticker!,
          analysis: section.content,
          signals: this.extractSignals(section.content),
          recommendation: this.extractRecommendation(section.content)
        }));
    } catch (error) {
      throw new Error(`Failed to fetch VPA analysis (${timeframe}): ${error.message}`);
    }
  }

  static async getReportData(timeframe: 'daily' | 'weekly'): Promise<ReportData[]> {
    const filename = timeframe === 'daily' ? 'REPORT.md' : 'REPORT_week.md';
    
    try {
      const content = await this.fetchRawContent(filename);
      const sections = this.parseMarkdownToSections(content);
      
      return sections
        .filter(section => section.ticker && section.level <= 2)
        .map(section => ({
          ticker: section.ticker!,
          summary: this.extractSummary(section.content),
          technicalAnalysis: section.content,
          recommendation: this.extractRecommendation(section.content)
        }));
    } catch (error) {
      throw new Error(`Failed to fetch report data (${timeframe}): ${error.message}`);
    }
  }

  static async getMarkdownContent(filename: string): Promise<string> {
    try {
      return await this.fetchRawContent(filename);
    } catch (error) {
      throw new Error(`Failed to fetch ${filename}: ${error.message}`);
    }
  }

  static async getPlanContent(): Promise<string> {
    return this.getMarkdownContent('PLAN.md');
  }

  static async getLeaderContent(): Promise<string> {
    return this.getMarkdownContent('LEADER.md');
  }

  static async getGroupContent(): Promise<string> {
    return this.getMarkdownContent('GROUP.md');
  }

  static async getImpactContent(): Promise<string> {
    return this.getMarkdownContent('IMPACT.md');
  }

  static async getFundsContent(): Promise<string> {
    return this.getMarkdownContent('FUNDS.md');
  }

  static async getHoldContent(): Promise<string> {
    return this.getMarkdownContent('hold.md');
  }

  // Helper methods
  private static extractSignals(content: string): string[] {
    const signals: string[] = [];
    const lines = content.split('\n');
    
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed.includes('Signal:') || trimmed.includes('signal:')) {
        signals.push(trimmed);
      }
      if (trimmed.includes('Buy') || trimmed.includes('Sell') || trimmed.includes('Hold')) {
        signals.push(trimmed);
      }
    }
    
    return signals;
  }

  private static extractRecommendation(content: string): 'BUY' | 'SELL' | 'HOLD' | undefined {
    const contentLower = content.toLowerCase();
    
    if (contentLower.includes('buy') || contentLower.includes('mua')) {
      return 'BUY';
    }
    if (contentLower.includes('sell') || contentLower.includes('ban')) {
      return 'SELL';
    }
    if (contentLower.includes('hold') || contentLower.includes('nam giu')) {
      return 'HOLD';
    }
    
    return undefined;
  }

  private static extractSummary(content: string): string {
    const lines = content.split('\n');
    const firstParagraph = lines.find(line => line.trim().length > 50);
    return firstParagraph ? firstParagraph.trim() : content.substring(0, 200) + '...';
  }
}
```

### 5. Chart Components
**File: `web/src/components/charts/CandlestickChart.tsx`** (New file)
```typescript
import React from 'react';
import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { MarketDataRow } from '../../types';
import { format } from 'date-fns';

interface CandlestickChartProps {
  data: MarketDataRow[];
  height?: number;
  showVolume?: boolean;
  showMovingAverages?: boolean;
}

interface CandlestickData extends MarketDataRow {
  ma20?: number;
  ma50?: number;
  bodyColor: string;
  wickColor: string;
  body: [number, number];
  wick: [number, number];
}

export const CandlestickChart: React.FC<CandlestickChartProps> = ({
  data,
  height = 400,
  showVolume = true,
  showMovingAverages = true
}) => {
  // Calculate moving averages
  const calculateMA = (data: MarketDataRow[], period: number): number[] => {
    const ma: number[] = [];
    for (let i = 0; i < data.length; i++) {
      if (i < period - 1) {
        ma.push(NaN);
      } else {
        const sum = data.slice(i - period + 1, i + 1).reduce((acc, item) => acc + item.close, 0);
        ma.push(sum / period);
      }
    }
    return ma;
  };

  const processedData: CandlestickData[] = React.useMemo(() => {
    const ma20 = calculateMA(data, 20);
    const ma50 = calculateMA(data, 50);
    
    return data.map((item, index) => {
      const isGreen = item.close >= item.open;
      return {
        ...item,
        ma20: ma20[index],
        ma50: ma50[index],
        bodyColor: isGreen ? '#10B981' : '#EF4444',
        wickColor: isGreen ? '#065F46' : '#7F1D1D',
        body: [Math.min(item.open, item.close), Math.max(item.open, item.close)],
        wick: [item.low, item.high]
      };
    });
  }, [data]);

  const CustomCandlestick = (props: any) => {
    const { payload, x, y, width, height } = props;
    if (!payload) return null;
    
    const { open, high, low, close, bodyColor, wickColor } = payload;
    
    // Calculate positions
    const priceRange = high - low;
    const chartHeight = height || 200;
    const candleWidth = Math.max(2, (width || 10) * 0.8);
    
    // Scale values to chart coordinates
    const yScale = chartHeight / priceRange;
    const openY = y + (high - open) * yScale;
    const closeY = y + (high - close) * yScale;
    const highY = y;
    const lowY = y + chartHeight;
    
    const bodyTop = Math.min(openY, closeY);
    const bodyHeight = Math.abs(openY - closeY);
    const centerX = x + (width || 10) / 2;
    
    return (
      <g>
        {/* Wick */}
        <line
          x1={centerX}
          y1={highY}
          x2={centerX}
          y2={lowY}
          stroke={wickColor}
          strokeWidth={1}
        />
        
        {/* Body */}
        <rect
          x={centerX - candleWidth / 2}
          y={bodyTop}
          width={candleWidth}
          height={Math.max(1, bodyHeight)}
          fill={bodyColor}
          stroke={wickColor}
          strokeWidth={1}
        />
      </g>
    );
  };

  const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
          <p className="font-semibold text-gray-800">
            {format(new Date(label), 'MMM dd, yyyy')}
          </p>
          <div className="grid grid-cols-2 gap-2 mt-2 text-sm">
            <div>
              <span className="text-gray-600">Open:</span>
              <span className="font-medium ml-1">{data.open?.toFixed(2)}</span>
            </div>
            <div>
              <span className="text-gray-600">High:</span>
              <span className="font-medium ml-1">{data.high?.toFixed(2)}</span>
            </div>
            <div>
              <span className="text-gray-600">Low:</span>
              <span className="font-medium ml-1">{data.low?.toFixed(2)}</span>
            </div>
            <div>
              <span className="text-gray-600">Close:</span>
              <span className="font-medium ml-1">{data.close?.toFixed(2)}</span>
            </div>
          </div>
          {showVolume && (
            <div className="mt-2 text-sm">
              <span className="text-gray-600">Volume:</span>
              <span className="font-medium ml-1">{data.volume?.toLocaleString()}</span>
            </div>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full">
      <ResponsiveContainer width="100%" height={height}>
        <ComposedChart data={processedData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
          <XAxis 
            dataKey="date" 
            tickFormatter={(value) => format(new Date(value), 'MMM dd')}
            stroke="#6B7280"
            fontSize={12}
          />
          <YAxis 
            domain={['dataMin - 1', 'dataMax + 1']}
            stroke="#6B7280"
            fontSize={12}
          />
          <Tooltip content={<CustomTooltip />} />
          
          {/* Candlestick bodies */}
          <Bar dataKey="close" fill="#8884d8" shape={<CustomCandlestick />} />
          
          {/* Moving averages */}
          {showMovingAverages && (
            <>
              <Line 
                type="monotone" 
                dataKey="ma20" 
                stroke="#F59E0B" 
                strokeWidth={2}
                dot={false}
                name="MA20"
              />
              <Line 
                type="monotone" 
                dataKey="ma50" 
                stroke="#8B5CF6" 
                strokeWidth={2}
                dot={false}
                name="MA50"
              />
            </>
          )}
        </ComposedChart>
      </ResponsiveContainer>
      
      {/* Volume chart */}
      {showVolume && (
        <ResponsiveContainer width="100%" height={100}>
          <ComposedChart data={processedData} margin={{ top: 10, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis 
              dataKey="date" 
              tickFormatter={(value) => format(new Date(value), 'MMM dd')}
              stroke="#6B7280"
              fontSize={12}
            />
            <YAxis stroke="#6B7280" fontSize={12} />
            <Tooltip 
              formatter={(value: any) => [value?.toLocaleString(), 'Volume']}
              labelFormatter={(label) => format(new Date(label), 'MMM dd, yyyy')}
            />
            <Bar dataKey="volume">
              {processedData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.bodyColor} />
              ))}
            </Bar>
          </ComposedChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};
```

### 6. Data Hooks
**File: `web/src/hooks/useMarketData.ts`** (New file)
```typescript
import { useQuery } from '@tanstack/react-query';
import { CSVService } from '../services/csvService';
import { MarkdownService } from '../services/markdownService';
import { TickerData, VPAAnalysis, ReportData, MarketCapData } from '../types';

export const useTickerData = (ticker: string, timeframe: 'daily' | 'weekly') => {
  return useQuery<TickerData>({
    queryKey: ['ticker-data', ticker, timeframe],
    queryFn: () => CSVService.getTickerData(ticker, timeframe),
    enabled: !!ticker,
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
    retry: 2,
    retryDelay: 1000,
  });
};

export const useAllTickers = () => {
  return useQuery<string[]>({
    queryKey: ['all-tickers'],
    queryFn: CSVService.getAllTickers,
    staleTime: 30 * 60 * 1000, // 30 minutes - tickers don't change often
    cacheTime: 60 * 60 * 1000, // 1 hour
  });
};

export const useVPAAnalysis = (timeframe: 'daily' | 'weekly') => {
  return useQuery<VPAAnalysis[]>({
    queryKey: ['vpa-analysis', timeframe],
    queryFn: () => MarkdownService.getVPAAnalysis(timeframe),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useReportData = (timeframe: 'daily' | 'weekly') => {
  return useQuery<ReportData[]>({
    queryKey: ['report-data', timeframe],
    queryFn: () => MarkdownService.getReportData(timeframe),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};

export const useMarketCapData = () => {
  return useQuery<MarketCapData[]>({
    queryKey: ['market-cap-data'],
    queryFn: CSVService.getMarketCapData,
    staleTime: 60 * 60 * 1000, // 1 hour - market cap doesn't change frequently
    cacheTime: 2 * 60 * 60 * 1000, // 2 hours
  });
};

export const usePlanContent = () => {
  return useQuery<string>({
    queryKey: ['plan-content'],
    queryFn: MarkdownService.getPlanContent,
    staleTime: 10 * 60 * 1000, // 10 minutes
    cacheTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useLeaderContent = () => {
  return useQuery<string>({
    queryKey: ['leader-content'],
    queryFn: MarkdownService.getLeaderContent,
    staleTime: 10 * 60 * 1000, // 10 minutes
    cacheTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useGroupContent = () => {
  return useQuery<string>({
    queryKey: ['group-content'],
    queryFn: MarkdownService.getGroupContent,
    staleTime: 10 * 60 * 1000, // 10 minutes
    cacheTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useImpactContent = () => {
  return useQuery<string>({
    queryKey: ['impact-content'],
    queryFn: MarkdownService.getImpactContent,
    staleTime: 10 * 60 * 1000, // 10 minutes
    cacheTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useFundsContent = () => {
  return useQuery<string>({
    queryKey: ['funds-content'],
    queryFn: MarkdownService.getFundsContent,
    staleTime: 10 * 60 * 1000, // 10 minutes
    cacheTime: 30 * 60 * 1000, // 30 minutes
  });
};

export const useHoldContent = () => {
  return useQuery<string>({
    queryKey: ['hold-content'],
    queryFn: MarkdownService.getHoldContent,
    staleTime: 10 * 60 * 1000, // 10 minutes
    cacheTime: 30 * 60 * 1000, // 30 minutes
  });
};
```

### 7. Error Boundary Component
**File: `web/src/components/ErrorBoundary.tsx`** (New file)
```typescript
import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
  errorInfo?: any;
}

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ComponentType<{ error: Error; retry: () => void }>;
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({ errorInfo });
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: undefined, errorInfo: undefined });
  };

  render() {
    if (this.state.hasError) {
      const FallbackComponent = this.props.fallback || DefaultErrorFallback;
      return <FallbackComponent error={this.state.error!} retry={this.handleRetry} />;
    }

    return this.props.children;
  }
}

const DefaultErrorFallback: React.FC<{ error: Error; retry: () => void }> = ({ error, retry }) => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[400px] p-8 bg-red-50 border border-red-200 rounded-lg">
      <AlertCircle className="w-12 h-12 text-red-500 mb-4" />
      <h2 className="text-xl font-semibold text-red-800 mb-2">Something went wrong</h2>
      <p className="text-red-600 text-center mb-4 max-w-md">
        {error.message || 'An unexpected error occurred while loading the data.'}
      </p>
      <button
        onClick={retry}
        className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
      >
        <RefreshCw className="w-4 h-4" />
        Try Again
      </button>
    </div>
  );
};
```

## Implementation Steps

1. **Create the types and interfaces:**
   ```bash
   mkdir -p web/src/types
   # Add types/index.ts
   ```

2. **Set up data services:**
   ```bash
   mkdir -p web/src/services
   # Add dataService.ts, csvService.ts, markdownService.ts
   ```

3. **Create chart components:**
   ```bash
   mkdir -p web/src/components/charts
   # Add CandlestickChart.tsx
   ```

4. **Set up hooks:**
   ```bash
   mkdir -p web/src/hooks
   # Add useMarketData.ts
   ```

5. **Add error handling:**
   ```bash
   mkdir -p web/src/components
   # Add ErrorBoundary.tsx
   ```

6. **Test the data services:**
   ```bash
   cd web
   npm run dev
   # Test API calls in browser console
   ```

## Expected Outcome
- Working data service layer that can fetch and parse CSV files
- Markdown parsing utilities for structured content
- Interactive candlestick charts with volume display
- React Query hooks for data fetching with caching
- Error boundary components for graceful error handling
- TypeScript interfaces for type safety

## Testing Strategy
Create test utilities to verify:
- CSV parsing accuracy
- Markdown content extraction
- Chart rendering with sample data
- Error handling for network failures
- Data caching functionality

## Troubleshooting

### Common Issues:
1. **CORS errors**: Ensure GitHub raw URLs are accessible
2. **CSV parsing errors**: Check data format consistency
3. **Chart rendering issues**: Verify Recharts setup and data format
4. **TypeScript errors**: Ensure all interfaces match actual data structure

### Fallback Options:
- Use mock data for development if GitHub API is unavailable
- Implement retry logic with exponential backoff
- Add offline data caching using localStorage
- Provide simplified chart fallback if Recharts fails

## Next Steps
After completing this stage, you should have:
- Fully functional data fetching from GitHub repository
- Interactive charts displaying market data
- Error handling and loading states
- Caching system for optimal performance
- TypeScript interfaces for all data structures

The next stage will focus on building the main UI components and routing system.