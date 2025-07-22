# Chương 5.1: Nâng Cấp VPA - Từ Trực Giác đến Khoa Học
## Làm Chính Xác Những Gì Chúng Ta Đã Học

### 🎯 Mục Tiêu Chương

Bạn đã học các tín hiệu VPA cơ bản như Stopping Volume và No Supply. Bây giờ chúng ta sẽ học cách **đo lường chính xác** mức độ mạnh yếu của các tín hiệu này, thay vì chỉ dựa vào cảm giác "có vẻ mạnh" hay "có vẻ yếu".

### 💡 Nguyên Lý Cốt Lõi

**Từ "Có vẻ" đến "Chắc chắn":**
- Trước: "Stopping Volume này có vẻ mạnh"  
- Sau: "Stopping Volume này có độ tin cậy 85%, kỳ vọng lợi nhuận 3.2%"

**Tại sao quan trọng?**
- Biết được tín hiệu nào đáng tin hơn
- Quyết định được nên đặt bao nhiều tiền vào mỗi tín hiệu
- Tránh được những tín hiệu "bẫy"

---

## 📚 Phần 1: Cơ Bản - Đo Lường Sức Mạnh Tín Hiệu

### A. Stopping Volume - Từ Mô Tả Đến Đo Lường

**Cách cũ (dựa vào mắt):**
- "Hôm nay khối lượng VCB lớn và giá hồi phục, có vẻ như Stopping Volume"
- Vấn đề: Không biết "lớn" là bao nhiều? "Hồi phục" đến mức nào?

**Cách mới (dựa vào số liệu):**
- "Khối lượng VCB hôm nay gấp 2.3 lần bình thường, giá đóng cửa ở 78% biên độ ngày"
- "Điểm tin cậy: 82/100, kỳ vọng lợi nhuận 5 ngày: +2.1%"

#### 🔧 Công Cụ Đo Lường Đơn Giản

```python
# Bước 1: Đo khối lượng "bất thường" như thế nào
def tinh_do_bat_thuong_khoi_luong(data_co_phieu):
    """
    Tính xem khối lượng hôm nay "bất thường" đến mức nào
    Trả về: Số từ 0-5 (5 = rất bất thường)
    """
    khoi_luong_hom_nay = data_co_phieu['volume'][-1]
    khoi_luong_binh_thuong = data_co_phieu['volume'][-20:-1].mean()  # 20 ngày trước
    
    ti_le = khoi_luong_hom_nay / khoi_luong_binh_thuong
    
    if ti_le >= 3.0:    return 5  # Cực kỳ bất thường
    elif ti_le >= 2.5:  return 4  # Rất bất thường  
    elif ti_le >= 2.0:  return 3  # Khá bất thường
    elif ti_le >= 1.5:  return 2  # Hơi bất thường
    elif ti_le >= 1.2:  return 1  # Bình thường+
    else:               return 0  # Bình thường hoặc thấp

# Bước 2: Đo mức độ "hồi phục" trong ngày
def tinh_muc_do_hoi_phuc(data_ngay):
    """
    Tính xem giá đóng cửa ở đâu trong biên độ ngày
    Trả về: Số từ 0-1 (1 = đóng cửa ở đỉnh ngày)
    """
    gia_cao = data_ngay['high']
    gia_thap = data_ngay['low'] 
    gia_dong_cua = data_ngay['close']
    
    vi_tri = (gia_dong_cua - gia_thap) / (gia_cao - gia_thap)
    return vi_tri

# Bước 3: Kết hợp thành điểm tin cậy
def tinh_diem_tin_cay_stopping_volume(data_co_phieu):
    """
    Tính điểm tin cậy tổng thể cho tín hiệu Stopping Volume
    """
    diem_khoi_luong = tinh_do_bat_thuong_khoi_luong(data_co_phieu) * 20  # Tối đa 100 điểm
    diem_hoi_phuc = tinh_muc_do_hoi_phuc(data_co_phieu.iloc[-1]) * 100  # Tối đa 100 điểm
    
    # Trọng số: Khối lượng 60%, Hồi phục 40%
    diem_tong = (diem_khoi_luong * 0.6) + (diem_hoi_phuc * 0.4)
    
    return min(diem_tong, 100)  # Tối đa 100 điểm
```

#### 📊 Ví Dụ Thực Tế: VCB Ngày 13/06/2025

```python
# Dữ liệu thực tế VCB
vcb_13_06 = {
    'date': '2025-06-13',
    'open': 85400,
    'high': 86800,
    'low': 84200,
    'close': 86500,
    'volume': 15420000
}

# Khối lượng 20 ngày trước đó (trung bình)
khoi_luong_bt = 6800000

# Tính toán
ti_le_khoi_luong = 15420000 / 6800000  # = 2.27 (gấp 2.27 lần)
diem_khoi_luong = 3 * 20 = 60  # Điểm khối lượng

vi_tri_dong_cua = (86500 - 84200) / (86800 - 84200)  # = 0.88 (88%)
diem_hoi_phuc = 0.88 * 100 = 88  # Điểm hồi phục

diem_tin_cay = (60 * 0.6) + (88 * 0.4) = 71.2  # Điểm tin cậy tổng

print(f"VCB 13/06/2025 - Stopping Volume:")
print(f"• Khối lượng gấp {ti_le_khoi_luong:.1f} lần bình thường")
print(f"• Đóng cửa ở {vi_tri_dong_cua:.0%} biên độ ngày")  
print(f"• Điểm tin cậy: {diem_tin_cay:.0f}/100")
print(f"• Đánh giá: Tín hiệu TỐT (>70 điểm)")
```

> 💡 **Giải Thích Kết Quả:**
> - Khối lượng gấp 2.27 lần → Có sự quan tâm bất thường
> - Đóng cửa ở 88% biên độ → Hồi phục mạnh từ đáy  
> - Điểm 71/100 → Tín hiệu đáng tin cậy, có thể theo dõi thêm

---

### B. No Supply - Đo Lường "Thiếu Áp Lực Bán"

**Nguyên lý cốt lõi:** Khi giá tăng mà khối lượng thấp = ít người bán = No Supply

#### 🔧 Công Cụ Đo Lường No Supply

```python
def phat_hien_no_supply_don_gian(data_co_phieu):
    """
    Phát hiện No Supply theo cách dễ hiểu
    """
    ngay_hom_nay = data_co_phieu.iloc[-1]
    
    # Điều kiện 1: Giá phải tăng (ít nhất 1%)
    tang_gia = (ngay_hom_nay['close'] - ngay_hom_nay['open']) / ngay_hom_nay['open']
    co_tang_gia = tang_gia > 0.01  # Tăng > 1%
    
    # Điều kiện 2: Khối lượng phải thấp (< 80% bình thường)
    khoi_luong_bt = data_co_phieu['volume'][-10:-1].mean()  # 10 ngày trước
    ti_le_khoi_luong = ngay_hom_nay['volume'] / khoi_luong_bt
    khoi_luong_thap = ti_le_khoi_luong < 0.8
    
    # Tính điểm
    if co_tang_gia and khoi_luong_thap:
        diem_tang_gia = min(tang_gia * 1000, 50)  # Tối đa 50 điểm
        diem_khoi_luong_thap = (0.8 - ti_le_khoi_luong) * 125  # Tối đa 50 điểm
        tong_diem = diem_tang_gia + diem_khoi_luong_thap
        
        return {
            'co_tin_hieu': True,
            'diem_tin_cay': min(tong_diem, 100),
            'tang_gia_phan_tram': tang_gia * 100,
            'ti_le_khoi_luong': ti_le_khoi_luong,
            'danh_gia': 'TỐT' if tong_diem > 70 else 'TRUNG BÌNH' if tong_diem > 50 else 'YẾU'
        }
    else:
        return {'co_tin_hieu': False}
```

---

## 📈 Phần 2: Thực Hành Với Dữ Liệu Thật

### Bài Tập: Phân Tích 3 Cổ Phiếu Ngân Hàng

#### 1. VCB - Ngân Hàng Ngoại Thương Việt Nam

```python
# Tải dữ liệu VCB từ file CSV
import pandas as pd
vcb_data = pd.read_csv('market_data/VCB.csv')

# Phân tích tháng 6/2025 
print("=== PHÂN TÍCH VCB THÁNG 6/2025 ===")
for index, row in vcb_data.iterrows():
    if '2025-06' in row['date']:
        # Áp dụng công cụ đo lường
        diem_stopping = tinh_diem_tin_cay_stopping_volume(vcb_data[:index+1])
        ket_qua_no_supply = phat_hien_no_supply_don_gian(vcb_data[:index+1])
        
        # Chỉ hiển thị tín hiệu mạnh
        if diem_stopping > 60 or (ket_qua_no_supply['co_tin_hieu'] and ket_qua_no_supply['diem_tin_cay'] > 60):
            print(f"\n📅 {row['date']}:")
            print(f"💰 VCB: {row['close']:,}đ")
            
            if diem_stopping > 60:
                print(f"⚡ Stopping Volume: {diem_stopping:.0f}/100")
            
            if ket_qua_no_supply['co_tin_hieu']:
                print(f"🔥 No Supply: {ket_qua_no_supply['diem_tin_cay']:.0f}/100")
                print(f"   • Tăng giá: {ket_qua_no_supply['tang_gia_phan_tram']:.1f}%")
                print(f"   • Khối lượng: {ket_qua_no_supply['ti_le_khoi_luong']:.0%} bình thường")
```

#### 2. TCB - Techcombank & 3. HPG - Hoa Phát Group
```python
# Áp dụng tương tự cho TCB và HPG
tcb_data = pd.read_csv('market_data/TCB.csv')
hpg_data = pd.read_csv('market_data/HPG.csv')
# (Code tương tự)
```

---

> 🚀 **Checkpoint Học Tập:**
> 1. ✅ Hiểu được cách đo lường sức mạnh tín hiệu bằng số
> 2. ✅ Biết cách áp dụng với dữ liệu thật (VCB, TCB, HPG)  
> 3. ✅ Có công cụ đánh giá tin cậy từ 0-100 điểm
> 4. ✅ Phân biệt được tín hiệu TỐT (>70), TRUNG BÌNH (50-70), YẾU (<50)

---

## 🔍 Phần 3: Nâng Cao - Đánh Giá Độ Tin Cậy

> 💡 **Lưu ý**: Phần này dành cho người muốn hiểu sâu hơn về thống kê. 
> Nếu bạn mới bắt đầu, có thể **bỏ qua** và quay lại sau.

### Tại Sao Cần Đánh Giá Độ Tin Cậy?

**Tình huống thực tế:**
- Bạn thấy 2 tín hiệu Stopping Volume cùng 75 điểm
- Cái nào đáng tin hơn?
- Làm sao biết tín hiệu này "thật" hay chỉ là ngẫu nhiên?

**Giải pháp:** Hệ thống đánh giá 5 yếu tố

### 🎯 Hệ Thống Đánh Giá 5 Yếu Tố

#### Yếu Tố 1: Tần Suất Xuất Hiện (20% trọng số)
- **Quá ít:** < 5 lần/năm → Không đủ dữ liệu 
- **Vừa đủ:** 10-20 lần/năm → Có thể tin được
- **Lý tưởng:** 20-50 lần/năm → Đáng tin cậy
- **Quá nhiều:** > 100 lần/năm → Có thể là nhiễu

#### Yếu Tố 2: Tỷ Lệ Thắng (25% trọng số)  
- **Kém:** < 50% → Không hiệu quả
- **Trung bình:** 50-60% → Chấp nhận được
- **Tốt:** 60-70% → Đáng đầu tư
- **Xuất sắc:** > 70% → Rất đáng tin

#### Yếu Tố 3: Lợi Nhuận Trung Bình (25% trọng số)
- **Âm:** < 0% → Tránh xa
- **Thấp:** 0-1% → Cân nhắc  
- **Khá:** 1-3% → Có thể theo
- **Cao:** > 3% → Ưu tiên cao

#### Yếu Tố 4: Tính Ổn Định (20% trọng số)
- Hiệu quả có nhất quán qua các tháng?
- Có bị ảnh hưởng bởi thị trường tăng/giảm?

#### Yếu Tố 5: Xác Nhận Khối Lượng (10% trọng số)
- Khối lượng có thực sự "bất thường"?
- Có phù hợp với lý thuyết VPA?

---

> 🔥 **PHẦN NÂNG CAO - CÓ THỂ BỎ QUA NẾU MỚI BẮT ĐẦU**
> 
> Phần dưới đây là code chi tiết cho việc tính toán tự động. 
> Nếu bạn muốn hiểu sâu hơn về mặt kỹ thuật, hãy đọc tiếp.
> Nếu không, có thể chuyển sang Chương tiếp theo.

<details>
<summary>📋 <strong>Code Chi Tiết - Chỉ Dành Cho Người Muốn Tìm Hiểu Sâu</strong></summary>

```python
class HeDanhGiaDoTinCay:
    def __init__(self):
        # Trọng số 5 yếu tố
        self.trong_so = {
            'tan_suat_xuat_hien': 0.20,     # 20%
            'ty_le_thang': 0.25,            # 25% 
            'loi_nhuan_trung_binh': 0.25,   # 25%
            'tinh_on_dinh': 0.20,           # 20%
            'xac_nhan_khoi_luong': 0.10     # 10%
        }
    
    def tinh_do_tin_cay_tong_the(self, du_lieu_tin_hieu: Dict) -> Dict:
        """
        Tính độ tin cậy tổng thể từ 5 yếu tố
        Trả về điểm từ 0-100 và xếp hạng A, B, C, D, F
        """
        
        diem_thanh_phan = {}
        
        # 1. Tần suất xuất hiện
        so_tin_hieu = du_lieu_tin_hieu.get('so_tin_hieu_nam', 0)
        if so_tin_hieu < 5:
            diem_1 = 20
        elif so_tin_hieu < 10:
            diem_1 = 50  
        elif so_tin_hieu <= 50:
            diem_1 = 100
        else:
            diem_1 = max(50, 100 - (so_tin_hieu - 50))
        
        diem_thanh_phan['tan_suat'] = diem_1
        
        # 2. Tỷ lệ thắng
        ty_le_thang = du_lieu_tin_hieu.get('ty_le_thang', 0.5) * 100
        if ty_le_thang >= 70:
            diem_2 = 100
        elif ty_le_thang >= 60:
            diem_2 = 80
        elif ty_le_thang >= 50:
            diem_2 = 60
        else:
            diem_2 = max(0, ty_le_thang)
            
        diem_thanh_phan['ty_le_thang'] = diem_2
        
        # 3. Lợi nhuận trung bình 
        loi_nhuan_tb = du_lieu_tin_hieu.get('loi_nhuan_trung_binh', 0) * 100
        if loi_nhuan_tb >= 3:
            diem_3 = 100
        elif loi_nhuan_tb >= 1:
            diem_3 = 80
        elif loi_nhuan_tb >= 0:
            diem_3 = 60
        else:
            diem_3 = 0
            
        diem_thanh_phan['loi_nhuan'] = diem_3
        
        # 4. Tính ổn định
        tinh_on_dinh = du_lieu_tin_hieu.get('tinh_on_dinh', 0.5) * 100
        diem_thanh_phan['on_dinh'] = tinh_on_dinh
        
        # 5. Xác nhận khối lượng
        xac_nhan_kl = du_lieu_tin_hieu.get('xac_nhan_khoi_luong', 0.5) * 100
        diem_thanh_phan['khoi_luong'] = xac_nhan_kl
        
        # Tính điểm tổng thể có trọng số
        diem_tong = (
            diem_thanh_phan['tan_suat'] * self.trong_so['tan_suat_xuat_hien'] +
            diem_thanh_phan['ty_le_thang'] * self.trong_so['ty_le_thang'] + 
            diem_thanh_phan['loi_nhuan'] * self.trong_so['loi_nhuan_trung_binh'] +
            diem_thanh_phan['on_dinh'] * self.trong_so['tinh_on_dinh'] +
            diem_thanh_phan['khoi_luong'] * self.trong_so['xac_nhan_khoi_luong']
        )
        
        # Xếp hạng A, B, C, D, F
        if diem_tong >= 85:
            xep_hang = "A (Xuất Sắc - Đáng Tin Tuyệt Đối)"
            mau_sac = "🟢"
        elif diem_tong >= 75:
            xep_hang = "B (Tốt - Đáng Đầu Tư)"
            mau_sac = "🔵" 
        elif diem_tong >= 65:
            xep_hang = "C (Trung Bình - Cẩn Thận)"
            mau_sac = "🟡"
        elif diem_tong >= 50:
            xep_hang = "D (Yếu - Tránh Xa)"
            mau_sac = "🟠"
        else:
            xep_hang = "F (Rất Tệ - Không Nên Dùng)"
            mau_sac = "🔴"
        
        return {
            'diem_tong': diem_tong,
            'xep_hang': xep_hang, 
            'mau_sac': mau_sac,
            'diem_chi_tiet': diem_thanh_phan,
            'khuyen_nghi': self.tao_khuyen_nghi(diem_thanh_phan)
        }
    
    def tao_khuyen_nghi(self, diem: Tu_Dien) -> Danh_Sach[str]:
        """
        Đưa ra lời khuyên cải thiện
        """
        loi_khuyen = []
        
        if diem['tan_suat'] < 70:
            loi_khuyen.append("📊 Cần theo dõi thêm để có đủ dữ liệu")
        
        if diem['ty_le_thang'] < 70:
            loi_khuyen.append("🎯 Tỷ lệ thắng thấp, cần xem xét lại điều kiện")
        
        if diem['loi_nhuan'] < 70:
            loi_khuyen.append("💰 Lợi nhuận chưa cao, có thể chỉ phù hợp rủi ro thấp")
        
        if diem['on_dinh'] < 70:
            loi_khuyen.append("📈 Hiệu quả không ổn định qua các tháng")
        
        if diem['khoi_luong'] < 70:
            loi_khuyen.append("🔊 Cần kiểm tra lại logic về khối lượng")
        
        return loi_khuyen

# Ví dụ sử dụng
he_danh_gia = HeDanhGiaDoTinCay()
ket_qua = he_danh_gia.tinh_do_tin_cay_tong_the({
    'so_tin_hieu_nam': 25,
    'ty_le_thang': 0.68,
    'loi_nhuan_trung_binh': 0.024,
    'tinh_on_dinh': 0.75,
    'xac_nhan_khoi_luong': 0.85
})

print(f"{ket_qua['mau_sac']} Điểm tổng: {ket_qua['diem_tong']:.0f}/100")
print(f"Xếp hạng: {ket_qua['xep_hang']}")
for khuyen_nghi in ket_qua['khuyen_nghi']:
    print(f"• {khuyen_nghi}")
```

</details>

---

## 📋 Tóm Tắt Chương

### Những Gì Đã Học:
1. **Đo lường chính xác** thay vì đoán mò
2. **Công cụ tính điểm** từ 0-100 cho từng tín hiệu
3. **Thực hành** với dữ liệu VCB, TCB, HPG thực tế
4. **Hệ thống đánh giá** 5 yếu tố (nâng cao)

### Lợi Ích Thiết Thực:
- ✅ Quyết định đầu tư có căn cứ khoa học
- ✅ Phân biệt tín hiệu mạnh/yếu một cách khách quan
- ✅ Tránh được những cú lừa ngẫu nhiên
- ✅ Quản lý rủi ro hiệu quả hơn

## Câu Hỏi Tự Kiểm Tra

1. **Sự khác biệt chính giữa phân tích VPA "cũ" và "mới" là gì?**
   - *Gợi ý: Từ "có vẻ" đến "chắc chắn"*

2. **Làm thế nào để tính độ bất thường của khối lượng?**
   - *Gợi ý: So sánh với trung bình 20 ngày và áp dụng scale 0-5*

3. **5 yếu tố trong hệ thống đánh giá nâng cao là gì?**
   - *Gợi ý: Khối lượng, Phục hồi giá, Bối cảnh, Kỹ thuật, Rủi ro*

4. **Tại sao cần phải đo lường chính xác thay vì dựa vào trực giác?**
   - *Gợi ý: Tính nhất quán, tính khách quan, quản lý rủi ro*

5. **Ứng dụng quantitative framework vào dữ liệu thực tế như thế nào?**
   - *Gợi ý: Triển khai mã với VCB, TCB, HPG*

📖 **[Xem Đáp Án Chi Tiết](../answers/chapter-5-1-quantitative-vpa-framework-answers.md)**

### Chương Tiếp Theo:
**Chương 5.2: Xây Dựng Hệ Thống Backtesting Chuyên Nghiệp** - Cách kiểm tra xem chiến lược của bạn có thực sự hiệu quả trong quá khứ hay không.