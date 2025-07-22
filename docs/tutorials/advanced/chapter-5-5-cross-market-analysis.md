# Chương 5.5: Phân Tích Đa Thị Trường
## Kết Nối VPA Việt Nam Với Thế Giới

### 🎯 Mục Tiêu Chương

Thị trường Việt Nam không tồn tại độc lập. Chương này sẽ dạy bạn cách kết hợp VPA với phân tích thị trường toàn cầu để đưa ra quyết định chính xác hơn.

### 💡 Nguyên Lý Cốt Lõi

**"Hiểu dòng tiền toàn cầu để dự đoán VN thị trường"**

- 🇺🇸 **S&P 500** ảnh hưởng tâm lý chung
- 🇨🇳 **Shanghai/Shenzhen** ảnh hưởng trực tiếp (xuất nhập khẩu)
- 💵 **USD/VND** ảnh hưởng dòng tiền ngoại
- ⚡ **Commodities** ảnh hưởng HPG, PVS, VRE...

---

## 📚 Phần 1: Cơ Bản - Hiểu Mối Liên Hệ Thị Trường

### A. Bản Đồ Tác Động Toàn Cầu

```python
def phan_tich_tac_dong_toan_cau(vn_stock_data, global_market_data):
    """
    Phân tích tác động của các thị trường toàn cầu lên cổ phiếu VN
    
    Global factors:
    - US S&P 500 (tâm lý risk-on/risk-off)
    - China CSI 300 (thương mại song phương) 
    - USD/VND (dòng tiền ngoại)
    - DXY (USD Index) - sức mạnh đồng USD
    - VIX (chỉ số sợ hãi) - tâm lý thị trường
    """
    
    correlations = {}
    impact_analysis = []
    
    # Tính correlation với các chỉ số toàn cầu
    for global_index, global_data in global_market_data.items():
        
        # Align dates
        aligned_data = align_market_data(vn_stock_data, global_data)
        
        if len(aligned_data) > 20:  # Đủ dữ liệu để tính
            correlation = calculate_rolling_correlation(
                aligned_data['vn_returns'], 
                aligned_data['global_returns'],
                window=20
            )
            
            correlations[global_index] = correlation
            
            # Phân tích impact timing
            impact_timing = analyze_impact_timing(
                aligned_data['vn_returns'],
                aligned_data['global_returns']
            )
            
            impact_analysis.append({
                'global_market': global_index,
                'avg_correlation': correlation.mean(),
                'correlation_trend': 'Tăng' if correlation.iloc[-10:].mean() > correlation.iloc[-30:-10].mean() else 'Giảm',
                'lead_lag': impact_timing['lead_lag_days'],  # +: VN theo sau, -: VN dẫn trước
                'impact_strength': impact_timing['impact_strength'],
                'best_correlation_regime': impact_timing['best_regime']
            })
    
    return correlations, impact_analysis

def calculate_rolling_correlation(series1, series2, window=20):
    """Tính correlation lăn"""
    return series1.rolling(window).corr(series2)

def analyze_impact_timing(vn_returns, global_returns, max_lag=5):
    """Phân tích timing của tác động (ai ảnh hưởng ai trước)"""
    
    correlations_by_lag = {}
    
    for lag in range(-max_lag, max_lag + 1):
        if lag == 0:
            corr = np.corrcoef(vn_returns, global_returns)[0, 1]
        elif lag > 0:
            # Global market leads VN by 'lag' days
            corr = np.corrcoef(vn_returns[lag:], global_returns[:-lag])[0, 1]
        else:  # lag < 0
            # VN leads global by abs(lag) days
            corr = np.corrcoef(vn_returns[:lag], global_returns[-lag:])[0, 1]
        
        correlations_by_lag[lag] = abs(corr) if not np.isnan(corr) else 0
    
    # Tìm lag có correlation cao nhất
    best_lag = max(correlations_by_lag.items(), key=lambda x: x[1])
    
    return {
        'lead_lag_days': best_lag[0],
        'impact_strength': best_lag[1],
        'best_regime': 'Global leads VN' if best_lag[0] > 0 else 'VN leads Global' if best_lag[0] < 0 else 'Simultaneous'
    }

# Ví dụ sử dụng với dữ liệu mô phỏng
def load_global_market_data():
    """Load dữ liệu thị trường toàn cầu (mô phỏng)"""
    
    # Trong thực tế, dữ liệu này được lấy từ Yahoo Finance, Bloomberg, etc.
    return {
        'SP500': create_mock_global_data('S&P 500', 0.8),    # High correlation
        'CSI300': create_mock_global_data('China CSI300', 0.6),  # Medium correlation  
        'VIX': create_mock_global_data('VIX', -0.4),         # Negative correlation
        'DXY': create_mock_global_data('DXY', -0.3),         # Weak negative
        'USDVND': create_mock_global_data('USD/VND', -0.5)   # Medium negative
    }

def create_mock_global_data(name, base_correlation):
    """Tạo dữ liệu global mô phỏng"""
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', periods=250, freq='D')
    
    # Tạo returns có correlation với VN market
    vn_proxy_returns = np.random.normal(0.001, 0.02, 250)  # VN market proxy
    noise = np.random.normal(0, 0.015, 250)
    
    global_returns = base_correlation * vn_proxy_returns + np.sqrt(1 - base_correlation**2) * noise
    
    return pd.DataFrame({
        'date': dates,
        'returns': global_returns,
        'market': name
    })

# Chạy phân tích
vcb_data = pd.read_csv('market_data/VCB.csv')
global_data = load_global_market_data()

correlations, impacts = phan_tich_tac_dong_toan_cau(vcb_data, global_data)

print("=== PHÂN TÍCH TÁC ĐỘNG TOÀN CẦU ===")
for impact in impacts:
    print(f"\n🌍 {impact['global_market']}:")
    print(f"   📊 Correlation TB: {impact['avg_correlation']:.3f}")
    print(f"   📈 Xu hướng: {impact['correlation_trend']}")
    print(f"   ⏱️  Lead/Lag: {impact['lead_lag']} ngày ({impact['best_correlation_regime']})")
    print(f"   💪 Sức mạnh tác động: {impact['impact_strength']:.3f}")
```

### B. VPA Multi-Market Context

```python
def vpa_trong_boi_canh_toan_cau(vn_stock_data, global_sentiment):
    """
    Đánh giá tín hiệu VPA trong bối cảnh thị trường toàn cầu
    """
    
    vpa_signals = []
    
    for i in range(20, len(vn_stock_data)):
        current_day = vn_stock_data.iloc[i]
        historical_data = vn_stock_data.iloc[i-19:i+1]
        
        # Tín hiệu VPA cơ bản
        vpa_score = tinh_diem_tin_cay_stopping_volume(historical_data)
        
        # Bối cảnh toàn cầu
        global_context = global_sentiment.get(current_day['date'], {})
        
        # Điều chỉnh VPA score theo global context
        adjusted_vpa_score = adjust_vpa_for_global_context(vpa_score, global_context)
        
        # Market regime (Risk-on vs Risk-off)
        market_regime = determine_market_regime(global_context)
        
        # Risk assessment
        risk_level = assess_global_risk(global_context, market_regime)
        
        vpa_signals.append({
            'date': current_day['date'],
            'price': current_day['close'],
            'base_vpa_score': vpa_score,
            'adjusted_vpa_score': adjusted_vpa_score,
            'market_regime': market_regime,
            'global_risk_level': risk_level,
            'recommendation': generate_global_aware_recommendation(
                adjusted_vpa_score, market_regime, risk_level
            ),
            'global_factors': global_context
        })
    
    return vpa_signals

def adjust_vpa_for_global_context(base_vpa_score, global_context):
    """
    Điều chỉnh điểm VPA dựa trên bối cảnh toàn cầu
    """
    adjusted_score = base_vpa_score
    
    # S&P 500 strong positive -> boost VPA signals
    if global_context.get('sp500_momentum', 0) > 0.02:  # S&P tăng > 2%
        adjusted_score *= 1.2
    elif global_context.get('sp500_momentum', 0) < -0.02:  # S&P giảm > 2%
        adjusted_score *= 0.7
    
    # VIX (Fear index) high -> reduce confidence
    if global_context.get('vix_level', 20) > 30:  # VIX > 30 = high fear
        adjusted_score *= 0.6
    elif global_context.get('vix_level', 20) < 15:  # VIX < 15 = complacency
        adjusted_score *= 1.1
    
    # USD strength -> affects foreign flows
    if global_context.get('dxy_momentum', 0) > 0.01:  # USD mạnh
        adjusted_score *= 0.8  # Harder for foreign money to flow in
    
    # China market (major trading partner)
    if global_context.get('china_momentum', 0) > 0.015:  # China strong
        adjusted_score *= 1.15
    elif global_context.get('china_momentum', 0) < -0.015:  # China weak
        adjusted_score *= 0.85
    
    return max(0, min(100, adjusted_score))

def determine_market_regime(global_context):
    """
    Xác định chế độ thị trường hiện tại
    """
    
    risk_on_signals = 0
    risk_off_signals = 0
    
    # S&P 500 momentum
    sp500_mom = global_context.get('sp500_momentum', 0)
    if sp500_mom > 0.01:
        risk_on_signals += 2
    elif sp500_mom < -0.01:
        risk_off_signals += 2
    
    # VIX level
    vix = global_context.get('vix_level', 20)
    if vix < 20:
        risk_on_signals += 1
    elif vix > 25:
        risk_off_signals += 1
    
    # USD/VND and foreign flows
    usdvnd_mom = global_context.get('usdvnd_momentum', 0)
    if usdvnd_mom < -0.005:  # VND strengthening
        risk_on_signals += 1
    elif usdvnd_mom > 0.005:  # VND weakening
        risk_off_signals += 1
    
    # China momentum
    china_mom = global_context.get('china_momentum', 0)
    if china_mom > 0.01:
        risk_on_signals += 1
    elif china_mom < -0.01:
        risk_off_signals += 1
    
    if risk_on_signals > risk_off_signals + 1:
        return "RISK-ON"
    elif risk_off_signals > risk_on_signals + 1:
        return "RISK-OFF"
    else:
        return "MIXED"

# Chạy phân tích VPA global-aware
global_sentiment_mock = create_mock_global_sentiment(vcb_data)
global_vpa_signals = vpa_trong_boi_canh_toan_cau(vcb_data, global_sentiment_mock)

print("\n=== VPA TRONG BỐI CẢNH TOÀN CẦU ===")
for signal in global_vpa_signals[-5:]:  # 5 tín hiệu gần nhất
    print(f"\n📅 {signal['date']}:")
    print(f"   💰 VCB: {signal['price']:,}đ")
    print(f"   📊 VPA cơ bản: {signal['base_vpa_score']:.0f}/100")
    print(f"   🌍 VPA điều chỉnh: {signal['adjusted_vpa_score']:.0f}/100")
    print(f"   🎯 Market regime: {signal['market_regime']}")
    print(f"   ⚠️ Risk level: {signal['global_risk_level']}")
    print(f"   💡 Recommendation: {signal['recommendation']}")
```

---

## 📈 Phần 2: Thực Hành - Sector Rotation Global

### A. Theo Dõi Vòng Quay Ngành Toàn Cầu

```python
def phan_tich_sector_rotation_toan_cau(vn_sectors_data, global_sectors_data):
    """
    Phân tích vòng quay ngành toàn cầu và ảnh hưởng đến VN
    
    VN Sectors: Banking, Real Estate, Steel, Consumer, Technology
    Global Sectors: Technology, Healthcare, Financials, Energy, Materials
    """
    
    sector_analysis = {}
    
    vn_sectors = {
        'Banking': ['VCB', 'TCB', 'BID', 'CTG', 'VPB'],
        'RealEstate': ['VIC', 'VHM', 'NVL', 'KDH', 'PDR'], 
        'Steel': ['HPG', 'HSG', 'NKG', 'TVN', 'TLH'],
        'Consumer': ['SAB', 'MSN', 'MCH', 'VNM', 'PNJ'],
        'Technology': ['CMG', 'ELC', 'ITD', 'CMT', 'ST8']
    }
    
    global_sectors = ['XLK', 'XLF', 'XLE', 'XLB', 'XLV']  # US Sector ETFs
    
    for vn_sector, vn_stocks in vn_sectors.items():
        
        # Tính performance VN sector
        vn_sector_performance = calculate_sector_performance(vn_stocks, vn_sectors_data)
        
        # Tìm global sector tương ứng
        corresponding_global = map_vn_to_global_sector(vn_sector)
        
        if corresponding_global in global_sectors_data:
            global_sector_performance = global_sectors_data[corresponding_global]
            
            # Phân tích correlation
            correlation = analyze_sector_correlation(
                vn_sector_performance, 
                global_sector_performance
            )
            
            # Lead/lag analysis
            lead_lag = analyze_sector_lead_lag(
                vn_sector_performance,
                global_sector_performance
            )
            
            # Rotation prediction
            rotation_signal = predict_sector_rotation(
                vn_sector_performance,
                global_sector_performance,
                correlation,
                lead_lag
            )
            
            sector_analysis[vn_sector] = {
                'correlation_with_global': correlation,
                'lead_lag_days': lead_lag,
                'current_relative_strength': calculate_relative_strength(vn_sector_performance),
                'rotation_signal': rotation_signal,
                'recommended_action': generate_sector_recommendation(rotation_signal),
                'top_stocks_in_sector': rank_stocks_in_sector(vn_stocks, vn_sectors_data),
                'global_sector_trend': analyze_global_sector_trend(global_sector_performance)
            }
    
    return sector_analysis

def predict_sector_rotation(vn_performance, global_performance, correlation, lead_lag):
    """
    Dự đoán vòng quay ngành dựa trên:
    1. Global sector momentum
    2. VN sector relative performance  
    3. Historical correlation patterns
    """
    
    # Global sector momentum (10 ngày gần nhất)
    global_momentum = global_performance['returns'][-10:].mean()
    
    # VN sector momentum
    vn_momentum = vn_performance['returns'][-10:].mean()
    
    # Relative performance vs benchmark
    vn_vs_market = vn_momentum - 0.001  # Assume market return = 0.1%/day
    
    signals = []
    
    # Signal 1: Global sector rotating in
    if global_momentum > 0.005 and correlation > 0.4:  # Strong global momentum + correlation
        if lead_lag > 0:  # Global leads VN
            signals.append(('ROTATION_IN_COMING', 0.7))
        else:
            signals.append(('ROTATION_IN_NOW', 0.8))
    
    # Signal 2: VN sector outperforming global
    if vn_vs_market > 0.002 and global_momentum < 0:
        signals.append(('VN_SECTOR_STRONG', 0.6))
    
    # Signal 3: Sector rotation out
    if global_momentum < -0.005 and correlation > 0.3:
        signals.append(('ROTATION_OUT_WARNING', 0.6))
    
    # Combine signals
    if not signals:
        return {'signal': 'NEUTRAL', 'strength': 0.5, 'reasoning': 'No clear rotation signal'}
    
    # Take strongest signal
    strongest_signal = max(signals, key=lambda x: x[1])
    
    return {
        'signal': strongest_signal[0],
        'strength': strongest_signal[1],
        'reasoning': generate_rotation_reasoning(strongest_signal, global_momentum, vn_momentum)
    }

# Chạy phân tích sector rotation
print("=== PHÂN TÍCH SECTOR ROTATION TOÀN CẦU ===")
print("🔄 Tracking global sector rotation impact on Vietnam sectors...")

# Mock data for demonstration
vn_sectors_mock = create_mock_vn_sectors_data()
global_sectors_mock = create_mock_global_sectors_data()

sector_rotation_analysis = phan_tich_sector_rotation_toan_cau(vn_sectors_mock, global_sectors_mock)

for sector, analysis in sector_rotation_analysis.items():
    print(f"\n🏭 {sector}:")
    print(f"   🌍 Correlation với Global: {analysis['correlation_with_global']:.3f}")
    print(f"   ⏱️ Lead/Lag: {analysis['lead_lag_days']} ngày")
    print(f"   📈 Relative Strength: {analysis['current_relative_strength']:.2f}")
    print(f"   🔄 Rotation Signal: {analysis['rotation_signal']['signal']}")
    print(f"   💪 Signal Strength: {analysis['rotation_signal']['strength']:.1%}")
    print(f"   💡 Recommended Action: {analysis['recommended_action']}")
```

---

## 🔍 Phần 3: Nâng Cao - Event-Driven Analysis

> 💡 **Lưu ý**: Phần này dành cho người muốn hiểu về event-driven trading. 
> Nếu bạn mới bắt đầu, có thể **bỏ qua** và quay lại sau.

### A. Theo Dõi Sự Kiện Toàn Cầu

```python
class GlobalEventTracker:
    def __init__(self):
        self.event_impact_history = {}
        self.event_types = {
            'fed_meeting': {'impact_duration': 3, 'volatility_multiplier': 1.5},
            'china_data': {'impact_duration': 2, 'volatility_multiplier': 1.2},
            'geopolitical': {'impact_duration': 7, 'volatility_multiplier': 2.0},
            'commodity_shock': {'impact_duration': 5, 'volatility_multiplier': 1.8},
            'currency_intervention': {'impact_duration': 2, 'volatility_multiplier': 1.3}
        }
    
    def track_upcoming_events(self):
        """
        Theo dõi các sự kiện quan trọng sắp tới
        """
        
        # Economic calendar (normally from API)
        upcoming_events = [
            {
                'date': '2025-07-30',
                'event': 'Fed Interest Rate Decision',
                'type': 'fed_meeting',
                'importance': 'HIGH',
                'expected_impact': {
                    'VN_stocks': 'HIGH',
                    'VND': 'MEDIUM', 
                    'foreign_flows': 'HIGH'
                }
            },
            {
                'date': '2025-07-25',
                'event': 'China Manufacturing PMI',
                'type': 'china_data',
                'importance': 'MEDIUM',
                'expected_impact': {
                    'VN_export_stocks': 'MEDIUM',
                    'commodities': 'MEDIUM'
                }
            }
        ]
        
        return upcoming_events
    
    def analyze_pre_event_positioning(self, vn_stock_data, event_date, event_type):
        """
        Phân tích positioning trước sự kiện
        """
        
        # Tìm dữ liệu 10 ngày trước event
        event_date_obj = pd.to_datetime(event_date)
        pre_event_data = vn_stock_data[
            (pd.to_datetime(vn_stock_data['date']) >= event_date_obj - pd.Timedelta(days=10)) &
            (pd.to_datetime(vn_stock_data['date']) < event_date_obj)
        ]
        
        if len(pre_event_data) < 5:
            return None
        
        # Phân tích volume patterns
        volume_trend = analyze_volume_trend_pre_event(pre_event_data)
        
        # Phân tích price positioning
        price_positioning = analyze_price_positioning_pre_event(pre_event_data)
        
        # VPA signals trước event
        vpa_signals_pre_event = []
        for i in range(5, len(pre_event_data)):
            window_data = pre_event_data.iloc[i-4:i+1]
            vpa_score = tinh_diem_tin_cay_stopping_volume_simple(window_data, pre_event_data.iloc[i])
            if vpa_score > 60:
                vpa_signals_pre_event.append(vpa_score)
        
        return {
            'volume_trend': volume_trend,
            'price_positioning': price_positioning,
            'vpa_signals_count': len(vpa_signals_pre_event),
            'avg_vpa_strength': np.mean(vpa_signals_pre_event) if vpa_signals_pre_event else 0,
            'positioning_risk': assess_pre_event_risk(volume_trend, price_positioning),
            'recommended_strategy': recommend_pre_event_strategy(
                volume_trend, price_positioning, event_type
            )
        }
    
    def backtest_event_impact(self, historical_events, stock_data):
        """
        Backtest impact của các events lịch sử
        """
        
        event_performance = []
        
        for event in historical_events:
            event_date = pd.to_datetime(event['date'])
            event_type = event['type']
            
            # Tìm dữ liệu around event date
            event_data = stock_data[
                (pd.to_datetime(stock_data['date']) >= event_date - pd.Timedelta(days=5)) &
                (pd.to_datetime(stock_data['date']) <= event_date + pd.Timedelta(days=10))
            ]
            
            if len(event_data) < 10:
                continue
            
            # Tính performance pre vs post event
            pre_event_price = event_data[event_data['date'] <= event['date']]['close'].iloc[-1]
            
            impact_duration = self.event_types[event_type]['impact_duration']
            post_event_data = event_data[event_data['date'] > event['date']]
            
            if len(post_event_data) >= impact_duration:
                post_event_price = post_event_data['close'].iloc[impact_duration-1]
                event_return = (post_event_price - pre_event_price) / pre_event_price
                
                event_performance.append({
                    'event_type': event_type,
                    'event_return': event_return,
                    'volatility_increase': calculate_volatility_increase(event_data, event_date),
                    'volume_spike': calculate_volume_spike(event_data, event_date)
                })
        
        # Phân tích thống kê
        performance_stats = {}
        for event_type in self.event_types.keys():
            type_events = [e for e in event_performance if e['event_type'] == event_type]
            
            if type_events:
                returns = [e['event_return'] for e in type_events]
                performance_stats[event_type] = {
                    'avg_return': np.mean(returns),
                    'volatility': np.std(returns),
                    'win_rate': sum(1 for r in returns if r > 0) / len(returns),
                    'max_return': max(returns),
                    'min_return': min(returns)
                }
        
        return performance_stats

# Sử dụng Event Tracker
event_tracker = GlobalEventTracker()
upcoming_events = event_tracker.track_upcoming_events()

print("\n=== GLOBAL EVENT ANALYSIS ===")
print("📅 Upcoming High-Impact Events:")

for event in upcoming_events:
    print(f"\n🗓️ {event['date']}: {event['event']}")
    print(f"   ⚠️ Importance: {event['importance']}")
    print(f"   📊 Expected Impact:")
    for asset, impact in event['expected_impact'].items():
        print(f"      • {asset}: {impact}")
    
    # Pre-event positioning analysis
    pre_analysis = event_tracker.analyze_pre_event_positioning(
        vcb_data, event['date'], event['type']
    )
    
    if pre_analysis:
        print(f"   💡 Pre-Event Strategy: {pre_analysis['recommended_strategy']}")
        print(f"   ⚠️ Positioning Risk: {pre_analysis['positioning_risk']}")
```

---

## 📋 Tóm Tắt Chương

### Những Gì Đã Học:
1. **Cross-market correlation** - Hiểu mối liên hệ VN với thế giới
2. **Global-aware VPA** - Điều chỉnh tín hiệu VPA theo bối cảnh toàn cầu
3. **Sector rotation tracking** - Theo dõi vòng quay ngành toàn cầu
4. **Event-driven analysis** - Phân tích tác động sự kiện kinh tế (nâng cao)

### Lợi Ích Thiết Thực:
- ✅ **Tránh được bẫy** - Không mua khi global sentiment xấu
- ✅ **Timing tốt hơn** - Biết khi nào nên aggressive, khi nào defensive
- ✅ **Sector selection** - Chọn ngành đang được favor globally
- ✅ **Risk management** - Giảm position trước events lớn

### Ma Trận Quyết Định:
| Global Context | VPA Signal Strong | VPA Signal Weak |
|----------------|-------------------|-----------------|
| Risk-On + China Strong | 🟢 STRONG BUY | 🔵 HOLD/WATCH |
| Risk-Off + High VIX | 🟡 WAIT | 🔴 AVOID |
| Mixed + USD Weak | 🔵 CAUTIOUS BUY | 🟡 NEUTRAL |

### Chương Tiếp Theo:
**Chương 5.6: Hệ Thống Cảnh Báo Thông Minh** - Xây dựng system theo dõi 24/7 và cảnh báo realtime khi có cơ hội.