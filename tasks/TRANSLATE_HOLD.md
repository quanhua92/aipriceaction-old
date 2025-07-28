# Kế Hoạch Dịch Thuật - TRANSLATE_HOLD.md

## Mục Tiêu
Dịch các đoạn văn bản hỗn hợp Tiếng Anh - Tiếng Việt trong file `hold.md` thành Tiếng Việt chuyên nghiệp, đảm bảo không làm mất format hoặc markdown heading.

## Phạm Vi Dịch Thuật
Chỉ dịch nội dung trong các phần con sau:

### 1. VPA Phân Tích Hiện Tại
- Các bullet point dưới "**Bối Cảnh Tuần:**" 
- Các bullet point dưới "**Bối Cảnh Ngày:**"

### 2. Hành Động Đề Xuất  
- Các bullet point dưới "**Lý Do Hành Động:**"

### 3. Top 3 Cổ Phiếu Thay Thế
- Nội dung mô tả trong các bullet point của từng cổ phiếu thay thế

## Nguyên Tắc Dịch Thuật

### Giữ Nguyên
- Tất cả markdown headers (# ## ###)
- Tất cả table format
- Tất cả image links
- Tất cả số liệu, ngày tháng, tỷ lệ phần trăm
- Tất cả tên mã cổ phiếu (CTS, HDB, VIX, etc.)
- Tất cả thuật ngữ kỹ thuật VPA (Sign of Strength, No Supply, etc.)

### Dịch Sang Tiếng Việt Chuyên Nghiệp
- Các từ và cụm từ tiếng Anh thông thường
- Các cấu trúc câu hỗn hợp
- Thuật ngữ tài chính tiếng Anh thành tiếng Việt tương đương

### Từ Vựng Chuẩn
- "breakthrough" → "đột phá"
- "consolidation" → "củng cố"
- "accumulation" → "tích lũy"
- "distribution" → "phân phối"
- "momentum" → "động lực"
- "resistance" → "kháng cự"
- "support" → "hỗ trợ"
- "volume explosion" → "khối lượng bùng nổ"
- "institutional buying" → "mua tổ chức"
- "climax action" → "hành động đỉnh điểm"

## Quy Trình Thực Hiện

1. **Tìm Kiếm Nội Dung** - Sử dụng Grep tool để định vị chính xác các phần cần dịch
2. **Phân Tích Ngữ Cảnh** - Đọc hiểu nội dung để đảm bảo dịch thuật chính xác
3. **Dịch Thuật** - Chuyển đổi từ hỗn hợp EN-VN sang VN chuyên nghiệp
4. **Kiểm Tra Format** - Đảm bảo không làm mất cấu trúc markdown
5. **Áp Dụng Thay Đổi** - Sử dụng Edit tool để cập nhật file

## Lưu Ý Quan Trọng
- KHÔNG thay đổi bất kỳ heading nào
- KHÔNG thay đổi cấu trúc table
- KHÔNG thay đổi format số liệu
- CHỈ dịch nội dung văn bản trong các bullet point được chỉ định