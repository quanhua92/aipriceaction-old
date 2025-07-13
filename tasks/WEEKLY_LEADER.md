# Weekly Leader Analysis Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `LEADER.md` file using the VPA-SectorLead methodology. The agent must follow the multi-stage protocol to identify sector-leading tickers and assess overall sector health based on weekly data.

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current

```bash
# Check for required input files
ls GROUP.md REPORT_week.md
ls vpa_data_week/ market_data_week/
```

**Actions**:
- Verify `GROUP.md` exists with sector-to-ticker mappings
- Verify `vpa_data_week/` directory exists with individual ticker weekly VPA files
- Verify `REPORT_week.md` exists with weekly analysis and signals
- Verify `market_data_week/` directory exists with individual ticker weekly CSV files (last 6 months)

**Success Criteria**: All core input files are present and accessible

### Step 2: STAGE 0 - Ticker Profile Creation
**Objective**: Create verified internal ticker profiles for ALL tickers to prevent data contamination

**Parallel Processing Approach**: Use Task tool to process sectors concurrently, with each sector processing its tickers in parallel.

**Critical Process**: For EVERY ticker from GROUP.md, create this internal data structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "sector": "Sector name from GROUP.md",
  "full_vpa_story_summary": "Concise summary from vpa_data_week/{TICKER}.md",
  "recent_vpa_signals": [
    {"signal": "SOS Bar", "date": "2025-07-07"},
    {"signal": "Test for Supply", "date": "2025-06-30"}
  ],
  "price_history_data": "Raw weekly OHLCV from market_data_week/{TICKER}_*.csv",
  "base_period_start": "Sector base period start date",
  "base_period_end": "Sector base period end date"
}
```

**File Reading Strategy for Each Ticker**:
1. Read `vpa_data_week/{TICKER}.md` for complete weekly VPA story
2. Read `market_data_week/{TICKER}_*.csv` for price history and calculations
3. Extract recent VPA signals from ticker file (last 2-3 significant signals)
4. Calculate performance from sector base period to latest close

**Data Extraction Rules**:
- Extract sector mappings ONLY from `GROUP.md`
- Extract VPA story summaries from individual `vpa_data_week/{TICKER}.md` files
- Extract recent signals from both individual VPA files and `REPORT_week.md`
- Extract price data from individual `market_data_week/{TICKER}_*.csv` files

**Parallel Processing Strategy**:
- Use Task tool to process multiple tickers concurrently for each sector
- Read ticker-specific files (vpa_data_week/{TICKER}.md, market_data_week/{TICKER}_*.csv)
- Avoid reading large consolidated files (VPA_week.md, market_data_week.txt)
- Enable sector-level parallel analysis

**Quality Control**: These ticker profiles become the SOLE source of truth for all subsequent stages

**Example Task Tool Usage by Sector**:
```
Task 1: "Process NGÂN HÀNG sector tickers (TCB,VCB,MBB,STB,CTG,VPB,LPB,ACB,HDB,TPB,SHB,VIB,BID) for weekly leader analysis. For each: 1) Read vpa_data_week/{TICKER}.md full story 2) Read market_data_week/{TICKER}_*.csv for price history 3) Return ticker profile JSON with VPA summary and recent signals"

Task 2: "Process BẤT ĐỘNG SẢN sector tickers (VHM,VIC,NVL,KDH,HDG,VRE) for weekly leader analysis. Same process as Task 1."
```

**Sector-Level Parallel Processing**:
- Process 3-5 sectors concurrently using Task tool
- Each sector processes its tickers in parallel
- Individual weekly VPA files: ~100-300 lines vs VPA_week.md: ~20,000+ lines
- Individual weekly CSV files: ~30 rows vs market_data_week.txt: ~4,000+ rows

### Step 3: STAGE 1 - Sector Aggregation & Universe Definition
**Objective**: Define eligible sectors for analysis

**Process**:
1. **Load Sector Universe**: Read `GROUP.md` to get all sector definitions
2. **Define Eligible Sectors**: Process ONLY sectors with at least 3 tickers
3. **Filter Rule**: Sectors with fewer than 3 tickers are omitted from analysis

**Output**: List of eligible sectors for comprehensive analysis

### Step 4: STAGE 2 - Sector Base Period Identification
**Objective**: Identify common base periods for each eligible sector

**Methodology**:
1. **Analyze 6-Month History**: Review weekly OHLCV data from `market_data_week.txt`
2. **Identify Stability Phases**: Find periods where majority of sector tickers showed:
   - Low volatility or sideways price action
   - Clear VPA signs of accumulation (No Supply bars, low volume tests)
   - Common consolidation patterns
3. **Define Base Period**: Establish date range representing sector-wide accumulation/stability phase
4. **Sector Exclusion**: Omit sectors without clear common base periods

**Output**: Base period date ranges for each eligible sector

### Step 5: STAGE 3 - Individual Ticker Analysis & Scoring
**Objective**: Calculate leadership scores for all tickers within eligible sectors

**Scoring Framework** (using ticker profiles and base periods):

#### 5.1 VPA Story Score (Weight: 60%)
**Scale**: 0-100 points
**Assessment Criteria**:
- **90-100**: Perfect multi-stage Wyckoff story (Accumulation → Shakeout → SOS → successful Backing Up/Test)
- **70-89**: Strong story with minor imperfections or still developing
- **<70**: Weak, unclear, or broken VPA narrative

**Data Source**: `full_vpa_story_summary` from ticker profiles

#### 5.2 Relative Performance Score (Weight: 40%)
**Calculation**: Percentage price change from sector base period start to most recent weekly close
**Scale**: Direct percentage (25% gain = 25 points)
**Data Source**: `price_history_lookup` from ticker profiles

#### 5.3 Confidence Score (Reporting Only)
**Scale**: 0-100%
**Assessment Criteria**:
- **90-100%**: Textbook VPA setup, clear recent signals, low risk
- **75-89%**: Strong setup with some ambiguity, needs confirmation
- **<75%**: Conflicting signals, high risk, broken narrative

**Data Source**: `recent_vpa_signals` from ticker profiles

#### 5.4 Final Leadership Score Calculation
**Formula**: `Leadership Score = (VPA Story Score × 0.6) + (Relative Performance Score × 0.4)`
**Ranking**: Top 3 tickers per sector become "Sector Leaders"

### Step 6: STAGE 4 - Sector Health & Context Analysis
**Objective**: Evaluate overall sector character and health

**Analysis Framework**:

#### 6.1 Trend Breadth Calculation
- Calculate percentage of sector tickers with positive relative performance
- High breadth (>70%) vs. Low breadth (<70%)

#### 6.2 VPA Signal Cohesion Assessment
- Scan `recent_vpa_signals` across all sector tickers
- Identify dominant theme: Bullish (SOS, Test, No Supply) vs. Bearish (SOW, Upthrust)

#### 6.3 Sector Classification (Mandatory)
**Categories**:
- **Dẫn Dắt Đồng Thuận**: High breadth (>70%), cohesive bullish signals, strong broad-based rally
- **Dẫn Dắt Phân Hóa**: Low breadth (<70%), mixed signals, narrow leadership
- **Đang Tích Lũy**: Sideways movement, flat performance, No Supply signals common
- **Yếu/Phân Phối**: Low breadth, negative performance, SOW/Upthrust prevalent

### Step 7: STAGE 5 - LEADER.md Generation
**Objective**: Generate complete LEADER.md using verified profiles and analysis

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

### Step 8: Quality Verification
**Objective**: Ensure LEADER.md accuracy and completeness

**Verification Checklist**:
- [ ] All sectors have at least 3 tickers
- [ ] Base periods are clearly identified for each sector
- [ ] Leadership scores calculated correctly using 60/40 weighting
- [ ] Sector classifications match actual trend breadth and signal cohesion
- [ ] All Top 3 analyses include specific VPA story and performance data
- [ ] Chart links use correct file paths (reports_week/)
- [ ] Vietnamese text is grammatically correct
- [ ] All scores are based on verified ticker profiles

### Step 9: File Output
**Objective**: Generate final LEADER.md file

```bash
# Generate new LEADER.md (git handles version control)
# [Output complete LEADER.md content]
```

## Quality Control Standards

### Data Accuracy Requirements
- **Verified Sources**: All data must trace back to ticker profiles
- **Calculation Accuracy**: Leadership scores must use exact 60/40 weighting
- **Date Precision**: Base periods must have clear start and end dates
- **Signal Verification**: Recent VPA signals must match source files

### Sector Analysis Standards
- **Breadth Calculation**: Must include all sector tickers in percentage
- **Signal Cohesion**: Must reflect actual distribution of recent signals
- **Classification Logic**: Must follow strict criteria for sector health categories
- **Comparative Context**: Leaders must be compared within sector health context

### Vietnamese Language Standards
- Use proper financial terminology
- Maintain professional tone and grammar
- Ensure decimal formatting uses dots (.), not commas (,)
- Use consistent sector naming from GROUP.md

### Technical Requirements
- **Chart Links**: Verify all image paths use reports_week/ directory
- **Report Links**: Ensure all links point to REPORT_week.md with correct anchors
- **Markdown Formatting**: Proper headers, tables, and structure
- **Score Precision**: Display leadership scores to one decimal place

## Error Handling

### Missing Input Files
- Document missing files in summary
- Use available data and note limitations
- Skip sectors with insufficient data

### Data Inconsistencies
- Cross-reference multiple sources for verification
- Prioritize most recent and reliable weekly data
- Document conflicts and resolution approach

### Sector Exclusions
- Log sectors excluded due to insufficient tickers (<3)
- Log sectors excluded due to unclear base periods
- Provide reasoning for all exclusions

## Success Metrics

- **Accuracy**: All ticker profiles match source data exactly
- **Completeness**: Every eligible sector analyzed and classified
- **Traceability**: All leadership scores can be verified from calculations
- **Sector Health**: Classifications accurately reflect trend breadth and signal cohesion
- **Actionability**: Top leaders provide clear investment insights

## Templates

### Ticker Profile Template
```json
{
  "ticker": "",
  "sector": "",
  "full_vpa_story_summary": "",
  "recent_vpa_signals": [{"signal": "", "date": ""}],
  "price_history_lookup": ""
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