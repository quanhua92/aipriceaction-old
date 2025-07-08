# Stage 4: Page Components and Views

## Overview
This stage focuses on creating all the individual page components that will display the various types of analysis data. Each page will be responsible for fetching and displaying specific content from the markdown files and CSV data.

## Goals
- Create HomePage with dashboard overview
- Build PlanPage as the main entry point
- Implement VPAPage for daily/weekly VPA analysis
- Create ReportPage for ticker reports
- Build TickerPage for individual ticker analysis
- Implement all other content pages (Leader, Group, Impact, Funds)
- Create HoldPage with restricted access
- Add data tables and interactive features

## Files to Create/Modify

### 1. Home Page - Dashboard Overview
**File: `web/src/pages/HomePage.tsx`** (New file)
```typescript
import React from 'react';
import { Link } from '@tanstack/react-router';
import { 
  Target, 
  TrendingUp, 
  FileText, 
  Users, 
  Building, 
  Impact, 
  Wallet,
  BarChart3,
  Clock,
  Star
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { TickerSearch } from '../components/TickerSearch';
import { useAppStore } from '../stores/appStore';
import { useAllTickers } from '../hooks/useMarketData';

export const HomePage: React.FC = () => {
  const { timeframe, favorites } = useAppStore();
  const { data: allTickers } = useAllTickers();

  const quickActions = [
    {
      title: 'Trading Plan',
      description: 'View the actionable trading plan and analysis',
      icon: Target,
      href: '/plan',
      color: 'bg-blue-500',
      textColor: 'text-blue-600'
    },
    {
      title: 'VPA Analysis',
      description: 'Detailed Volume Price Analysis signals',
      icon: TrendingUp,
      href: '/vpa',
      color: 'bg-green-500',
      textColor: 'text-green-600'
    },
    {
      title: 'Reports',
      description: 'Comprehensive ticker reports and summaries',
      icon: FileText,
      href: '/report',
      color: 'bg-orange-500',
      textColor: 'text-orange-600'
    },
    {
      title: 'Market Leaders',
      description: 'Weekly analysis of group leader tickers',
      icon: Users,
      href: '/leader',
      color: 'bg-purple-500',
      textColor: 'text-purple-600'
    }
  ];

  const additionalSections = [
    { title: 'Industry Groups', href: '/group', icon: Building },
    { title: 'Market Impact', href: '/impact', icon: Impact },
    { title: 'Funds Analysis', href: '/funds', icon: Wallet }
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="text-center py-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI Price Action Dashboard
        </h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Comprehensive Vietnamese stock market analysis with VPA signals, 
          technical reports, and actionable trading insights.
        </p>
        <div className="mt-6 flex justify-center gap-4">
          <Button asChild size="lg">
            <Link to="/plan" className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              View Trading Plan
            </Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link to="/vpa" className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              VPA Analysis
            </Link>
          </Button>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Total Tickers</p>
                <p className="text-2xl font-bold">{allTickers?.length || 0}</p>
              </div>
              <BarChart3 className="h-8 w-8 text-blue-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Favorites</p>
                <p className="text-2xl font-bold">{favorites.length}</p>
              </div>
              <Star className="h-8 w-8 text-yellow-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Timeframe</p>
                <p className="text-2xl font-bold capitalize">{timeframe}</p>
              </div>
              <Clock className="h-8 w-8 text-green-500" />
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">Last Updated</p>
                <p className="text-sm font-bold">Today</p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-500" />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-2xl font-bold mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {quickActions.map(({ title, description, icon: Icon, href, color, textColor }) => (
            <Card key={href} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <Link to={href} className="block">
                  <div className={`w-12 h-12 ${color} rounded-lg flex items-center justify-center mb-4`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                  <h3 className={`font-semibold mb-2 ${textColor}`}>{title}</h3>
                  <p className="text-sm text-gray-600">{description}</p>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Additional Sections */}
      <div>
        <h2 className="text-2xl font-bold mb-6">Additional Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {additionalSections.map(({ title, href, icon: Icon }) => (
            <Card key={href} className="hover:shadow-lg transition-shadow">
              <CardContent className="p-6">
                <Link to={href} className="flex items-center gap-3">
                  <Icon className="h-6 w-6 text-gray-600" />
                  <span className="font-medium">{title}</span>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Ticker Search */}
      <div>
        <h2 className="text-2xl font-bold mb-6">Search Tickers</h2>
        <TickerSearch />
      </div>
    </div>
  );
};
```

### 2. Plan Page - Main Entry Point
**File: `web/src/pages/PlanPage.tsx`** (New file)
```typescript
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Target, RefreshCw, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Loading } from '../components/Loading';
import { usePlanContent } from '../hooks/useMarketData';

export const PlanPage: React.FC = () => {
  const { data: planContent, isLoading, error, refetch } = usePlanContent();

  if (isLoading) {
    return <Loading message="Loading trading plan..." />;
  }

  if (error) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardContent className="p-8 text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error Loading Plan</h2>
          <p className="text-gray-600 mb-4">{error.message}</p>
          <Button onClick={() => refetch()} className="flex items-center gap-2">
            <RefreshCw className="h-4 w-4" />
            Try Again
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Target className="h-8 w-8 text-blue-600" />
          <h1 className="text-3xl font-bold">Trading Plan</h1>
        </div>
        <p className="text-gray-600">
          Actionable trading plan and market analysis for Vietnamese stocks
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Market Analysis & Trading Strategy</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="prose prose-lg max-w-none">
            <ReactMarkdown 
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ children }) => <h1 className="text-2xl font-bold mt-8 mb-4 text-gray-900">{children}</h1>,
                h2: ({ children }) => <h2 className="text-xl font-semibold mt-6 mb-3 text-gray-800">{children}</h2>,
                h3: ({ children }) => <h3 className="text-lg font-medium mt-4 mb-2 text-gray-700">{children}</h3>,
                p: ({ children }) => <p className="mb-4 text-gray-600 leading-relaxed">{children}</p>,
                ul: ({ children }) => <ul className="list-disc list-inside mb-4 space-y-1 text-gray-600">{children}</ul>,
                ol: ({ children }) => <ol className="list-decimal list-inside mb-4 space-y-1 text-gray-600">{children}</ol>,
                li: ({ children }) => <li className="ml-4">{children}</li>,
                strong: ({ children }) => <strong className="font-semibold text-gray-900">{children}</strong>,
                em: ({ children }) => <em className="italic text-gray-700">{children}</em>,
                blockquote: ({ children }) => (
                  <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-700 my-4">
                    {children}
                  </blockquote>
                ),
                table: ({ children }) => (
                  <div className="overflow-x-auto my-4">
                    <table className="min-w-full divide-y divide-gray-200">{children}</table>
                  </div>
                ),
                thead: ({ children }) => <thead className="bg-gray-50">{children}</thead>,
                th: ({ children }) => (
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {children}
                  </th>
                ),
                td: ({ children }) => <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{children}</td>,
              }}
            >
              {planContent}
            </ReactMarkdown>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
```

### 3. VPA Analysis Page
**File: `web/src/pages/VPAPage.tsx`** (New file)
```typescript
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { TrendingUp, Search, Filter, RefreshCw, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Loading } from '../components/Loading';
import { useVPAAnalysis } from '../hooks/useMarketData';
import { useAppStore } from '../stores/appStore';

export const VPAPage: React.FC = () => {
  const { timeframe } = useAppStore();
  const { data: vpaAnalysis, isLoading, error, refetch } = useVPAAnalysis(timeframe);
  const [searchQuery, setSearchQuery] = React.useState('');
  const [filterSignal, setFilterSignal] = React.useState<'ALL' | 'BUY' | 'SELL' | 'HOLD'>('ALL');

  const filteredAnalysis = React.useMemo(() => {
    if (!vpaAnalysis) return [];
    
    return vpaAnalysis.filter(analysis => {
      const matchesSearch = analysis.ticker.toLowerCase().includes(searchQuery.toLowerCase()) ||
                          analysis.analysis.toLowerCase().includes(searchQuery.toLowerCase());
      
      const matchesFilter = filterSignal === 'ALL' || analysis.recommendation === filterSignal;
      
      return matchesSearch && matchesFilter;
    });
  }, [vpaAnalysis, searchQuery, filterSignal]);

  if (isLoading) {
    return <Loading message="Loading VPA analysis..." />;
  }

  if (error) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardContent className="p-8 text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error Loading VPA Analysis</h2>
          <p className="text-gray-600 mb-4">{error.message}</p>
          <Button onClick={() => refetch()} className="flex items-center gap-2">
            <RefreshCw className="h-4 w-4" />
            Try Again
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <TrendingUp className="h-8 w-8 text-green-600" />
          <h1 className="text-3xl font-bold">VPA Analysis</h1>
          <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
            {timeframe.toUpperCase()}
          </span>
        </div>
        <p className="text-gray-600">
          Volume Price Analysis signals and recommendations for Vietnamese stocks
        </p>
      </div>

      {/* Filters */}
      <Card className="mb-6">
        <CardContent className="p-6">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
                <Input
                  placeholder="Search tickers or analysis..."
                  className="pl-10"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>
            <div className="flex gap-2">
              <Button
                variant={filterSignal === 'ALL' ? 'default' : 'outline'}
                onClick={() => setFilterSignal('ALL')}
                size="sm"
              >
                All
              </Button>
              <Button
                variant={filterSignal === 'BUY' ? 'default' : 'outline'}
                onClick={() => setFilterSignal('BUY')}
                size="sm"
                className="text-green-600 border-green-600 hover:bg-green-50"
              >
                Buy
              </Button>
              <Button
                variant={filterSignal === 'SELL' ? 'default' : 'outline'}
                onClick={() => setFilterSignal('SELL')}
                size="sm"
                className="text-red-600 border-red-600 hover:bg-red-50"
              >
                Sell
              </Button>
              <Button
                variant={filterSignal === 'HOLD' ? 'default' : 'outline'}
                onClick={() => setFilterSignal('HOLD')}
                size="sm"
                className="text-yellow-600 border-yellow-600 hover:bg-yellow-50"
              >
                Hold
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Analysis Results */}
      <div className="space-y-6">
        {filteredAnalysis.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">No Analysis Found</h3>
              <p className="text-gray-600">
                {searchQuery ? `No analysis found matching "${searchQuery}"` : 'No VPA analysis available'}
              </p>
            </CardContent>
          </Card>
        ) : (
          filteredAnalysis.map((analysis) => (
            <VPAAnalysisCard key={analysis.ticker} analysis={analysis} />
          ))
        )}
      </div>
    </div>
  );
};

interface VPAAnalysisCardProps {
  analysis: {
    ticker: string;
    analysis: string;
    signals: string[];
    recommendation?: 'BUY' | 'SELL' | 'HOLD';
  };
}

const VPAAnalysisCard: React.FC<VPAAnalysisCardProps> = ({ analysis }) => {
  const getRecommendationColor = (rec?: string) => {
    switch (rec) {
      case 'BUY': return 'bg-green-100 text-green-800 border-green-200';
      case 'SELL': return 'bg-red-100 text-red-800 border-red-200';
      case 'HOLD': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl">{analysis.ticker}</CardTitle>
          {analysis.recommendation && (
            <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getRecommendationColor(analysis.recommendation)}`}>
              {analysis.recommendation}
            </span>
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="prose max-w-none">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>
            {analysis.analysis}
          </ReactMarkdown>
        </div>
        
        {analysis.signals.length > 0 && (
          <div className="mt-4 pt-4 border-t">
            <h4 className="font-semibold mb-2">Key Signals:</h4>
            <ul className="space-y-1">
              {analysis.signals.map((signal, index) => (
                <li key={index} className="text-sm text-gray-600 flex items-start gap-2">
                  <span className="text-blue-500">•</span>
                  {signal}
                </li>
              ))}
            </ul>
          </div>
        )}
      </CardContent>
    </Card>
  );
};
```

### 4. Individual Ticker Page
**File: `web/src/pages/TickerPage.tsx`** (New file)
```typescript
import React from 'react';
import { useParams, Link } from '@tanstack/react-router';
import { 
  ArrowLeft, 
  Star, 
  TrendingUp, 
  TrendingDown, 
  Calendar,
  BarChart3,
  RefreshCw,
  AlertCircle
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { CandlestickChart } from '../components/charts/CandlestickChart';
import { Loading } from '../components/Loading';
import { useTickerData, useVPAAnalysis, useReportData, useMarketCapData } from '../hooks/useMarketData';
import { useAppStore } from '../stores/appStore';
import { format } from 'date-fns';

export const TickerPage: React.FC = () => {
  const { ticker } = useParams({ from: '/ticker/$ticker' });
  const { timeframe, favorites, toggleFavorite, chartConfig } = useAppStore();
  
  const { data: tickerData, isLoading: isLoadingData, error: dataError, refetch: refetchData } = useTickerData(ticker, timeframe);
  const { data: vpaAnalysis } = useVPAAnalysis(timeframe);
  const { data: reportData } = useReportData(timeframe);
  const { data: marketCapData } = useMarketCapData();

  const isFavorite = favorites.includes(ticker);
  
  const tickerVPA = vpaAnalysis?.find(vpa => vpa.ticker === ticker);
  const tickerReport = reportData?.find(report => report.ticker === ticker);
  const tickerMarketCap = marketCapData?.find(cap => cap.ticker === ticker);

  // Calculate basic statistics
  const stats = React.useMemo(() => {
    if (!tickerData?.data.length) return null;
    
    const data = tickerData.data;
    const latest = data[data.length - 1];
    const previous = data[data.length - 2];
    
    const change = previous ? latest.close - previous.close : 0;
    const changePercent = previous ? ((latest.close - previous.close) / previous.close) * 100 : 0;
    
    const high52w = Math.max(...data.map(d => d.high));
    const low52w = Math.min(...data.map(d => d.low));
    const avgVolume = data.reduce((sum, d) => sum + d.volume, 0) / data.length;
    
    return {
      latest: latest.close,
      change,
      changePercent,
      high52w,
      low52w,
      avgVolume,
      lastUpdate: latest.date
    };
  }, [tickerData]);

  if (isLoadingData) {
    return <Loading message={`Loading ${ticker} data...`} />;
  }

  if (dataError) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardContent className="p-8 text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error Loading {ticker}</h2>
          <p className="text-gray-600 mb-4">{dataError.message}</p>
          <div className="flex gap-2 justify-center">
            <Button onClick={() => refetchData()} className="flex items-center gap-2">
              <RefreshCw className="h-4 w-4" />
              Try Again
            </Button>
            <Button asChild variant="outline">
              <Link to="/" className="flex items-center gap-2">
                <ArrowLeft className="h-4 w-4" />
                Back to Home
              </Link>
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <Button asChild variant="outline" size="sm">
              <Link to="/" className="flex items-center gap-2">
                <ArrowLeft className="h-4 w-4" />
                Back
              </Link>
            </Button>
            <h1 className="text-3xl font-bold">{ticker}</h1>
            <Button
              variant="outline"
              size="sm"
              onClick={() => toggleFavorite(ticker)}
              className="flex items-center gap-2"
            >
              <Star className={`h-4 w-4 ${isFavorite ? 'fill-yellow-400 text-yellow-400' : ''}`} />
              {isFavorite ? 'Remove' : 'Add'} Favorite
            </Button>
          </div>
          <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
            {timeframe.toUpperCase()}
          </span>
        </div>

        {/* Price Stats */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
            <Card>
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">Current Price</p>
                <p className="text-xl font-bold">{stats.latest.toFixed(2)}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">Change</p>
                <p className={`text-xl font-bold flex items-center gap-1 ${stats.change >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {stats.change >= 0 ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
                  {stats.change.toFixed(2)} ({stats.changePercent.toFixed(2)}%)
                </p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">52W High</p>
                <p className="text-xl font-bold">{stats.high52w.toFixed(2)}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">52W Low</p>
                <p className="text-xl font-bold">{stats.low52w.toFixed(2)}</p>
              </CardContent>
            </Card>
            <Card>
              <CardContent className="p-4">
                <p className="text-sm text-gray-600">Avg Volume</p>
                <p className="text-xl font-bold">{(stats.avgVolume / 1000).toFixed(0)}K</p>
              </CardContent>
            </Card>
            {tickerMarketCap && (
              <Card>
                <CardContent className="p-4">
                  <p className="text-sm text-gray-600">Market Cap</p>
                  <p className="text-lg font-bold">{(tickerMarketCap.marketCap / 1e9).toFixed(1)}B</p>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>

      {/* Main Content */}
      <Tabs defaultValue="chart" className="space-y-6">
        <TabsList>
          <TabsTrigger value="chart" className="flex items-center gap-2">
            <BarChart3 className="h-4 w-4" />
            Chart
          </TabsTrigger>
          <TabsTrigger value="vpa" className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            VPA Analysis
          </TabsTrigger>
          <TabsTrigger value="report" className="flex items-center gap-2">
            <Calendar className="h-4 w-4" />
            Report
          </TabsTrigger>
          <TabsTrigger value="data">Raw Data</TabsTrigger>
        </TabsList>

        <TabsContent value="chart">
          <Card>
            <CardHeader>
              <CardTitle>Price Chart</CardTitle>
            </CardHeader>
            <CardContent>
              {tickerData?.data && (
                <CandlestickChart
                  data={tickerData.data}
                  height={500}
                  showVolume={chartConfig.showVolume}
                  showMovingAverages={chartConfig.showMovingAverages}
                />
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="vpa">
          <Card>
            <CardHeader>
              <CardTitle>VPA Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              {tickerVPA ? (
                <div>
                  {tickerVPA.recommendation && (
                    <div className="mb-4">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                        tickerVPA.recommendation === 'BUY' ? 'bg-green-100 text-green-800' :
                        tickerVPA.recommendation === 'SELL' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {tickerVPA.recommendation}
                      </span>
                    </div>
                  )}
                  <div className="prose max-w-none">
                    <pre className="whitespace-pre-wrap text-sm">{tickerVPA.analysis}</pre>
                  </div>
                  {tickerVPA.signals.length > 0 && (
                    <div className="mt-4 pt-4 border-t">
                      <h4 className="font-semibold mb-2">Key Signals:</h4>
                      <ul className="space-y-1">
                        {tickerVPA.signals.map((signal, index) => (
                          <li key={index} className="text-sm text-gray-600">• {signal}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-600">No VPA analysis available for {ticker}</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="report">
          <Card>
            <CardHeader>
              <CardTitle>Technical Report</CardTitle>
            </CardHeader>
            <CardContent>
              {tickerReport ? (
                <div className="prose max-w-none">
                  <pre className="whitespace-pre-wrap text-sm">{tickerReport.technicalAnalysis}</pre>
                </div>
              ) : (
                <p className="text-gray-600">No report available for {ticker}</p>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="data">
          <Card>
            <CardHeader>
              <CardTitle>Raw Data</CardTitle>
            </CardHeader>
            <CardContent>
              {tickerData?.data && (
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Open</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">High</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Low</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Close</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Volume</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {tickerData.data.slice(-50).reverse().map((row) => (
                        <tr key={row.date}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {format(new Date(row.date), 'MMM dd, yyyy')}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {row.open.toFixed(2)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {row.high.toFixed(2)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {row.low.toFixed(2)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {row.close.toFixed(2)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {row.volume.toLocaleString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};
```

### 5. Reports Page
**File: `web/src/pages/ReportPage.tsx`** (New file)
```typescript
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { FileText, Search, RefreshCw, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Loading } from '../components/Loading';
import { Button } from '../components/ui/button';
import { useReportData } from '../hooks/useMarketData';
import { useAppStore } from '../stores/appStore';

export const ReportPage: React.FC = () => {
  const { timeframe } = useAppStore();
  const { data: reportData, isLoading, error, refetch } = useReportData(timeframe);
  const [searchQuery, setSearchQuery] = React.useState('');

  const filteredReports = React.useMemo(() => {
    if (!reportData) return [];
    
    return reportData.filter(report => 
      report.ticker.toLowerCase().includes(searchQuery.toLowerCase()) ||
      report.technicalAnalysis.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [reportData, searchQuery]);

  if (isLoading) {
    return <Loading message="Loading reports..." />;
  }

  if (error) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardContent className="p-8 text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error Loading Reports</h2>
          <p className="text-gray-600 mb-4">{error.message}</p>
          <Button onClick={() => refetch()} className="flex items-center gap-2">
            <RefreshCw className="h-4 w-4" />
            Try Again
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <FileText className="h-8 w-8 text-orange-600" />
          <h1 className="text-3xl font-bold">Technical Reports</h1>
          <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
            {timeframe.toUpperCase()}
          </span>
        </div>
        <p className="text-gray-600">
          Comprehensive technical analysis reports for each ticker
        </p>
      </div>

      {/* Search */}
      <Card className="mb-6">
        <CardContent className="p-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
            <Input
              placeholder="Search reports..."
              className="pl-10"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </CardContent>
      </Card>

      {/* Reports */}
      <div className="space-y-6">
        {filteredReports.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">No Reports Found</h3>
              <p className="text-gray-600">
                {searchQuery ? `No reports found matching "${searchQuery}"` : 'No reports available'}
              </p>
            </CardContent>
          </Card>
        ) : (
          filteredReports.map((report) => (
            <Card key={report.ticker}>
              <CardHeader>
                <CardTitle className="text-xl">{report.ticker}</CardTitle>
                {report.summary && (
                  <p className="text-gray-600">{report.summary}</p>
                )}
              </CardHeader>
              <CardContent>
                <div className="prose max-w-none">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {report.technicalAnalysis}
                  </ReactMarkdown>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};
```

### 6. Create remaining page components
**File: `web/src/pages/LeaderPage.tsx`** (New file)
```typescript
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Users, RefreshCw, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Loading } from '../components/Loading';
import { useLeaderContent } from '../hooks/useMarketData';

export const LeaderPage: React.FC = () => {
  const { data: leaderContent, isLoading, error, refetch } = useLeaderContent();

  if (isLoading) {
    return <Loading message="Loading market leaders..." />;
  }

  if (error) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardContent className="p-8 text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error Loading Leaders</h2>
          <p className="text-gray-600 mb-4">{error.message}</p>
          <Button onClick={() => refetch()} className="flex items-center gap-2">
            <RefreshCw className="h-4 w-4" />
            Try Again
          </Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Users className="h-8 w-8 text-purple-600" />
          <h1 className="text-3xl font-bold">Market Leaders</h1>
        </div>
        <p className="text-gray-600">
          Analysis of group leader tickers using weekly data
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Weekly Leadership Analysis</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="prose prose-lg max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {leaderContent}
            </ReactMarkdown>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
```

### 7. Group, Impact, and Funds Pages (Similar structure)
**File: `web/src/pages/GroupPage.tsx`** (New file)
```typescript
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Building, RefreshCw, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Loading } from '../components/Loading';
import { useGroupContent } from '../hooks/useMarketData';

export const GroupPage: React.FC = () => {
  const { data: groupContent, isLoading, error, refetch } = useGroupContent();

  if (isLoading) return <Loading message="Loading industry groups..." />;
  if (error) {
    return (
      <Card className="max-w-2xl mx-auto">
        <CardContent className="p-8 text-center">
          <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold mb-2">Error Loading Groups</h2>
          <p className="text-gray-600 mb-4">{error.message}</p>
          <Button onClick={() => refetch()}>Try Again</Button>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Building className="h-8 w-8 text-blue-600" />
          <h1 className="text-3xl font-bold">Industry Groups</h1>
        </div>
        <p className="text-gray-600">Industry groupings and sector analysis</p>
      </div>
      <Card>
        <CardContent className="p-6">
          <div className="prose prose-lg max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{groupContent}</ReactMarkdown>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
```

### 8. Hold Page (Secret Access)
**File: `web/src/pages/HoldPage.tsx`** (New file)
```typescript
import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Lock, Eye, EyeOff } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Loading } from '../components/Loading';
import { useHoldContent } from '../hooks/useMarketData';

export const HoldPage: React.FC = () => {
  const { data: holdContent, isLoading, error } = useHoldContent();
  const [isVisible, setIsVisible] = React.useState(false);

  if (isLoading) return <Loading message="Loading portfolio analysis..." />;
  if (error) return <div>Error loading content</div>;

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Lock className="h-8 w-8 text-red-600" />
          <h1 className="text-3xl font-bold">Portfolio Analysis</h1>
          <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">PRIVATE</span>
        </div>
        <p className="text-gray-600">Personal portfolio holdings and analysis</p>
      </div>

      <Card className="mb-6 bg-yellow-50 border-yellow-200">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <p className="text-sm text-yellow-800">
              🔒 This is private content accessible only via direct link
            </p>
            <Button
              variant="outline"
              size="sm"
              onClick={() => setIsVisible(!isVisible)}
              className="flex items-center gap-2"
            >
              {isVisible ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              {isVisible ? 'Hide' : 'Show'} Content
            </Button>
          </div>
        </CardContent>
      </Card>

      {isVisible && (
        <Card>
          <CardHeader>
            <CardTitle>Holdings Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {holdContent}
              </ReactMarkdown>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
```

## Implementation Steps

1. **Create page components:**
   ```bash
   mkdir -p web/src/pages
   # Add all page components
   ```

2. **Add missing dependencies:**
   ```bash
   cd web
   npm install zustand
   ```

3. **Update imports in router:**
   ```bash
   # Update router.tsx to import all page components
   ```

4. **Test each page:**
   ```bash
   npm run dev
   # Navigate to each route and test functionality
   ```

## Expected Outcome
- Fully functional pages for all content types
- Interactive ticker pages with charts and data
- Search and filtering capabilities
- Responsive design across all pages
- Error handling and loading states
- Secret access page for hold.md

## Testing Strategy
- Test all routes load correctly
- Verify data fetching works for each page
- Test search and filter functionality
- Verify chart rendering on ticker pages
- Test responsive design on mobile
- Verify error states display properly

## Troubleshooting

### Common Issues:
1. **Import errors**: Check all import paths
2. **Data not loading**: Verify API endpoints and data structure
3. **Chart not rendering**: Check Recharts configuration
4. **Route errors**: Verify router configuration

### Fallback Options:
- Use placeholder data if API fails
- Implement simpler charts if Recharts fails
- Add offline mode for cached data

## Next Steps
After completing this stage, you should have:
- Complete web application with all pages functional
- Interactive charts and data visualization
- Search and filtering capabilities
- Responsive design
- Error handling throughout

The final stage will focus on deployment configuration and testing.