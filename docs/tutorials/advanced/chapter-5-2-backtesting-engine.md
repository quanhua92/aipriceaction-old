# Chương 5.2: Kiểm Tra Chiến Lược - Backtesting Chuyên Nghiệp
## Làm Sao Biết Chiến Lược Có Thực Sự Hiệu Quả?

### 🎯 Mục Tiêu Chương

Bạn đã có tín hiệu VPA với điểm tin cậy. Nhưng làm sao biết chúng có thực sự kiếm được tiền trong quá khứ? Chương này sẽ dạy bạn cách **kiểm tra lịch sử** một cách khoa học.

### 💡 Câu Hỏi Cốt Lõi

**"Nếu tôi theo chiến lược này từ đầu năm, tôi sẽ lãi/lỗ bao nhiều?"**

- Thay vì đoán → **Tính toán chính xác**
- Thay vì hy vọng → **Dựa trên dữ liệu lịch sử**
- Thay vì rủi ro mù quáng → **Biết trước mức độ rủi ro**

---

## 📚 Phần 1: Cơ Bản - Backtesting Đơn Giản

### A. Backtesting Là Gì?

**Định nghĩa đơn giản:**
Backtesting = Áp dụng chiến lược lên dữ liệu quá khứ để xem kết quả

**Ví dụ thực tế:**
```
Chiến lược: "Mua khi VCB có Stopping Volume điểm > 70"

Kiểm tra năm 2024:
- 15/03/2024: VCB có tín hiệu 75 điểm → Mua 85,000đ
- 20/03/2024: Bán sau 5 ngày → 87,500đ (+2.9%)
- 08/05/2024: VCB có tín hiệu 82 điểm → Mua 82,000đ  
- 15/05/2024: Bán sau 5 ngày → 83,200đ (+1.5%)
...

Kết quả cuối năm: 25 giao dịch, 16 thắng, 9 thua, lãi 12.3%
```

### B. Backtesting Cơ Bản Với Python

```python
def backtest_don_gian(data_co_phieu, chien_luoc_mua, so_ngay_giu=5):
    """
    Kiểm tra chiến lược đơn giản: mua tín hiệu VPA, giữ N ngày rồi bán
    """
    ket_qua = []
    
    for i in range(len(data_co_phieu) - so_ngay_giu):
        ngay_hien_tai = data_co_phieu.iloc[i]
        
        # Kiểm tra có tín hiệu mua không
        if chien_luoc_mua(data_co_phieu[:i+1]):
            gia_mua = ngay_hien_tai['close']
            
            # Bán sau N ngày
            ngay_ban = data_co_phieu.iloc[i + so_ngay_giu]
            gia_ban = ngay_ban['close']
            
            loi_nhuan = (gia_ban - gia_mua) / gia_mua
            
            ket_qua.append({
                'ngay_mua': ngay_hien_tai['date'],
                'gia_mua': gia_mua,
                'ngay_ban': ngay_ban['date'], 
                'gia_ban': gia_ban,
                'loi_nhuan_phan_tram': loi_nhuan * 100
            })
    
    return ket_qua

# Áp dụng với chiến lược Stopping Volume
def chien_luoc_stopping_volume(data):
    diem = tinh_diem_tin_cay_stopping_volume(data)
    return diem > 70  # Chỉ mua khi điểm > 70

# Kiểm tra với dữ liệu VCB
vcb_data = pd.read_csv('market_data/VCB.csv')
ket_qua_backtest = backtest_don_gian(vcb_data, chien_luoc_stopping_volume)

print(f"=== KẾT QUẢ BACKTEST VCB - STOPPING VOLUME ===")
print(f"Tổng số giao dịch: {len(ket_qua_backtest)}")

if ket_qua_backtest:
    loi_nhuan_list = [gd['loi_nhuan_phan_tram'] for gd in ket_qua_backtest]
    so_thang = sum(1 for ln in loi_nhuan_list if ln > 0)
    
    print(f"Số giao dịch thắng: {so_thang}")
    print(f"Tỷ lệ thắng: {so_thang/len(ket_qua_backtest):.1%}")
    print(f"Lợi nhuận trung bình: {np.mean(loi_nhuan_list):.2f}%")
    print(f"Lợi nhuận tổng: {sum(loi_nhuan_list):.2f}%")
```

### C. Ví Dụ Thực Tế: Backtesting VCB 2024

```python
# Dữ liệu thực tế VCB 2024 (mô phỏng)
ket_qua_vcb_2024 = [
    {'ngay_mua': '2024-03-15', 'gia_mua': 85000, 'gia_ban': 87500, 'loi_nhuan_phan_tram': 2.9},
    {'ngay_mua': '2024-05-08', 'gia_mua': 82000, 'gia_ban': 83200, 'loi_nhuan_phan_tram': 1.5},
    {'ngay_mua': '2024-07-22', 'gia_mua': 89000, 'gia_ban': 86500, 'loi_nhuan_phan_tram': -2.8},
    {'ngay_mua': '2024-09-11', 'gia_mua': 91000, 'gia_ban': 94200, 'loi_nhuan_phan_tram': 3.5},
    {'ngay_mua': '2024-11-05', 'gia_mua': 88500, 'gia_ban': 89800, 'loi_nhuan_phan_tram': 1.5}
]

# Phân tích kết quả
tong_giao_dich = len(ket_qua_vcb_2024)
giao_dich_thang = sum(1 for kq in ket_qua_vcb_2024 if kq['loi_nhuan_phan_tram'] > 0)
ty_le_thang = giao_dich_thang / tong_giao_dich
loi_nhuan_tb = np.mean([kq['loi_nhuan_phan_tram'] for kq in ket_qua_vcb_2024])

print(f"📊 Kết quả VCB 2024:")
print(f"• Tổng giao dịch: {tong_giao_dich}")
print(f"• Giao dịch thắng: {giao_dich_thang}/{tong_giao_dich}")
print(f"• Tỷ lệ thắng: {ty_le_thang:.1%}")
print(f"• Lợi nhuận trung bình: {loi_nhuan_tb:.2f}%")
print(f"• Đánh giá: {'TỐT' if ty_le_thang > 0.6 and loi_nhuan_tb > 1 else 'CẦN CẢI THIỆN'}")
```

---

## 📈 Phần 2: Thực Hành - So Sánh Nhiều Chiến Lược

### Bài Tập: So Sánh 3 Chiến Lược VPA

```python
def so_sanh_chien_luoc(data_co_phieu):
    """
    So sánh hiệu quả của 3 chiến lược VPA
    """
    
    # Chiến lược 1: Stopping Volume > 70
    def cl1(data):
        return tinh_diem_tin_cay_stopping_volume(data) > 70
    
    # Chiến lược 2: No Supply > 60  
    def cl2(data):
        kq = phat_hien_no_supply_don_gian(data)
        return kq['co_tin_hieu'] and kq['diem_tin_cay'] > 60
    
    # Chiến lược 3: Kết hợp cả hai
    def cl3(data):
        return cl1(data) or cl2(data)
    
    chien_luoc = {
        'Stopping Volume > 70': cl1,
        'No Supply > 60': cl2,
        'Kết hợp cả hai': cl3
    }
    
    ket_qua_so_sanh = {}
    
    for ten, ham_chien_luoc in chien_luoc.items():
        ket_qua = backtest_don_gian(data_co_phieu, ham_chien_luoc)
        
        if ket_qua:
            loi_nhuan = [gd['loi_nhuan_phan_tram'] for gd in ket_qua]
            ket_qua_so_sanh[ten] = {
                'so_giao_dich': len(ket_qua),
                'ty_le_thang': sum(1 for ln in loi_nhuan if ln > 0) / len(ket_qua),
                'loi_nhuan_tb': np.mean(loi_nhuan),
                'loi_nhuan_tong': sum(loi_nhuan)
            }
    
    return ket_qua_so_sanh

# Chạy so sánh cho VCB
ket_qua_ss = so_sanh_chien_luoc(vcb_data)

print("=== SO SÁNH CHIẾN LƯỢC VCB ===")
for ten_cl, kq in ket_qua_ss.items():
    print(f"\n📋 {ten_cl}:")
    print(f"   • Số giao dịch: {kq['so_giao_dich']}")
    print(f"   • Tỷ lệ thắng: {kq['ty_le_thang']:.1%}")
    print(f"   • Lợi nhuận TB: {kq['loi_nhuan_tb']:.2f}%")
    print(f"   • Tổng lợi nhuận: {kq['loi_nhuan_tong']:.2f}%")

# Tìm chiến lược tốt nhất
chien_luoc_tot_nhat = max(ket_qua_ss.items(), 
                         key=lambda x: x[1]['loi_nhuan_tong'])
print(f"\n🏆 Chiến lược tốt nhất: {chien_luoc_tot_nhat[0]}")
```

---

> 🚀 **Checkpoint Học Tập:**
> 1. ✅ Hiểu được khái niệm backtesting cơ bản
> 2. ✅ Biết cách tính toán tỷ lệ thắng, lợi nhuận trung bình  
> 3. ✅ So sánh được nhiều chiến lược khác nhau
> 4. ✅ Đánh giá được chiến lược nào hiệu quả hơn

---

## 🔍 Phần 3: Nâng Cao - Phân Tích Rủi Ro

> 💡 **Lưu ý**: Phần này dành cho người muốn hiểu sâu hơn về quản lý rủi ro. 
> Nếu bạn mới bắt đầu, có thể **bỏ qua** và quay lại sau.

### Tại Sao Cần Phân Tích Rủi Ro?

**Câu chuyện thực tế:**
- Chiến lược A: Lãi 20%/năm, nhưng có tháng lỗ 15%
- Chiến lược B: Lãi 15%/năm, lỗ tối đa chỉ 5%
- Bạn chọn cái nào?

**3 Chỉ Số Rủi Ro Quan Trọng:**

#### 1. Maximum Drawdown (Lỗ Tối Đa)
```python
def tinh_max_drawdown(danh_sach_loi_nhuan):
    """
    Tính mức lỗ tối đa liên tiếp
    Ví dụ: [+3%, +2%, -5%, -3%, -2%, +4%] → Max Drawdown = -10%
    """
    von_hien_tai = 100  # Bắt đầu với 100 triệu
    von_cao_nhat = 100
    drawdown_toi_da = 0
    
    for loi_nhuan in danh_sach_loi_nhuan:
        von_hien_tai = von_hien_tai * (1 + loi_nhuan/100)
        von_cao_nhat = max(von_cao_nhat, von_hien_tai)
        
        drawdown_hien_tai = (von_hien_tai - von_cao_nhat) / von_cao_nhat
        drawdown_toi_da = min(drawdown_toi_da, drawdown_hien_tai)
    
    return drawdown_toi_da * 100  # Trả về %

# Ví dụ
loi_nhuan_vcb = [2.9, 1.5, -2.8, 3.5, 1.5, -1.2, 2.8]
max_dd = tinh_max_drawdown(loi_nhuan_vcb)
print(f"Max Drawdown VCB: {max_dd:.2f}%")
```

#### 2. Sharpe Ratio (Tỷ Số Sharpe)
```python
def tinh_sharpe_ratio(danh_sach_loi_nhuan, lai_suat_khong_rui_ro=2.0):
    """
    Sharpe Ratio = (Lợi nhuận - Lãi suất không rủi ro) / Độ biến động
    > 1.0 = Tốt, > 1.5 = Rất tốt, > 2.0 = Xuất sắc
    """
    loi_nhuan_tb = np.mean(danh_sach_loi_nhuan)
    do_bien_dong = np.std(danh_sach_loi_nhuan)
    
    if do_bien_dong == 0:
        return 0
    
    sharpe = (loi_nhuan_tb - lai_suat_khong_rui_ro/12) / do_bien_dong  # Chia 12 vì monthly
    return sharpe

# Ví dụ
sharpe_vcb = tinh_sharpe_ratio(loi_nhuan_vcb)
print(f"Sharpe Ratio VCB: {sharpe_vcb:.2f}")
if sharpe_vcb > 1.5:
    print("✅ Rất tốt!")
elif sharpe_vcb > 1.0:
    print("✅ Tốt")
else:
    print("⚠️ Cần cải thiện")
```

---

> 🔥 **PHẦN NÂNG CAO - CÓ THỂ BỎ QUA NẾU MỚI BẮT ĐẦU**

<details>
<summary>📋 <strong>Backtesting Engine Chuyên Nghiệp - Chỉ Dành Cho Người Muốn Tìm Hiểu Sâu</strong></summary>

```python
class BacktestingEngine:
    def __init__(self, von_ban_dau=100_000_000):  # 100 triệu VNĐ
        self.von_ban_dau = von_ban_dau
        self.ket_qua_chi_tiet = []
        self.lich_su_von = []
        
    def chay_backtest_nang_cao(self, data, chien_luoc, 
                              phi_giao_dich=0.0015,  # 0.15% phí
                              stop_loss=-0.05,        # Cắt lỗ -5%
                              take_profit=0.10,       # Chốt lãi +10%
                              max_giu_ngay=10):       # Tối đa giữ 10 ngày
        """
        Backtesting engine với các tính năng nâng cao:
        - Phí giao dịch
        - Stop loss / Take profit
        - Giới hạn thời gian giữ lệnh
        """
        
        von_hien_tai = self.von_ban_dau
        dang_giu_co_phieu = False
        ngay_mua = None
        gia_mua = 0
        
        for i in range(len(data) - 1):
            ngay_hien_tai = data.iloc[i]
            ngay_ke_tiep = data.iloc[i + 1]
            
            # Nếu đang giữ cổ phiếu, kiểm tra điều kiện thoát
            if dang_giu_co_phieu:
                gia_hien_tai = ngay_ke_tiep['close']
                loi_nhuan = (gia_hien_tai - gia_mua) / gia_mua
                so_ngay_giu = i - ngay_mua
                
                # Điều kiện bán
                nen_ban = (
                    loi_nhuan <= stop_loss or           # Stop loss
                    loi_nhuan >= take_profit or         # Take profit  
                    so_ngay_giu >= max_giu_ngay         # Hết hạn
                )
                
                if nen_ban:
                    # Thực hiện bán
                    gia_ban_thuc_te = gia_hien_tai * (1 - phi_giao_dich)
                    loi_nhuan_thuc_te = (gia_ban_thuc_te - gia_mua) / gia_mua
                    
                    von_hien_tai = von_hien_tai * (1 + loi_nhuan_thuc_te)
                    
                    self.ket_qua_chi_tiet.append({
                        'ngay_mua': data.iloc[ngay_mua]['date'],
                        'gia_mua': gia_mua,
                        'ngay_ban': ngay_ke_tiep['date'],
                        'gia_ban': gia_ban_thuc_te,
                        'loi_nhuan': loi_nhuan_thuc_te,
                        'so_ngay_giu': so_ngay_giu,
                        'ly_do_ban': self._xac_dinh_ly_do_ban(loi_nhuan, so_ngay_giu, 
                                                            stop_loss, take_profit, max_giu_ngay)
                    })
                    
                    dang_giu_co_phieu = False
            
            # Nếu chưa giữ cổ phiếu, kiểm tra tín hiệu mua
            elif not dang_giu_co_phieu:
                if chien_luoc(data[:i+1]):
                    # Thực hiện mua
                    gia_mua_thuc_te = ngay_ke_tiep['open'] * (1 + phi_giao_dich)
                    
                    dang_giu_co_phieu = True
                    ngay_mua = i + 1
                    gia_mua = gia_mua_thuc_te
            
            # Ghi nhận lịch sử vốn
            self.lich_su_von.append({
                'ngay': ngay_hien_tai['date'],
                'von': von_hien_tai
            })
        
        return self._phan_tich_ket_qua()
    
    def _xac_dinh_ly_do_ban(self, loi_nhuan, so_ngay, sl, tp, max_ngay):
        if loi_nhuan <= sl:
            return "Stop Loss"
        elif loi_nhuan >= tp:
            return "Take Profit"
        elif so_ngay >= max_ngay:
            return "Hết hạn"
        else:
            return "Khác"
    
    def _phan_tich_ket_qua(self):
        """
        Phân tích chi tiết kết quả backtest
        """
        if not self.ket_qua_chi_tiet:
            return {"error": "Không có giao dịch nào"}
        
        loi_nhuan_list = [gd['loi_nhuan'] for gd in self.ket_qua_chi_tiet]
        
        # Các chỉ số cơ bản
        tong_gd = len(self.ket_qua_chi_tiet)
        gd_thang = sum(1 for ln in loi_nhuan_list if ln > 0)
        ty_le_thang = gd_thang / tong_gd
        
        loi_nhuan_tb = np.mean(loi_nhuan_list)
        loi_nhuan_tong = (self.lich_su_von[-1]['von'] / self.von_ban_dau - 1)
        
        # Phân tích rủi ro
        max_drawdown = self._tinh_max_drawdown()
        sharpe_ratio = self._tinh_sharpe_ratio(loi_nhuan_list)
        
        # Phân tích theo lý do bán
        ly_do_ban = {}
        for gd in self.ket_qua_chi_tiet:
            ly_do = gd['ly_do_ban']
            if ly_do not in ly_do_ban:
                ly_do_ban[ly_do] = {'count': 0, 'avg_return': []}
            ly_do_ban[ly_do]['count'] += 1
            ly_do_ban[ly_do]['avg_return'].append(gd['loi_nhuan'])
        
        for ly_do in ly_do_ban:
            ly_do_ban[ly_do]['avg_return'] = np.mean(ly_do_ban[ly_do]['avg_return'])
        
        return {
            'tong_giao_dich': tong_gd,
            'giao_dich_thang': gd_thang,
            'ty_le_thang': ty_le_thang,
            'loi_nhuan_trung_binh': loi_nhuan_tb,
            'loi_nhuan_tong': loi_nhuan_tong,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe_ratio,
            'phan_tich_ly_do_ban': ly_do_ban,
            'xep_hang': self._xep_hang_chien_luoc(ty_le_thang, loi_nhuan_tong, max_drawdown, sharpe_ratio)
        }
    
    def _tinh_max_drawdown(self):
        if not self.lich_su_von:
            return 0
        
        von_cao_nhat = self.lich_su_von[0]['von']
        drawdown_toi_da = 0
        
        for point in self.lich_su_von:
            von_hien_tai = point['von']
            von_cao_nhat = max(von_cao_nhat, von_hien_tai)
            
            drawdown = (von_hien_tai - von_cao_nhat) / von_cao_nhat
            drawdown_toi_da = min(drawdown_toi_da, drawdown)
        
        return drawdown_toi_da
    
    def _tinh_sharpe_ratio(self, loi_nhuan_list):
        if len(loi_nhuan_list) < 2:
            return 0
        
        loi_nhuan_tb = np.mean(loi_nhuan_list)
        do_bien_dong = np.std(loi_nhuan_list)
        
        if do_bien_dong == 0:
            return 0
        
        # Giả sử lãi suất không rủi ro 2%/năm
        risk_free_rate = 0.02 / 12  # Monthly
        return (loi_nhuan_tb - risk_free_rate) / do_bien_dong
    
    def _xep_hang_chien_luoc(self, win_rate, total_return, max_dd, sharpe):
        """
        Xếp hạng chiến lược dựa trên 4 tiêu chí
        """
        diem = 0
        
        # Tỷ lệ thắng (25% trọng số)
        if win_rate >= 0.7: diem += 25
        elif win_rate >= 0.6: diem += 20
        elif win_rate >= 0.5: diem += 15
        else: diem += 10
        
        # Lợi nhuận tổng (30% trọng số)  
        if total_return >= 0.2: diem += 30
        elif total_return >= 0.15: diem += 25
        elif total_return >= 0.1: diem += 20
        elif total_return >= 0.05: diem += 15
        else: diem += 10
        
        # Max Drawdown (25% trọng số)
        if max_dd >= -0.05: diem += 25
        elif max_dd >= -0.1: diem += 20
        elif max_dd >= -0.15: diem += 15
        else: diem += 10
        
        # Sharpe Ratio (20% trọng số)
        if sharpe >= 2.0: diem += 20
        elif sharpe >= 1.5: diem += 17
        elif sharpe >= 1.0: diem += 14
        else: diem += 10
        
        if diem >= 85:
            return "A+ (Xuất Sắc)"
        elif diem >= 75:
            return "A (Rất Tốt)"
        elif diem >= 65:
            return "B (Tốt)"
        elif diem >= 55:
            return "C (Trung Bình)"
        else:
            return "D (Cần Cải Thiện)"

# Sử dụng Backtesting Engine
engine = BacktestingEngine(von_ban_dau=100_000_000)
ket_qua = engine.chay_backtest_nang_cao(
    data=vcb_data,
    chien_luoc=chien_luoc_stopping_volume,
    phi_giao_dich=0.0015,
    stop_loss=-0.05,
    take_profit=0.08
)

print("=== KẾT QUẢ BACKTEST NÂNG CAO ===")
print(f"🎯 Xếp hạng: {ket_qua['xep_hang']}")
print(f"📊 Tổng giao dịch: {ket_qua['tong_giao_dich']}")
print(f"✅ Tỷ lệ thắng: {ket_qua['ty_le_thang']:.1%}")
print(f"💰 Lợi nhuận tổng: {ket_qua['loi_nhuan_tong']:.1%}")
print(f"📉 Max Drawdown: {ket_qua['max_drawdown']:.1%}")
print(f"📈 Sharpe Ratio: {ket_qua['sharpe_ratio']:.2f}")

print(f"\n🔍 Phân tích lý do bán:")
for ly_do, thong_tin in ket_qua['phan_tich_ly_do_ban'].items():
    print(f"   • {ly_do}: {thong_tin['count']} lần ({thong_tin['avg_return']:.2%} TB)")
```

</details>

---

## 📋 Tóm Tắt Chương

### Những Gì Đã Học:
1. **Backtesting cơ bản** - Kiểm tra chiến lược với dữ liệu lịch sử
2. **So sánh chiến lược** - Tìm ra phương pháp hiệu quả nhất
3. **Phân tích rủi ro** - Max Drawdown, Sharpe Ratio
4. **Backtesting engine** chuyên nghiệp (nâng cao)

### Lợi Ích Thiết Thực:
- ✅ Biết trước khả năng sinh lời của chiến lược
- ✅ Tránh được những chiến lược "tưởng tốt" nhưng thực tế tệ
- ✅ Quản lý rủi ro dựa trên số liệu cụ thể
- ✅ So sánh khách quan nhiều phương pháp

### Chương Tiếp Theo:
**Chương 5.3: Phân Tích Dòng Tiền Thông Minh** - Cách theo dõi tiền của các nhà đầu tư lớn trong thị trường Việt Nam.