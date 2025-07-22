# AIPriceAction - Vietnamese Stock Market Analysis Pipeline

A comprehensive automated system for analyzing Vietnamese stock market data with VPA (Volume Price Analysis) using AI-powered analysis and dividend detection.

## 📋 Table of Contents

- [Overview](#overview)
- [Core Pipeline Scripts](#core-pipeline-scripts)
- [Data Management Scripts](#data-management-scripts)
- [VPA Analysis Scripts](#vpa-analysis-scripts)
- [Dividend Detection System](#dividend-detection-system)
- [Utilities and Testing](#utilities-and-testing)
- [Configuration Files](#configuration-files)
- [GitHub Actions Workflows](#github-actions-workflows)
- [Usage Examples](#usage-examples)
- [Directory Structure](#directory-structure)

## 🎯 Overview

AIPriceAction is a flexible data pipeline that:
- Downloads Vietnamese stock market data automatically
- Generates professional candlestick charts with technical indicators
- Performs AI-powered Volume Price Analysis (VPA) using Wyckoff methodology
- Detects dividend adjustments automatically using multi-agent scanning
- Produces comprehensive markdown reports with actionable insights
- Supports both daily and weekly analysis modes

## 🔧 Core Pipeline Scripts

### `main.py` - Primary Data Pipeline
**The heart of the system** - orchestrates the entire data processing workflow.

```bash
# Basic usage
python main.py

# Custom date range
python main.py --start-date 2025-01-01 --end-date 2025-12-31

# Weekly analysis mode
python main.py --week

# Enable dividend detection
python main.py --check-dividend

# Weekly with dividend detection
python main.py --week --check-dividend
```

**What it does:**
- Downloads stock data using vnstock library for all tickers in `TICKERS.csv`
- Generates candlestick charts with volume and moving averages using mplfinance
- Parses VPA analysis from `VPA.md` or `VPA_week.md`
- Creates comprehensive `REPORT.md` with market analysis
- Supports smart caching to avoid redundant API calls
- Handles both daily (1D) and weekly (1W) intervals

**Key Features:**
- **Smart Caching**: Automatically caches downloaded data to avoid redundant API calls
- **Dual Timeframes**: Supports both daily and weekly analysis modes
- **VPA Integration**: Seamlessly integrates manual volume price analysis
- **Industry Grouping**: Categorizes stocks by industry using `ticker_group.json`
- **Professional Charts**: Generated candlestick charts with comprehensive technical indicators

## 📊 Data Management Scripts

### `get_market_cap.py` - Market Capitalization Data
Downloads and caches market capitalization data for all Vietnamese stocks.

```bash
# Fresh download
python get_market_cap.py

# Resume using existing data as cache
python get_market_cap.py --resume
```

**Features:**
- Fetches market cap data from Vietnamese exchanges
- Implements intelligent caching to prevent redundant API calls
- Supports resume mode for interrupted downloads
- Rate limiting to respect API constraints

### `merge_vpa.py` - VPA Data Combiner
Combines individual ticker VPA files from `vpa_data/` directory into main VPA file.

```bash
# Merge daily VPA analysis
python merge_vpa.py

# Merge weekly VPA analysis
python merge_vpa.py --week
```

**What it does:**
- Reads all individual ticker files from `vpa_data/` directory (e.g., `vpa_data/SIP.md`, `vpa_data/TPB.md`)
- Combines into single `VPA.md` or `VPA_week.md` file with proper formatting
- Maintains alphabetical ticker ordering with proper `# TICKER` headers
- Handles both daily and weekly modes
- Preserves existing analysis structure and formatting
- Creates backup of processed data automatically

### `merge_vpa_legacy.py` - Legacy VPA Merger
Legacy script for merging `VPA_NEW.md` into existing VPA files (kept for reference).

## 🧠 VPA Analysis Scripts

### VPA Data Files Structure
The system uses structured markdown files for VPA analysis:

- **`VPA.md`** - Daily VPA analysis (combined from vpa_data/)
- **`VPA_week.md`** - Weekly VPA analysis  
- **`vpa_data/{TICKER}.md`** - Individual ticker analysis files (primary workspace)
- **`VPA_NEW.md`** - Legacy format (used by old system)

**VPA Analysis Format:**
```markdown
# TICKER

- **Ngày 2025-07-13:** TICKER tăng từ 64.4 lên 64.9. Nến có biên độ hẹp...
    - **Phân tích VPA/Wyckoff:** Đây là một tín hiệu **No Demand**...

---
```

**Current Workflow:**
1. AI agents write analysis to individual `vpa_data/{TICKER}.md` files (e.g., `vpa_data/SIP.md`, `vpa_data/TPB.md`)
2. `merge_vpa.py` combines all ticker files into main `VPA.md` with proper formatting
3. `main.py` integrates VPA analysis into final reports and generates charts

## 🔍 Dividend Detection System

### `vpa_dividend_scanner.py` - Multi-Agent Dividend Scanner
**Advanced multi-agent system** that intelligently scans VPA data and compares with CSV prices to detect dividend adjustments.

```bash
# Scan daily data
python vpa_dividend_scanner.py

# Scan weekly data  
python vpa_dividend_scanner.py --week

# Use custom number of agents
python vpa_dividend_scanner.py --workers 8
```

**How it works:**
1. **Deploys multiple agents** (default: 8) to analyze tickers in parallel
2. **Extracts prices** from Vietnamese VPA text using intelligent regex patterns
3. **Compares with CSV data** using statistical analysis
4. **Detects dividend patterns** when prices show consistent adjustments
5. **Copies flagged files** to `market_data_check_dividends/` for AI processing

**Features:**
- **Multi-threaded processing** for speed and efficiency
- **Vietnamese text parsing** with intelligent price extraction
- **Statistical validation** (15%+ difference, 60%+ confidence required)
- **False positive prevention** with consistency checking
- **Detailed reporting** with JSON results and confidence scores

### `verify_dividends.py` - Legacy Dividend Checker
Original dividend detection script (now superseded by multi-agent scanner).

```bash
python verify_dividends.py
```

**Note:** This script has been replaced by the more advanced `vpa_dividend_scanner.py` but is kept for reference.

## 🛠 Utilities and Testing

### Utility Scripts
Development and maintenance utilities are located in the `utilities/` directory:

- **`split_vpa.py`** - Splits VPA.md into individual ticker files (one-time use)
- **`verify_vpa.py`** - Verifies VPA analysis accuracy against market data  
- **`test_vpa_scanner.py`** - Tests dividend scanner functionality
- **`verify_dividends.py`** - Legacy dividend checker (superseded)
- **`get_fund_data.py`** - Downloads Vietnamese fund data

See `utilities/README.md` for detailed usage instructions.

## ⚙️ Configuration Files

### Data Configuration
- **`TICKERS.csv`** - List of stock symbols to analyze (single column: `ticker`)
- **`FUNDS.csv`** - List of fund symbols for fund analysis  
- **`ticker_group.json`** - Industry groupings mapping groups to stock arrays

### VPA Configuration
- **`VPA.md`** - Main daily VPA analysis file
- **`VPA_week.md`** - Weekly VPA analysis file
- **`VPA_NEW.md`** - Staging file for new analysis to be merged

### Documentation
- **`tasks/dividends_plan.md`** - Complete guide for AI dividend processing
- **`tasks/DAILY_VPA.md`** - Complete protocol for daily VPA analysis workflow
- **`merge_vpa_legacy.py`** - Legacy VPA merger for reference (superseded by new merge_vpa.py)
- **`CLAUDE.md`** - Project instructions and architecture overview

## 🤖 GitHub Actions Workflows

### `.github/workflows/main.yml` - Daily Automation
Runs daily at 8:30 UTC (3:30 PM Vietnam time) after market close.

**Process:**
1. Backs up existing `market_data/` to `market_data_backup/`
2. Runs `python main.py --check-dividend`
3. Combines market data files
4. Commits and pushes results

### `.github/workflows/weekly.yaml` - Weekly Automation  
Runs weekly on Fridays at 20:00 UTC.

**Process:**
1. Backs up existing `market_data_week/` to `market_data_week_backup/`
2. Runs `python main.py --week --check-dividend`
3. Processes weekly data
4. Commits and pushes results

### `.github/workflows/funds.yaml` - Fund Analysis
Handles fund-specific analysis and reporting.

## 🚀 Usage Examples

### Basic Daily Analysis
```bash
# Download today's data and generate reports
python main.py

# The system will:
# 1. Download data for all tickers in TICKERS.csv
# 2. Generate candlestick charts in reports/
# 3. Create REPORT.md with comprehensive analysis
# 4. Cache data in market_data/
```

### Weekly Analysis with Dividend Detection
```bash
# Run weekly analysis with dividend checking
python main.py --week --check-dividend

# The system will:
# 1. Use market_data_week/ directory
# 2. Download weekly (1W) interval data
# 3. Check for dividend adjustments
# 4. Generate REPORT_week.md
# 5. Flag any dividend issues for AI processing
```

### Dividend Detection Workflow
```bash
# 1. Run multi-agent dividend scanner
python vpa_dividend_scanner.py

# 2. If dividends detected, files will be in:
#    market_data_check_dividends/

# 3. AI should process according to:
#    tasks/dividends_plan.md
```

### Daily VPA Analysis Workflow
```bash
# 1. Check for dividend adjustments
ls market_data_check_dividends/

# 2. Process individual tickers (AI agents)
# Write analysis to vpa_data/{TICKER}.md files
# Example: echo "# SIP\n\n- **Analysis here...**" > vpa_data/SIP.md

# 3. Verify analysis accuracy
# Review individual files in vpa_data/ directory

# 4. Combine all ticker files into main VPA
python merge_vpa.py
# This reads all vpa_data/*.md files and combines into VPA.md

# 5. Generate final report with integrated VPA
python main.py
# Creates REPORT.md with charts and VPA analysis

# Complete protocol documented in tasks/DAILY_VPA.md
```

## 📁 Directory Structure

```
aipriceaction/
├── 📄 main.py                     # Primary data pipeline
├── 📄 get_market_cap.py          # Market cap data fetcher  
├── 📄 merge_vpa.py               # VPA analysis merger
├── 📄 vpa_dividend_scanner.py   # Multi-agent dividend scanner
├── 📂 utilities/                # Development and testing utilities
│   ├── 📄 README.md             # Utilities documentation
│   ├── 📄 split_vpa.py          # VPA file splitter
│   ├── 📄 verify_vpa.py         # VPA accuracy verifier
│   ├── 📄 test_vpa_scanner.py   # Scanner testing utility
│   ├── 📄 verify_dividends.py   # Legacy dividend checker
│   └── 📄 get_fund_data.py      # Fund data downloader
├── 
├── 📊 TICKERS.csv               # Stock symbols list
├── 📊 FUNDS.csv                 # Fund symbols list  
├── 📊 ticker_group.json         # Industry groupings
├── 
├── 📝 VPA.md                    # Daily VPA analysis
├── 📝 VPA_week.md               # Weekly VPA analysis
├── 📝 VPA_NEW.md                # New analysis staging
├── 
├── 📈 REPORT.md                 # Daily report output
├── 📈 REPORT_week.md            # Weekly report output
├── 
├── 📂 market_data/              # Daily CSV data
├── 📂 market_data_week/         # Weekly CSV data  
├── 📂 market_data_backup/       # Backup data for dividend detection
├── 📂 market_data_processed/    # Processed/archived data
├── 📂 market_data_check_dividends/ # Dividend-flagged files
├── 
├── 📂 reports/                  # Daily chart images
├── 📂 reports_week/             # Weekly chart images
├── 📂 funds_data/               # Fund performance data
├── 📂 vpa_data/                 # Individual ticker VPA files
├── 
├── 📂 tasks/                    # Task documentation
│   └── 📄 dividends_plan.md     # AI dividend processing guide
├── 
├── 📂 docs/                     # Documentation
│   └── 📄 README.md             # This file
├── 
├── 📂 .github/workflows/        # GitHub Actions
│   ├── 📄 main.yml             # Daily automation
│   ├── 📄 weekly.yaml          # Weekly automation
│   └── 📄 funds.yaml           # Fund analysis
└── 
└── 📄 CLAUDE.md                 # Project instructions for AI
```

## 🎯 Key Workflows

### 1. Daily Market Analysis
```mermaid
graph LR
    A[GitHub Actions] --> B[Backup market_data]
    B --> C[Run main.py --check-dividend]
    C --> D[Download fresh data]
    D --> E[Check for dividends]
    E --> F[Generate charts & reports]
    F --> G[Commit results]
```

### 2. Dividend Detection Process
```mermaid
graph LR
    A[VPA Dividend Scanner] --> B[Deploy 8 Agents]
    B --> C[Extract VPA prices]
    C --> D[Compare with CSV]
    D --> E[Statistical analysis]
    E --> F[Flag dividend files]
    F --> G[AI processes flagged files]
```

### 3. VPA Analysis Integration
```mermaid
graph LR
    A[Write analysis in vpa_data/{TICKER}.md] --> B[Run merge_vpa.py]
    B --> C[Combine all ticker files]
    C --> D[Generate VPA.md]
    D --> E[Run main.py with integrated VPA]
```

## 🔧 Environment Setup

### Required Environment Variables
```bash
export ACCEPT_TC="tôi đồng ý"  # For vnstock library
```

### Dependencies
```bash
pip install -r requirements.txt
# or
uv run python main.py  # Auto-installs dependencies
```

### Key Libraries
- **vnstock** - Vietnamese stock data provider
- **mplfinance** - Professional financial charting
- **pandas** - Data manipulation and analysis
- **matplotlib** - Chart generation and visualization

## 🚨 Important Notes

- **API Rate Limiting**: All scripts include delays to respect API constraints
- **Data Caching**: Smart caching prevents redundant API calls and speeds up processing
- **Error Handling**: Comprehensive error handling with graceful degradation
- **Vietnamese Support**: Full UTF-8 support for Vietnamese text and currency formatting
- **Dividend Safety**: Multi-layer validation prevents false positive dividend detection
- **Production Ready**: Automated workflows with proper error handling and logging

## 🆘 Troubleshooting

### Common Issues

1. **"No module named 'pandas'"**
   ```bash
   # Use uv for automatic dependency management
   uv run python main.py
   ```

2. **"ACCEPT_TC environment variable not set"**
   ```bash
   export ACCEPT_TC="tôi đồng ý"
   ```

3. **"No data found for ticker"**
   - Check if ticker exists in Vietnamese market
   - Verify TICKERS.csv format (single column named 'ticker')
   - Check network connectivity

4. **"Dividend false positives"**
   - Use `vpa_dividend_scanner.py` instead of legacy `verify_dividends.py`
   - Multi-agent scanner has better accuracy with statistical validation

5. **"VPA analysis not appearing in reports"**
   - Ensure VPA.md follows correct format with `# TICKER` headers
   - Run `merge_vpa.py` to properly structure VPA files
   - Check that ticker names match between VPA.md and TICKERS.csv

### Getting Help

- Check `CLAUDE.md` for detailed project instructions
- Review `tasks/dividends_plan.md` for dividend processing guidance
- Run test scripts to validate system functionality
- Check GitHub Actions logs for automated workflow issues

---

## 📚 Hệ Thống Giáo Dục VPA & Phương Pháp Wyckoff

### Tổng Quan

Dự án này bao gồm một **hệ thống giáo dục toàn diện bằng tiếng Việt** về Phân Tích Khối Lượng Giá (VPA) và các nguyên lý Phương Pháp Wyckoff. Hệ thống tutorial này đại diện cho một bản dịch và nâng cấp hoàn chỉnh của giáo dục giao dịch cấp tổ chức, được điều chỉnh đặc biệt cho thị trường Việt Nam với các ví dụ dữ liệu thị trường thực tế.

### 🎓 Triết Lý Giáo Dục & Phương Pháp Tiếp Cận

**Thiết Kế Học Tập Tiến Bộ:**
Hệ thống tutorial tuân theo một tiến trình có cấu trúc cẩn thận từ **các khái niệm cấp đại học** (độ khó 9.2/10) đến **kiến thức chuyên gia tổ chức** (độ khó 10/10), đảm bảo chuyển giao kiến thức mượt mà mà không làm choáng ngợp người mới bắt đầu.

**Tích Hợp Thị Trường Thực Tế:**
Mọi khái niệm đều được minh họa bằng **dữ liệu cổ phiếu Việt Nam thực tế** từ các thư mục `market_data/` và `vpa_data/` của pipeline, cung cấp trải nghiệm học tập chân thực thay vì các ví dụ lý thuyết.

**Thuật Ngữ Tài Chính Việt Nam:**
Tất cả các khái niệm kỹ thuật đã được dịch chuyên nghiệp sử dụng thuật ngữ tài chính Việt Nam phù hợp, làm cho các khái niệm VPA nâng cao có thể tiếp cận được đối với các nhà đầu tư nói tiếng Việt lần đầu tiên.

### 📖 Các Chương Tutorial - Phân Tích Chi Tiết

#### **Khái Niệm Cơ Bản (Chương 1.1-1.3)**

**Chương 1.1: Căn Bản VPA (Tiếng Việt)**
- **Mục Đích:** Giới thiệu các nguyên tắc cơ bản của Phân Tích Khối Lượng Giá
- **Khái Niệm Chính:** 
  - Động lực mối quan hệ khối lượng-giá
  - Hành vi dòng tiền thông minh vs dòng tiền retail
  - Nhận dạng tín hiệu VPA cơ bản
- **Dữ Liệu Thực Tế:** Sử dụng cổ phiếu Việt Nam thực tế từ `market_data/` với phân tích VPA tiếng Việt từ `vpa_data/`
- **Thuật Ngữ Việt Nam:** Khối lượng (Volume), Giá (Price), Phân tích (Analysis), Smart Money (Dòng tiền thông minh)

**Chương 1.2: Các Định Luật Wyckoff (Tiếng Việt)**
- **Mục Đích:** Ba định luật cơ bản chi phối hành vi thị trường
- **Khái Niệm Chính:**
  - Luật Cung - Cầu (Law of Supply & Demand)
  - Luật Nhân - Quả (Law of Cause & Effect)
  - Luật Nỗ lực vs Kết quả (Law of Effort vs Result)
- **Tích Hợp Thị Trường:** Ví dụ từ chuyển động VNINDEX và luân chuyển ngành
- **Bối Cảnh Việt Nam:** Điều chỉnh cho đặc điểm thị trường và mô hình giao dịch Việt Nam

**Chương 1.3: Composite Man (Tiếng Việt)**
- **Mục Đích:** Hiểu góc nhìn tổ chức
- **Khái Niệm Chính:**
  - Chiến thuật tích lũy/phân phối của dòng tiền thông minh
  - Nhận dạng thao túng thị trường
  - Mô hình hành vi tổ chức vs retail
- **Phương Pháp Giáo Dục:** Sử dụng các công ty dẫn đầu thị trường Việt Nam (VIC, VCB, FPT) làm ví dụ

#### **Các Giai Đoạn Thị Trường (Chương 2.1-2.2)**

**Chương 2.1: Các Pha Tích Lũy (Tiếng Việt)**
- **Độ Sâu:** Phân tích chi tiết tất cả 5 pha tích lũy Wyckoff
- **Ví Dụ Thực Tế:** Sử dụng các mô hình tích lũy thực tế từ blue chips Việt Nam
- **Tích Hợp Kỹ Thuật:** Biểu đồ được tạo bởi `main.py` với thư viện mplfinance
- **Thuật Ngữ Việt Nam:** Tích lũy (Accumulation), Pha (Phase), Kiểm tra (Test)

**Chương 2.2: Các Pha Phân Phối (Tiếng Việt)**
- **Mục Đích:** Nhận dạng các mô hình bán tổ chức
- **Thông Đảm Quan Trọng:** Dấu hiệu cảnh báo sớm của đỉnh thị trường
- **Nghiên Cứu Tình Huống:** Ví dụ phân phối thị trường Việt Nam lịch sử
- **Quản Lý Rủi Ro:** Khung đánh giá rủi ro đặc thù Việt Nam

#### **Nhận Dạng Tín Hiệu (Chương 3.1-3.2)**

**Chương 3.1: Tín Hiệu VPA Tăng Giá (Tiếng Việt)**
- **Bao Phủ Toàn Diện:** Tất cả các mô hình VPA tăng giá chính
- **Các Loại Tín Hiệu:**
  - No Supply (Không có Nguồn Cung)
  - Sign of Strength (Dấu hiệu Mạnh mẽ)
  - Effort to Rise (Nỗ lực Tăng giá)
  - Test for Supply (Kiểm tra Nguồn cung)
- **Tích Hợp Dữ Liệu Thực Tế:** Sử dụng trích dẫn chính xác từ các file `vpa_data/{TICKER}.md`
- **Ứng Dụng Thực Tế:** Tích hợp trực tiếp với quy trình VPA hàng ngày

**Chương 3.2: Tín Hiệu VPA Giảm Giá (Tiếng Việt)**
- **Khung Hoàn Chỉnh:** Tất cả các mô hình giảm giá chính và cảnh báo
- **Nhận Dạng Tín Hiệu:**
  - Sign of Weakness (Dấu hiệu Yếu kém)
  - No Demand (Không có Nhu cầu)
  - Effort to Fall (Nỗ lực Giảm giá)
  - Các mô hình phân phối
- **Bối Cảnh Thị Trường Việt Nam:** Điều chỉnh cho hành vi và chu kỳ thị trường địa phương

#### **Khái Niệm Nâng Cao (Chương 5.1-5.4)**

**Chương 5.1: Nhận Dạng Mô Hình Nâng Cao**
- **Nội Dung Cấp Tổ Chức:** Kỹ thuật phân tích mô hình chuyên nghiệp
- **Mô Hình Phức Tạp:** Chu kỳ tích lũy/phân phối đa pha
- **Phần Tìm Hiểu Sâu:** Giải thích nâng cao cho các khái niệm phức tạp
- **Tích Hợp Việt Nam:** Sử dụng ví dụ cổ phiếu Việt Nam toàn diện

**Chương 5.2: Engine Backtesting Tổ Chức**
- **Độ Sâu Kỹ Thuật:** Xây dựng khung kiểm tra VPA có hệ thống
- **Tích Hợp Code:** Hoạt động với cấu trúc dữ liệu CSV của pipeline
- **Xác Thực Thống Kê:** Phương pháp backtesting đặc thù thị trường Việt Nam
- **Chỉ Số Hiệu Suất:** Tính toán ROI được điều chỉnh cho chi phí giao dịch Việt Nam

**Chương 5.3: Phân Tích Dòng Tiền Thông Minh**
- **Kỹ Thuật Nâng Cao:** Theo dõi chuyển động tiền tổ chức
- **Chỉ Báo Dòng Chảy:** Phát hiện dòng tiền thông minh dựa trên khối lượng
- **Bối Cảnh Việt Nam:** Điều chỉnh cho mô hình hành vi tổ chức Việt Nam
- **Tích Hợp:** Sử dụng `market_data/` cho tính toán phân tích dòng chảy

**Chương 5.4: Nhận Dạng Mô Hình Machine Learning**
- **Phương Pháp Tiên Tiến:** Phát hiện tín hiệu VPA được hỗ trợ AI
- **Triển Khai Kỹ Thuật:** Nhận dạng mô hình ML dựa trên Python
- **Tích Hợp Dữ Liệu:** Tận dụng thu thập dữ liệu toàn diện của pipeline
- **Điều Chỉnh Việt Nam:** Mô hình ML được đào tạo trên mô hình thị trường Việt Nam

### 🎯 Nghiên Cứu Tình Huống: Chiến Dịch Tích Lũy 2025 - Phân Tích Sâu

#### **Phương Pháp Giáo Dục**

Mỗi nghiên cứu tình huống đại diện cho một **phân tích chiến dịch tích lũy tổ chức hoàn chỉnh** sử dụng dữ liệu thị trường Việt Nam thực tế từ năm 2025. Đây không phải là các ví dụ lý thuyết mà là các sự kiện thị trường thực tế với phân tích VPA được ghi chép.

#### **Cấu Trúc & Thông Đảm Nghiên Cứu Tình Huống**

**VIC - Chiến Dịch Tích Lũy Bất Động Sản 2025**
- **Tập Trung Ngành:** Phân tích vai trò dẫn dắt thị trường bất động sản
- **Loại Mô Hình:** Minh chứng chuỗi VPA hoàn hảo
- **Học Hỏi Chính:** Cách các công ty dẫn đầu bất động sản hoạt động trong phục hồi thị trường
- **Nguồn Dữ Liệu:** Phân tích VPA thực tế từ `vpa_data/VIC.md`
- **Thông Đảm Việt Nam:** 
  - "Đây là một tín hiệu Effort to Rise mạnh mẽ"
  - "Lực cầu đã quay trở lại quyết đoán"
- **Giảng Dạy Kỹ Thuật:** Xác nhận markup Phase D với phân tích khối lượng
- **Rủi Ro/Lợi Nhuận:** Chiến lược định cỡ vị thế và cắt lỗ thế giới thực

**VHM - Chiến Dịch Tích Lũy Biến Động 2025**
- **Tập Trung Biến Động:** Mô hình tích lũy cổ phiếu beta cao
- **Khái Niệm Nâng Cao:** Quản lý mô hình tích lũy biến động
- **Động Lực Ngành:** Vinhomes như cổ phiếu beta bất động sản
- **Nhận Dạng Mô Hình:** Tích lũy phạm vi rộng với biến động cao
- **Bối Cảnh Thị Trường Việt Nam:** Hiểu chu kỳ bất động sản Việt Nam
- **Thông Đảm Chuyên Nghiệp:** Cách tổ chức xử lý tích lũy biến động

**SSI - Chiến Dịch Tích Lũy Nhà Vô Địch Ngành Chứng Khoán 2025**
- **Luân Chuyển Ngành:** Thời điểm phục hồi dịch vụ tài chính
- **Mô Hình Nâng Cao:** Nhận dạng và phản ứng Shakeout
- **Mô Hình Kinh Doanh:** Đặc điểm và chu kỳ ngành chứng khoán
- **Bối Cảnh Việt Nam:** Hiểu động lực môi giới địa phương
- **Thành Thạo Kỹ Thuật:** Chuỗi Shakeout → Phục hồi hoàn hảo
- **Ứng Dụng Chuyên Nghiệp:** Chiến lược đầu tư luân chuyển ngành

**VIX - Chiến Dịch Tích Lũy Gã Khổng Lồ Cơ Sở Hạ Tầng 2025**
- **Phân Tích Chu Kỳ:** Thời điểm và mô hình ngành cơ sở hạ tầng
- **Đảo Chiều Mô Hình:** Chuyển đổi từ phân phối sang tích lũy
- **Bối Cảnh Kinh Tế:** Chi tiêu Chính phủ và chu kỳ cơ sở hạ tầng
- **Nhận Dạng Nâng Cao:** Xác định tín hiệu đảo chiều sớm
- **Kinh Tế Việt Nam:** Chu kỳ và thời điểm đầu tư cơ sở hạ tầng
- **Đầu Tư Chiến Lược:** Phương pháp đầu tư cơ sở hạ tầng dài hạn

**LPB - Chiến Dịch Tích Lũy Chuyển Đổi Ngân Hàng 2025**
- **Ví Dụ Sách Giáo Khoa:** Minh chứng chuỗi VPA hoàn hảo
- **Ngân Hàng Khu Vực:** Câu chuyện chuyển đổi ngân hàng nhỏ hơn
- **Hoàn Hảo Tuần Tự:** No Supply → Test → SOS → Markup
- **Tích Hợp Dữ Liệu Chính Xác:** Sử dụng trích dẫn chính xác từ `vpa_data/LPB.md`:
  - "Đây là một tín hiệu No Supply (Không có Nguồn Cung) rõ ràng"
  - "Test for Supply (Kiểm tra Nguồn cung)"
  - "Sign of Strength (SOS), là kết quả của các tín hiệu No Supply và Test for Supply thành công"
- **Chuyển Đổi Ngân Hàng:** Chủ đề hiện đại hóa ngân hàng khu vực
- **Thực Thi Chuyên Nghiệp:** Chiến lược vào và ra lệnh tổ chức

### 🔄 Integration with Pipeline Data

#### **Real-Time Learning**
The tutorial system is **directly integrated** with the pipeline's live data:

- **Tutorial Examples ←→ `market_data/` CSV files**
- **VPA Analysis ←→ `vpa_data/{TICKER}.md` files**  
- **Chart Integration ←→ `reports/` generated images**
- **Live Updates ←→ Daily `main.py` execution**

#### **Educational Data Flow**
```mermaid
graph LR
    A[Live Market Data] --> B[VPA Analysis in vpa_data/]
    B --> C[Tutorial Examples]
    C --> D[Student Learning]
    D --> E[Applied Analysis]
    E --> A
```

### 🎓 Learning Path Recommendations

#### **Beginner Path (0-3 months)**
1. Start with Chapter 1.1 (VPA Basics)
2. Master Chapter 1.2 (Wyckoff Laws)  
3. Read VIC case study for practical application
4. Practice with live `VPA.md` daily analysis

#### **Intermediate Path (3-6 months)**
1. Complete Chapters 2.1-2.2 (Market Phases)
2. Study all 5 case studies in sequence
3. Begin writing own VPA analysis in `vpa_data/` format
4. Use `merge_vpa.py` workflow for practice

#### **Advanced Path (6+ months)**
1. Master Chapters 3.1-3.2 (Signal Recognition)
2. Implement Chapter 5.1-5.4 (Advanced Concepts)
3. Develop personal trading systems using pipeline data
4. Contribute to VPA analysis using institutional-grade methodology

### 🇻🇳 Vietnamese Market Adaptation

#### **Cultural & Market Context**
- **Trading Hours:** Adapted for Vietnamese market sessions (9:00-15:00)
- **Settlement:** T+2 settlement cycle considerations
- **Regulations:** Vietnamese market regulations and restrictions
- **Currency:** VND-specific calculations and risk management
- **Broker Integration:** Compatible with Vietnamese brokerage platforms

#### **Linguistic Excellence**
- **Financial Terminology:** Professional Vietnamese financial vocabulary
- **Technical Precision:** Accurate translation of complex VPA concepts
- **Cultural Adaptation:** Vietnamese business culture and investment mentality
- **Educational Style:** Vietnamese pedagogical approaches and learning preferences

### 🛠 Technical Implementation

#### **File Structure Integration**
```
docs/tutorials/
├── vpa-basics-vi.md              # Chapter 1.1
├── wyckoff-laws-vi.md             # Chapter 1.2  
├── composite-man-vi.md            # Chapter 1.3
├── accumulation-phases-vi.md      # Chapter 2.1
├── distribution-phases-vi.md      # Chapter 2.2
├── bullish-vpa-signals-vi.md      # Chapter 3.1
├── bearish-vpa-signals-vi.md      # Chapter 3.2
├── trading-systems-vi.md          # Chapter 4.1
├── advanced-pattern-recognition.md # Chapter 5.1
├── institutional-backtesting.md    # Chapter 5.2
├── smart-money-flow.md            # Chapter 5.3
├── ml-pattern-recognition.md      # Chapter 5.4
└── case-studies/
    ├── vic-accumulation-2025.md   # VIC case study
    ├── vhm-accumulation-2025.md   # VHM case study
    ├── ssi-accumulation-2025.md   # SSI case study  
    ├── vix-accumulation-2025.md   # VIX case study
    └── lpb-accumulation-2025.md   # LPB case study
```

#### **Data Dependencies**
- **Market Data:** `market_data/{TICKER}_2025-01-02_to_2025-07-21.csv`
- **VPA Analysis:** `vpa_data/{TICKER}.md` 
- **Charts:** `reports/{TICKER}_chart.png`
- **Configuration:** `ticker_group.json` for sector analysis

### 🎯 Educational Outcomes

#### **Student Achievements**
Upon completion, students will be able to:

1. **Recognize Institutional Activity:** Identify smart money accumulation/distribution
2. **Time Market Entries:** Use VPA signals for optimal position timing  
3. **Manage Risk:** Apply Vietnamese market-specific risk management
4. **Sector Analysis:** Understand Vietnamese market sector rotation
5. **Professional Analysis:** Write institutional-grade VPA analysis
6. **System Integration:** Use pipeline tools for ongoing market analysis

#### **Professional Application**
- **Portfolio Management:** Institutional-grade stock selection
- **Risk Assessment:** Vietnamese market-specific risk frameworks
- **Sector Allocation:** Industry rotation strategies using Vietnamese market dynamics
- **Performance Measurement:** ROI calculation with Vietnamese trading costs
- **Continuous Learning:** Integration with live market data for ongoing education

### 🔗 Navigation & Resources

#### **Quick Access Links**
- **[Tutorial Map & Content Overview](MAP_OF_CONTENT.md)** - Complete curriculum structure
- **[VPA Methods & Methodology](methods/README.md)** - Technical methodology documentation
- **Main Pipeline Integration:** All tutorials work seamlessly with `main.py` and data pipeline

#### **Support Materials**
- **Live Data:** Updated daily through GitHub Actions workflow
- **Vietnamese Support:** Full UTF-8 support with proper Vietnamese financial terminology
- **Chart Integration:** Professional mplfinance charts with Vietnamese labels
- **Real-time Examples:** Examples update automatically with market data

---

**Made with ❤️ for Vietnamese stock market analysis and education**