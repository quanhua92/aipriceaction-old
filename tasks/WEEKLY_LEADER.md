# Weekly Leader Analysis Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `LEADER.md` file using the VPA-SectorLead methodology with **manual natural language analysis only**. No unreliable Python text parsing utilities.

**⚠️ CRITICAL: ALWAYS USE ACTUAL DATA DATES**
- Never assume "today's date" or "this week" for analysis
- Always get the actual last available date from CSV files using `df.iloc[-1]["Date"]`
- Use `glob.glob()` to find the most recent CSV file for each ticker
- Compare actual data dates with existing analysis dates to determine if new analysis is needed

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current

**Use LS tool to check for required input files:**
- Verify paths: `GROUP.md`, `REPORT_week.md`
- Verify directories: `vpa_data_week/`, `market_data_week/`

**Manual Verification Actions**:
- **Use Read tool** to verify `GROUP.md` exists with sector-to-ticker mappings
- **Use LS tool** to verify `vpa_data_week/` directory exists with individual ticker weekly VPA files
- **Use Read tool** to verify `REPORT_week.md` exists with weekly analysis and signals
- **Use LS tool** to verify `market_data_week/` directory exists with individual ticker weekly CSV files (last 6 months)

**Success Criteria**: All core input files are present and accessible through manual verification

### Step 2: STAGE 0 - Manual Ticker Profile Creation
**Objective**: Create verified internal ticker profiles for ALL tickers using manual natural language analysis

**Manual Processing Approach**: Use Task tools to process sectors with **manual natural language analysis guidance**, with each sector processing its tickers through human intelligence.

**Critical Manual Process**: For EVERY ticker from GROUP.md, manually create this internal data structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "sector": "Sector name from GROUP.md - manually verified",
  "full_vpa_story_summary": "Concise summary from vpa_data_week/{TICKER}.md - manually analyzed",
  "recent_vpa_signals": [
    {"signal": "SOS Bar - manually identified", "date": "2025-07-07"},
    {"signal": "Test for Supply - manually identified", "date": "2025-06-30"}
  ],
  "price_history_data": "Raw weekly OHLCV from most recent market_data_week/{TICKER}_*.csv using reliable Python with glob.glob()",
  "base_period_start": "Sector base period start date - manually determined",
  "base_period_end": "Sector base period end date - manually determined"
}
```

**Manual File Reading Strategy for Each Ticker**:
1. **Use Read tool** to manually read `vpa_data_week/{TICKER}.md` for complete weekly VPA story - manual analysis
2. **Use reliable Python** to read the most recent `market_data_week/{TICKER}_*.csv` file for price history and calculations:
```bash
# Example reliable Python for weekly price data - gets most recent CSV file
uv run -c "
import pandas as pd
import glob
ticker = 'VHM'
try:
    # Find the most recent weekly CSV file for this ticker
    csv_files = glob.glob(f'market_data_week/{ticker}_*.csv')
    if not csv_files:
        print(f'No weekly CSV files found for {ticker}')
    else:
        # Get the most recent file by modification time or filename
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        latest = df.iloc[-1]  # Last row = most recent week
        print(f'{ticker}: Latest week ending {latest[\"Date\"]}, Close={latest[\"Close\"]}')
        print(f'CSV file: {latest_file}')
        print(f'Weekly data range: {df.iloc[0][\"Date\"]} to {df.iloc[-1][\"Date\"]}')
        print(f'Performance: {((df.iloc[-1][\"Close\"] / df.iloc[0][\"Close\"]) - 1) * 100:.2f}%')
except Exception as e:
    print(f'Could not read CSV for {ticker}: {e}')
"
```
3. **Manual extraction** of recent VPA signals from ticker file (last 2-3 significant signals) using human intelligence
4. **Manual calculation** of performance from sector base period to latest close

**Manual Data Extraction Rules**:
- **Manual extraction** of sector mappings from `GROUP.md` using Read tool
- **Manual extraction** of VPA story summaries from individual `vpa_data_week/{TICKER}.md` files using Read tool
- **Manual extraction** of recent signals from both individual VPA files and `REPORT_week.md` using Read tool
- **Reliable Python only** for price data from individual `market_data_week/{TICKER}_*.csv` files

**Manual Processing Strategy**:
- Use Task tools to process multiple tickers with **manual analysis instructions**
- **NO automated text parsing** - all VPA signal identification through human intelligence
- Read ticker-specific files using Read tool for VPA data and reliable Python for CSV data
- **Manual verification** of all extracted information

**Quality Control**: These manually created ticker profiles become the SOLE source of truth for all subsequent stages

**Example Manual Task Tool Usage by Sector**:
```
Task 1: "MANUAL ANALYSIS ONLY - Process NGÂN HÀNG sector tickers (TCB,VCB,MBB,STB,CTG,VPB,LPB,ACB,HDB,TPB,SHB,VIB,BID) for weekly leader analysis. For each: 1) Use Read tool to manually read vpa_data_week/{TICKER}.md full story and manually analyze VPA narrative 2) Use reliable Python to read market_data_week/{TICKER}_*.csv for price history 3) Manually identify recent VPA signals using human intelligence 4) Return manually-created ticker profile JSON with VPA summary and recent signals. NO automated text parsing."

Task 2: "MANUAL ANALYSIS ONLY - Process BẤT ĐỘNG SẢN sector tickers (VHM,VIC,NVL,KDH,HDG,VRE) for weekly leader analysis. Same manual process as Task 1. Use Read tool for VPA analysis, reliable Python for CSV data, manual signal identification."
```

**Manual Sector-Level Processing**:
- Process 3-5 sectors concurrently using Task tools with **manual analysis guidance**
- Each sector processes its tickers through **human intelligence analysis**
- **Individual weekly VPA files**: Read using Read tool - ~100-300 lines focused analysis
- **Individual weekly CSV files**: Process using reliable Python - ~30 rows clean data
- **Manual verification** of all extracted information before proceeding

### Step 3: STAGE 1 - Manual Sector Aggregation & Universe Definition
**Objective**: Define eligible sectors for analysis using manual counting and verification

**Manual Process**:
1. **Manual Sector Universe Loading**: **Use Read tool** to manually read `GROUP.md` to get all sector definitions
2. **Manual Eligible Sectors Definition**: **Manual counting** to process ONLY sectors with at least 3 tickers
3. **Manual Filter Rule**: **Human verification** - sectors with fewer than 3 tickers are omitted from analysis through manual counting

**Output**: Manually verified list of eligible sectors for comprehensive analysis

### Step 4: STAGE 2 - Manual Sector Base Period Identification
**Objective**: Identify common base periods for each eligible sector using manual analysis

**Manual Methodology**:
1. **Manual 6-Month History Analysis**: **Use reliable Python** to review weekly OHLCV data from individual `market_data_week/{TICKER}_*.csv` files
2. **Manual Stability Phases Identification**: **Human intelligence** to find periods where majority of sector tickers showed:
   - Low volatility or sideways price action - manually identified from price data
   - Clear VPA signs of accumulation (No Supply bars, low volume tests) - manually identified from VPA files
   - Common consolidation patterns - manually recognized through chart analysis
3. **Manual Base Period Definition**: **Human judgment** to establish date range representing sector-wide accumulation/stability phase
4. **Manual Sector Exclusion**: **Human decision** to omit sectors without clear common base periods

**Manual Data Sources**:
- **Reliable Python** for historical price analysis from individual CSV files
- **Read tool** for VPA pattern analysis from individual weekly VPA files
- **Human intelligence** for pattern recognition and period identification

**Output**: Manually determined base period date ranges for each eligible sector

### Step 5: STAGE 3 - Manual Individual Ticker Analysis & Scoring
**Objective**: Calculate leadership scores for all tickers within eligible sectors using manual analysis

**Manual Scoring Framework** (using manually created ticker profiles and manually determined base periods):

#### 5.1 Manual VPA Story Score (Weight: 60%)
**Scale**: 0-100 points
**Manual Assessment Criteria**:
- **90-100**: Perfect multi-stage Wyckoff story (Accumulation → Shakeout → SOS → successful Backing Up/Test) - manually identified
- **70-89**: Strong story with minor imperfections or still developing - manually assessed
- **<70**: Weak, unclear, or broken VPA narrative - manually determined

**Data Source**: `full_vpa_story_summary` from manually created ticker profiles through human intelligence

#### 5.2 Manual Relative Performance Score (Weight: 40%)
**Manual Calculation**: Percentage price change from sector base period start to most recent weekly close
**Scale**: Direct percentage (25% gain = 25 points)
**Data Source**: `price_history_lookup` from manually created ticker profiles using reliable Python calculations

#### 5.3 Manual Confidence Score (Reporting Only)
**Scale**: 0-100%
**Manual Assessment Criteria**:
- **90-100%**: Textbook VPA setup, clear recent signals, low risk - manually assessed
- **75-89%**: Strong setup with some ambiguity, needs confirmation - manually evaluated
- **<75%**: Conflicting signals, high risk, broken narrative - manually identified

**Data Source**: `recent_vpa_signals` from manually created ticker profiles through human intelligence

#### 5.4 Manual Final Leadership Score Calculation
**Manual Formula**: `Leadership Score = (VPA Story Score × 0.6) + (Relative Performance Score × 0.4)`
**Manual Ranking**: **Human judgment** to select top 3 tickers per sector as "Sector Leaders"

### Step 6: STAGE 4 - Manual Sector Health & Context Analysis
**Objective**: Evaluate overall sector character and health using manual analysis

**Manual Analysis Framework**:

#### 6.1 Manual Trend Breadth Calculation
- **Manual calculation** of percentage of sector tickers with positive relative performance
- **Manual assessment**: High breadth (>70%) vs. Low breadth (<70%) using human counting

#### 6.2 Manual VPA Signal Cohesion Assessment
- **Manual scan** of `recent_vpa_signals` across all sector tickers from manually created profiles
- **Human intelligence** to identify dominant theme: Bullish (SOS, Test, No Supply) vs. Bearish (SOW, Upthrust)

#### 6.3 Manual Sector Classification (Mandatory)
**Manual Categories** (determined through human analysis):
- **Dẫn Dắt Đồng Thuận**: High breadth (>70%), cohesive bullish signals, strong broad-based rally - manually verified
- **Dẫn Dắt Phân Hóa**: Low breadth (<70%), mixed signals, narrow leadership - manually assessed
- **Đang Tích Lũy**: Sideways movement, flat performance, No Supply signals common - manually identified
- **Yếu/Phân Phối**: Low breadth, negative performance, SOW/Upthrust prevalent - manually determined

### Step 7: STAGE 5 - Manual LEADER.md Generation
**Objective**: Generate complete LEADER.md using manually verified profiles and manual analysis

#### 7.1 File Header Generation
```markdown
# Phân Tích Cổ Phiếu Dẫn Dắt Theo Ngành

Báo cáo này xác định các cổ phiếu dẫn dắt và đánh giá sức khỏe tổng thể của từng ngành. Phân tích dựa trên sự kết hợp giữa: (1) Sức mạnh câu chuyện VPA/Wyckoff, (2) Hiệu suất giá tương đối, và (3) Mức độ lan tỏa của xu hướng trong nội bộ ngành.

**➡️ [Click here to view the latest market report](REPORT.md)**
**➡️ [Click here to view the latest market report (weekly)](REPORT_week.md)**
**⛳ [Click here to view the trading plan](PLAN.md)**
```

#### 7.2 Table of Contents Generation
- Generate alphabetically sorted (A-Z) list of eligible sectors
- Each sector as Markdown link to corresponding section
- Format: `- [**SECTOR_NAME**](#sector-name)`

#### 7.3 Detailed Sector Analysis (Alphabetical Order)
For EACH eligible sector, generate using this template:

```markdown
## **[SECTOR_NAME]**

* **Giai Đoạn Nền Giá Tham Chiếu:** [Base Period Start] - [Base Period End]
* **Đánh Giá Tổng Quan Ngành:** **[Sector Classification]**. [Detailed narrative explaining sector health, breadth, signal cohesion, and leadership characteristics]

**Bảng Xếp Hạng Cổ Phiếu Dẫn Dắt:**

| Hạng | Mã CP & Liên Kết | Điểm Dẫn Dắt | Độ tin cậy | Tóm Tắt Lý Do |
| :--- | :--------------- | :----------- | :--------- | :------------ |
| 1    | [**TICKER**](#TICKER) | [Score] | [Confidence] | [Reasoning] |
| 2    | [**TICKER**](#TICKER) | [Score] | [Confidence] | [Reasoning] |
| 3    | [**TICKER**](#TICKER) | [Score] | [Confidence] | [Reasoning] |

---

### **Phân Tích Chi Tiết Top 3:**

---

#### **1. [Company Name] ([TICKER])**

![View Chart](reports_week/[TICKER]/[TICKER]_candlestick_chart.png)

* [View Report](REPORT_week.md#[TICKER])
* **Các Chỉ Số Chính:**
  * **Điểm Câu Chuyện VPA:** [VPA Story Score] / 100
  * **Điểm Hiệu Suất Tương Đối:** [Relative Performance Score] (tương ứng +[X]% change)
  * **Mức Độ Tin Cậy:** [Confidence Score]%
* **Phân Tích Dẫn Dắt:** [Explanation of why this ticker leads, comparing to sector peers within sector health context]
* **Câu Chuyện VPA Nổi Bật:** [Summary of key VPA/Wyckoff signals based on full_vpa_story_summary]
* **Hiệu Suất Tương Đối:** [Quantitative performance statement vs sector average]

---

#### **2. [Company Name] ([TICKER])**
[Same format as above]

---

#### **3. [Company Name] ([TICKER])**
[Same format as above]
```

### Step 8: Manual Quality Verification
**Objective**: Ensure LEADER.md accuracy and completeness through manual verification

**Manual Verification Checklist**:
- [ ] All sectors have at least 3 tickers - manually counted and verified
- [ ] Base periods are clearly identified for each sector - manually determined and verified
- [ ] Leadership scores calculated correctly using 60/40 weighting - manually computed and checked
- [ ] Sector classifications match actual trend breadth and signal cohesion - manually verified through human analysis
- [ ] All Top 3 analyses include specific VPA story and performance data - manually verified from profiles
- [ ] Chart links use correct file paths (reports_week/) - manually checked
- [ ] Vietnamese text is grammatically correct - manually reviewed
- [ ] All scores are based on manually verified ticker profiles - human verification

### Step 9: Manual File Output
**Objective**: Generate final LEADER.md file using manual compilation

**Manual Output Process**:
- **Use Write tool** to create the complete LEADER.md file with all manually verified analysis and data
- **Manual compilation** of all sections based on human analysis
- **Manual formatting** verification for Vietnamese content

## Manual Quality Control Standards

### Manual Data Accuracy Requirements
- **Manually Verified Sources**: All data must trace back to manually created ticker profiles
- **Manual Calculation Accuracy**: Leadership scores must use exact 60/40 weighting - manually verified
- **Manual Date Precision**: Base periods must have clear start and end dates - manually determined
- **Manual Signal Verification**: Recent VPA signals must match source files - manually cross-checked

### Manual Sector Analysis Standards
- **Manual Breadth Calculation**: Must include all sector tickers in percentage - manually counted
- **Manual Signal Cohesion**: Must reflect actual distribution of recent signals - manually analyzed
- **Manual Classification Logic**: Must follow strict criteria for sector health categories - human judgment
- **Manual Comparative Context**: Leaders must be compared within sector health context - human analysis

### Vietnamese Language Standards
- Use proper Vietnamese financial terminology - manually verified
- Maintain professional tone and grammar - manually checked
- Ensure decimal formatting uses dots (.), not commas (,) - manually enforced
- Use consistent sector naming from GROUP.md - manually cross-checked

### Technical Requirements
- **Chart Links**: Verify all image paths use reports_week/ directory - manually checked
- **Report Links**: Ensure all links point to REPORT_week.md with correct anchors - manually verified
- **Markdown Formatting**: Proper headers, tables, and structure - manually inspected
- **Score Precision**: Display leadership scores to one decimal place - manually formatted

## Manual Error Handling

### Manual Missing Input Files
- Document missing files in manual summary
- Use available data and manually note limitations
- Manually skip sectors with insufficient data

### Manual Data Inconsistencies
- **Manual cross-reference** multiple sources for verification
- **Human judgment** to prioritize most recent and reliable weekly data
- Document conflicts and manual resolution approach

### Manual Sector Exclusions
- **Manual log** sectors excluded due to insufficient tickers (<3) through human counting
- **Manual log** sectors excluded due to unclear base periods through human analysis
- **Manual reasoning** for all exclusions with human justification

## Manual Success Metrics

- **Accuracy**: All manually created ticker profiles match source data exactly - human verification
- **Completeness**: Every eligible sector analyzed and classified manually - human coverage
- **Traceability**: All leadership scores can be verified from manual calculations - human math verification
- **Sector Health**: Classifications accurately reflect trend breadth and signal cohesion - manual analysis
- **Actionability**: Top leaders provide clear investment insights based on manual assessment

## Manual Templates

### Manual Ticker Profile Template
```json
{
  "ticker": "",
  "sector": "manually verified from GROUP.md",
  "full_vpa_story_summary": "manually analyzed from vpa_data_week files",
  "recent_vpa_signals": [{"signal": "manually identified", "date": "manually verified"}],
  "price_history_lookup": "manually calculated using reliable Python"
}
```

### Sector Classification Examples
- **Dẫn Dắt Đồng Thuận**: "Ngành đang có xu hướng tăng giá mạnh mẽ và lan tỏa. Các cổ phiếu trụ cột đều có tín hiệu SOS và hiệu suất vượt trội. Dòng tiền đang chảy mạnh vào toàn ngành."
- **Dẫn Dắt Phân Hóa**: "Mặc dù có một vài cổ phiếu tăng giá rất mạnh, phần lớn các cổ phiếu trong ngành vẫn đang trong giai đoạn tích lũy. Sự lựa chọn cổ phiếu là rất quan trọng."
- **Đang Tích Lũy**: "Ngành đang trong giai đoạn tích lũy với hầu hết cổ phiếu đi ngang. Tín hiệu No Supply phổ biến, tạo tiền đề cho xu hướng tăng trong tương lai."
- **Yếu/Phân Phối**: "Ngành đang yếu với đa số cổ phiếu có hiệu suất âm. Tín hiệu SOW và Upthrust xuất hiện nhiều, cho thấy rủi ro giảm giá."

## Weekly Analysis Specific Notes

- **Weekly Focus**: Emphasize weekly trends and patterns over daily noise
- **Volume Context**: Compare weekly volumes to historical weekly averages
- **Signal Weight**: Weekly signals carry more significance than daily signals
- **Trend Duration**: Consider sustainability of weekly trends for leadership assessment
- **Market Context**: Factor in broader weekly market trends when evaluating sectors