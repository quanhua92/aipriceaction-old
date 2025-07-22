# Chương 5.7: Tối Ưu Hóa Danh Mục VPA
## Xây Dựng Portfolio Thông Minh Với VPA

### 🎯 Mục Tiêu Chương

Bạn đã biết cách tìm tín hiệu VPA tốt. Nhưng làm sao phân bổ vốn một cách thông minh? Chương này sẽ dạy bạn xây dựng portfolio tối ưu dựa trên VPA signals.

### 💡 Nguyên Lý Cốt Lõi

**"Không chỉ chọn cổ phiếu tốt, mà phải biết đặt bao nhiều tiền vào mỗi cổ phiếu"**

- 🎯 **Signal Strength** → Quyết định tỷ trọng
- ⚖️ **Risk Management** → Giới hạn loss tối đa
- 🔄 **Rebalancing** → Điều chỉnh theo market conditions
- 📊 **Performance Attribution** → Biết lợi nhuận đến từ đâu

---

## 📚 Phần 1: Cơ Bản - Portfolio Construction

### A. VPA-Based Position Sizing

```python
import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class VPAPortfolioManager:
    def __init__(self, initial_capital=1_000_000_000):  # 1 tỷ VNĐ
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = {}
        self.transaction_history = []
        self.performance_history = []
        self.risk_budget = 0.02  # 2% risk per trade
        self.max_position_size = 0.1  # Tối đa 10% portfolio per stock
        self.max_sector_weight = 0.3  # Tối đa 30% per sector
        
    def calculate_position_size(self, vpa_signal_data, stock_volatility, current_price):
        """
        Tính kích thước position dựa trên:
        1. VPA signal strength
        2. Volatility của cổ phiếu  
        3. Risk budget
        """
        
        # Base position size dựa trên risk budget
        risk_per_share = stock_volatility * current_price  # Risk estimate per share
        base_position_shares = (self.current_capital * self.risk_budget) / risk_per_share
        
        # Điều chỉnh theo VPA signal strength
        vpa_score = vpa_signal_data.get('vpa_score', 50)
        confidence = vpa_signal_data.get('confidence', 0.5)
        
        # Signal strength multiplier (0.5x to 2.0x)
        if vpa_score >= 90 and confidence >= 0.8:
            signal_multiplier = 2.0  # Very strong signal
        elif vpa_score >= 80 and confidence >= 0.7:
            signal_multiplier = 1.5  # Strong signal
        elif vpa_score >= 70 and confidence >= 0.6:
            signal_multiplier = 1.0  # Good signal
        elif vpa_score >= 60 and confidence >= 0.5:
            signal_multiplier = 0.7  # Weak signal
        else:
            signal_multiplier = 0.5  # Very weak signal
        
        # Adjusted position size
        adjusted_shares = base_position_shares * signal_multiplier
        
        # Apply maximum position constraint
        max_shares_by_weight = (self.current_capital * self.max_position_size) / current_price
        final_shares = min(adjusted_shares, max_shares_by_weight)
        
        # Position value
        position_value = final_shares * current_price
        position_weight = position_value / self.current_capital
        
        return {
            'shares': int(final_shares),
            'position_value': position_value,
            'position_weight': position_weight,
            'signal_multiplier': signal_multiplier,
            'risk_estimate': final_shares * risk_per_share
        }
    
    def add_vpa_position(self, symbol, vpa_signal_data, market_data):
        """
        Thêm position mới dựa trên VPA signal
        """
        
        current_price = market_data['current_price']
        volatility = market_data.get('volatility', 0.02)  # Default 2% daily volatility
        sector = market_data.get('sector', 'Unknown')
        
        # Check sector concentration
        current_sector_weight = self.get_sector_weight(sector)
        if current_sector_weight >= self.max_sector_weight:
            return {
                'success': False,
                'reason': f'Sector {sector} already at max weight ({self.max_sector_weight:.1%})'
            }
        
        # Calculate position size
        position_info = self.calculate_position_size(vpa_signal_data, volatility, current_price)
        
        if position_info['shares'] < 100:  # Minimum lot size
            return {
                'success': False,
                'reason': 'Position size too small (< 100 shares)'
            }
        
        # Add position
        self.positions[symbol] = {
            'shares': position_info['shares'],
            'entry_price': current_price,
            'entry_date': pd.Timestamp.now(),
            'sector': sector,
            'vpa_signal': vpa_signal_data.copy(),
            'position_value': position_info['position_value'],
            'position_weight': position_info['position_weight'],
            'stop_loss': current_price * (1 - vpa_signal_data.get('stop_loss', 0.08)),  # 8% default stop
            'take_profit': current_price * (1 + vpa_signal_data.get('take_profit', 0.15))  # 15% default target
        }
        
        # Update capital
        self.current_capital -= position_info['position_value']
        
        # Record transaction
        self.transaction_history.append({
            'date': pd.Timestamp.now(),
            'symbol': symbol,
            'action': 'BUY',
            'shares': position_info['shares'],
            'price': current_price,
            'value': position_info['position_value'],
            'vpa_score': vpa_signal_data.get('vpa_score'),
            'reason': vpa_signal_data.get('signal_type', 'VPA Signal')
        })
        
        return {
            'success': True,
            'position_info': position_info,
            'stop_loss': self.positions[symbol]['stop_loss'],
            'take_profit': self.positions[symbol]['take_profit']
        }
    
    def get_sector_weight(self, sector):
        """Tính trọng số hiện tại của sector"""
        sector_value = sum(
            pos['position_value'] for pos in self.positions.values() 
            if pos['sector'] == sector
        )
        total_portfolio_value = self.get_total_portfolio_value()
        return sector_value / total_portfolio_value if total_portfolio_value > 0 else 0
    
    def get_total_portfolio_value(self):
        """Tính tổng giá trị portfolio hiện tại"""
        positions_value = sum(pos['position_value'] for pos in self.positions.values())
        return self.current_capital + positions_value
    
    def update_positions(self, current_prices):
        """Cập nhật giá trị positions với giá hiện tại"""
        
        portfolio_value = self.current_capital
        
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                current_price = current_prices[symbol]
                position['current_price'] = current_price
                position['current_value'] = position['shares'] * current_price
                position['unrealized_pnl'] = position['current_value'] - position['position_value']
                position['unrealized_pnl_pct'] = position['unrealized_pnl'] / position['position_value']
                
                portfolio_value += position['current_value']
        
        # Update performance history
        total_return = (portfolio_value - self.initial_capital) / self.initial_capital
        self.performance_history.append({
            'date': pd.Timestamp.now(),
            'portfolio_value': portfolio_value,
            'total_return': total_return,
            'cash_weight': self.current_capital / portfolio_value
        })
        
        return portfolio_value
    
    def check_exit_conditions(self, current_prices):
        """Kiểm tra điều kiện thoát positions"""
        
        exit_signals = []
        
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                current_price = current_prices[symbol]
                
                # Stop loss hit
                if current_price <= position['stop_loss']:
                    exit_signals.append({
                        'symbol': symbol,
                        'reason': 'STOP_LOSS',
                        'current_price': current_price,
                        'loss_pct': (current_price - position['entry_price']) / position['entry_price']
                    })
                
                # Take profit hit
                elif current_price >= position['take_profit']:
                    exit_signals.append({
                        'symbol': symbol,
                        'reason': 'TAKE_PROFIT',
                        'current_price': current_price,
                        'profit_pct': (current_price - position['entry_price']) / position['entry_price']
                    })
                
                # Time-based exit (hold > 30 days)
                elif (pd.Timestamp.now() - position['entry_date']).days > 30:
                    exit_signals.append({
                        'symbol': symbol,
                        'reason': 'TIME_EXIT',
                        'current_price': current_price,
                        'return_pct': (current_price - position['entry_price']) / position['entry_price']
                    })
        
        return exit_signals
    
    def execute_exit(self, symbol, exit_price, reason):
        """Thực hiện thoát position"""
        
        if symbol not in self.positions:
            return False
        
        position = self.positions[symbol]
        exit_value = position['shares'] * exit_price
        realized_pnl = exit_value - position['position_value']
        realized_pnl_pct = realized_pnl / position['position_value']
        
        # Update capital
        self.current_capital += exit_value
        
        # Record transaction
        self.transaction_history.append({
            'date': pd.Timestamp.now(),
            'symbol': symbol,
            'action': 'SELL',
            'shares': position['shares'],
            'price': exit_price,
            'value': exit_value,
            'realized_pnl': realized_pnl,
            'realized_pnl_pct': realized_pnl_pct,
            'reason': reason,
            'hold_days': (pd.Timestamp.now() - position['entry_date']).days
        })
        
        # Remove position
        del self.positions[symbol]
        
        return {
            'realized_pnl': realized_pnl,
            'realized_pnl_pct': realized_pnl_pct,
            'exit_value': exit_value
        }

# Khởi tạo Portfolio Manager
portfolio = VPAPortfolioManager(initial_capital=1_000_000_000)

print("💼 VPA Portfolio Manager initialized")
print(f"Initial Capital: {portfolio.initial_capital:,}đ")
print(f"Risk per trade: {portfolio.risk_budget:.1%}")
print(f"Max position size: {portfolio.max_position_size:.1%}")
```

### B. Ví Dụ Thực Tế: Xây Dựng Portfolio

```python
def demo_portfolio_construction():
    """
    Demo xây dựng portfolio với nhiều VPA signals
    """
    
    # Mô phỏng VPA signals từ market scanner
    vpa_opportunities = [
        {
            'symbol': 'VCB',
            'vpa_score': 85,
            'confidence': 0.8,
            'signal_type': 'Stopping Volume',
            'stop_loss': 0.06,  # 6% stop loss
            'take_profit': 0.12  # 12% target
        },
        {
            'symbol': 'TCB',
            'vpa_score': 78,
            'confidence': 0.7,
            'signal_type': 'No Supply',
            'stop_loss': 0.08,
            'take_profit': 0.15
        },
        {
            'symbol': 'HPG',
            'vpa_score': 92,
            'confidence': 0.9,
            'signal_type': 'Spring Pattern',
            'stop_loss': 0.05,
            'take_profit': 0.20
        },
        {
            'symbol': 'VIC',
            'vpa_score': 72,
            'confidence': 0.6,
            'signal_type': 'Professional Volume',
            'stop_loss': 0.07,
            'take_profit': 0.10
        }
    ]
    
    # Market data cho từng cổ phiếu
    market_data = {
        'VCB': {'current_price': 86500, 'volatility': 0.018, 'sector': 'Banking'},
        'TCB': {'current_price': 23800, 'volatility': 0.022, 'sector': 'Banking'},
        'HPG': {'current_price': 27100, 'volatility': 0.025, 'sector': 'Steel'},
        'VIC': {'current_price': 42300, 'volatility': 0.020, 'sector': 'Real Estate'}
    }
    
    print("=== PORTFOLIO CONSTRUCTION DEMO ===")
    print(f"Starting capital: {portfolio.initial_capital:,}đ\n")
    
    # Thêm từng position
    for opportunity in vpa_opportunities:
        symbol = opportunity['symbol']
        market_info = market_data[symbol]
        
        result = portfolio.add_vpa_position(symbol, opportunity, market_info)
        
        if result['success']:
            pos_info = result['position_info']
            print(f"✅ Added {symbol}:")
            print(f"   • VPA Score: {opportunity['vpa_score']}/100")
            print(f"   • Position: {pos_info['shares']:,} shares = {pos_info['position_value']:,.0f}đ")
            print(f"   • Weight: {pos_info['position_weight']:.1%}")
            print(f"   • Stop Loss: {result['stop_loss']:,}đ")
            print(f"   • Take Profit: {result['take_profit']:,}đ")
        else:
            print(f"❌ Failed to add {symbol}: {result['reason']}")
        print()
    
    # Hiển thị portfolio summary
    total_value = portfolio.get_total_portfolio_value()
    print("📊 PORTFOLIO SUMMARY:")
    print(f"Total Value: {total_value:,}đ")
    print(f"Cash Remaining: {portfolio.current_capital:,}đ ({portfolio.current_capital/total_value:.1%})")
    print(f"Invested Amount: {total_value - portfolio.current_capital:,}đ")
    
    print(f"\n📈 POSITIONS:")
    for symbol, position in portfolio.positions.items():
        print(f"   • {symbol}: {position['shares']:,} shares @ {position['entry_price']:,}đ")
        print(f"     Sector: {position['sector']}, Weight: {position['position_weight']:.1%}")
    
    print(f"\n🏭 SECTOR ALLOCATION:")
    sectors = {}
    for position in portfolio.positions.values():
        sector = position['sector']
        if sector not in sectors:
            sectors[sector] = 0
        sectors[sector] += position['position_value']
    
    for sector, value in sectors.items():
        weight = value / total_value
        print(f"   • {sector}: {weight:.1%} ({value:,.0f}đ)")

# Chạy demo
demo_portfolio_construction()
```

### C. Quản Lý Rủi Ro và Cân Bằng Lại

```python
def implement_risk_management(portfolio, current_prices):
    """
    Thực hiện risk management cho portfolio
    """
    
    print("\n=== RISK MANAGEMENT CHECK ===")
    
    # 1. Cập nhật giá trị positions
    portfolio_value = portfolio.update_positions(current_prices)
    
    # 2. Kiểm tra exit conditions
    exit_signals = portfolio.check_exit_conditions(current_prices)
    
    if exit_signals:
        print("🚨 Exit signals detected:")
        for signal in exit_signals:
            print(f"   • {signal['symbol']}: {signal['reason']}")
            if signal['reason'] == 'STOP_LOSS':
                print(f"     Loss: {signal['loss_pct']:.1%}")
            elif signal['reason'] == 'TAKE_PROFIT':
                print(f"     Profit: {signal['profit_pct']:.1%}")
            else:
                print(f"     Return: {signal['return_pct']:.1%}")
    else:
        print("✅ No exit signals")
    
    # 3. Portfolio risk metrics
    print(f"\n📊 RISK METRICS:")
    
    # Position concentration
    max_position_weight = max(pos['position_weight'] for pos in portfolio.positions.values()) if portfolio.positions else 0
    print(f"   • Largest position: {max_position_weight:.1%}")
    
    # Sector concentration
    sector_weights = {}
    for position in portfolio.positions.values():
        sector = position['sector']
        if sector not in sector_weights:
            sector_weights[sector] = 0
        sector_weights[sector] += position['position_weight']
    
    max_sector_weight = max(sector_weights.values()) if sector_weights else 0
    print(f"   • Largest sector: {max_sector_weight:.1%}")
    
    # Unrealized P&L
    total_unrealized = sum(pos.get('unrealized_pnl', 0) for pos in portfolio.positions.values())
    unrealized_pct = total_unrealized / portfolio.initial_capital
    print(f"   • Unrealized P&L: {total_unrealized:,.0f}đ ({unrealized_pct:.1%})")
    
    # Cash level
    cash_weight = portfolio.current_capital / portfolio_value
    print(f"   • Cash level: {cash_weight:.1%}")
    
    # Risk warnings
    warnings = []
    if max_position_weight > portfolio.max_position_size:
        warnings.append(f"Position concentration risk: {max_position_weight:.1%} > {portfolio.max_position_size:.1%}")
    
    if max_sector_weight > portfolio.max_sector_weight:
        warnings.append(f"Sector concentration risk: {max_sector_weight:.1%} > {portfolio.max_sector_weight:.1%}")
    
    if cash_weight < 0.1:  # < 10% cash
        warnings.append(f"Low cash level: {cash_weight:.1%}")
    
    if unrealized_pct < -0.1:  # > 10% unrealized loss
        warnings.append(f"High unrealized losses: {unrealized_pct:.1%}")
    
    if warnings:
        print(f"\n⚠️ RISK WARNINGS:")
        for warning in warnings:
            print(f"   • {warning}")
    else:
        print(f"\n✅ All risk metrics within limits")
    
    return {
        'portfolio_value': portfolio_value,
        'exit_signals': exit_signals,
        'risk_warnings': warnings,
        'unrealized_pnl': total_unrealized
    }

# Mô phỏng market movement và risk check
new_prices = {
    'VCB': 89200,  # +3.1%
    'TCB': 23100,  # -2.9%
    'HPG': 28500,  # +5.2%
    'VIC': 41800   # -1.2%
}

print("\n💹 Market Update - New Prices:")
for symbol, price in new_prices.items():
    if symbol in portfolio.positions:
        old_price = portfolio.positions[symbol]['entry_price']
        change = (price - old_price) / old_price
        print(f"   • {symbol}: {price:,}đ ({change:+.1%})")

# Thực hiện risk management
risk_report = implement_risk_management(portfolio, new_prices)
```

---

## 📈 Phần 2: Thực Hành - Portfolio Optimization

### A. Thuyết Danh Mục Hiện Đại với VPA

```python
def optimize_vpa_portfolio(vpa_signals, historical_returns, risk_tolerance=0.15):
    """
    Tối ưu hóa portfolio sử dụng Modern Portfolio Theory kết hợp VPA signals
    """
    
    symbols = list(vpa_signals.keys())
    n_assets = len(symbols)
    
    if n_assets < 2:
        return None
    
    # Expected returns dựa trên VPA scores
    expected_returns = []
    for symbol in symbols:
        vpa_score = vpa_signals[symbol]['vpa_score']
        confidence = vpa_signals[symbol]['confidence']
        
        # Base expected return từ VPA score
        base_return = (vpa_score - 50) / 1000  # Scale to reasonable return
        
        # Adjust bằng confidence
        adjusted_return = base_return * confidence
        
        expected_returns.append(adjusted_return)
    
    expected_returns = np.array(expected_returns)
    
    # Covariance matrix từ historical returns
    returns_df = pd.DataFrame(historical_returns)[symbols]
    cov_matrix = returns_df.cov().values
    
    # Portfolio optimization
    def portfolio_stats(weights):
        portfolio_return = np.sum(weights * expected_returns)
        portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = portfolio_return / portfolio_volatility if portfolio_volatility > 0 else 0
        return portfolio_return, portfolio_volatility, sharpe_ratio
    
    def negative_sharpe(weights):
        return -portfolio_stats(weights)[2]
    
    # Constraints
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})  # Weights sum to 1
    
    # Bounds cho từng asset
    bounds = []
    for symbol in symbols:
        vpa_score = vpa_signals[symbol]['vpa_score']
        confidence = vpa_signals[symbol]['confidence']
        
        # Minimum weight dựa trên VPA strength
        if vpa_score >= 80 and confidence >= 0.7:
            min_weight = 0.05  # At least 5% for strong signals
            max_weight = 0.25  # Max 25%
        elif vpa_score >= 70 and confidence >= 0.6:
            min_weight = 0.02  # At least 2% for good signals
            max_weight = 0.20  # Max 20%
        else:
            min_weight = 0.01  # At least 1% for weak signals
            max_weight = 0.15  # Max 15%
        
        bounds.append((min_weight, max_weight))
    
    # Initial guess - equal weights
    initial_guess = np.array([1/n_assets] * n_assets)
    
    # Optimize
    try:
        result = minimize(
            negative_sharpe,
            initial_guess,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        if result.success:
            optimal_weights = result.x
            port_return, port_vol, sharpe = portfolio_stats(optimal_weights)
            
            return {
                'success': True,
                'weights': dict(zip(symbols, optimal_weights)),
                'expected_return': port_return,
                'volatility': port_vol,
                'sharpe_ratio': sharpe,
                'optimization_result': result
            }
        else:
            return {'success': False, 'error': 'Optimization failed'}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}

# Ví dụ optimization
vpa_signals_for_optimization = {
    'VCB': {'vpa_score': 85, 'confidence': 0.8},
    'TCB': {'vpa_score': 78, 'confidence': 0.7},
    'HPG': {'vpa_score': 92, 'confidence': 0.9},
    'VIC': {'vpa_score': 72, 'confidence': 0.6},
    'VHM': {'vpa_score': 68, 'confidence': 0.55}
}

# Mock historical returns
np.random.seed(42)
historical_returns_mock = {}
for symbol in vpa_signals_for_optimization.keys():
    # Generate correlated returns
    base_return = np.random.normal(0.001, 0.02, 252)  # Daily returns for 1 year
    historical_returns_mock[symbol] = base_return

# Run optimization
optimization_result = optimize_vpa_portfolio(
    vpa_signals_for_optimization, 
    historical_returns_mock,
    risk_tolerance=0.15
)

if optimization_result and optimization_result['success']:
    print("\n=== PORTFOLIO OPTIMIZATION RESULTS ===")
    print(f"Expected Return: {optimization_result['expected_return']:.2%}")
    print(f"Volatility: {optimization_result['volatility']:.2%}")
    print(f"Sharpe Ratio: {optimization_result['sharpe_ratio']:.3f}")
    
    print(f"\n📊 OPTIMAL WEIGHTS:")
    sorted_weights = sorted(
        optimization_result['weights'].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    for symbol, weight in sorted_weights:
        vpa_score = vpa_signals_for_optimization[symbol]['vpa_score']
        print(f"   • {symbol}: {weight:.1%} (VPA: {vpa_score}/100)")
else:
    print("❌ Portfolio optimization failed")
```

---

## 🔍 Phần 3: Nâng Cao - Dynamic Rebalancing

> 💡 **Lưu ý**: Phần này dành cho portfolio management nâng cao. 
> Nếu bạn mới bắt đầu, có thể **bỏ qua** và quay lại sau.

### A. Chiến Lược Cân Bằng Thích Ứng

```python
class DynamicPortfolioRebalancer:
    def __init__(self, portfolio_manager):
        self.portfolio = portfolio_manager
        self.rebalance_frequency = 'weekly'  # weekly, monthly, or signal-based
        self.drift_threshold = 0.05  # 5% drift triggers rebalance
        self.momentum_lookback = 20  # days
        self.mean_reversion_threshold = 0.15  # 15% deviation
        
    def should_rebalance(self, current_weights, target_weights):
        """
        Quyết định có nên rebalance không dựa trên:
        1. Weight drift
        2. Market conditions
        3. VPA signal changes
        """
        
        # 1. Check weight drift
        max_drift = 0
        for symbol in target_weights:
            if symbol in current_weights:
                drift = abs(current_weights[symbol] - target_weights[symbol])
                max_drift = max(max_drift, drift)
        
        drift_trigger = max_drift > self.drift_threshold
        
        # 2. Check market momentum
        # (simplified - would use actual market data)
        market_momentum = self.calculate_market_momentum()
        momentum_trigger = abs(market_momentum) > 0.05  # Strong momentum = delay rebalance
        
        # 3. Check new VPA signals
        new_signals = self.scan_for_new_vpa_signals()
        signal_trigger = len(new_signals) > 0
        
        # Rebalancing logic
        if signal_trigger:
            return True, "New VPA signals detected"
        elif drift_trigger and not momentum_trigger:
            return True, f"Weight drift exceeded threshold: {max_drift:.1%}"
        elif market_momentum < -0.08:  # Strong negative momentum
            return True, "Defensive rebalancing due to market stress"
        else:
            return False, "No rebalancing trigger"
    
    def calculate_market_momentum(self):
        """
        Tính market momentum đơn giản
        """
        # Mock implementation - in practice would use VN-Index data
        return np.random.normal(0, 0.03)  # Random momentum
    
    def scan_for_new_vpa_signals(self):
        """
        Quét tín hiệu VPA mới
        """
        # Mock implementation - would integrate with alert system
        return []  # No new signals for demo
    
    def execute_tactical_rebalancing(self, current_market_conditions):
        """
        Thực hiện tactical rebalancing dựa trên market conditions
        """
        
        rebalancing_actions = []
        
        # Market condition analysis
        vix_equivalent = current_market_conditions.get('volatility_index', 20)
        foreign_flow = current_market_conditions.get('foreign_flow', 0)
        sector_momentum = current_market_conditions.get('sector_momentum', {})
        
        # 1. Volatility-based adjustments
        if vix_equivalent > 30:  # High volatility
            # Reduce risk, increase cash
            for symbol in list(self.portfolio.positions.keys()):
                position = self.portfolio.positions[symbol]
                if position['position_weight'] > 0.08:  # Large positions
                    rebalancing_actions.append({
                        'symbol': symbol,
                        'action': 'REDUCE',
                        'target_weight': position['position_weight'] * 0.8,
                        'reason': 'High volatility risk reduction'
                    })
        
        elif vix_equivalent < 15:  # Low volatility (complacency)
            # Slightly more aggressive on high-conviction positions
            for symbol in list(self.portfolio.positions.keys()):
                position = self.portfolio.positions[symbol]
                vpa_score = position['vpa_signal']['vpa_score']
                if vpa_score > 85:  # High conviction positions
                    rebalancing_actions.append({
                        'symbol': symbol,
                        'action': 'INCREASE',
                        'target_weight': min(position['position_weight'] * 1.2, 0.15),
                        'reason': 'Low volatility opportunity'
                    })
        
        # 2. Foreign flow adjustments
        if foreign_flow < -10_000_000_000:  # Strong foreign selling
            # Defensive positioning - favor domestic-focused stocks
            domestic_bias = ['MSN', 'SAB', 'VNM']  # Consumer staples
            for symbol in domestic_bias:
                if symbol in self.portfolio.positions:
                    position = self.portfolio.positions[symbol]
                    rebalancing_actions.append({
                        'symbol': symbol,
                        'action': 'INCREASE',
                        'target_weight': min(position['position_weight'] * 1.1, 0.12),
                        'reason': 'Defensive positioning during foreign outflow'
                    })
        
        # 3. Sector momentum adjustments
        for sector, momentum in sector_momentum.items():
            if momentum > 0.05:  # Strong positive momentum
                # Increase allocation to winning sectors
                sector_symbols = [s for s, p in self.portfolio.positions.items() 
                                if p['sector'] == sector]
                for symbol in sector_symbols:
                    position = self.portfolio.positions[symbol]
                    rebalancing_actions.append({
                        'symbol': symbol,
                        'action': 'INCREASE',
                        'target_weight': min(position['position_weight'] * 1.15, 0.15),
                        'reason': f'Sector momentum: {sector}'
                    })
        
        return rebalancing_actions
    
    def generate_rebalancing_report(self, rebalancing_actions):
        """
        Tạo báo cáo rebalancing
        """
        
        if not rebalancing_actions:
            return "No rebalancing actions recommended"
        
        report = "=== DYNAMIC REBALANCING REPORT ===\n\n"
        
        # Group by action type
        increases = [a for a in rebalancing_actions if a['action'] == 'INCREASE']
        decreases = [a for a in rebalancing_actions if a['action'] == 'REDUCE']
        
        if increases:
            report += "📈 POSITION INCREASES:\n"
            for action in increases:
                current_weight = self.portfolio.positions[action['symbol']]['position_weight']
                report += f"   • {action['symbol']}: {current_weight:.1%} → {action['target_weight']:.1%}\n"
                report += f"     Reason: {action['reason']}\n"
        
        if decreases:
            report += "\n📉 POSITION DECREASES:\n"
            for action in decreases:
                current_weight = self.portfolio.positions[action['symbol']]['position_weight']
                report += f"   • {action['symbol']}: {current_weight:.1%} → {action['target_weight']:.1%}\n"
                report += f"     Reason: {action['reason']}\n"
        
        # Calculate expected impact
        total_trades = len(rebalancing_actions)
        estimated_costs = total_trades * 0.0015  # 0.15% transaction cost per trade
        
        report += f"\n💰 EXPECTED IMPACT:\n"
        report += f"   • Total trades: {total_trades}\n"
        report += f"   • Estimated transaction costs: {estimated_costs:.2%}\n"
        
        return report

# Demo dynamic rebalancing
rebalancer = DynamicPortfolioRebalancer(portfolio)

# Mock market conditions
current_market_conditions = {
    'volatility_index': 25,  # Moderate volatility
    'foreign_flow': -5_000_000_000,  # Moderate foreign selling
    'sector_momentum': {
        'Banking': 0.03,
        'Steel': 0.07,
        'Real Estate': -0.02
    }
}

# Execute tactical rebalancing
rebalancing_actions = rebalancer.execute_tactical_rebalancing(current_market_conditions)
rebalancing_report = rebalancer.generate_rebalancing_report(rebalancing_actions)

print(rebalancing_report)
```

---

## 📋 Tóm Tắt Chương

### Những Gì Đã Xây Dựng:
1. **VPA Portfolio Manager** - Position sizing dựa trên VPA signals
2. **Risk Management** - Stop loss, take profit, concentration limits
3. **Portfolio Optimization** - Modern Portfolio Theory + VPA
4. **Dynamic Rebalancing** - Adaptive adjustments theo market conditions

### Nguyên Tắc Quản Lý Danh Mục:
- ✅ **Signal-based sizing** - VPA mạnh hơn = position lớn hơn
- ✅ **Risk budgeting** - Giới hạn risk mỗi trade và tổng thể
- ✅ **Diversification** - Không tập trung quá nhiều 1 cổ phiếu/sector
- ✅ **Dynamic adjustment** - Thay đổi theo market conditions
- ✅ **Performance tracking** - Theo dõi và học hỏi từ kết quả

### Ma Trận Allocation:
| VPA Score | Confidence | Base Weight | Risk Multiplier |
|-----------|------------|-------------|-----------------|
| 90+ | 0.8+ | 8-15% | 2.0x |
| 80-89 | 0.7+ | 5-12% | 1.5x |
| 70-79 | 0.6+ | 3-8% | 1.0x |
| 60-69 | 0.5+ | 2-5% | 0.7x |
| <60 | <0.5 | 1-3% | 0.5x |

### Thành Phần Portfolio Lý Tưởng:
- 🏦 **Banking (25-35%)** - VCB, TCB, BID
- 🏗️ **Industrial (20-30%)** - HPG, HOA, HSG
- 🏠 **Real Estate (15-25%)** - VIC, VHM, NVL  
- 🛒 **Consumer (10-20%)** - MSN, SAB, VNM
- 💵 **Cash (10-20%)** - Cơ hội và an toàn

### Chương Tiếp Theo:
**Chương 5.8: Báo Cáo Performance & Attribution** - Phân tích chi tiết hiệu suất portfolio và tìm nguồn gốc lợi nhuận.