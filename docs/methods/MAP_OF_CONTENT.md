# Bản Đồ Nội Dung: Hướng Dẫn Viết Lại Tutorial VPA & Wyckoff

## Nguyên Tắc Cốt Lõi

- **Nguồn Tham Khảo Chính:** Thư mục `docs/methods/` là nguồn chuẩn mực duy nhất cho **thuật ngữ, cấu trúc và phong cách giảng dạy**
- **Mục Tiêu Viết Lại:** Thư mục `docs/tutorials/` chứa các file cần được viết lại hoàn toàn
- **Tích Hợp Dữ Liệu:** Tất cả tutorial đã viết lại phải sử dụng dữ liệu thực từ `market_data/` và `vpa_data/` làm ví dụ

## Bảng Ánh Xạ Chi Tiết

| Tutorial Cần Viết Lại | File Tham Khảo (methods/) | Khái Niệm Chính Cần Chuyển Giao |
|----------------------|--------------------------|----------------------------------|
| `chapter-1-1-vpa-basics.md` | `phần-1-nền-tảng-vững-chắc-vpa...md` | Nền tảng VPA, mối quan hệ giá-khối lượng, nguyên lý cốt lõi VPA |
| `chapter-1-2-wyckoff-laws.md` | `phần-1-nền-tảng-vững-chắc-vpa...md` | Ba quy luật Wyckoff: Cung-Cầu, Nguyên nhân-Kết quả, Nỗ lực-Kết quả |
| `chapter-1-3-composite-man.md` | `phần-1-nền-tảng-vững-chắc-vpa...md` | Khái niệm "Composite Man" hay "Dòng tiền thông minh" |
| `chapter-2-1-accumulation-phases.md` | `phần-2-giải-phẫu-chi-tiết...md` | Phân tích chi tiết các giai đoạn tích lũy Wyckoff (Phase A, B, C, D, E) |
| `chapter-2-2-distribution-phases.md` | `phần-2-giải-phẫu-chi-tiết...md` | Phân tích chi tiết các giai đoạn phân phối Wyckoff |
| `chapter-3-1-bullish-vpa-signals.md` | `phần-2-giải-phẫu-chi-tiết...md` | Tín hiệu VPA tích cực (Test for Supply, Shakeout, v.v.) |
| `chapter-3-2-bearish-vpa-signals.md` | `phần-2-giải-phẫu-chi-tiết...md` | Tín hiệu VPA tiêu cực (Upthrust, No Demand, v.v.) |
| `chapter-4-1-trading-systems.md` | `phần-4-xây-dựng-chiến-lược...md` | Cách xây dựng hệ thống giao dịch hoàn chỉnh dựa trên VPA và Wyckoff |
| `case-studies/` (tất cả files) | `phần-3-thực-chiến...md` + `phần-6-nghiên-cứu...md` | Ứng dụng thực tế phương pháp trên cổ phiếu Việt Nam |

## Quy Trình Viết Lại Chi Tiết

### Bước 1: Chuẩn Bị
1. **Chọn Tutorial File**: Chọn file từ `docs/tutorials/` cần viết lại
2. **Xác Định File Tham Khảo**: Sử dụng bảng ánh xạ để tìm file tương ứng trong `docs/methods/`
3. **Đọc và Hiểu**: Đọc kỹ cả tutorial hiện tại và file tham khảo

### Bước 2: Viết Lại Bằng Tiếng Việt Chất Lượng Cao
1. **Thuật Ngữ**: Sử dụng chính xác thuật ngữ tiếng Việt từ file `methods`
2. **Phong Cách**: Áp dụng tone giảng dạy rõ ràng, có tính giáo dục và uy tín từ file `methods`
3. **Cấu Trúc**: Tổ chức tutorial logic, theo cấu trúc của file `methods`

### Bước 3: Tích Hợp Dữ Liệu Thực Tế
1. **Thay Thế Ví Dụ**: Thay tất cả ví dụ chung chung bằng ví dụ cụ thể từ `market_data/` và `vpa_data/`
2. **Dữ Liệu Cụ Thể**: Khi giải thích "Test for Supply", tìm ví dụ thực tế trong dữ liệu VCB hoặc TCB
3. **Biểu Đồ và Dữ Liệu**: Bao gồm biểu đồ và đoạn dữ liệu để minh họa

### Bước 4: Thêm Bài Tập Thực Hành
1. **Bài Tập Cuối Chương**: Thêm phần bài tập thực hành cuối mỗi tutorial
2. **Ví Dụ**: "Mở file `TCB_2025-01-02_to_2025-07-21.csv` và xác định ba trường hợp tín hiệu 'No Demand'"

## Chuẩn Mực Chất Lượng Tiếng Việt

### Thuật Ngữ Chuẩn
- **Volume Price Analysis** → **Phân tích Giá và Khối lượng (VPA)**
- **Smart Money** → **Dòng tiền thông minh**
- **Composite Man** → **Composite Man** (giữ nguyên) hoặc **"Tay to"**
- **Accumulation** → **Tích lũy (gom hàng)**
- **Distribution** → **Phân phối (xả hàng)**
- **Test for Supply** → **Kiểm tra Nguồn cung**
- **No Demand** → **Không có Nhu cầu**
- **Spring/Shakeout** → **Spring/Cú rũ bỏ**
- **Upthrust** → **Đẩy lên Thất bại**

### Phong Cách Giáo Dục
1. **Sử dụng ẩn dụ**: Như "máy phát hiện nói dối" cho khối lượng
2. **Tone chuyên môn**: Không quá thông thường, giữ tính giáo dục cao
3. **Giải thích rõ ràng**: Mỗi khái niệm được giải thích từ cơ bản đến nâng cao
4. **Ví dụ thực tế**: Luôn kèm theo ví dụ từ thị trường Việt Nam

## Ví Dụ Cụ Thể: Viết Lại `chapter-1-1-vpa-basics.md`

### Tham Khảo
File: `phần-1-nền-tảng-vững-chắc-vpa-theo-anna-coulling-và-nguyên-lý-wyckoff-bất-biến.md`

### Khái Niệm Chính
1. Giới thiệu VPA là "Phân tích Giá và Khối lượng"
2. Giải thích mối quan hệ giữa biên độ giá, khối lượng và giá đóng cửa
3. Sử dụng thuật ngữ tiếng Việt cho tín hiệu tăng và giảm như định nghĩa trong file tham khảo

### Tích Hợp Dữ Liệu
1. **Sử dụng `VCB_2025-01-02_to_2025-07-21.csv`** để tạo biểu đồ
2. **Trên biểu đồ**, highlight một ngày cụ thể và giải thích cách giá, khối lượng và đóng cửa ngày đó kể câu chuyện gì
3. **Ví dụ cụ thể từ VCB ngày 2025-06-13**: 
   ```
   Ngày: 2025-06-13
   Mở: 56.8, Cao: 57.2, Thấp: 56.0, Đóng: 56.2
   Khối lượng: 5,300,000 (vs trung bình 1,200,000)
   Phân tích: Stopping Volume hoàn hảo tại mức hỗ trợ 56.0, dẫn đến đợt tăng 8% trong tuần sau
   ```

### Bài Tập
"Phân tích 10 phiên giao dịch gần nhất của FPT trong dữ liệu được cung cấp. Với mỗi ngày, mô tả mối quan hệ giữa biên độ giá và khối lượng. Điều này cho bạn biết gì về tâm lý thị trường hiện tại đối với FPT?"

## Danh Sách Kiểm Tra Chất Lượng

### Trước Khi Hoàn Thành
- [ ] Đã sử dụng đúng thuật ngữ tiếng Việt từ file methods
- [ ] Đã tích hợp ít nhất 3 ví dụ cụ thể từ market_data/
- [ ] Đã cross-reference với vpa_data/ để validation
- [ ] Đã thêm bài tập thực hành cuối chương
- [ ] Tone giảng dạy chuyên nghiệp và dễ hiểu
- [ ] Cấu trúc logic và dễ theo dõi
- [ ] Đã review grammar và chính tả tiếng Việt

### Đặc Biệt Quan Trọng Cho Case Studies
- [ ] **Ticker cụ thể**: Phải nêu rõ mã cổ phiếu (VCB, TCB, HPG, v.v.)
- [ ] **Ngày tháng chính xác**: Chỉ định ngày/tháng/năm cụ thể của pattern
- [ ] **Dữ liệu RAW**: Bao gồm OHLCV data thô từ CSV
- [ ] **Khoảng thời gian**: Nêu rõ time range phân tích (ví dụ: 2025-01-02 đến 2025-07-21)
- [ ] **Weekly vs Daily**: Chỉ định rõ đang phân tích daily hay weekly data

## Kết Luận

Bằng cách tuân theo hướng dẫn này, bạn có thể viết lại một cách có hệ thống các tutorial để tạo ra một tài nguyên giáo dục comprehensive và chất lượng cao cho việc học VPA và phương pháp Wyckoff trong bối cảnh thị trường chứng khoán Việt Nam.

**Mục tiêu cuối cùng**: Mỗi tutorial được viết lại sẽ là một bài học hoàn chỉnh, dễ hiểu, có tính thực tiễn cao và sử dụng đúng chuẩn mực tiếng Việt giáo dục.