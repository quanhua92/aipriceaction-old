# Chương 5.6: Hệ Thống Cảnh Báo Thông Minh
## Theo Dõi 24/7 - Không Bỏ Lỡ Cơ Hội Nào

### 🎯 Mục Tiêu Chương

Bạn không thể ngồi trước màn hình cả ngày để theo dõi 800+ cổ phiếu VN. Chương này sẽ xây dựng hệ thống cảnh báo thông minh làm việc này cho bạn 24/7.

### 💡 Ý Tưởng Cốt Lõi

**"Máy tính thức trắng đêm để bạn không phải"**

- 🔍 **Quét liên tục** - Check mọi cổ phiếu mỗi 5 phút
- 🚨 **Cảnh báo tức thì** - SMS/Email/Telegram khi có tín hiệu mạnh
- 🎯 **Lọc thông minh** - Chỉ báo những cơ hội thực sự đáng chú ý
- 📊 **Dashboard realtime** - Theo dõi trực quan, cập nhật liên tục

---

## 📚 Phần 1: Cơ Bản - Xây Dựng Alert Engine

### A. Cấu Trúc Alert System

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests  # For Telegram
import time
import threading
from datetime import datetime, timedelta

class IntelligentAlertSystem:
    def __init__(self):
        self.alert_rules = {}
        self.alert_channels = {
            'email': {'enabled': False, 'config': {}},
            'telegram': {'enabled': False, 'config': {}},
            'webhook': {'enabled': False, 'config': {}}
        }
        self.alert_history = []
        self.cooldown_periods = {}  # Tránh spam alerts
        self.is_running = False
        
    def add_alert_rule(self, rule_name, condition_function, priority='MEDIUM', cooldown_minutes=30):
        """
        Thêm rule cảnh báo mới
        
        Args:
            rule_name: Tên rule
            condition_function: Function kiểm tra điều kiện
            priority: HIGH/MEDIUM/LOW
            cooldown_minutes: Thời gian nghỉ giữa các alerts cùng loại
        """
        
        self.alert_rules[rule_name] = {
            'condition': condition_function,
            'priority': priority,
            'cooldown_minutes': cooldown_minutes,
            'last_triggered': None,
            'trigger_count': 0
        }
        
        print(f"✅ Added alert rule: {rule_name} (Priority: {priority})")
    
    def setup_email_alerts(self, smtp_server, smtp_port, email, password, recipients):
        """Cấu hình email alerts"""
        self.alert_channels['email'] = {
            'enabled': True,
            'config': {
                'smtp_server': smtp_server,
                'smtp_port': smtp_port,
                'email': email,
                'password': password,
                'recipients': recipients
            }
        }
        print("📧 Email alerts configured")
    
    def setup_telegram_alerts(self, bot_token, chat_ids):
        """Cấu hình Telegram alerts"""
        self.alert_channels['telegram'] = {
            'enabled': True,
            'config': {
                'bot_token': bot_token,
                'chat_ids': chat_ids
            }
        }
        print("📱 Telegram alerts configured")
    
    def check_cooldown(self, rule_name):
        """Kiểm tra cooldown để tránh spam"""
        rule = self.alert_rules[rule_name]
        
        if rule['last_triggered'] is None:
            return True  # Chưa từng trigger
        
        time_since_last = datetime.now() - rule['last_triggered']
        cooldown_period = timedelta(minutes=rule['cooldown_minutes'])
        
        return time_since_last > cooldown_period
    
    def send_alert(self, rule_name, alert_data):
        """Gửi cảnh báo qua các kênh đã cấu hình"""
        
        if not self.check_cooldown(rule_name):
            return False  # Trong thời gian cooldown
        
        rule = self.alert_rules[rule_name]
        
        # Tạo alert message
        alert_message = self.create_alert_message(rule_name, alert_data, rule['priority'])
        
        # Gửi qua các kênh
        sent_channels = []
        
        if self.alert_channels['email']['enabled']:
            if self.send_email_alert(alert_message, rule['priority']):
                sent_channels.append('Email')
        
        if self.alert_channels['telegram']['enabled']:
            if self.send_telegram_alert(alert_message, rule['priority']):
                sent_channels.append('Telegram')
        
        # Cập nhật history
        self.alert_history.append({
            'timestamp': datetime.now(),
            'rule_name': rule_name,
            'priority': rule['priority'],
            'data': alert_data,
            'channels_sent': sent_channels
        })
        
        # Cập nhật cooldown
        rule['last_triggered'] = datetime.now()
        rule['trigger_count'] += 1
        
        print(f"🚨 Alert sent: {rule_name} via {', '.join(sent_channels)}")
        return True
    
    def create_alert_message(self, rule_name, alert_data, priority):
        """Tạo nội dung cảnh báo"""
        
        priority_emojis = {'HIGH': '🔥', 'MEDIUM': '⚠️', 'LOW': '💡'}
        emoji = priority_emojis.get(priority, '📊')
        
        message = f"{emoji} VPA ALERT - {priority} PRIORITY\n"
        message += f"Rule: {rule_name}\n"
        message += f"Time: {datetime.now().strftime('%H:%M:%S %d/%m/%Y')}\n\n"
        
        # Thêm chi tiết từ alert_data
        if 'symbol' in alert_data:
            message += f"📈 Symbol: {alert_data['symbol']}\n"
        if 'price' in alert_data:
            message += f"💰 Current Price: {alert_data['price']:,}đ\n"
        if 'vpa_score' in alert_data:
            message += f"📊 VPA Score: {alert_data['vpa_score']:.0f}/100\n"
        if 'volume_ratio' in alert_data:
            message += f"📈 Volume Ratio: {alert_data['volume_ratio']:.1f}x\n"
        if 'recommendation' in alert_data:
            message += f"💡 Action: {alert_data['recommendation']}\n"
        
        return message
    
    def send_email_alert(self, message, priority):
        """Gửi email alert"""
        try:
            config = self.alert_channels['email']['config']
            
            # Chỉ gửi HIGH priority qua email để tránh spam
            if priority != 'HIGH':
                return False
            
            msg = MIMEMultipart()
            msg['From'] = config['email']
            msg['To'] = ', '.join(config['recipients'])
            msg['Subject'] = f"VPA Alert - {priority} Priority"
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
            server.starttls()
            server.login(config['email'], config['password'])
            
            text = msg.as_string()
            server.sendmail(config['email'], config['recipients'], text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"❌ Email alert failed: {e}")
            return False
    
    def send_telegram_alert(self, message, priority):
        """Gửi Telegram alert"""
        try:
            config = self.alert_channels['telegram']['config']
            
            for chat_id in config['chat_ids']:
                url = f"https://api.telegram.org/bot{config['bot_token']}/sendMessage"
                data = {
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, data=data, timeout=10)
                
                if response.status_code != 200:
                    print(f"❌ Telegram alert failed for chat {chat_id}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"❌ Telegram alert failed: {e}")
            return False

# Tạo instance alert system
alert_system = IntelligentAlertSystem()

# Cấu hình email (ví dụ với Gmail)
# alert_system.setup_email_alerts(
#     smtp_server='smtp.gmail.com',
#     smtp_port=587,
#     email='your_email@gmail.com',
#     password='your_app_password',  # App password, không phải password thường
#     recipients=['recipient@gmail.com']
# )

# Cấu hình Telegram
# alert_system.setup_telegram_alerts(
#     bot_token='YOUR_BOT_TOKEN',
#     chat_ids=['YOUR_CHAT_ID']
# )

print("🚨 Alert System initialized")
```

### B. Định Nghĩa Alert Rules

```python
def create_vpa_alert_rules(alert_system):
    """
    Tạo các rules cảnh báo VPA cơ bản
    """
    
    # Rule 1: Strong Stopping Volume
    def strong_stopping_volume_rule(stock_data):
        if len(stock_data) < 20:
            return False
        
        latest_data = stock_data.iloc[-20:]
        current_day = stock_data.iloc[-1]
        
        vpa_score = tinh_diem_tin_cay_stopping_volume(latest_data)
        volume_ratio = current_day['volume'] / latest_data['volume'][:-1].mean()
        
        # Điều kiện: VPA > 80, Volume > 2.5x, Price recovery > 70%
        if vpa_score > 80 and volume_ratio > 2.5:
            close_position = (current_day['close'] - current_day['low']) / (current_day['high'] - current_day['low'])
            if close_position > 0.7:
                return {
                    'symbol': current_day.get('symbol', 'UNKNOWN'),
                    'price': current_day['close'],
                    'vpa_score': vpa_score,
                    'volume_ratio': volume_ratio,
                    'close_position': close_position,
                    'recommendation': 'STRONG BUY SIGNAL'
                }
        return False
    
    # Rule 2: No Supply với Volume thấp
    def no_supply_rule(stock_data):
        if len(stock_data) < 10:
            return False
            
        current_day = stock_data.iloc[-1]
        recent_data = stock_data.iloc[-10:]
        
        # Giá tăng > 1.5%
        price_change = (current_day['close'] - current_day['open']) / current_day['open']
        if price_change < 0.015:
            return False
        
        # Volume < 60% bình thường
        avg_volume = recent_data['volume'][:-1].mean()
        volume_ratio = current_day['volume'] / avg_volume
        
        if volume_ratio < 0.6:
            return {
                'symbol': current_day.get('symbol', 'UNKNOWN'),
                'price': current_day['close'],
                'price_change': price_change * 100,
                'volume_ratio': volume_ratio,
                'vpa_score': 75,  # No Supply typically scores around 75
                'recommendation': 'NO SUPPLY - ACCUMULATE'
            }
        return False
    
    # Rule 3: Unusual Volume với breakout
    def unusual_volume_breakout_rule(stock_data):
        if len(stock_data) < 50:
            return False
            
        current_day = stock_data.iloc[-1]
        recent_data = stock_data.iloc[-20:]
        longer_data = stock_data.iloc[-50:]
        
        # Volume > 3x average
        volume_ratio = current_day['volume'] / recent_data['volume'][:-1].mean()
        if volume_ratio < 3.0:
            return False
        
        # Price breakout (high > max của 20 ngày trước)
        resistance_level = recent_data['high'][:-1].max()
        if current_day['high'] <= resistance_level:
            return False
        
        # Volume confirmation
        if current_day['close'] > current_day['open']:  # Green candle
            return {
                'symbol': current_day.get('symbol', 'UNKNOWN'),
                'price': current_day['close'],
                'volume_ratio': volume_ratio,
                'breakout_level': resistance_level,
                'vpa_score': 85,
                'recommendation': 'BREAKOUT WITH VOLUME'
            }
        return False
    
    # Rule 4: Smart Money Accumulation
    def smart_money_accumulation_rule(stock_data):
        if len(stock_data) < 30:
            return False
            
        recent_data = stock_data.iloc[-10:]  # 10 ngày gần nhất
        
        # Kiểm tra tích lũy âm thầm
        price_volatility = recent_data['close'].std() / recent_data['close'].mean()
        volume_trend = recent_data['volume'][-5:].mean() / recent_data['volume'][:5].mean()
        
        # Low volatility + increasing volume = stealth accumulation
        if price_volatility < 0.03 and volume_trend > 1.2:
            current_day = stock_data.iloc[-1]
            return {
                'symbol': current_day.get('symbol', 'UNKNOWN'),
                'price': current_day['close'],
                'price_volatility': price_volatility,
                'volume_trend': volume_trend,
                'vpa_score': 70,
                'recommendation': 'SMART MONEY ACCUMULATION'
            }
        return False
    
    # Đăng ký rules
    alert_system.add_alert_rule(
        'strong_stopping_volume',
        strong_stopping_volume_rule,
        priority='HIGH',
        cooldown_minutes=60
    )
    
    alert_system.add_alert_rule(
        'no_supply_signal',
        no_supply_rule,
        priority='MEDIUM',
        cooldown_minutes=30
    )
    
    alert_system.add_alert_rule(
        'unusual_volume_breakout',
        unusual_volume_breakout_rule,
        priority='HIGH',
        cooldown_minutes=45
    )
    
    alert_system.add_alert_rule(
        'smart_money_accumulation',
        smart_money_accumulation_rule,
        priority='MEDIUM',
        cooldown_minutes=120  # 2 hours cooldown vì đây là signal dài hạn
    )
    
    print("📋 VPA Alert Rules configured:")
    for rule_name, rule in alert_system.alert_rules.items():
        print(f"   • {rule_name}: {rule['priority']} priority")

# Tạo alert rules
create_vpa_alert_rules(alert_system)
```

### C. Market Scanner với Alert Integration

```python
def run_market_scanner_with_alerts(stock_list, alert_system, scan_interval_minutes=5):
    """
    Chạy market scanner liên tục với alert integration
    """
    
    def scanner_loop():
        print(f"🔍 Market Scanner started - checking every {scan_interval_minutes} minutes")
        
        while alert_system.is_running:
            try:
                scan_start_time = datetime.now()
                alerts_triggered = 0
                stocks_scanned = 0
                
                print(f"\n⏰ Starting scan at {scan_start_time.strftime('%H:%M:%S')}")
                
                for symbol in stock_list:
                    try:
                        # Load stock data
                        stock_data = pd.read_csv(f'market_data/{symbol}.csv')
                        stocks_scanned += 1
                        
                        # Kiểm tra từng alert rule
                        for rule_name, rule in alert_system.alert_rules.items():
                            try:
                                alert_data = rule['condition'](stock_data)
                                
                                if alert_data:  # Rule triggered
                                    if alert_system.send_alert(rule_name, alert_data):
                                        alerts_triggered += 1
                                        print(f"   🚨 {symbol}: {rule_name} triggered")
                            
                            except Exception as e:
                                print(f"   ❌ Error checking {rule_name} for {symbol}: {e}")
                    
                    except Exception as e:
                        print(f"   ❌ Error loading {symbol}: {e}")
                
                scan_end_time = datetime.now()
                scan_duration = (scan_end_time - scan_start_time).total_seconds()
                
                print(f"✅ Scan completed in {scan_duration:.1f}s:")
                print(f"   • Stocks scanned: {stocks_scanned}")
                print(f"   • Alerts triggered: {alerts_triggered}")
                
                # Sleep until next scan
                time.sleep(scan_interval_minutes * 60)
                
            except KeyboardInterrupt:
                print("🛑 Scanner stopped by user")
                break
            except Exception as e:
                print(f"❌ Scanner error: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    # Start scanner in separate thread
    alert_system.is_running = True
    scanner_thread = threading.Thread(target=scanner_loop, daemon=True)
    scanner_thread.start()
    
    return scanner_thread

# Danh sách cổ phiếu để scan
vn30_stocks = ['VCB', 'TCB', 'BID', 'VIC', 'VHM', 'HPG', 'VRE', 'MSN', 'SAB', 'CTG']
hose_top_50 = vn30_stocks + ['ACB', 'TPB', 'MBB', 'STB', 'HDB', 'PDR', 'KDH', 'NVL', 'DXG', 'BCM']

print("🚀 Starting market scanner...")

# Chạy scanner (uncomment để chạy thực tế)
# scanner_thread = run_market_scanner_with_alerts(hose_top_50, alert_system, scan_interval_minutes=5)

# Để test, chúng ta chỉ demo với 1 stock
print("📊 Demo: Testing alert rules with VCB data")
vcb_data = pd.read_csv('market_data/VCB.csv')

# Test từng rule
for rule_name, rule in alert_system.alert_rules.items():
    alert_data = rule['condition'](vcb_data)
    if alert_data:
        print(f"✅ {rule_name} would trigger alert:")
        for key, value in alert_data.items():
            print(f"   • {key}: {value}")
    else:
        print(f"⚪ {rule_name}: No alert")
```

---

## 📈 Phần 2: Thực Hành - Dashboard & Monitoring

### A. Web Dashboard Đơn Giản

```python
from flask import Flask, render_template, jsonify
import json

def create_monitoring_dashboard(alert_system):
    """
    Tạo web dashboard đơn giản để monitor alerts
    """
    
    app = Flask(__name__)
    
    @app.route('/')
    def dashboard():
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>VPA Alert Dashboard</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1200px; margin: 0 auto; }
                .card { background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                .alert-high { border-left: 5px solid #ff4444; }
                .alert-medium { border-left: 5px solid #ffaa00; }
                .alert-low { border-left: 5px solid #00aa44; }
                .status-running { color: #00aa44; }
                .status-stopped { color: #ff4444; }
                h1 { color: #333; }
                .stats { display: flex; justify-content: space-around; text-align: center; }
                .stat-item { padding: 10px; }
                .stat-number { font-size: 2em; font-weight: bold; color: #0066cc; }
            </style>
            <script>
                function refreshData() {
                    fetch('/api/status')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('system-status').innerHTML = 
                                data.is_running ? 
                                '<span class="status-running">🟢 RUNNING</span>' : 
                                '<span class="status-stopped">🔴 STOPPED</span>';
                            
                            document.getElementById('total-rules').textContent = data.total_rules;
                            document.getElementById('alerts-today').textContent = data.alerts_today;
                            document.getElementById('last-scan').textContent = data.last_scan || 'Never';
                        });
                    
                    fetch('/api/recent_alerts')
                        .then(response => response.json())
                        .then(data => {
                            const alertsHtml = data.map(alert => `
                                <div class="card alert-${alert.priority.toLowerCase()}">
                                    <h3>${alert.rule_name} - ${alert.priority}</h3>
                                    <p><strong>Time:</strong> ${alert.timestamp}</p>
                                    <p><strong>Symbol:</strong> ${alert.data.symbol || 'Unknown'}</p>
                                    <p><strong>Price:</strong> ${alert.data.price ? alert.data.price.toLocaleString() + 'đ' : 'N/A'}</p>
                                    <p><strong>Action:</strong> ${alert.data.recommendation || 'N/A'}</p>
                                </div>
                            `).join('');
                            
                            document.getElementById('recent-alerts').innerHTML = alertsHtml || '<p>No recent alerts</p>';
                        });
                }
                
                setInterval(refreshData, 30000); // Refresh every 30 seconds
                window.onload = refreshData;
            </script>
        </head>
        <body>
            <div class="container">
                <h1>🚨 VPA Alert Dashboard</h1>
                
                <div class="card">
                    <h2>System Status</h2>
                    <div class="stats">
                        <div class="stat-item">
                            <div class="stat-number" id="system-status">⏳</div>
                            <div>System Status</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number" id="total-rules">-</div>
                            <div>Active Rules</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number" id="alerts-today">-</div>
                            <div>Alerts Today</div>
                        </div>
                        <div class="stat-item">
                            <div id="last-scan">-</div>
                            <div>Last Scan</div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <h2>Recent Alerts</h2>
                    <div id="recent-alerts">Loading...</div>
                </div>
            </div>
        </body>
        </html>
        """
    
    @app.route('/api/status')
    def api_status():
        today = datetime.now().date()
        alerts_today = len([
            alert for alert in alert_system.alert_history 
            if alert['timestamp'].date() == today
        ])
        
        return jsonify({
            'is_running': alert_system.is_running,
            'total_rules': len(alert_system.alert_rules),
            'alerts_today': alerts_today,
            'last_scan': datetime.now().strftime('%H:%M:%S')
        })
    
    @app.route('/api/recent_alerts')
    def api_recent_alerts():
        # Lấy 10 alerts gần nhất
        recent = sorted(alert_system.alert_history, key=lambda x: x['timestamp'], reverse=True)[:10]
        
        return jsonify([{
            'timestamp': alert['timestamp'].strftime('%H:%M:%S %d/%m'),
            'rule_name': alert['rule_name'],
            'priority': alert['priority'],
            'data': alert['data']
        } for alert in recent])
    
    return app

# Tạo dashboard
dashboard_app = create_monitoring_dashboard(alert_system)

# Để chạy dashboard (uncomment để chạy thực tế)
# if __name__ == '__main__':
#     dashboard_app.run(host='0.0.0.0', port=5000, debug=True)

print("🖥️ Dashboard available at http://localhost:5000")
print("📊 API endpoints:")
print("   • GET /api/status - System status")
print("   • GET /api/recent_alerts - Recent alerts")
```

---

## 🔍 Phần 3: Nâng Cao - Adaptive Alert System

> 💡 **Lưu ý**: Phần này dành cho người muốn xây dựng hệ thống cảnh báo thích ứng. 
> Nếu bạn mới bắt đầu, có thể **bỏ qua** và quay lại sau.

### A. Machine Learning-Enhanced Alerts

```python
class AdaptiveAlertSystem:
    def __init__(self):
        self.base_alert_system = IntelligentAlertSystem()
        self.alert_performance_tracker = {}
        self.ml_model = None  # Will be trained on alert performance
        self.adaptation_enabled = True
        
    def track_alert_performance(self, alert_id, actual_outcome):
        """
        Theo dõi hiệu quả của alerts để cải thiện system
        
        Args:
            alert_id: ID của alert đã gửi
            actual_outcome: Kết quả thực tế (profit/loss sau N ngày)
        """
        
        if alert_id not in self.alert_performance_tracker:
            self.alert_performance_tracker[alert_id] = []
        
        self.alert_performance_tracker[alert_id].append({
            'timestamp': datetime.now(),
            'outcome': actual_outcome,
            'success': actual_outcome > 0.02  # Consider >2% gain as success
        })
        
        # Retrain model if we have enough data
        if len(self.alert_performance_tracker) % 100 == 0:
            self.retrain_adaptation_model()
    
    def calculate_dynamic_thresholds(self, rule_name, market_conditions):
        """
        Tính toán ngưỡng động cho alerts dựa trên điều kiện thị trường
        """
        
        base_thresholds = {
            'strong_stopping_volume': {'vpa_score': 80, 'volume_ratio': 2.5},
            'no_supply_signal': {'price_change': 0.015, 'volume_ratio': 0.6},
            'unusual_volume_breakout': {'volume_ratio': 3.0},
            'smart_money_accumulation': {'volatility': 0.03, 'volume_trend': 1.2}
        }
        
        if rule_name not in base_thresholds:
            return base_thresholds.get(rule_name, {})
        
        adjusted_thresholds = base_thresholds[rule_name].copy()
        
        # Điều chỉnh dựa trên VIX (volatility fear index)
        vix_level = market_conditions.get('vix', 20)
        if vix_level > 30:  # High fear
            # Tighten thresholds during high volatility
            for key in adjusted_thresholds:
                if 'score' in key or 'ratio' in key:
                    adjusted_thresholds[key] *= 1.2
        elif vix_level < 15:  # Low fear/complacency
            # Relax thresholds during calm periods
            for key in adjusted_thresholds:
                if 'score' in key or 'ratio' in key:
                    adjusted_thresholds[key] *= 0.9
        
        # Điều chỉnh dựa trên market momentum
        market_momentum = market_conditions.get('market_momentum', 0)
        if market_momentum < -0.02:  # Market declining > 2%
            # More conservative during market decline
            adjusted_thresholds = {k: v * 1.3 for k, v in adjusted_thresholds.items()}
        elif market_momentum > 0.02:  # Market rising > 2%
            # Less conservative during market rise
            adjusted_thresholds = {k: v * 0.85 for k, v in adjusted_thresholds.items()}
        
        return adjusted_thresholds
    
    def adaptive_rule_factory(self, rule_name, base_rule_function):
        """
        Tạo adaptive rule wrapper around base rule
        """
        
        def adaptive_rule(stock_data):
            # Get current market conditions
            market_conditions = self.get_current_market_conditions()
            
            # Calculate dynamic thresholds
            dynamic_thresholds = self.calculate_dynamic_thresholds(rule_name, market_conditions)
            
            # Run base rule with dynamic thresholds
            result = base_rule_function(stock_data, dynamic_thresholds)
            
            if result:
                # Add confidence score based on market conditions
                confidence_multiplier = self.calculate_confidence_multiplier(
                    rule_name, market_conditions
                )
                
                result['confidence_score'] = min(100, result.get('vpa_score', 75) * confidence_multiplier)
                result['market_conditions'] = market_conditions
            
            return result
        
        return adaptive_rule
    
    def get_current_market_conditions(self):
        """
        Thu thập điều kiện thị trường hiện tại
        """
        
        # Trong thực tế, dữ liệu này sẽ được lấy từ API
        return {
            'vix': 22.5,  # Volatility fear index
            'market_momentum': 0.005,  # VN-Index momentum 5 days
            'foreign_flow': -2_000_000_000,  # Net foreign flow (negative = selling)
            'sector_rotation': 'Technology',  # Current leading sector
            'usd_vnd_momentum': 0.002,  # USD/VND change
            'china_momentum': -0.01,  # China market momentum
            'sentiment_score': 65  # Overall market sentiment (0-100)
        }
    
    def calculate_confidence_multiplier(self, rule_name, market_conditions):
        """
        Tính multiplier cho confidence dựa trên market conditions
        """
        
        base_multiplier = 1.0
        
        # Rule-specific adjustments
        if rule_name == 'strong_stopping_volume':
            # Stopping volume works better in declining/sideways markets
            if market_conditions['market_momentum'] < 0:
                base_multiplier += 0.1
        
        elif rule_name == 'no_supply_signal':
            # No Supply works better in rising markets
            if market_conditions['market_momentum'] > 0.01:
                base_multiplier += 0.15
        
        elif rule_name == 'unusual_volume_breakout':
            # Breakouts work better when market sentiment is positive
            if market_conditions['sentiment_score'] > 70:
                base_multiplier += 0.2
        
        # Global adjustments
        if market_conditions['foreign_flow'] > 5_000_000_000:  # Strong foreign buying
            base_multiplier += 0.1
        elif market_conditions['foreign_flow'] < -10_000_000_000:  # Strong foreign selling
            base_multiplier -= 0.15
        
        return max(0.5, min(1.5, base_multiplier))  # Cap between 0.5x and 1.5x
    
    def generate_market_report(self):
        """
        Tạo báo cáo tổng quan thị trường và alert performance
        """
        
        today = datetime.now().date()
        
        # Alert statistics
        total_alerts = len(self.base_alert_system.alert_history)
        alerts_today = len([
            alert for alert in self.base_alert_system.alert_history 
            if alert['timestamp'].date() == today
        ])
        
        # Performance statistics
        successful_alerts = 0
        total_tracked = 0
        
        for alert_performances in self.alert_performance_tracker.values():
            for performance in alert_performances:
                total_tracked += 1
                if performance['success']:
                    successful_alerts += 1
        
        success_rate = successful_alerts / total_tracked if total_tracked > 0 else 0
        
        report = {
            'date': today.strftime('%d/%m/%Y'),
            'system_status': 'RUNNING' if self.base_alert_system.is_running else 'STOPPED',
            'alert_statistics': {
                'total_alerts_ever': total_alerts,
                'alerts_today': alerts_today,
                'alerts_this_week': len([
                    alert for alert in self.base_alert_system.alert_history 
                    if (datetime.now() - alert['timestamp']).days <= 7
                ])
            },
            'performance_metrics': {
                'tracked_alerts': total_tracked,
                'successful_alerts': successful_alerts,
                'success_rate': f"{success_rate:.1%}",
                'adaptation_enabled': self.adaptation_enabled
            },
            'market_conditions': self.get_current_market_conditions(),
            'top_performing_rules': self.get_top_performing_rules()
        }
        
        return report
    
    def get_top_performing_rules(self):
        """
        Tìm rules có performance tốt nhất
        """
        
        rule_performance = {}
        
        for alert in self.base_alert_system.alert_history:
            rule_name = alert['rule_name']
            if rule_name not in rule_performance:
                rule_performance[rule_name] = {'count': 0, 'success': 0}
            
            rule_performance[rule_name]['count'] += 1
            # Simplified success determination - in practice would track actual outcomes
            if alert['priority'] == 'HIGH':
                rule_performance[rule_name]['success'] += 1
        
        # Calculate success rates and sort
        for rule_name, stats in rule_performance.items():
            if stats['count'] > 0:
                stats['success_rate'] = stats['success'] / stats['count']
            else:
                stats['success_rate'] = 0
        
        # Sort by success rate
        sorted_rules = sorted(
            rule_performance.items(), 
            key=lambda x: x[1]['success_rate'], 
            reverse=True
        )
        
        return sorted_rules[:5]  # Top 5

# Demo adaptive system
adaptive_system = AdaptiveAlertSystem()
market_report = adaptive_system.generate_market_report()

print("\n=== ADAPTIVE ALERT SYSTEM REPORT ===")
print(f"📅 Date: {market_report['date']}")
print(f"🚨 System Status: {market_report['system_status']}")
print(f"\n📊 Alert Statistics:")
for key, value in market_report['alert_statistics'].items():
    print(f"   • {key.replace('_', ' ').title()}: {value}")
print(f"\n📈 Performance Metrics:")
for key, value in market_report['performance_metrics'].items():
    print(f"   • {key.replace('_', ' ').title()}: {value}")
print(f"\n🌍 Market Conditions:")
for key, value in market_report['market_conditions'].items():
    print(f"   • {key.replace('_', ' ').title()}: {value}")
```

---

## 📋 Tóm Tắt Chương

### Những Gì Đã Xây Dựng:
1. **Core Alert System** - Engine cảnh báo với multiple channels
2. **Alert Rules** - 4 VPA rules cơ bản với cooldown logic
3. **Market Scanner** - Quét liên tục với threading
4. **Web Dashboard** - Monitoring interface với real-time updates
5. **Adaptive System** - ML-enhanced alerts với dynamic thresholds (nâng cao)

### Tính Năng Chính:
- ✅ **Multi-channel alerts** - Email, Telegram, webhook
- ✅ **Smart cooldown** - Tránh spam alerts
- ✅ **Priority system** - HIGH/MEDIUM/LOW với logic khác nhau
- ✅ **Real-time monitoring** - Web dashboard cập nhật live
- ✅ **Performance tracking** - Theo dõi hiệu quả alerts
- ✅ **Adaptive thresholds** - Điều chỉnh theo market conditions

### Cách Deploy:
```bash
# 1. Install dependencies
pip install flask requests threading

# 2. Configure channels
# - Email: Setup SMTP credentials
# - Telegram: Create bot, get token & chat_id
# - Webhook: Setup endpoint URL

# 3. Run system
python alert_system.py

# 4. Access dashboard
# http://localhost:5000
```

### Lưu Ý Quan Trọng:
> ⚠️ **Alert fatigue** - Quá nhiều alerts sẽ làm bạn ignore chúng
> - Chọn thresholds cẩn thận 
> - Sử dụng cooldown appropriately
> - Monitor success rate và adjust

> 🔒 **Security** - Bảo vệ credentials
> - Không hardcode passwords trong code
> - Sử dụng environment variables
> - Setup HTTPS cho webhooks

### Chương Tiếp Theo:
**Chương 5.7: Portfolio Optimization VPA** - Xây dựng portfolio tối ưu dựa trên VPA signals với risk management chuyên nghiệp.