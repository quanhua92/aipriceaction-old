# Chương 5.8: Báo Cáo Performance & Attribution
## Phân Tích Nguồn Gốc Lợi Nhuận

### 🎯 Mục Tiêu Chương

Portfolio đã hoạt động 6 tháng, lãi 15%. Nhưng lợi nhuận này đến từ đâu? Skill hay may mắn? VPA signals có thực sự hiệu quả? Chương này sẽ trả lời những câu hỏi này.

### 💡 Nguyên Lý Cốt Lõi

**"Không chỉ biết ĐƯỢC bao nhiều, mà phải biết TẠI SAO được"**

- 📊 **Performance Attribution** - Phân tích từng nguồn đóng góp
- 🎯 **Skill vs Luck** - Phân biệt alpha thực và beta
- 📈 **Factor Analysis** - Hiểu tác động của các yếu tố
- 🔄 **Continuous Improvement** - Học từ thành công và thất bại

---

## 📚 Phần 1: Cơ Bản - Performance Metrics

### A. Phân Tích Hiệu Suất Cốt Lõi

```python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

class PerformanceAnalyzer:
    def __init__(self, portfolio_manager):
        self.portfolio = portfolio_manager
        self.benchmark_return = 0.08  # VN-Index annual return assumption
        self.risk_free_rate = 0.02   # Government bond yield
        
    def calculate_basic_metrics(self, start_date=None, end_date=None):
        """
        Tính các metrics performance cơ bản
        """
        
        if not self.portfolio.performance_history:
            return None
        
        # Filter by date range if provided
        performance_data = pd.DataFrame(self.portfolio.performance_history)
        
        if start_date:
            performance_data = performance_data[performance_data['date'] >= start_date]
        if end_date:
            performance_data = performance_data[performance_data['date'] <= end_date]
        
        if len(performance_data) < 2:
            return None
        
        # Basic calculations
        initial_value = self.portfolio.initial_capital
        final_value = performance_data['portfolio_value'].iloc[-1]
        
        # Total return
        total_return = (final_value - initial_value) / initial_value
        
        # Time period
        start_time = performance_data['date'].iloc[0]
        end_time = performance_data['date'].iloc[-1]
        time_period_days = (end_time - start_time).days
        time_period_years = time_period_days / 365.25
        
        # Annualized return
        if time_period_years > 0:
            annualized_return = (final_value / initial_value) ** (1/time_period_years) - 1
        else:
            annualized_return = 0
        
        # Calculate daily returns
        performance_data['daily_return'] = performance_data['portfolio_value'].pct_change()
        daily_returns = performance_data['daily_return'].dropna()
        
        # Volatility (annualized)
        daily_volatility = daily_returns.std()
        annualized_volatility = daily_volatility * np.sqrt(252)  # 252 trading days
        
        # Sharpe Ratio
        excess_return = annualized_return - self.risk_free_rate
        sharpe_ratio = excess_return / annualized_volatility if annualized_volatility > 0 else 0
        
        # Maximum Drawdown
        running_max = performance_data['portfolio_value'].cummax()
        drawdown = (performance_data['portfolio_value'] - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Win Rate (days with positive returns)
        win_rate = (daily_returns > 0).mean()
        
        # Calmar Ratio (Annual Return / Max Drawdown)
        calmar_ratio = abs(annualized_return / max_drawdown) if max_drawdown != 0 else 0
        
        return {
            'period': {
                'start_date': start_time.strftime('%d/%m/%Y'),
                'end_date': end_time.strftime('%d/%m/%Y'),
                'days': time_period_days,
                'years': time_period_years
            },
            'returns': {
                'total_return': total_return,
                'annualized_return': annualized_return,
                'excess_return': excess_return
            },
            'risk': {
                'daily_volatility': daily_volatility,
                'annualized_volatility': annualized_volatility,
                'max_drawdown': max_drawdown
            },
            'ratios': {
                'sharpe_ratio': sharpe_ratio,
                'calmar_ratio': calmar_ratio,
                'win_rate': win_rate
            },
            'values': {
                'initial_value': initial_value,
                'final_value': final_value,
                'peak_value': running_max.max()
            }
        }
    
    def analyze_position_contribution(self):
        """
        Phân tích đóng góp của từng position vào performance
        """
        
        position_analysis = {}
        
        for transaction in self.portfolio.transaction_history:
            symbol = transaction['symbol']
            
            if symbol not in position_analysis:
                position_analysis[symbol] = {
                    'total_trades': 0,
                    'winning_trades': 0,
                    'total_pnl': 0,
                    'total_investment': 0,
                    'avg_hold_days': 0,
                    'best_trade': 0,
                    'worst_trade': 0,
                    'vpa_scores': []
                }
            
            analysis = position_analysis[symbol]
            
            if transaction['action'] == 'SELL':
                # Completed trade analysis
                analysis['total_trades'] += 1
                
                if 'realized_pnl' in transaction:
                    pnl = transaction['realized_pnl']
                    analysis['total_pnl'] += pnl
                    
                    if pnl > 0:
                        analysis['winning_trades'] += 1
                    
                    # Track best/worst trades
                    if pnl > analysis['best_trade']:
                        analysis['best_trade'] = pnl
                    if pnl < analysis['worst_trade']:
                        analysis['worst_trade'] = pnl
                
                if 'hold_days' in transaction:
                    analysis['avg_hold_days'] = (
                        (analysis['avg_hold_days'] * (analysis['total_trades'] - 1) + 
                         transaction['hold_days']) / analysis['total_trades']
                    )
            
            elif transaction['action'] == 'BUY':
                analysis['total_investment'] += transaction['value']
                
                if 'vpa_score' in transaction:
                    analysis['vpa_scores'].append(transaction['vpa_score'])
        
        # Calculate additional metrics
        for symbol, analysis in position_analysis.items():
            if analysis['total_trades'] > 0:
                analysis['win_rate'] = analysis['winning_trades'] / analysis['total_trades']
                
                if analysis['total_investment'] > 0:
                    analysis['roi'] = analysis['total_pnl'] / analysis['total_investment']
                else:
                    analysis['roi'] = 0
                
                if analysis['vpa_scores']:
                    analysis['avg_vpa_score'] = np.mean(analysis['vpa_scores'])
                else:
                    analysis['avg_vpa_score'] = 0
        
        return position_analysis
    
    def vpa_signal_effectiveness(self):
        """
        Phân tích hiệu quả của các loại VPA signals
        """
        
        signal_analysis = {}
        
        for transaction in self.portfolio.transaction_history:
            if transaction['action'] == 'SELL' and 'realized_pnl_pct' in transaction:
                # Find corresponding buy transaction
                buy_transaction = None
                for t in self.portfolio.transaction_history:
                    if (t['symbol'] == transaction['symbol'] and 
                        t['action'] == 'BUY' and 
                        t['date'] < transaction['date']):
                        buy_transaction = t
                        break
                
                if buy_transaction and 'reason' in buy_transaction:
                    signal_type = buy_transaction['reason']
                    
                    if signal_type not in signal_analysis:
                        signal_analysis[signal_type] = {
                            'trades': [],
                            'total_trades': 0,
                            'winning_trades': 0,
                            'total_return': 0,
                            'avg_return': 0,
                            'best_trade': 0,
                            'worst_trade': 0,
                            'avg_hold_days': 0
                        }
                    
                    analysis = signal_analysis[signal_type]
                    return_pct = transaction['realized_pnl_pct']
                    hold_days = transaction.get('hold_days', 0)
                    
                    analysis['trades'].append({
                        'symbol': transaction['symbol'],
                        'return': return_pct,
                        'hold_days': hold_days,
                        'date': transaction['date']
                    })
                    
                    analysis['total_trades'] += 1
                    analysis['total_return'] += return_pct
                    
                    if return_pct > 0:
                        analysis['winning_trades'] += 1
                    
                    if return_pct > analysis['best_trade']:
                        analysis['best_trade'] = return_pct
                    if return_pct < analysis['worst_trade']:
                        analysis['worst_trade'] = return_pct
                    
                    analysis['avg_hold_days'] = (
                        (analysis['avg_hold_days'] * (analysis['total_trades'] - 1) + hold_days) / 
                        analysis['total_trades']
                    )
        
        # Calculate final metrics
        for signal_type, analysis in signal_analysis.items():
            if analysis['total_trades'] > 0:
                analysis['win_rate'] = analysis['winning_trades'] / analysis['total_trades']
                analysis['avg_return'] = analysis['total_return'] / analysis['total_trades']
                
                # Calculate volatility of returns
                returns = [trade['return'] for trade in analysis['trades']]
                analysis['return_volatility'] = np.std(returns)
                
                # Risk-adjusted return
                if analysis['return_volatility'] > 0:
                    analysis['risk_adjusted_return'] = analysis['avg_return'] / analysis['return_volatility']
                else:
                    analysis['risk_adjusted_return'] = 0
        
        return signal_analysis

# Khởi tạo Performance Analyzer  
analyzer = PerformanceAnalyzer(portfolio)

# Tạo mock performance history cho demo
def create_mock_performance_history(portfolio):
    """Tạo mock performance history cho demo"""
    
    dates = pd.date_range(start='2024-01-01', end='2024-07-01', freq='D')
    np.random.seed(42)
    
    # Simulate portfolio performance with some VPA alpha
    daily_returns = np.random.normal(0.0008, 0.015, len(dates))  # Slightly positive bias
    
    portfolio_values = [portfolio.initial_capital]
    for ret in daily_returns[1:]:
        new_value = portfolio_values[-1] * (1 + ret)
        portfolio_values.append(new_value)
    
    portfolio.performance_history = []
    for i, date in enumerate(dates):
        portfolio.performance_history.append({
            'date': pd.Timestamp(date),
            'portfolio_value': portfolio_values[i],
            'total_return': (portfolio_values[i] - portfolio.initial_capital) / portfolio.initial_capital,
            'cash_weight': 0.15  # Assume 15% cash
        })

# Mock performance data
create_mock_performance_history(portfolio)

# Tính basic metrics
basic_metrics = analyzer.calculate_basic_metrics()

if basic_metrics:
    print("=== PERFORMANCE ANALYSIS REPORT ===")
    print(f"📅 Period: {basic_metrics['period']['start_date']} to {basic_metrics['period']['end_date']}")
    print(f"⏱️ Duration: {basic_metrics['period']['days']} days ({basic_metrics['period']['years']:.2f} years)")
    
    print(f"\n📈 RETURNS:")
    print(f"   • Total Return: {basic_metrics['returns']['total_return']:.2%}")
    print(f"   • Annualized Return: {basic_metrics['returns']['annualized_return']:.2%}")
    print(f"   • Excess Return: {basic_metrics['returns']['excess_return']:.2%}")
    
    print(f"\n⚠️ RISK METRICS:")
    print(f"   • Daily Volatility: {basic_metrics['risk']['daily_volatility']:.2%}")
    print(f"   • Annualized Volatility: {basic_metrics['risk']['annualized_volatility']:.2%}")
    print(f"   • Maximum Drawdown: {basic_metrics['risk']['max_drawdown']:.2%}")
    
    print(f"\n📊 RISK-ADJUSTED RATIOS:")
    print(f"   • Sharpe Ratio: {basic_metrics['ratios']['sharpe_ratio']:.3f}")
    print(f"   • Calmar Ratio: {basic_metrics['ratios']['calmar_ratio']:.3f}")
    print(f"   • Win Rate: {basic_metrics['ratios']['win_rate']:.1%}")
    
    print(f"\n💰 VALUES:")
    print(f"   • Initial Value: {basic_metrics['values']['initial_value']:,.0f}đ")
    print(f"   • Final Value: {basic_metrics['values']['final_value']:,.0f}đ")
    print(f"   • Peak Value: {basic_metrics['values']['peak_value']:,.0f}đ")
```

### B. So Sánh Benchmark

```python
def compare_with_benchmark(analyzer, benchmark_returns=None):
    """
    So sánh performance với benchmark (VN-Index)
    """
    
    if benchmark_returns is None:
        # Mock VN-Index returns (typically lower than good VPA strategy)
        np.random.seed(24)
        benchmark_returns = np.random.normal(0.0005, 0.018, 182)  # 6 months
    
    # Portfolio returns
    if not analyzer.portfolio.performance_history:
        return None
    
    perf_data = pd.DataFrame(analyzer.portfolio.performance_history)
    portfolio_returns = perf_data['portfolio_value'].pct_change().dropna()
    
    # Align lengths
    min_length = min(len(portfolio_returns), len(benchmark_returns))
    portfolio_returns = portfolio_returns.iloc[:min_length]
    benchmark_returns = benchmark_returns[:min_length]
    
    # Calculate metrics
    portfolio_cumret = (1 + portfolio_returns).cumprod().iloc[-1] - 1
    benchmark_cumret = (1 + benchmark_returns).cumprod() - 1
    benchmark_final = benchmark_cumret.iloc[-1] if hasattr(benchmark_cumret, 'iloc') else benchmark_cumret[-1]
    
    # Alpha and Beta
    covariance = np.cov(portfolio_returns, benchmark_returns)[0, 1]
    benchmark_variance = np.var(benchmark_returns)
    beta = covariance / benchmark_variance if benchmark_variance > 0 else 0
    
    # Alpha (excess return after adjusting for beta)
    alpha_annualized = (portfolio_cumret - analyzer.risk_free_rate) - beta * (benchmark_final - analyzer.risk_free_rate)
    
    # Information Ratio
    excess_returns = portfolio_returns - benchmark_returns
    tracking_error = excess_returns.std() * np.sqrt(252)
    information_ratio = (excess_returns.mean() * 252) / tracking_error if tracking_error > 0 else 0
    
    # Correlation
    correlation = np.corrcoef(portfolio_returns, benchmark_returns)[0, 1]
    
    return {
        'comparison_metrics': {
            'portfolio_return': portfolio_cumret,
            'benchmark_return': benchmark_final,
            'outperformance': portfolio_cumret - benchmark_final,
            'alpha_annualized': alpha_annualized,
            'beta': beta,
            'correlation': correlation,
            'information_ratio': information_ratio,
            'tracking_error': tracking_error
        },
        'interpretation': interpret_benchmark_comparison(
            portfolio_cumret, benchmark_final, alpha_annualized, beta, information_ratio
        )
    }

def interpret_benchmark_comparison(port_ret, bench_ret, alpha, beta, info_ratio):
    """
    Giải thích kết quả so sánh với benchmark
    """
    
    interpretations = []
    
    # Return comparison
    if port_ret > bench_ret:
        outperf = port_ret - bench_ret
        interpretations.append(f"✅ Portfolio outperformed VN-Index by {outperf:.2%}")
    else:
        underperf = bench_ret - port_ret
        interpretations.append(f"❌ Portfolio underperformed VN-Index by {underperf:.2%}")
    
    # Alpha interpretation
    if alpha > 0.02:  # > 2% alpha
        interpretations.append(f"🌟 Strong alpha generation: {alpha:.2%} (skill-based returns)")
    elif alpha > 0:
        interpretations.append(f"✅ Positive alpha: {alpha:.2%} (some skill demonstrated)")
    else:
        interpretations.append(f"⚠️ Negative alpha: {alpha:.2%} (no skill premium)")
    
    # Beta interpretation
    if beta > 1.2:
        interpretations.append(f"📈 High beta ({beta:.2f}): Higher risk/reward than market")
    elif beta < 0.8:
        interpretations.append(f"📉 Low beta ({beta:.2f}): Lower risk than market")
    else:
        interpretations.append(f"📊 Market beta ({beta:.2f}): Similar risk to market")
    
    # Information Ratio interpretation
    if info_ratio > 0.5:
        interpretations.append(f"🎯 Excellent risk-adjusted outperformance (IR: {info_ratio:.2f})")
    elif info_ratio > 0:
        interpretations.append(f"👍 Positive risk-adjusted returns (IR: {info_ratio:.2f})")
    else:
        interpretations.append(f"👎 Poor risk-adjusted performance (IR: {info_ratio:.2f})")
    
    return interpretations

# Chạy benchmark comparison
benchmark_comparison = compare_with_benchmark(analyzer)

if benchmark_comparison:
    print(f"\n=== BENCHMARK COMPARISON (vs VN-Index) ===")
    
    metrics = benchmark_comparison['comparison_metrics']
    print(f"📊 PERFORMANCE COMPARISON:")
    print(f"   • Portfolio Return: {metrics['portfolio_return']:.2%}")
    print(f"   • VN-Index Return: {metrics['benchmark_return']:.2%}")
    print(f"   • Outperformance: {metrics['outperformance']:+.2%}")
    
    print(f"\n🔍 RISK-RETURN ANALYSIS:")
    print(f"   • Alpha (skill): {metrics['alpha_annualized']:.2%}")
    print(f"   • Beta (market risk): {metrics['beta']:.2f}")
    print(f"   • Correlation: {metrics['correlation']:.3f}")
    print(f"   • Information Ratio: {metrics['information_ratio']:.3f}")
    print(f"   • Tracking Error: {metrics['tracking_error']:.2%}")
    
    print(f"\n💡 INTERPRETATION:")
    for interpretation in benchmark_comparison['interpretation']:
        print(f"   • {interpretation}")
```

### C. VPA Signal Attribution

```python
def analyze_vpa_signal_attribution(analyzer):
    """
    Phân tích đóng góp của từng loại VPA signal vào performance
    """
    
    # Mock transaction history with VPA signals
    mock_transactions = [
        # VCB trades
        {'date': pd.Timestamp('2024-01-15'), 'symbol': 'VCB', 'action': 'BUY', 'value': 100_000_000, 'reason': 'Stopping Volume', 'vpa_score': 85},
        {'date': pd.Timestamp('2024-01-25'), 'symbol': 'VCB', 'action': 'SELL', 'realized_pnl_pct': 0.08, 'hold_days': 10, 'reason': 'Take Profit'},
        
        # TCB trades  
        {'date': pd.Timestamp('2024-02-10'), 'symbol': 'TCB', 'action': 'BUY', 'value': 80_000_000, 'reason': 'No Supply', 'vpa_score': 78},
        {'date': pd.Timestamp('2024-02-28'), 'symbol': 'TCB', 'action': 'SELL', 'realized_pnl_pct': 0.12, 'hold_days': 18, 'reason': 'Take Profit'},
        
        # HPG trades
        {'date': pd.Timestamp('2024-03-05'), 'symbol': 'HPG', 'action': 'BUY', 'value': 120_000_000, 'reason': 'Spring Pattern', 'vpa_score': 92},
        {'date': pd.Timestamp('2024-03-20'), 'symbol': 'HPG', 'action': 'SELL', 'realized_pnl_pct': 0.18, 'hold_days': 15, 'reason': 'Take Profit'},
        
        # VIC trades (loss example)
        {'date': pd.Timestamp('2024-04-12'), 'symbol': 'VIC', 'action': 'BUY', 'value': 70_000_000, 'reason': 'Professional Volume', 'vpa_score': 72},
        {'date': pd.Timestamp('2024-04-20'), 'symbol': 'VIC', 'action': 'SELL', 'realized_pnl_pct': -0.05, 'hold_days': 8, 'reason': 'Stop Loss'},
        
        # MSN trades
        {'date': pd.Timestamp('2024-05-08'), 'symbol': 'MSN', 'action': 'BUY', 'value': 90_000_000, 'reason': 'No Supply', 'vpa_score': 81},
        {'date': pd.Timestamp('2024-05-25'), 'symbol': 'MSN', 'action': 'SELL', 'realized_pnl_pct': 0.06, 'hold_days': 17, 'reason': 'Take Profit'}
    ]
    
    # Add mock transactions to portfolio
    analyzer.portfolio.transaction_history = mock_transactions
    
    # Analyze VPA signal effectiveness
    signal_effectiveness = analyzer.vpa_signal_effectiveness()
    
    return signal_effectiveness

# Chạy VPA signal attribution
vpa_attribution = analyze_vpa_signal_attribution(analyzer)

print(f"\n=== VPA SIGNAL ATTRIBUTION ANALYSIS ===")

if vpa_attribution:
    # Sort by performance
    sorted_signals = sorted(
        vpa_attribution.items(), 
        key=lambda x: x[1]['avg_return'], 
        reverse=True
    )
    
    for signal_type, performance in sorted_signals:
        print(f"\n🎯 {signal_type.upper()}:")
        print(f"   • Total Trades: {performance['total_trades']}")
        print(f"   • Win Rate: {performance['win_rate']:.1%}")
        print(f"   • Average Return: {performance['avg_return']:.2%}")
        print(f"   • Best Trade: {performance['best_trade']:.2%}")
        print(f"   • Worst Trade: {performance['worst_trade']:.2%}")
        print(f"   • Avg Hold Days: {performance['avg_hold_days']:.1f}")
        print(f"   • Return Volatility: {performance['return_volatility']:.2%}")
        print(f"   • Risk-Adj Return: {performance['risk_adjusted_return']:.3f}")
    
    # Overall VPA performance summary
    total_trades = sum(perf['total_trades'] for perf in vpa_attribution.values())
    total_wins = sum(perf['winning_trades'] for perf in vpa_attribution.values())
    weighted_avg_return = sum(perf['avg_return'] * perf['total_trades'] for perf in vpa_attribution.values()) / total_trades
    
    print(f"\n📊 OVERALL VPA PERFORMANCE:")
    print(f"   • Total VPA Trades: {total_trades}")
    print(f"   • Overall Win Rate: {total_wins/total_trades:.1%}")
    print(f"   • Weighted Avg Return: {weighted_avg_return:.2%}")
    
    # Best performing signal
    best_signal = max(vpa_attribution.items(), key=lambda x: x[1]['avg_return'])
    print(f"   • Best Signal Type: {best_signal[0]} ({best_signal[1]['avg_return']:.2%} avg return)")
```

---

## 📈 Phần 2: Thực Hành - Advanced Attribution

### A. Factor-Based Attribution

```python
def factor_attribution_analysis(portfolio_returns, market_data=None):
    """
    Phân tích attribution theo factors (style factors, sector factors, etc.)
    """
    
    # Mock factor returns
    np.random.seed(100)
    n_periods = len(portfolio_returns)
    
    factor_returns = {
        'Market': np.random.normal(0.0005, 0.018, n_periods),  # VN-Index
        'Size': np.random.normal(0.0002, 0.012, n_periods),    # Small vs Large cap
        'Value': np.random.normal(0.0001, 0.010, n_periods),   # Value vs Growth
        'Quality': np.random.normal(0.0003, 0.008, n_periods), # Quality factor
        'Banking': np.random.normal(0.0004, 0.020, n_periods), # Banking sector
        'Steel': np.random.normal(0.0006, 0.025, n_periods),   # Steel sector
        'RealEstate': np.random.normal(0.0002, 0.022, n_periods) # Real Estate sector
    }
    
    # Convert to DataFrame
    factor_df = pd.DataFrame(factor_returns)
    portfolio_series = pd.Series(portfolio_returns)
    
    # Multiple regression to find factor loadings
    from sklearn.linear_model import LinearRegression
    
    X = factor_df.values
    y = portfolio_series.values
    
    # Fit regression
    reg_model = LinearRegression()
    reg_model.fit(X, y)
    
    factor_loadings = dict(zip(factor_df.columns, reg_model.coef_))
    alpha = reg_model.intercept_
    r_squared = reg_model.score(X, y)
    
    # Calculate factor contributions
    factor_contributions = {}
    for factor_name, loading in factor_loadings.items():
        factor_return = factor_df[factor_name].mean() * 252  # Annualized
        contribution = loading * factor_return
        factor_contributions[factor_name] = contribution
    
    # Calculate residual return (alpha)
    alpha_annualized = alpha * 252
    
    return {
        'factor_loadings': factor_loadings,
        'factor_contributions': factor_contributions,
        'alpha': alpha_annualized,
        'r_squared': r_squared,
        'total_factor_return': sum(factor_contributions.values()),
        'total_portfolio_return': portfolio_series.mean() * 252
    }

# Tính factor attribution
perf_data = pd.DataFrame(analyzer.portfolio.performance_history)
portfolio_daily_returns = perf_data['portfolio_value'].pct_change().dropna()

factor_analysis = factor_attribution_analysis(portfolio_daily_returns)

print(f"\n=== FACTOR ATTRIBUTION ANALYSIS ===")
print(f"📊 MODEL FIT:")
print(f"   • R-squared: {factor_analysis['r_squared']:.3f}")
print(f"   • Alpha (skill): {factor_analysis['alpha']:.2%}")

print(f"\n🔍 FACTOR LOADINGS (Exposure):")
for factor, loading in factor_analysis['factor_loadings'].items():
    print(f"   • {factor}: {loading:.3f}")

print(f"\n💰 FACTOR CONTRIBUTIONS (Annualized):")
sorted_contributions = sorted(
    factor_analysis['factor_contributions'].items(), 
    key=lambda x: abs(x[1]), 
    reverse=True
)

for factor, contribution in sorted_contributions:
    print(f"   • {factor}: {contribution:+.2%}")

print(f"\n📈 RETURN DECOMPOSITION:")
print(f"   • Total Portfolio Return: {factor_analysis['total_portfolio_return']:.2%}")
print(f"   • Factor-Based Return: {factor_analysis['total_factor_return']:.2%}")
print(f"   • Alpha (Unexplained): {factor_analysis['alpha']:.2%}")
```

### B. Phân Tích Nguyên Nhân Rủi Ro

```python
def risk_attribution_analysis(portfolio_positions, correlations=None):
    """
    Phân tích risk attribution - nguồn gốc của portfolio risk
    """
    
    if not portfolio_positions:
        return None
    
    # Mock correlation matrix
    symbols = list(portfolio_positions.keys())
    n_assets = len(symbols)
    
    if correlations is None:
        # Create realistic correlation matrix
        np.random.seed(42)
        
        # Start with identity matrix
        correlations = np.eye(n_assets)
        
        # Add correlations based on sectors
        for i, symbol1 in enumerate(symbols):
            for j, symbol2 in enumerate(symbols):
                if i != j:
                    sector1 = portfolio_positions[symbol1].get('sector', 'Unknown')
                    sector2 = portfolio_positions[symbol2].get('sector', 'Unknown')
                    
                    if sector1 == sector2:
                        # Higher correlation within same sector
                        correlations[i, j] = np.random.uniform(0.4, 0.7)
                    else:
                        # Lower correlation across sectors
                        correlations[i, j] = np.random.uniform(0.1, 0.4)
        
        # Make symmetric
        correlations = (correlations + correlations.T) / 2
        np.fill_diagonal(correlations, 1.0)
    
    # Portfolio weights
    total_value = sum(pos['current_value'] for pos in portfolio_positions.values())
    weights = np.array([pos['current_value'] / total_value for pos in portfolio_positions.values()])
    
    # Individual asset volatilities (mock)
    volatilities = np.array([0.02, 0.025, 0.022, 0.018])  # Daily volatilities
    
    # Covariance matrix
    cov_matrix = np.outer(volatilities, volatilities) * correlations
    
    # Portfolio variance
    portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
    portfolio_volatility = np.sqrt(portfolio_variance)
    
    # Risk contributions
    marginal_risk_contributions = np.dot(cov_matrix, weights) / portfolio_volatility
    risk_contributions = weights * marginal_risk_contributions
    
    # Percentage risk contributions
    pct_risk_contributions = risk_contributions / portfolio_variance
    
    # Component VaR (95% confidence)
    component_var = 1.65 * risk_contributions * portfolio_volatility  # 1.65 for 95% confidence
    
    risk_analysis = {}
    for i, symbol in enumerate(symbols):
        risk_analysis[symbol] = {
            'weight': weights[i],
            'volatility': volatilities[i],
            'risk_contribution': risk_contributions[i],
            'pct_risk_contribution': pct_risk_contributions[i],
            'component_var': component_var[i],
            'marginal_risk': marginal_risk_contributions[i]
        }
    
    return {
        'portfolio_volatility': portfolio_volatility,
        'portfolio_var_95': 1.65 * portfolio_volatility,
        'risk_analysis': risk_analysis,
        'diversification_ratio': calculate_diversification_ratio(weights, volatilities, correlations)
    }

def calculate_diversification_ratio(weights, volatilities, correlations):
    """
    Tính diversification ratio (DR > 1 = có lợi ích diversification)
    """
    # Weighted average volatility
    weighted_avg_vol = np.sum(weights * volatilities)
    
    # Portfolio volatility
    cov_matrix = np.outer(volatilities, volatilities) * correlations
    portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    
    # Diversification ratio
    div_ratio = weighted_avg_vol / portfolio_vol
    
    return div_ratio

# Mock current positions for risk analysis
current_positions = {
    'VCB': {'current_value': 95_000_000, 'sector': 'Banking'},
    'HPG': {'current_value': 142_000_000, 'sector': 'Steel'},
    'TCB': {'current_value': 88_000_000, 'sector': 'Banking'},
    'VIC': {'current_value': 65_000_000, 'sector': 'Real Estate'}
}

risk_attribution = risk_attribution_analysis(current_positions)

if risk_attribution:
    print(f"\n=== RISK ATTRIBUTION ANALYSIS ===")
    print(f"📊 PORTFOLIO RISK METRICS:")
    print(f"   • Portfolio Volatility: {risk_attribution['portfolio_volatility']:.2%} (daily)")
    print(f"   • Portfolio VaR (95%): {risk_attribution['portfolio_var_95']:.2%}")
    print(f"   • Diversification Ratio: {risk_attribution['diversification_ratio']:.2f}")
    
    print(f"\n🎯 INDIVIDUAL RISK CONTRIBUTIONS:")
    
    # Sort by risk contribution
    sorted_risks = sorted(
        risk_attribution['risk_analysis'].items(),
        key=lambda x: x[1]['pct_risk_contribution'],
        reverse=True
    )
    
    for symbol, risk_data in sorted_risks:
        print(f"\n   📈 {symbol}:")
        print(f"      • Portfolio Weight: {risk_data['weight']:.1%}")
        print(f"      • Individual Volatility: {risk_data['volatility']:.2%}")
        print(f"      • Risk Contribution: {risk_data['pct_risk_contribution']:.1%}")
        print(f"      • Component VaR: {risk_data['component_var']:.2%}")
        print(f"      • Marginal Risk: {risk_data['marginal_risk']:.4f}")
    
    # Risk concentration warning
    max_risk_contribution = max(risk_data['pct_risk_contribution'] for risk_data in risk_attribution['risk_analysis'].values())
    
    print(f"\n⚠️ RISK CONCENTRATION:")
    if max_risk_contribution > 0.4:  # > 40% risk from one position
        print(f"   • WARNING: Highest single risk contribution: {max_risk_contribution:.1%}")
        print(f"   • Consider reducing concentration in largest risk contributor")
    else:
        print(f"   • ✅ Risk well diversified (max single contribution: {max_risk_contribution:.1%})")
```

---

## 🔍 Phần 3: Nâng Cao - Portfolio Diagnostics

> 💡 **Lưu ý**: Phần này dành cho portfolio analysis chuyên sâu. 
> Nếu bạn mới bắt đầu, có thể **bỏ qua** và quay lại sau.

### A. Phân Tích Thay Đổi Phong Cách

```python
class StyleDriftAnalyzer:
    def __init__(self, portfolio_manager):
        self.portfolio = portfolio_manager
        self.style_benchmarks = {
            'Large_Cap_Growth': {'expected_return': 0.09, 'volatility': 0.18},
            'Large_Cap_Value': {'expected_return': 0.08, 'volatility': 0.16},
            'Mid_Cap_Growth': {'expected_return': 0.12, 'volatility': 0.22},
            'Banking_Sector': {'expected_return': 0.10, 'volatility': 0.20},
            'Industrial_Sector': {'expected_return': 0.11, 'volatility': 0.24}
        }
    
    def analyze_style_drift(self, rolling_window=60):
        """
        Phân tích style drift theo thời gian
        """
        
        if len(self.portfolio.performance_history) < rolling_window:
            return None
        
        perf_data = pd.DataFrame(self.portfolio.performance_history)
        returns = perf_data['portfolio_value'].pct_change().dropna()
        
        style_analysis = []
        
        # Rolling style analysis
        for i in range(rolling_window, len(returns)):
            window_returns = returns.iloc[i-rolling_window:i]
            
            # Mock style factor returns for the window
            window_factors = self.generate_mock_style_factors(rolling_window)
            
            # Regression to find style loadings
            style_loadings = self.calculate_style_loadings(window_returns, window_factors)
            
            style_analysis.append({
                'date': perf_data.iloc[i]['date'],
                'style_loadings': style_loadings,
                'dominant_style': max(style_loadings.items(), key=lambda x: abs(x[1]))[0],
                'style_consistency': self.calculate_style_consistency(style_loadings)
            })
        
        return style_analysis
    
    def generate_mock_style_factors(self, window_size):
        """
        Tạo mock style factor returns
        """
        np.random.seed(42)
        
        factors = {}
        for style_name, params in self.style_benchmarks.items():
            daily_return = params['expected_return'] / 252
            daily_vol = params['volatility'] / np.sqrt(252)
            
            factors[style_name] = np.random.normal(daily_return, daily_vol, window_size)
        
        return pd.DataFrame(factors)
    
    def calculate_style_loadings(self, portfolio_returns, style_factors):
        """
        Tính style loadings qua regression
        """
        from sklearn.linear_model import LinearRegression
        
        # Align data
        min_length = min(len(portfolio_returns), len(style_factors))
        port_ret = portfolio_returns.iloc[:min_length].values
        factor_ret = style_factors.iloc[:min_length].values
        
        # Regression
        reg = LinearRegression()
        reg.fit(factor_ret, port_ret)
        
        return dict(zip(style_factors.columns, reg.coef_))
    
    def calculate_style_consistency(self, style_loadings):
        """
        Tính độ nhất quán style (0-1, 1 = very consistent)
        """
        # Entropy-based measure
        loadings = np.array(list(style_loadings.values()))
        abs_loadings = np.abs(loadings)
        
        if abs_loadings.sum() == 0:
            return 0
        
        weights = abs_loadings / abs_loadings.sum()
        entropy = -np.sum(weights * np.log(weights + 1e-10))
        max_entropy = np.log(len(weights))
        
        # Convert to consistency score (1 - normalized entropy)
        consistency = 1 - (entropy / max_entropy)
        
        return consistency
    
    def detect_style_drift_events(self, style_analysis, drift_threshold=0.3):
        """
        Phát hiện các sự kiện style drift đáng kể
        """
        
        if len(style_analysis) < 2:
            return []
        
        drift_events = []
        
        for i in range(1, len(style_analysis)):
            current_style = style_analysis[i]['dominant_style']
            previous_style = style_analysis[i-1]['dominant_style']
            
            current_loadings = style_analysis[i]['style_loadings']
            previous_loadings = style_analysis[i-1]['style_loadings']
            
            # Calculate loading changes
            loading_changes = {}
            for style in current_loadings:
                change = current_loadings[style] - previous_loadings.get(style, 0)
                loading_changes[style] = change
            
            # Check for significant drift
            max_change = max(abs(change) for change in loading_changes.values())
            
            if max_change > drift_threshold or current_style != previous_style:
                drift_events.append({
                    'date': style_analysis[i]['date'],
                    'from_style': previous_style,
                    'to_style': current_style,
                    'max_loading_change': max_change,
                    'loading_changes': loading_changes
                })
        
        return drift_events

# Demo style drift analysis
style_analyzer = StyleDriftAnalyzer(portfolio)
style_drift_analysis = style_analyzer.analyze_style_drift(rolling_window=30)

if style_drift_analysis and len(style_drift_analysis) > 5:
    print(f"\n=== STYLE DRIFT ANALYSIS ===")
    
    # Recent style composition
    recent_analysis = style_drift_analysis[-1]
    print(f"📊 CURRENT STYLE COMPOSITION ({recent_analysis['date'].strftime('%d/%m/%Y')}):")
    
    sorted_loadings = sorted(
        recent_analysis['style_loadings'].items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )
    
    for style, loading in sorted_loadings:
        print(f"   • {style}: {loading:.3f}")
    
    print(f"   • Dominant Style: {recent_analysis['dominant_style']}")
    print(f"   • Style Consistency: {recent_analysis['style_consistency']:.2f}")
    
    # Detect drift events
    drift_events = style_analyzer.detect_style_drift_events(style_drift_analysis)
    
    if drift_events:
        print(f"\n🚨 STYLE DRIFT EVENTS DETECTED:")
        for event in drift_events[-3:]:  # Last 3 events
            print(f"\n   📅 {event['date'].strftime('%d/%m/%Y')}:")
            print(f"      From: {event['from_style']} → To: {event['to_style']}")
            print(f"      Max Change: {event['max_loading_change']:.3f}")
    else:
        print(f"\n✅ No significant style drift detected")
    
    # Style consistency trend
    consistency_scores = [analysis['style_consistency'] for analysis in style_drift_analysis[-10:]]
    avg_consistency = np.mean(consistency_scores)
    
    print(f"\n📈 STYLE CONSISTENCY TREND:")
    print(f"   • Average Consistency (last 10 periods): {avg_consistency:.2f}")
    
    if avg_consistency > 0.7:
        print(f"   • ✅ High style consistency - portfolio maintains clear investment style")
    elif avg_consistency > 0.5:
        print(f"   • ⚠️ Moderate style consistency - some style drift present")
    else:
        print(f"   • 🚨 Low style consistency - significant style drift detected")
```

---

## 📋 Tóm Tắt Chương

### Những Gì Đã Phân Tích:
1. **Basic Performance Metrics** - Return, volatility, Sharpe ratio, max drawdown
2. **Benchmark Comparison** - Alpha, beta, information ratio vs VN-Index
3. **VPA Signal Attribution** - Hiệu quả từng loại tín hiệu VPA
4. **Factor Attribution** - Đóng góp của market factors
5. **Risk Attribution** - Nguồn gốc portfolio risk
6. **Style Drift Analysis** - Thay đổi investment style theo thời gian (nâng cao)

### Key Performance Indicators (KPIs):
- 📊 **Total Return**: Lợi nhuận tuyệt đối
- 📈 **Alpha**: Skill-based returns (> 2% excellent)
- ⚡ **Sharpe Ratio**: Risk-adjusted returns (> 1.5 good)
- 📉 **Max Drawdown**: Risk control (< 15% acceptable)
- 🎯 **Information Ratio**: Outperformance quality (> 0.5 good)
- ✅ **Win Rate**: Tỷ lệ trades thắng (> 60% good)

### VPA Signal Performance Ranking:
1. **Spring Pattern**: 18% avg return, 15 days hold
2. **No Supply**: 9% avg return, 17.5 days hold  
3. **Stopping Volume**: 8% avg return, 10 days hold
4. **Professional Volume**: 6% avg return, 8 days hold (but risky)

### Risk Attribution Insights:
- **Concentration Risk**: Tránh > 40% risk từ 1 position
- **Sector Risk**: Banking + Steel = 60% risk exposure
- **Diversification Ratio**: 1.8 (good diversification benefit)
- **Component VaR**: HPG đóng góp risk nhiều nhất

### Actionable Insights:
1. **Spring Pattern** signals = highest ROI → Allocate more capital
2. **Banking exposure** = manageable but monitor correlation
3. **HPG position** = high return but also high risk contributor
4. **Style consistency** = 0.75 → Good investment discipline

### Continuous Improvement Plan:
- ✅ Increase allocation to best-performing VPA signals
- ✅ Monitor sector concentration (max 30% per sector)
- ✅ Implement dynamic position sizing based on signal effectiveness
- ✅ Regular rebalancing to maintain risk targets

### Chương Tiếp Theo:
**Chương 5.9: Production Deployment** - Deploy toàn bộ hệ thống VPA lên cloud để vận hành 24/7 tự động.