# Chương 5.4: Machine Learning cho VPA
## Dạy Máy Tính Nhận Diện Pattern VPA

### 🎯 Mục Tiêu Chương

Bạn đã biết cách nhận diện Stopping Volume, No Supply bằng mắt. Nhưng nếu có 100 cổ phiếu, liệu bạn có đủ thời gian kiểm tra hết? Chương này sẽ dạy máy tính làm việc đó cho bạn!

### 💡 Ý Tưởng Cốt Lõi

**"Dạy máy tính nhìn charts như một chuyên gia VPA"**

- Con người: Nhìn 1 chart mất 30 giây
- Máy tính: "Nhìn" 1000 charts trong 1 giây
- Kết quả: Tìm được cơ hội mà con người có thể bỏ lỡ

### 🤖 AI Sẽ Làm Gì Cho Bạn?

1. **Quét toàn thị trường** - Tự động kiểm tra 800+ cổ phiếu VN
2. **Phát hiện patterns** - Tìm Stopping Volume, No Supply, Springs...
3. **Xếp hạng cơ hội** - Đưa ra top 10 cổ phiếu đáng chú ý nhất
4. **Cảnh báo realtime** - Báo ngay khi có tín hiệu mạnh

---

## 📚 Phần 1: Cơ Bản - Dạy AI Nhận Diện VPA

### A. Chuẩn Bị Dữ Liệu Cho AI

```python
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def tao_features_cho_ai(data_co_phieu, so_ngay_lookback=20):
    """
    Tạo features (đặc trưng) từ dữ liệu giá để AI có thể học
    
    Features bao gồm:
    1. Volume features - Đặc trưng về khối lượng  
    2. Price features - Đặc trưng về giá
    3. Technical indicators - Các chỉ báo kỹ thuật
    """
    
    features_list = []
    
    for i in range(so_ngay_lookback, len(data_co_phieu)):
        window_data = data_co_phieu.iloc[i-so_ngay_lookback:i]
        current_day = data_co_phieu.iloc[i]
        
        # === VOLUME FEATURES ===
        volume_features = {
            # Khối lượng tương đối
            'volume_ratio_5d': current_day['volume'] / window_data['volume'][-5:].mean(),
            'volume_ratio_10d': current_day['volume'] / window_data['volume'][-10:].mean(),
            'volume_ratio_20d': current_day['volume'] / window_data['volume'][-20:].mean(),
            
            # Z-score khối lượng (đo mức độ bất thường)
            'volume_zscore': (current_day['volume'] - window_data['volume'].mean()) / window_data['volume'].std(),
            
            # Xu hướng khối lượng
            'volume_trend_5d': (window_data['volume'][-5:].mean() / window_data['volume'][-10:-5].mean()) - 1,
            
            # Volume ranking (khối lượng hôm nay xếp thứ mấy trong 20 ngày)
            'volume_percentile': (current_day['volume'] > window_data['volume']).sum() / len(window_data['volume'])
        }
        
        # === PRICE FEATURES ===
        price_features = {
            # Vị trí đóng cửa trong ngày
            'close_position_in_day': (current_day['close'] - current_day['low']) / (current_day['high'] - current_day['low']) if current_day['high'] != current_day['low'] else 0.5,
            
            # Biến động giá
            'daily_range': (current_day['high'] - current_day['low']) / current_day['close'],
            'price_change_1d': (current_day['close'] - window_data['close'].iloc[-2]) / window_data['close'].iloc[-2],
            'price_change_5d': (current_day['close'] - window_data['close'][-6]) / window_data['close'][-6],
            
            # Xu hướng giá
            'price_trend_5d': (window_data['close'][-5:].mean() / window_data['close'][-10:-5].mean()) - 1,
            'price_trend_20d': (window_data['close'][-10:].mean() / window_data['close'][:10].mean()) - 1,
        }
        
        # === TECHNICAL INDICATORS ===
        tech_features = {
            # RSI đơn giản
            'rsi_14': tinh_rsi_don_gian(window_data['close'], 14),
            
            # Moving averages
            'price_vs_ma5': current_day['close'] / window_data['close'][-5:].mean() - 1,
            'price_vs_ma10': current_day['close'] / window_data['close'][-10:].mean() - 1,
            'price_vs_ma20': current_day['close'] / window_data['close'].mean() - 1,
        }
        
        # === VPA-SPECIFIC FEATURES ===
        vpa_features = {
            # Stopping Volume indicators
            'stopping_volume_score': tinh_diem_tin_cay_stopping_volume_simple(window_data, current_day),
            
            # No Supply indicators
            'no_supply_likelihood': tinh_kha_nang_no_supply(window_data, current_day),
            
            # Volume-Price divergence
            'volume_price_correlation': tinh_tuong_quan_volume_price(window_data),
        }
        
        # Kết hợp tất cả features
        all_features = {**volume_features, **price_features, **tech_features, **vpa_features}
        all_features['date'] = current_day['date']
        all_features['symbol'] = current_day.get('symbol', 'UNKNOWN')
        
        features_list.append(all_features)
    
    return pd.DataFrame(features_list)

def tinh_rsi_don_gian(prices, period=14):
    """Tính RSI đơn giản"""
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    
    avg_gain = np.mean(gains[-period:]) if len(gains) >= period else np.mean(gains)
    avg_loss = np.mean(losses[-period:]) if len(losses) >= period else np.mean(losses)
    
    if avg_loss == 0:
        return 100
    else:
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

def tinh_diem_tin_cay_stopping_volume_simple(window_data, current_day):
    """Tính điểm Stopping Volume đơn giản cho AI"""
    volume_ratio = current_day['volume'] / window_data['volume'][:-1].mean()
    close_position = (current_day['close'] - current_day['low']) / (current_day['high'] - current_day['low']) if current_day['high'] != current_day['low'] else 0.5
    
    volume_score = min(volume_ratio * 20, 60)  # Tối đa 60 điểm
    close_score = close_position * 40          # Tối đa 40 điểm
    
    return volume_score + close_score

def tinh_kha_nang_no_supply(window_data, current_day):
    """Tính khả năng No Supply"""
    price_change = (current_day['close'] - current_day['open']) / current_day['open']
    volume_ratio = current_day['volume'] / window_data['volume'][:-1].mean()
    
    if price_change > 0.01 and volume_ratio < 0.8:  # Giá tăng > 1%, volume < 80% TB
        return min((price_change * 50) + ((0.8 - volume_ratio) * 100), 100)
    else:
        return 0

def tinh_tuong_quan_volume_price(window_data):
    """Tính tương quan giữa volume và price"""
    prices = window_data['close'].values
    volumes = window_data['volume'].values
    
    if len(prices) < 2:
        return 0
    
    correlation = np.corrcoef(prices, volumes)[0, 1]
    return correlation if not np.isnan(correlation) else 0
```

### B. Tạo Nhãn (Labels) Cho AI Học

```python
def tao_nhan_cho_ai(data_co_phieu, features_df, so_ngay_forward=5, nguong_loi_nhuan=0.02):
    """
    Tạo nhãn cho AI học:
    - 1: Tín hiệu TỐT (giá tăng > 2% trong 5 ngày)
    - 0: Tín hiệu XẤU (giá không tăng hoặc giảm)
    """
    
    labels = []
    
    for i, row in features_df.iterrows():
        # Tìm vị trí trong dữ liệu gốc
        current_date = row['date']
        current_idx = data_co_phieu[data_co_phieu['date'] == current_date].index[0]
        
        # Kiểm tra có đủ dữ liệu forward không
        if current_idx + so_ngay_forward < len(data_co_phieu):
            gia_hien_tai = data_co_phieu.iloc[current_idx]['close']
            gia_tuong_lai = data_co_phieu.iloc[current_idx + so_ngay_forward]['close']
            
            loi_nhuan = (gia_tuong_lai - gia_hien_tai) / gia_hien_tai
            
            # Gán nhãn
            if loi_nhuan >= nguong_loi_nhuan:
                nhan = 1  # Tín hiệu TỐT
            else:
                nhan = 0  # Tín hiệu XẤU
        else:
            nhan = -1  # Không đủ dữ liệu
        
        labels.append({
            'date': current_date,
            'label': nhan,
            'forward_return': loi_nhuan if nhan != -1 else None
        })
    
    return pd.DataFrame(labels)

# Sử dụng
vcb_data = pd.read_csv('market_data/VCB.csv')
vcb_features = tao_features_cho_ai(vcb_data)
vcb_labels = tao_nhan_cho_ai(vcb_data, vcb_features)

print("=== DỮ LIỆU ĐÃ CHUẨN BỊ CHO AI ===")
print(f"Số mẫu features: {len(vcb_features)}")
print(f"Số features: {len(vcb_features.columns) - 2}")  # Trừ date và symbol
print(f"Tỷ lệ tín hiệu TỐT: {(vcb_labels['label'] == 1).sum() / len(vcb_labels):.1%}")

# Hiển thị một vài features
print(f"\nVí dụ features:")
feature_columns = [col for col in vcb_features.columns if col not in ['date', 'symbol']]
print(vcb_features[feature_columns[:5]].head())
```

### C. Huấn Luyện AI Model Đầu Tiên

```python
def huan_luyen_ai_vpa_co_ban(features_df, labels_df):
    """
    Huấn luyện model AI đơn giản để nhận diện VPA patterns
    """
    
    # Kết hợp features và labels
    merged_data = pd.merge(features_df, labels_df, on='date')
    
    # Chỉ lấy những mẫu có label hợp lệ
    valid_data = merged_data[merged_data['label'] != -1].copy()
    
    # Chuẩn bị X (features) và y (labels)
    feature_columns = [col for col in features_df.columns if col not in ['date', 'symbol']]
    X = valid_data[feature_columns].fillna(0)  # Điền giá trị 0 cho missing values
    y = valid_data['label']
    
    # Chia train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Huấn luyện model Random Forest
    model = RandomForestClassifier(
        n_estimators=100,  # 100 cây quyết định
        max_depth=10,      # Độ sâu tối đa
        random_state=42,
        class_weight='balanced'  # Cân bằng tỷ lệ class
    )
    
    model.fit(X_train, y_train)
    
    # Đánh giá model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("=== KẾT QUẢ HUẤN LUYỆN AI ===")
    print(f"✅ Độ chính xác: {accuracy:.1%}")
    print(f"📊 Số mẫu training: {len(X_train)}")
    print(f"🧪 Số mẫu testing: {len(X_test)}")
    
    print(f"\n🔥 Top 5 features quan trọng nhất:")
    for i, row in feature_importance.head().iterrows():
        print(f"   {i+1}. {row['feature']}: {row['importance']:.3f}")
    
    # Báo cáo chi tiết
    print(f"\n📋 Báo cáo chi tiết:")
    print(classification_report(y_test, y_pred, target_names=['Tín hiệu XẤU', 'Tín hiệu TỐT']))
    
    return model, feature_columns, feature_importance

# Huấn luyện model
ai_model, feature_cols, importance_df = huan_luyen_ai_vpa_co_ban(vcb_features, vcb_labels)
```

---

## 📈 Phần 2: Thực Hành - Sử Dụng AI Để Quét Thị Trường

### A. Tạo Scanner Tự Động

```python
def ai_vpa_scanner(co_phieu_list, ai_model, feature_columns, top_n=10):
    """
    Quét toàn bộ danh sách cổ phiếu và tìm những cơ hội tốt nhất
    """
    
    ket_qua_scan = []
    
    for symbol in co_phieu_list:
        try:
            # Tải dữ liệu cổ phiếu
            data = pd.read_csv(f'market_data/{symbol}.csv')
            
            # Tạo features cho ngày gần nhất
            features = tao_features_cho_ai(data)
            if len(features) == 0:
                continue
                
            # Lấy features ngày cuối cùng
            latest_features = features.iloc[-1]
            X_latest = latest_features[feature_columns].values.reshape(1, -1)
            
            # Dự đoán bằng AI
            prediction = ai_model.predict(X_latest)[0]
            prediction_proba = ai_model.predict_proba(X_latest)[0]
            
            # Nếu AI dự đoán là tín hiệu TỐT
            if prediction == 1:
                ket_qua_scan.append({
                    'symbol': symbol,
                    'date': latest_features['date'],
                    'ai_prediction': 'TỐT',
                    'confidence': prediction_proba[1] * 100,  # Xác suất là tín hiệu tốt
                    'current_price': data.iloc[-1]['close'],
                    'volume_ratio': latest_features.get('volume_ratio_20d', 0),
                    'stopping_volume_score': latest_features.get('stopping_volume_score', 0),
                    'no_supply_score': latest_features.get('no_supply_likelihood', 0),
                })
        
        except Exception as e:
            print(f"⚠️ Lỗi khi xử lý {symbol}: {e}")
            continue
    
    # Sắp xếp theo confidence giảm dần
    ket_qua_scan.sort(key=lambda x: x['confidence'], reverse=True)
    
    print(f"=== AI VPA SCANNER RESULTS ===")
    print(f"🔍 Đã quét: {len(co_phieu_list)} cổ phiếu")
    print(f"✅ Tìm thấy: {len(ket_qua_scan)} cơ hội")
    
    print(f"\n🏆 TOP {min(top_n, len(ket_qua_scan))} CỔ PHIẾU ĐÁNG CHÚ Ý:")
    for i, result in enumerate(ket_qua_scan[:top_n]):
        print(f"\n   {i+1}. {result['symbol']} - Tin cậy: {result['confidence']:.1f}%")
        print(f"      💰 Giá hiện tại: {result['current_price']:,}đ")
        print(f"      📊 Volume ratio: {result['volume_ratio']:.1f}x")
        print(f"      ⚡ Stopping Volume: {result['stopping_volume_score']:.0f}/100")
        print(f"      🔥 No Supply: {result['no_supply_score']:.0f}/100")
    
    return ket_qua_scan

# Danh sách cổ phiếu để quét (ví dụ)
co_phieu_vn30 = ['VCB', 'TCB', 'BID', 'VIC', 'VHM', 'HPG', 'VRE', 'MSN', 'SAB', 'CTG']

# Chạy scanner
scan_results = ai_vpa_scanner(co_phieu_vn30, ai_model, feature_cols, top_n=5)
```

### B. Backtesting AI Model

```python
def backtest_ai_model(ai_model, feature_columns, test_data, so_ngay_giu=5):
    """
    Kiểm tra hiệu quả của AI model với dữ liệu lịch sử
    """
    
    giao_dich_list = []
    
    # Tạo features cho toàn bộ dữ liệu test
    features_test = tao_features_cho_ai(test_data)
    
    for i in range(len(features_test) - so_ngay_giu):
        current_features = features_test.iloc[i]
        X_current = current_features[feature_columns].values.reshape(1, -1)
        
        # AI dự đoán
        prediction = ai_model.predict(X_current)[0]
        confidence = ai_model.predict_proba(X_current)[0][1]
        
        # Chỉ giao dịch khi AI tin tưởng > 70%
        if prediction == 1 and confidence > 0.7:
            # Tìm giá mua/bán
            ngay_mua_idx = test_data[test_data['date'] == current_features['date']].index[0]
            ngay_ban_idx = ngay_mua_idx + so_ngay_giu
            
            if ngay_ban_idx < len(test_data):
                gia_mua = test_data.iloc[ngay_mua_idx]['close']
                gia_ban = test_data.iloc[ngay_ban_idx]['close']
                
                loi_nhuan = (gia_ban - gia_mua) / gia_mua
                
                giao_dich_list.append({
                    'ngay_mua': current_features['date'],
                    'gia_mua': gia_mua,
                    'ngay_ban': test_data.iloc[ngay_ban_idx]['date'],
                    'gia_ban': gia_ban,
                    'loi_nhuan': loi_nhuan,
                    'ai_confidence': confidence
                })
    
    # Phân tích kết quả
    if giao_dich_list:
        loi_nhuan_list = [gd['loi_nhuan'] for gd in giao_dich_list]
        
        tong_gd = len(giao_dich_list)
        gd_thang = sum(1 for ln in loi_nhuan_list if ln > 0)
        ty_le_thang = gd_thang / tong_gd
        loi_nhuan_tb = np.mean(loi_nhuan_list)
        loi_nhuan_tong = sum(loi_nhuan_list)
        
        print("=== KẾT QUẢ BACKTEST AI MODEL ===")
        print(f"🤖 AI Model Performance:")
        print(f"   • Tổng giao dịch: {tong_gd}")
        print(f"   • Giao dịch thắng: {gd_thang}")
        print(f"   • Tỷ lệ thắng: {ty_le_thang:.1%}")
        print(f"   • Lợi nhuận trung bình: {loi_nhuan_tb:.2%}")
        print(f"   • Tổng lợi nhuận: {loi_nhuan_tong:.2%}")
        
        # So sánh với benchmark
        gia_dau = test_data.iloc[0]['close']
        gia_cuoi = test_data.iloc[-1]['close']
        benchmark_return = (gia_cuoi - gia_dau) / gia_dau
        
        print(f"\n📊 So sánh với Buy & Hold:")
        print(f"   • Buy & Hold return: {benchmark_return:.2%}")
        print(f"   • AI Model return: {loi_nhuan_tong:.2%}")
        print(f"   • Outperformance: {loi_nhuan_tong - benchmark_return:.2%}")
        
        return {
            'total_trades': tong_gd,
            'win_rate': ty_le_thang,
            'avg_return': loi_nhuan_tb,
            'total_return': loi_nhuan_tong,
            'outperformance': loi_nhuan_tong - benchmark_return
        }
    
    return None

# Backtest AI model với dữ liệu VCB
backtest_results = backtest_ai_model(ai_model, feature_cols, vcb_data)
```

---

## 🔍 Phần 3: Nâng Cao - Deep Learning VPA

> 💡 **Lưu ý**: Phần này dành cho người muốn tìm hiểu về Deep Learning. 
> Nếu bạn mới bắt đầu với AI, có thể **bỏ qua** và quay lại sau.

### A. CNN Để Nhận Diện Các Mẫu Biểu Đồ

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

def tao_hinh_anh_bieu_do_cho_cnn(du_lieu_co_phieu, kich_thuoc_cua_so=50, kich_thuoc_hinh=(64, 64)):
    """
    Chuyển đổi dữ liệu OHLCV thành hình ảnh để CNN có thể học
    """
    
    hinh_anh_bieu_do = []
    nhan = []
    
    for i in range(kich_thuoc_cua_so, len(du_lieu_co_phieu) - 5):  # -5 để có lợi nhuận tương lai
        # Lấy dữ liệu cửa sổ
        du_lieu_cua_so = du_lieu_co_phieu.iloc[i-kich_thuoc_cua_so:i]
        
        # Tạo hình ảnh biểu đồ (đơn giản hóa)
        hinh_anh_bieu_do_item = tao_ma_tran_hinh_nen(du_lieu_cua_so, kich_thuoc_hinh)
        
        # Tính lợi nhuận tương lai để làm nhãn
        gia_hien_tai = du_lieu_co_phieu.iloc[i]['close']
        gia_tuong_lai = du_lieu_co_phieu.iloc[i+5]['close']
        loi_nhuan_tuong_lai = (gia_tuong_lai - gia_hien_tai) / gia_hien_tai
        
        # Nhãn nhị phân: 1 nếu lợi nhuận > 2%, 0 nếu không
        nhan_item = 1 if loi_nhuan_tuong_lai > 0.02 else 0
        
        hinh_anh_bieu_do.append(hinh_anh_bieu_do_item)
        nhan.append(nhan_item)
    
    return np.array(hinh_anh_bieu_do), np.array(nhan)

def tao_ma_tran_hinh_nen(du_lieu_cua_so, kich_thuoc_hinh):
    """
    Tạo ma trận hình ảnh từ dữ liệu candlestick
    """
    chieu_cao, chieu_rong = kich_thuoc_hinh
    ma_tran_hinh = np.zeros((chieu_cao, chieu_rong, 3))  # Các kênh RGB
    
    # Chuẩn hóa dữ liệu giá về [0, 1]
    gia_min = du_lieu_cua_so[['open', 'high', 'low', 'close']].min().min()
    gia_max = du_lieu_cua_so[['open', 'high', 'low', 'close']].max().max()
    
    khoi_luong_min = du_lieu_cua_so['volume'].min()
    khoi_luong_max = du_lieu_cua_so['volume'].max()
    
    for i, (_, ngay) in enumerate(du_lieu_cua_so.iterrows()):
        if i >= chieu_rong:  # Không vượt quá chiều rộng của hình
            break
            
        # Chuẩn hóa giá
        mo_norm = (ngay['open'] - gia_min) / (gia_max - gia_min)
        cao_norm = (ngay['high'] - gia_min) / (gia_max - gia_min)
        thap_norm = (ngay['low'] - gia_min) / (gia_max - gia_min)
        dong_norm = (ngay['close'] - gia_min) / (gia_max - gia_min)
        khoi_luong_norm = (ngay['volume'] - khoi_luong_min) / (khoi_luong_max - khoi_luong_min)
        
        # Chuyển về toạ độ pixel
        mo_y = int((1 - mo_norm) * (chieu_cao - 1))
        cao_y = int((1 - cao_norm) * (chieu_cao - 1))
        thap_y = int((1 - thap_norm) * (chieu_cao - 1))
        dong_y = int((1 - dong_norm) * (chieu_cao - 1))
        
        # Vẽ nến
        # Kênh đỏ: Hành động giá
        for y in range(min(cao_y, thap_y), max(cao_y, thap_y) + 1):
            ma_tran_hinh[y, i, 0] = 0.5  # Đường cao-thấp
        
        # Thân của nến
        than_bat_dau = min(mo_y, dong_y)
        than_ket_thuc = max(mo_y, dong_y)
        
        if dong_norm > mo_norm:  # Nến xanh
            ma_tran_hinh[than_bat_dau:than_ket_thuc+1, i, 1] = 1.0  # Kênh xanh
        else:  # Nến đỏ
            ma_tran_hinh[than_bat_dau:than_ket_thuc+1, i, 0] = 1.0  # Kênh đỏ
        
        # Kênh xanh dương: Khối lượng
        chieu_cao_khoi_luong = int(khoi_luong_norm * chieu_cao * 0.3)  # Cột khối lượng ở dưới
        if chieu_cao_khoi_luong > 0:
            ma_tran_hinh[-chieu_cao_khoi_luong:, i, 2] = khoi_luong_norm
    
    return ma_tran_hinh

def tao_mo_hinh_cnn(hinh_dang_dau_vao):
    """
    Tạo mô hình CNN để nhận diện các mẫu VPA từ hình ảnh biểu đồ
    """
    
    mo_hinh = keras.Sequential([
        # Các lớp tích chập
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=hinh_dang_dau_vao),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        
        # Các lớp dày đặc
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(1, activation='sigmoid')  # Binary classification
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# Chuẩn bị dữ liệu và training CNN (ví dụ conceptual)
# Trong thực tế cần nhiều dữ liệu hơn
print("=== DEEP LEARNING VPA - CNN APPROACH ===")
print("💡 Đây là ví dụ conceptual. Trong thực tế cần:")
print("   • Nhiều dữ liệu hơn (1000+ cổ phiếu)")
print("   • GPU để training nhanh")
print("   • Fine-tuning nhiều parameters")
print("   • Data augmentation techniques")

# X_images, y_labels = tao_chart_images_cho_cnn(vcb_data)
# cnn_model = tao_cnn_model((64, 64, 3))
# cnn_model.fit(X_images, y_labels, epochs=50, validation_split=0.2)
```

---

> 🔥 **PHẦN NÂNG CAO - CÓ THỂ BỎ QUA NẾU MỚI BẮT ĐẦU**

<details>
<summary>📋 <strong>Advanced ML Pipeline - Production Ready System</strong></summary>

```python
class ProductionVPAMLSystem:
    def __init__(self):
        self.models = {
            'random_forest': None,
            'gradient_boosting': None,
            'neural_network': None,
            'ensemble': None
        }
        
        self.feature_pipeline = None
        self.scaler = None
        self.feature_selector = None
        
    def create_advanced_features(self, stock_data, lookback_period=50):
        """
        Tạo features nâng cao cho production system
        """
        
        advanced_features = []
        
        for i in range(lookback_period, len(stock_data)):
            window_data = stock_data.iloc[i-lookback_period:i]
            current_day = stock_data.iloc[i]
            
            # Advanced Volume Features
            volume_features = self._extract_volume_features(window_data, current_day)
            
            # Advanced Price Action Features
            price_features = self._extract_price_action_features(window_data, current_day)
            
            # Market Microstructure Features
            microstructure_features = self._extract_microstructure_features(window_data, current_day)
            
            # Time Series Features
            time_series_features = self._extract_time_series_features(window_data)
            
            # VPA Specific Features
            vpa_features = self._extract_advanced_vpa_features(window_data, current_day)
            
            # Combine all features
            combined_features = {
                **volume_features,
                **price_features,
                **microstructure_features,
                **time_series_features,
                **vpa_features,
                'date': current_day['date'],
                'symbol': current_day.get('symbol', 'UNKNOWN')
            }
            
            advanced_features.append(combined_features)
        
        return pd.DataFrame(advanced_features)
    
    def _extract_volume_features(self, window_data, current_day):
        """Extract advanced volume-based features"""
        volumes = window_data['volume'].values
        prices = window_data['close'].values
        
        return {
            # Volume Distribution
            'volume_skewness': self._calculate_skewness(volumes),
            'volume_kurtosis': self._calculate_kurtosis(volumes),
            
            # Volume Persistence
            'volume_autocorr_1': self._calculate_autocorr(volumes, lag=1),
            'volume_autocorr_5': self._calculate_autocorr(volumes, lag=5),
            
            # Volume-Price Relationship
            'volume_price_elasticity': self._calculate_price_volume_elasticity(prices, volumes),
            'volume_weighted_price': np.average(prices, weights=volumes),
            
            # Volume Clustering
            'volume_cluster_strength': self._calculate_volume_clustering(volumes),
            
            # Abnormal Volume Detection
            'volume_anomaly_score': self._detect_volume_anomalies(volumes, current_day['volume']),
        }
    
    def _extract_price_action_features(self, window_data, current_day):
        """Extract advanced price action features"""
        opens = window_data['open'].values
        highs = window_data['high'].values
        lows = window_data['low'].values  
        closes = window_data['close'].values
        
        return {
            # Candlestick Patterns
            'doji_strength': self._calculate_doji_strength(opens, closes, highs, lows),
            'hammer_strength': self._calculate_hammer_strength(opens, closes, highs, lows),
            'engulfing_pattern': self._detect_engulfing_pattern(opens, closes),
            
            # Price Level Analysis
            'support_resistance_strength': self._calculate_sr_strength(highs, lows, closes),
            'breakout_strength': self._calculate_breakout_strength(highs, lows, closes),
            
            # Gap Analysis
            'gap_frequency': self._calculate_gap_frequency(opens, closes),
            'gap_fill_ratio': self._calculate_gap_fill_ratio(opens, closes, highs, lows),
            
            # Intraday Patterns
            'intraday_reversal_tendency': self._calculate_intraday_reversal(opens, closes, highs, lows),
            'closing_strength': self._calculate_closing_strength(opens, closes, highs, lows),
        }
    
    def _extract_microstructure_features(self, window_data, current_day):
        """Extract market microstructure features"""
        
        return {
            # Bid-Ask Spread Proxy (using high-low)
            'effective_spread_proxy': self._calculate_effective_spread_proxy(window_data),
            
            # Order Flow Imbalance Proxy
            'order_imbalance_proxy': self._calculate_order_imbalance_proxy(window_data),
            
            # Price Impact
            'price_impact_ratio': self._calculate_price_impact_ratio(window_data),
            
            # Liquidity Measures
            'liquidity_ratio': self._calculate_liquidity_ratio(window_data),
            'depth_proxy': self._calculate_market_depth_proxy(window_data),
        }
    
    def train_ensemble_model(self, X_train, y_train, X_val, y_val):
        """
        Train ensemble of multiple ML models
        """
        from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
        from sklearn.neural_network import MLPClassifier
        from sklearn.ensemble import VotingClassifier
        
        # Individual models
        rf_model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            random_state=42
        )
        
        gb_model = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=8,
            random_state=42
        )
        
        nn_model = MLPClassifier(
            hidden_layer_sizes=(100, 50, 25),
            activation='relu',
            solver='adam',
            alpha=0.001,
            batch_size='auto',
            learning_rate='constant',
            learning_rate_init=0.001,
            max_iter=500,
            random_state=42
        )
        
        # Ensemble model
        ensemble_model = VotingClassifier(
            estimators=[
                ('rf', rf_model),
                ('gb', gb_model),
                ('nn', nn_model)
            ],
            voting='soft'
        )
        
        # Train models
        print("Training Random Forest...")
        rf_model.fit(X_train, y_train)
        self.models['random_forest'] = rf_model
        
        print("Training Gradient Boosting...")
        gb_model.fit(X_train, y_train)
        self.models['gradient_boosting'] = gb_model
        
        print("Training Neural Network...")
        nn_model.fit(X_train, y_train)
        self.models['neural_network'] = nn_model
        
        print("Training Ensemble...")
        ensemble_model.fit(X_train, y_train)
        self.models['ensemble'] = ensemble_model
        
        # Evaluate models
        self._evaluate_models(X_val, y_val)
        
        return self.models
    
    def _evaluate_models(self, X_val, y_val):
        """Evaluate all trained models"""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        
        print("\n=== MODEL EVALUATION ===")
        
        for model_name, model in self.models.items():
            if model is not None:
                y_pred = model.predict(X_val)
                
                accuracy = accuracy_score(y_val, y_pred)
                precision = precision_score(y_val, y_pred, average='weighted')
                recall = recall_score(y_val, y_pred, average='weighted')
                f1 = f1_score(y_val, y_pred, average='weighted')
                
                print(f"\n{model_name.upper()}:")
                print(f"   Accuracy:  {accuracy:.3f}")
                print(f"   Precision: {precision:.3f}")
                print(f"   Recall:    {recall:.3f}")
                print(f"   F1-Score:  {f1:.3f}")
    
    def real_time_prediction_pipeline(self, current_stock_data):
        """
        Real-time prediction pipeline for production use
        """
        
        # Feature extraction
        features = self.create_advanced_features(current_stock_data)
        if len(features) == 0:
            return None
        
        # Get latest features
        latest_features = features.iloc[-1]
        feature_columns = [col for col in features.columns if col not in ['date', 'symbol']]
        X_latest = latest_features[feature_columns].values.reshape(1, -1)
        
        # Feature preprocessing
        if self.scaler:
            X_latest = self.scaler.transform(X_latest)
        
        if self.feature_selector:
            X_latest = self.feature_selector.transform(X_latest)
        
        # Predictions from all models
        predictions = {}
        confidences = {}
        
        for model_name, model in self.models.items():
            if model is not None:
                pred = model.predict(X_latest)[0]
                pred_proba = model.predict_proba(X_latest)[0]
                
                predictions[model_name] = pred
                confidences[model_name] = pred_proba[1] if pred == 1 else pred_proba[0]
        
        # Ensemble decision
        ensemble_pred = predictions.get('ensemble', 0)
        ensemble_confidence = confidences.get('ensemble', 0.5)
        
        # Risk assessment
        risk_level = self._assess_prediction_risk(predictions, confidences)
        
        return {
            'symbol': latest_features.get('symbol', 'UNKNOWN'),
            'date': latest_features['date'],
            'predictions': predictions,
            'confidences': confidences,
            'ensemble_prediction': ensemble_pred,
            'ensemble_confidence': ensemble_confidence,
            'risk_level': risk_level,
            'recommendation': self._generate_recommendation(ensemble_pred, ensemble_confidence, risk_level)
        }
    
    def _assess_prediction_risk(self, predictions, confidences):
        """Assess the risk level of predictions"""
        
        # Check prediction consensus
        pred_values = list(predictions.values())
        consensus = len(set(pred_values)) == 1  # All models agree
        
        # Check confidence levels
        avg_confidence = np.mean(list(confidences.values()))
        
        if consensus and avg_confidence > 0.8:
            return "LOW"
        elif consensus and avg_confidence > 0.6:
            return "MEDIUM"
        elif not consensus and avg_confidence > 0.7:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def _generate_recommendation(self, prediction, confidence, risk_level):
        """Generate trading recommendation"""
        
        if prediction == 1 and confidence > 0.75 and risk_level in ["LOW", "MEDIUM"]:
            return "STRONG BUY"
        elif prediction == 1 and confidence > 0.6:
            return "BUY"
        elif prediction == 1 and confidence > 0.5:
            return "WEAK BUY"
        elif prediction == 0 and confidence > 0.75:
            return "AVOID"
        else:
            return "NEUTRAL"
    
    # Helper methods for advanced feature extraction
    def _calculate_skewness(self, data):
        from scipy.stats import skew
        return skew(data)
    
    def _calculate_kurtosis(self, data):
        from scipy.stats import kurtosis
        return kurtosis(data)
    
    def _calculate_autocorr(self, data, lag):
        if len(data) <= lag:
            return 0
        return np.corrcoef(data[:-lag], data[lag:])[0, 1] if not np.isnan(np.corrcoef(data[:-lag], data[lag:])[0, 1]) else 0
    
    # ... other helper methods would be implemented here
    
    def save_models(self, filepath):
        """Save trained models to disk"""
        import joblib
        joblib.dump(self.models, filepath)
        print(f"Models saved to {filepath}")
    
    def load_models(self, filepath):
        """Load trained models from disk"""
        import joblib
        self.models = joblib.load(filepath)
        print(f"Models loaded from {filepath}")

# Usage example
# production_system = ProductionVPAMLSystem()
# models = production_system.train_ensemble_model(X_train, y_train, X_val, y_val)
# prediction_result = production_system.real_time_prediction_pipeline(current_stock_data)
```

</details>

---

## 📋 Tóm Tắt Chương

### Những Gì Đã Học:
1. **Chuẩn bị dữ liệu cho AI** - Features, labels, preprocessing
2. **Huấn luyện AI model** - Random Forest để nhận diện VPA
3. **AI Scanner tự động** - Quét toàn thị trường tìm cơ hội
4. **Backtesting AI** - Kiểm tra hiệu quả model
5. **Deep Learning CNN** - Nhận diện patterns từ chart images (nâng cao)
6. **Production System** - Hệ thống ML hoàn chỉnh (nâng cao)

### Lợi Ích Thiết Thực:
- ✅ **Tiết kiệm thời gian** - AI quét 1000 cổ phiếu trong vài giây
- ✅ **Không bỏ sót cơ hội** - Máy tính không mệt mỏi, không cảm xúc
- ✅ **Khách quan** - Quyết định dựa trên dữ liệu, không subjective
- ✅ **Scalable** - Có thể mở rộng cho toàn bộ thị trường VN
- ✅ **24/7 Monitoring** - Theo dõi liên tục, cảnh báo realtime

### Cảnh Báo Quan Trọng:
> ⚠️ **AI chỉ là công cụ hỗ trợ, không phải thay thế cho kiến thức VPA**
> - AI có thể nhầm trong những tình huống bất thường
> - Luôn kết hợp AI prediction với phân tích thủ công
> - Backtest tốt không đảm bảo tương lai sẽ tốt

### Chương Tiếp Theo:
**Chương 5.5: Phân Tích Đa Thị Trường** - Kết hợp VPA Việt Nam với thị trường toàn cầu để đưa ra quyết định tốt hơn.