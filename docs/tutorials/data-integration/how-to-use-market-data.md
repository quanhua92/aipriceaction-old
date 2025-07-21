# Hướng dẫn Sử dụng Market Data cho VPA Analysis

## Tổng quan Dataset

Project này cung cấp **comprehensive dataset** cho Vietnam stock market analysis:

### 📁 Data Structure Overview
```
├── market_data/           # Daily data (2025-01-02 to 2025-07-21)
│   ├── VNINDEX_*.csv     # VN-Index daily
│   ├── VCB_*.csv         # Vietcombank daily
│   ├── TCB_*.csv         # Techcombank daily
│   └── [100+ other stocks]
├── market_data_week/      # Weekly data (same period, weekly intervals)
│   ├── VNINDEX_*.csv     # VN-Index weekly
│   └── [same stocks as daily]
├── vpa_data/             # Expert VPA analysis (daily basis)
│   ├── VNINDEX.md        # Professional VPA analysis for VN-Index
│   ├── VCB.md            # VPA analysis for VCB
│   └── [100+ analysis files]
└── vpa_data_week/        # Expert VPA analysis (weekly basis)
    └── [same structure as vpa_data]
```

## CSV Data Format

### Daily/Weekly Market Data Schema
```csv
ticker,time,open,high,low,close,volume
VCB,2025-01-02,61.27,61.87,61.2,61.47,1631368
VCB,2025-01-03,61.47,61.81,61.47,61.54,1403040
```

**Columns explanation:**
- `ticker`: Stock symbol (VCB, TCB, VNINDEX, etc.)
- `time`: Date in YYYY-MM-DD format
- `open`: Opening price
- `high`: Highest price of the session
- `low`: Lowest price of the session  
- `close`: Closing price
- `volume`: Trading volume (shares traded)

### VPA Analysis Format (.md files)

**Structure example từ `vpa_data/VCB.md`:**
```markdown
# VCB

- **Ngày 2025-06-13:** VCB tăng, đóng cửa ở 56.2. Cây nến có bóng dưới...
  - **Phân tích VPA/Wyckoff:** Đây là một tín hiệu **Stopping Volume**...

- **Ngày 2025-06-16:** VCB tăng nhẹ lên 56.6...  
  - **Phân tích VPA/Wyckoff:** Sau phiên Stopping Volume...
```

## Python Code Examples

### 1. Basic Data Loading

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def load_stock_data(ticker, timeframe='daily'):
    """Load stock data from CSV files"""
    folder = 'market_data' if timeframe == 'daily' else 'market_data_week'
    end_date = '2025-07-21' if timeframe == 'daily' else '2025-07-18'
    
    file_path = f'{folder}/{ticker}_2025-01-02_to_{end_date}.csv'
    df = pd.read_csv(file_path)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    return df

# Load VCB daily data
vcb_daily = load_stock_data('VCB', 'daily')
print(vcb_daily.head())

# Load VNINDEX weekly data  
vnindex_weekly = load_stock_data('VNINDEX', 'weekly')
print(vnindex_weekly.head())
```

### 2. VPA Indicators Calculation

```python
def calculate_vpa_indicators(df):
    """Calculate essential VPA indicators"""
    df = df.copy()
    
    # Price indicators
    df['price_change'] = df['close'].pct_change() * 100
    df['price_range'] = df['high'] - df['low']
    df['price_spread'] = (df['high'] - df['low']) / df['close'] * 100
    
    # Volume indicators  
    df['volume_ma'] = df['volume'].rolling(window=20).mean()
    df['volume_ratio'] = df['volume'] / df['volume_ma']
    df['volume_spike'] = df['volume_ratio'] > 1.5
    
    # VPA signals
    df['ultra_high_volume'] = df['volume_ratio'] > 2.0
    df['low_volume'] = df['volume_ratio'] < 0.7
    
    # Close position relative to range
    df['close_position'] = (df['close'] - df['low']) / (df['high'] - df['low'])
    
    return df

# Apply VPA indicators
vcb_vpa = calculate_vpa_indicators(vcb_daily)
print("VPA indicators calculated:")
print(vcb_vpa[['close', 'volume', 'volume_ratio', 'close_position']].tail())
```

### 3. VPA Signal Detection

```python
def detect_vpa_signals(df):
    """Detect major VPA signals automatically"""
    signals = []
    
    for i in range(1, len(df)):
        date = df.index[i]
        row = df.iloc[i]
        prev_row = df.iloc[i-1]
        
        # Stopping Volume detection
        if (row['volume_ratio'] > 2.0 and 
            row['close_position'] > 0.7 and 
            row['price_change'] > 0):
            signals.append({
                'date': date,
                'signal': 'Stopping Volume',
                'strength': 'Strong',
                'description': f"Volume spike {row['volume_ratio']:.1f}x with bullish close"
            })
            
        # No Supply detection  
        elif (row['volume_ratio'] < 0.8 and 
              abs(row['price_change']) < 0.5 and
              row['close'] > prev_row['close']):
            signals.append({
                'date': date, 
                'signal': 'No Supply',
                'strength': 'Medium',
                'description': f"Low volume ({row['volume_ratio']:.1f}x) test with no selling"
            })
            
        # Effort vs Result anomaly
        elif (row['volume_ratio'] > 1.8 and 
              abs(row['price_change']) < 0.3):
            signals.append({
                'date': date,
                'signal': 'Effort vs Result Anomaly', 
                'strength': 'Warning',
                'description': f"High volume ({row['volume_ratio']:.1f}x) with minimal price movement"
            })
    
    return pd.DataFrame(signals)

# Detect signals in VCB data
vcb_signals = detect_vpa_signals(vcb_vpa)
print("Detected VPA signals:")
print(vcb_signals)
```

### 4. Multi-Stock Analysis

```python
def analyze_multiple_stocks(tickers, date_range=None):
    """Analyze multiple stocks for VPA patterns"""
    results = {}
    
    for ticker in tickers:
        try:
            # Load data
            df = load_stock_data(ticker, 'daily')
            if date_range:
                df = df.loc[date_range[0]:date_range[1]]
            
            # Calculate indicators
            df_vpa = calculate_vpa_indicators(df)
            
            # Detect signals  
            signals = detect_vpa_signals(df_vpa)
            
            results[ticker] = {
                'data': df_vpa,
                'signals': signals,
                'total_signals': len(signals),
                'strong_signals': len(signals[signals['strength'] == 'Strong'])
            }
            
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            continue
    
    return results

# Analyze banking sector
banking_stocks = ['VCB', 'TCB', 'STB', 'MBB', 'BID']
banking_analysis = analyze_multiple_stocks(banking_stocks)

# Print summary
for ticker, data in banking_analysis.items():
    print(f"{ticker}: {data['total_signals']} signals, {data['strong_signals']} strong")
```

## Data Quality và Validation

### 1. Data Consistency Check

```python
def validate_data_quality(df, ticker):
    """Validate data quality and consistency"""
    issues = []
    
    # Check for missing data
    if df.isnull().sum().sum() > 0:
        issues.append("Missing data points found")
        
    # Check for impossible price relationships  
    invalid_prices = df[(df['high'] < df['low']) | 
                       (df['close'] > df['high']) | 
                       (df['close'] < df['low'])]
    if len(invalid_prices) > 0:
        issues.append(f"Invalid price relationships: {len(invalid_prices)} days")
        
    # Check for zero/negative volumes
    invalid_volumes = df[df['volume'] <= 0]
    if len(invalid_volumes) > 0:
        issues.append(f"Invalid volumes: {len(invalid_volumes)} days")
    
    # Check for extreme outliers (price gaps > 15%)
    price_changes = df['close'].pct_change().abs()
    extreme_moves = price_changes[price_changes > 0.15]
    if len(extreme_moves) > 0:
        issues.append(f"Extreme price moves (>15%): {len(extreme_moves)} days")
    
    if issues:
        print(f"Data quality issues for {ticker}:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"{ticker}: Data quality OK ✅")
    
    return issues

# Validate all major stocks
major_stocks = ['VNINDEX', 'VCB', 'TCB', 'HPG', 'VIC', 'VHM']
for ticker in major_stocks:
    try:
        data = load_stock_data(ticker)
        validate_data_quality(data, ticker)
    except Exception as e:
        print(f"Error validating {ticker}: {e}")
```

### 2. Cross-reference với VPA Analysis

```python
def cross_reference_vpa_analysis(ticker, date, csv_data, vpa_file_path):
    """Cross-reference CSV data với expert VPA analysis"""
    
    # Get CSV data for the date
    try:
        csv_row = csv_data.loc[date]
        csv_analysis = {
            'price_change': csv_row['price_change'],
            'volume_ratio': csv_row['volume_ratio'],
            'close_position': csv_row['close_position']
        }
    except:
        return None
        
    # Read VPA analysis file (simplified - in practice would parse markdown)
    # This is a simplified example - actual implementation would parse .md files
    print(f"CSV Data for {ticker} on {date}:")
    print(f"  Price change: {csv_analysis['price_change']:.2f}%")
    print(f"  Volume ratio: {csv_analysis['volume_ratio']:.1f}x")
    print(f"  Close position: {csv_analysis['close_position']:.2f}")
    print(f"\nRefer to {vpa_file_path} for expert analysis")
    
    return csv_analysis

# Example usage
vcb_data = calculate_vpa_indicators(load_stock_data('VCB'))
cross_reference_vpa_analysis('VCB', '2025-06-13', vcb_data, 'vpa_data/VCB.md')
```

## Visualization Templates

### 1. VPA Chart with Volume

```python
def plot_vpa_chart(df, ticker, start_date=None, end_date=None):
    """Create VPA chart với price và volume"""
    
    if start_date:
        df = df.loc[start_date:end_date]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), height_ratios=[3, 1])
    
    # Price chart
    ax1.plot(df.index, df['close'], linewidth=2, label='Close Price')
    ax1.fill_between(df.index, df['low'], df['high'], alpha=0.3, label='Day Range')
    
    # Volume spikes
    volume_spikes = df[df['volume_ratio'] > 1.5]
    ax1.scatter(volume_spikes.index, volume_spikes['close'], 
               color='red', s=50, label='Volume Spikes')
    
    ax1.set_title(f'{ticker} - VPA Analysis')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Volume chart
    ax2.bar(df.index, df['volume'], alpha=0.7, label='Volume')
    ax2.axhline(y=df['volume'].mean(), color='orange', linestyle='--', label='Avg Volume')
    
    # Highlight high volume days
    high_vol = df[df['volume_ratio'] > 1.5]
    ax2.bar(high_vol.index, high_vol['volume'], color='red', alpha=0.8)
    
    ax2.set_ylabel('Volume')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Plot VCB VPA chart
vcb_vpa = calculate_vpa_indicators(load_stock_data('VCB'))
plot_vpa_chart(vcb_vpa, 'VCB', '2025-06-01', '2025-07-01')
```

## Best Practices

### 1. Data Loading Best Practices
- Always validate data quality before analysis
- Use consistent date formats across all operations
- Handle missing data appropriately
- Cache loaded data for performance

### 2. VPA Analysis Best Practices  
- Combine multiple timeframes (daily + weekly)
- Cross-reference automated signals với expert analysis
- Consider market context (VNINDEX behavior)
- Validate signals với subsequent price action

### 3. Performance Optimization
- Use vectorized operations with pandas
- Limit date ranges for large calculations
- Cache frequently used indicators
- Process multiple stocks in parallel

### 4. Integration với Expert Analysis
- Always compare automated signals với `vpa_data/*.md` files
- Use expert analysis to validate edge cases
- Learn from expert interpretation của unusual patterns
- Combine quantitative signals với qualitative insights

## Next Steps

1. **Explore Tutorials:** Start với [Chapter 1.1 VPA Basics](../chapter-1-1-vpa-basics.md)
2. **Practice Exercises:** Try [Exercise Notebooks](../exercises/)
3. **Case Studies:** Read detailed [Case Studies](../case-studies/)
4. **Advanced Analysis:** Learn [Weekly vs Daily Analysis](weekly-vs-daily-analysis.md)

---

*💡 **Pro Tip:** Luôn combine multiple data sources và timeframes để có complete picture của market behavior. CSV data cho quantitative analysis, VPA files cho qualitative insights.*