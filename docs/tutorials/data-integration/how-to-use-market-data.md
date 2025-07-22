# Hướng dẫn Sử dụng Market Data cho VPA Analysis

## Tổng quan Dataset

Project này cung cấp **bộ dữ liệu toàn diện** cho phân tích thị trường chứng khoán Việt Nam:

### 📁 Tổng Quan Cấu Trúc Dữ Liệu
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

**Giải thích các cột:**
- `ticker`: Stock symbol (VCB, TCB, VNINDEX, etc.)
- `time`: Date in YYYY-MM-DD format
- `open`: Opening price
- `high`: Highest price of the session
- `low`: Lowest price of the session  
- `close`: Closing price
- `volume`: Trading volume (shares traded)

### VPA Analysis Format (.md files)

**Ví dụ cấu trúc từ `vpa_data/VCB.md`:**
```markdown
# VCB

- **Ngày 2025-06-13:** VCB tăng, đóng cửa ở 56.2. Cây nến có bóng dưới...
  - **Phân tích VPA/Wyckoff:** Đây là một tín hiệu **Stopping Volume**...

- **Ngày 2025-06-16:** VCB tăng nhẹ lên 56.6...  
  - **Phân tích VPA/Wyckoff:** Sau phiên Stopping Volume...
```

## Python Code Examples

### 1. Tải Dữ Liệu Cơ Bản

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def load_stock_data(ticker, timeframe='daily'):
    """Tải dữ liệu cổ phiếu từ file CSV"""
    folder = 'market_data' if timeframe == 'daily' else 'market_data_week'
    end_date = '2025-07-21' if timeframe == 'daily' else '2025-07-18'
    
    file_path = f'{folder}/{ticker}_2025-01-02_to_{end_date}.csv'
    df = pd.read_csv(file_path)
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)
    return df

# Tải dữ liệu VCB theo ngày
vcb_daily = load_stock_data('VCB', 'daily')
print(vcb_daily.head())

# Tải dữ liệu VNINDEX theo tuần
vnindex_weekly = load_stock_data('VNINDEX', 'weekly')
print(vnindex_weekly.head())
```

### 2. Tính Toán Chỉ Báo VPA

```python
def calculate_vpa_indicators(df):
    """Tính toán các chỉ báo VPA cần thiết"""
    df = df.copy()
    
    # Chỉ báo giá
    df['price_change'] = df['close'].pct_change() * 100
    df['price_range'] = df['high'] - df['low']
    df['price_spread'] = (df['high'] - df['low']) / df['close'] * 100
    
    # Chỉ báo khối lượng  
    df['volume_ma'] = df['volume'].rolling(window=20).mean()
    df['volume_ratio'] = df['volume'] / df['volume_ma']
    df['volume_spike'] = df['volume_ratio'] > 1.5
    
    # Tín hiệu VPA
    df['ultra_high_volume'] = df['volume_ratio'] > 2.0
    df['low_volume'] = df['volume_ratio'] < 0.7
    
    # Vị trí đóng cửa tương đối với biên độ
    df['close_position'] = (df['close'] - df['low']) / (df['high'] - df['low'])
    
    return df

# Áp dụng chỉ báo VPA
vcb_vpa = calculate_vpa_indicators(vcb_daily)
print("Các chỉ báo VPA đã được tính:")
print(vcb_vpa[['close', 'volume', 'volume_ratio', 'close_position']].tail())
```

### 3. Phát Hiện Tín Hiệu VPA

```python
def detect_vpa_signals(df):
    """Phát hiện tự động các tín hiệu VPA chính"""
    signals = []
    
    for i in range(1, len(df)):
        date = df.index[i]
        row = df.iloc[i]
        prev_row = df.iloc[i-1]
        
        # Phát hiện Stopping Volume
        if (row['volume_ratio'] > 2.0 and 
            row['close_position'] > 0.7 and 
            row['price_change'] > 0):
            signals.append({
                'date': date,
                'signal': 'Stopping Volume',
                'strength': 'Strong',
                'description': f"Tăng đột biến khối lượng {row['volume_ratio']:.1f}x với đóng cửa bullish"
            })
            
        # Phát hiện No Supply  
        elif (row['volume_ratio'] < 0.8 and 
              abs(row['price_change']) < 0.5 and
              row['close'] > prev_row['close']):
            signals.append({
                'date': date, 
                'signal': 'No Supply',
                'strength': 'Medium',
                'description': f"Kiểm tra khối lượng thấp ({row['volume_ratio']:.1f}x) không có bán"
            })
            
        # Bất thường Effort vs Result
        elif (row['volume_ratio'] > 1.8 and 
              abs(row['price_change']) < 0.3):
            signals.append({
                'date': date,
                'signal': 'Effort vs Result Anomaly', 
                'strength': 'Warning',
                'description': f"Khối lượng cao ({row['volume_ratio']:.1f}x) với biến động giá tối thiểu"
            })
    
    return pd.DataFrame(signals)

# Phát hiện tín hiệu trong dữ liệu VCB
vcb_signals = detect_vpa_signals(vcb_vpa)
print("Đã phát hiện các tín hiệu VPA:")
print(vcb_signals)
```

### 4. Phân Tích Đa Cổ Phiếu

```python
def analyze_multiple_stocks(tickers, date_range=None):
    """Phân tích nhiều cổ phiếu tìm mẫu hình VPA"""
    results = {}
    
    for ticker in tickers:
        try:
            # Tải dữ liệu
            df = load_stock_data(ticker, 'daily')
            if date_range:
                df = df.loc[date_range[0]:date_range[1]]
            
            # Tính các chỉ báo
            df_vpa = calculate_vpa_indicators(df)
            
            # Phát hiện tín hiệu  
            signals = detect_vpa_signals(df_vpa)
            
            results[ticker] = {
                'data': df_vpa,
                'signals': signals,
                'total_signals': len(signals),
                'strong_signals': len(signals[signals['strength'] == 'Strong'])
            }
            
        except Exception as e:
            print(f"Lỗi khi xử lý {ticker}: {e}")
            continue
    
    return results

# Phân tích ngành ngân hàng
banking_stocks = ['VCB', 'TCB', 'STB', 'MBB', 'BID']
banking_analysis = analyze_multiple_stocks(banking_stocks)

# In tóm tắt
for ticker, data in banking_analysis.items():
    print(f"{ticker}: {data['total_signals']} tín hiệu, {data['strong_signals']} mạnh")
```

## Chất Lượng Dữ Liệu và Xác Thực

### 1. Kiểm Tra Tính Nhất Quán Dữ Liệu

```python
def validate_data_quality(df, ticker):
    """Xác thực chất lượng và tính nhất quán dữ liệu"""
    issues = []
    
    # Kiểm tra dữ liệu thiếu
    if df.isnull().sum().sum() > 0:
        issues.append("Tìm thấy các điểm dữ liệu thiếu")
        
    # Kiểm tra mối quan hệ giá không thể  
    invalid_prices = df[(df['high'] < df['low']) | 
                       (df['close'] > df['high']) | 
                       (df['close'] < df['low'])]
    if len(invalid_prices) > 0:
        issues.append(f"Mối quan hệ giá không hợp lệ: {len(invalid_prices)} ngày")
        
    # Kiểm tra khối lượng zero/âm
    invalid_volumes = df[df['volume'] <= 0]
    if len(invalid_volumes) > 0:
        issues.append(f"Khối lượng không hợp lệ: {len(invalid_volumes)} ngày")
    
    # Kiểm tra các ngoại lệ cực đoan (gap giá > 15%)
    price_changes = df['close'].pct_change().abs()
    extreme_moves = price_changes[price_changes > 0.15]
    if len(extreme_moves) > 0:
        issues.append(f"Biến động giá cực đoan (>15%): {len(extreme_moves)} ngày")
    
    if issues:
        print(f"Các vấn đề chất lượng dữ liệu cho {ticker}:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print(f"{ticker}: Chất lượng dữ liệu OK ✅")
    
    return issues

# Xác thực tất cả cổ phiếu chính
major_stocks = ['VNINDEX', 'VCB', 'TCB', 'HPG', 'VIC', 'VHM']
for ticker in major_stocks:
    try:
        data = load_stock_data(ticker)
        validate_data_quality(data, ticker)
    except Exception as e:
        print(f"Lỗi xác thực {ticker}: {e}")
```

### 2. Tham Chiếu Chéo với Phân Tích VPA

```python
def cross_reference_vpa_analysis(ticker, date, csv_data, vpa_file_path):
    """Tham chiếu chéo dữ liệu CSV với phân tích VPA chuyên gia"""
    
    # Lấy dữ liệu CSV cho ngày
    try:
        csv_row = csv_data.loc[date]
        csv_analysis = {
            'price_change': csv_row['price_change'],
            'volume_ratio': csv_row['volume_ratio'],
            'close_position': csv_row['close_position']
        }
    except:
        return None
        
    # Đọc file phân tích VPA (đã được đơn giản hóa - trong thực tế sẽ parse file markdown)
    # Đây là ví dụ được được đơn giản hóa - triển khai thực tế sẽ parse file .md
    print(f"Dữ Liệu CSV cho {ticker} vào {date}:")
    print(f"  Biến động giá: {csv_analysis['price_change']:.2f}%")
    print(f"  Tỷ lệ khối lượng: {csv_analysis['volume_ratio']:.1f}x")
    print(f"  Vị trí đóng cửa: {csv_analysis['close_position']:.2f}")
    print(f"\nTham khảo {vpa_file_path} cho phân tích chuyên gia")
    
    return csv_analysis

# Ví dụ sử dụng
vcb_data = calculate_vpa_indicators(load_stock_data('VCB'))
cross_reference_vpa_analysis('VCB', '2025-06-13', vcb_data, 'vpa_data/VCB.md')
```

## Mẫu Trực Quan Hóa

### 1. Biểu Đồ VPA với Khối Lượng

```python
def plot_vpa_chart(df, ticker, start_date=None, end_date=None):
    """Tạo biểu đồ VPA với giá và khối lượng"""
    
    if start_date:
        df = df.loc[start_date:end_date]
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), height_ratios=[3, 1])
    
    # Biểu đồ giá
    ax1.plot(df.index, df['close'], linewidth=2, label='Close Price')
    ax1.fill_between(df.index, df['low'], df['high'], alpha=0.3, label='Day Range')
    
    # Tăng đột biến khối lượng
    volume_spikes = df[df['volume_ratio'] > 1.5]
    ax1.scatter(volume_spikes.index, volume_spikes['close'], 
               color='red', s=50, label='Volume Spikes')
    
    ax1.set_title(f'{ticker} - VPA Analysis')
    ax1.set_ylabel('Price')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Biểu đồ khối lượng
    ax2.bar(df.index, df['volume'], alpha=0.7, label='Volume')
    ax2.axhline(y=df['volume'].mean(), color='orange', linestyle='--', label='Avg Volume')
    
    # Đánh dấu những ngày khối lượng cao
    high_vol = df[df['volume_ratio'] > 1.5]
    ax2.bar(high_vol.index, high_vol['volume'], color='red', alpha=0.8)
    
    ax2.set_ylabel('Volume')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

# Vẽ biểu đồ VPA của VCB
vcb_vpa = calculate_vpa_indicators(load_stock_data('VCB'))
plot_vpa_chart(vcb_vpa, 'VCB', '2025-06-01', '2025-07-01')
```

## Thực Hành Tốt Nhất

### 1. Thực Hành Tốt Nhất Khi Tải Dữ Liệu
- Luôn xác thực chất lượng dữ liệu trước khi phân tích
- Sử dụng định dạng ngày nhất quán cho tất cả thao tác
- Xử lý dữ liệu thiếu một cách thích hợp
- Cache dữ liệu đã tải để tối ưu hiệu suất

### 2. Thực Hành Tốt Nhất Phân Tích VPA  
- Kết hợp nhiều khung thời gian (ngày + tuần)
- Tham chiếu chéo tín hiệu tự động với phân tích chuyên gia
- Xem xét bối cảnh thị trường (hành vi VNINDEX)
- Xác thực tín hiệu với hành động giá tiếp theo

### 3. Tối Ưuu Hiệu Suất
- Sử dụng các thao tác vector hóa với pandas
- Giới hạn phạm vi ngày cho các phép tính lớn
- Cache các chỉ báo thường sử dụng
- Xử lý nhiều cổ phiếu song song

### 4. Tích Hợp với Phân Tích Chuyên Gia
- Luôn so sánh tín hiệu tự động với file `vpa_data/*.md`
- Sử dụng phân tích chuyên gia để xác thực các trường hợp đặc biệt
- Học hỏi từ việc giải thích của chuyên gia về các mẫu hình bất thường
- Kết hợp tín hiệu định lượng với các góc nhìn định tính

## Các Bước Tiếp Theo

1. **Khám Phá Hướng Dẫn:** Bắt đầu với [Chương 1.1 Cơ Bản VPA](../chapter-1-1-vpa-basics.md)
2. **Thực Hành Bài Tập:** Thử [Exercise Notebooks](../exercises/)
3. **Nghiên Cứu Tình Huống:** Đọc chi tiết [Case Studies](../case-studies/)
4. **Phân Tích Nâng Cao:** Học [Phân Tích Tuần vs Ngày](weekly-vs-daily-analysis.md)

---

*💡 **Mẹo Chuyên Nghiệp:** Luôn kết hợp nhiều nguồn dữ liệu và khung thời gian để có bức tranh hoàn chỉnh về hành vi thị trường. Dữ liệu CSV cho phân tích định lượng, file VPA cho các góc nhìn định tính.*