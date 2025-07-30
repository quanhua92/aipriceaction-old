# Daily Planning Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `PLAN.md` file using the VPA-Strategist methodology. The agent must follow these steps sequentially to ensure accurate, verifiable analysis using natural language processing and reliable Python operations only.

**⚠️ CRITICAL: ALWAYS USE ACTUAL DATA DATES**
- Never assume "today's date" for analysis
- Always get the actual last available date from CSV files using `df.iloc[-1]["Date"]`
- Use `glob.glob()` to find the most recent CSV file for each ticker
- Compare actual data dates with existing analysis dates to determine if new analysis is needed

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current

**Use LS tool to check for required input files:**
- Verify paths: `REPORT.md`, `REPORT_week.md`, `LEADER.md`, `GROUP.md`, `PLAN.md`
- Verify directories: `vpa_data/`, `market_data/`

**Actions**:
- Verify `REPORT.md` exists and contains recent daily signals
- Verify `REPORT_week.md` exists with weekly analysis (reflects last completed trading week)
- Verify `vpa_data/` directory exists with individual ticker VPA files
- Verify `market_data/` directory exists with individual ticker CSV files
- Verify `LEADER.md` exists with industry context analysis
- Verify `GROUP.md` exists with ticker-to-industry mappings
- Verify `PLAN.md` exists with current Top List (market leaders foundation)

**Success Criteria**: All core input files are present and accessible

### Step 1.5: Group Classification Validation
**Objective**: Ensure all ticker sector classifications match GROUP.md using reliable Python operations

```bash
# Only use reliable Python for CSV/JSON reading
uv run -c "
import pandas as pd
import json

# Read GROUP.md using reliable text operations
with open('GROUP.md', 'r', encoding='utf-8') as f:
    group_content = f.read()
    print('GROUP.md loaded successfully')
    print(f'File size: {len(group_content)} characters')
"
```

**Critical Validation Process**:
- **MANUAL NATURAL LANGUAGE ANALYSIS ONLY** - read GROUP.md directly with Read tool
- Compare ticker sector classifications manually by reading and analyzing text
- Identify mismatched sector classifications through human-readable analysis
- Ensure consistent Vietnamese sector naming conventions
- NO automated text parsing - use human intelligence for text understanding

**Required Actions**:
- Fix any sector mismatches found manually (e.g., FOX should be "Công Nghệ" not "Chứng Khoán")
- Update Vietnamese sector names to match GROUP.md conventions through manual analysis
- Add missing tickers to GROUP.md if needed
- Document any classification changes in audit log

**Success Criteria**: All ticker sector classifications are accurate and consistent

### Step 2: Market Leaders Foundation Analysis
**Objective**: Use current Top List from PLAN.md as proven market leaders foundation

**Actions**:
- **Read PLAN.md using Read tool** to understand current Top List holdings
- Identify the proven market leaders from existing Top 15 list as foundation
- **Use these leaders as the starting point for the new TOP list**
- Analyze performance and VPA signals for each leader
- **NATURAL LANGUAGE ANALYSIS ONLY** - no Python text parsing

**Proven Market Leaders from PLAN.md Top List**:
- **VHM (Bất Động Sản)**: Proven leader, confidence 95%
- **SSI (Chứng Khoán)**: Proven leader, confidence 95%
- **VND (Chứng Khoán)**: Proven leader, confidence 95%
- **VPB (Ngân Hàng)**: Proven leader, confidence 95%
- **VIX (Chứng Khoán)**: Proven leader, confidence 90%
- **HDC (Bất Động Sản)**: Proven leader, confidence 85%
- **HDB (Ngân Hàng)**: Proven leader, confidence 85%
- **TCH (Bất Động Sản)**: Proven leader, confidence 85%
- **MWG (Bán Lẻ)**: Proven leader, confidence 85%
- **CTS (Chứng Khoán)**: Proven leader, confidence 75%
- **HPG (Thép)**: Proven leader, confidence 80%
- **MSN (Thực Phẩm)**: Proven leader, confidence 80%
- **REE (Năng Lượng)**: Proven leader, confidence 80%
- **MBS (Chứng Khoán)**: Proven leader, confidence 80%
- **VCI (Chứng Khoán)**: Proven leader, confidence 80%

**Foundation Principle**: These 15 proven leaders start as TOP candidates unless signals severely deteriorate

**Output**: Proven foundation for creating new TOP, POTENTIAL, and DOWNGRADED lists

### Step 3: STAGE 0 - Manual Data Analysis Using Natural Language
**Objective**: Analyze ticker data using natural language processing and reliable Python operations only

**MANUAL ANALYSIS APPROACH - NO TEXT PARSING UTILITIES**:

**For Market Leaders (Top 15 from PLAN.md)**:
1. **Read REPORT.md** using Read tool - manually identify signals for each Top List ticker
2. **Read REPORT_week.md** using Read tool - manually identify weekly signals for each leader
3. **For each leader, read individual vpa_data/{TICKER}.md** using Read tool - extract recent VPA context
4. **Use reliable Python ONLY for CSV operations**:
```bash
# Example reliable Python for price data - gets the most recent CSV file
uv run -c "
import pandas as pd
import glob
ticker = 'VHM'
try:
    # Find the most recent CSV file for this ticker
    csv_files = glob.glob(f'market_data/{ticker}_*.csv')
    if not csv_files:
        print(f'No CSV files found for {ticker}')
    else:
        # Get the most recent file by modification time or filename
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        latest = df.iloc[-1]  # Last row = most recent data
        print(f'{ticker}: Latest date={latest["Date"]}, Close={latest["Close"]}')
        print(f'CSV file: {latest_file}')
        print(f'Data date range: {df.iloc[0]["Date"]} to {df.iloc[-1]["Date"]}')
except Exception as e:
    print(f'Could not read CSV for {ticker}: {e}')
"
```

**For Potential Candidates (Beyond Top 15)**:
1. **Read TICKERS.csv using reliable Python**:
```bash
uv run -c "
import pandas as pd
tickers = pd.read_csv('TICKERS.csv')
print(f'Total tickers to analyze: {len(tickers)}')
print('Sample tickers:', tickers.head(10).to_list())
"
```
2. **Manually scan REPORT.md for strong signals (SOS, Effort to Rise)** from non-Top List tickers
3. **Use Read tool to check individual vpa_data files** for promising candidates
4. **Manual analysis of weekly patterns** from REPORT_week.md
5. **Review current Potential List** from PLAN.md for promotion candidates

**Data Analysis Rules**:
- **NO automated text parsing or regex operations**
- **Use natural language understanding to read reports**
- **Use reliable Python ONLY for CSV, JSON, basic file operations**
- **Extract signals manually by reading and understanding context**
- **Cross-reference findings using human intelligence, not automation**

**Quality Control**: Manual verification ensures accuracy over automation

### Step 4: STAGE 1 - Manual Ticker State Assessment Using VPA-Strategist Methodology
**Objective**: Determine new state for each ticker using manual analysis and VPA principles

**MANUAL ASSESSMENT PROCESS - NO AUTOMATED UTILITIES**:

**Foundation Principle**: Top 15 proven leaders from PLAN.md are market leaders and form the core TOP list unless severely compromised

**Assessment Categories**:

#### For Market Leaders (Current Top 15):
**MANUAL ANALYSIS APPROACH**:
1. **Read PLAN.md Top List** - understand current proven leaders and their VPA status
2. **Cross-reference with REPORT.md** - manually find daily signals for each leader
3. **Cross-reference with REPORT_week.md** - manually find weekly signals for each leader
4. **Apply VPA-Strategist methodology manually**

**Assessment Rules for Market Leaders**:
- **VHM, SSI, VND, VPB, VIX, HDC, HDB, TCH, MWG, CTS, HPG, MSN, REE, MBS, VCI**: Start as TOP candidates (proven leaders)
- **High threshold for removing proven leaders** - they have demonstrated consistent performance
- **Weekly signals dominate** - daily signals fine-tune confidence levels
- **Confidence scoring**: 95% (strong weekly+daily), 85% (weekly strong, daily mixed), 75% (weekly neutral, daily strong)

#### For Non-Top List Strong Signal Candidates:
**MANUAL IDENTIFICATION PROCESS**:
1. **Scan REPORT.md manually** - look for strong daily signals (SOS, Effort to Rise) from non-Top List tickers
2. **Check weekly context in REPORT_week.md** - confirm weekly foundation for candidates
3. **Read individual vpa_data files** for context on promising tickers
4. **Apply manual VPA assessment** - evaluate for POTENTIAL list inclusion

**Promotion Criteria**:
- **Daily SOS + Weekly supportive**: Strong POTENTIAL candidate
- **Daily Effort to Rise + Industry strength**: Consider for POTENTIAL
- **Multiple day patterns**: Higher confidence for POTENTIAL inclusion
- **New breakouts**: Fast-track evaluation for opportunities

#### For Previously Downgraded Tickers:
**RECOVERY ASSESSMENT**:
- **Manual scan for recovery signals** in daily and weekly reports
- **Fast recovery on strong signals** - daily SOS can promote to POTENTIAL quickly
- **Patient approach** - allow time for signal confirmation
- **Industry context matters** - sector improvement supports recovery

#### For Unlisted Ticker Universe:
**OPPORTUNITY SCANNING**:
- **Manual review of strong signals** from entire ticker universe in reports
- **Focus on SOS and Effort to Rise** patterns for new opportunities
- **Industry rotation opportunities** - look for emerging sector strength
- **Don't miss breakouts** - prioritize capturing new trends early

**MANUAL ASSESSMENT OUTPUT**:
- **New TOP List**: Proven leaders + any exceptional new candidates (manual assessment)
- **New POTENTIAL List**: Strong signal candidates not yet in TOP (manual assessment)  
- **New DOWNGRADED List**: Weakening tickers requiring monitoring (manual assessment)
- **Confidence scores**: Based on manual evaluation of signal strength and context
- **Complete audit trail**: Document all reasoning for state changes

### Step 5: STAGE 2 - PLAN.md Creation Using Manual Natural Language Analysis
**Objective**: Create new PLAN.md using manual analysis and natural language understanding

**MANUAL CREATION PROCESS - NO AUTOMATED UTILITIES**:

**Key Requirements**:
- **Create completely new PLAN.md** based on manual analysis results
- **Use portfolio holdings from hold.md as foundation** for TOP list
- **Apply manual VPA assessment results** to categorize all tickers appropriately
- **Maintain professional Vietnamese financial writing style**
- **Include proper audit trail** documenting all changes and reasoning
- **EXACT OUTPUT FORMAT** as specified in template

**Quality Standards**:
- Organize Top List by confidence tiers (90-95%, 85-89%, 75-84%)
- Categorize Potential List by opportunity type (Strong Growth, Special Watch, Need Confirmation)
- Add strategic context and portfolio allocation recommendations
- Include actionable entry strategies and risk management guidance
- Provide comprehensive VNINDEX market analysis with both weekly and daily synthesis

**Data Sources for Manual Analysis**:
- `PLAN.md`: Market leaders foundation from proven Top 15 list
- `REPORT.md` and `REPORT_week.md`: VNINDEX analysis and ticker signals (manual reading)
- `LEADER.md` and `GROUP.md`: Industry context and sector analysis (manual reading)
- Individual `vpa_data/*.md` files: Ticker-specific VPA context (manual reading)
- Reliable Python for CSV price data only

#### 5.1 VNINDEX Analysis Section
```markdown
## 1. Phân Tích Trạng Thái VNINDEX & Chiến Lược

![Weekly Chart](reports_week/VNINDEX/VNINDEX_candlestick_chart.png) ![Daily Chart](reports/VNINDEX/VNINDEX_candlestick_chart.png)

**Bối Cảnh Tuần**: [Synthesize weekly context from REPORT_week.md]

**Hành Động Gần Đây**: [Describe how recent daily action from REPORT.md confirms/contradicts weekly picture]

**Vùng Tốt Nhất Để Gia Tăng Tỷ Trọng**: [Define specific support/resistance levels with justification]
```

#### 5.2 Top List Generation (Market Leaders Foundation + Strong Signals)
**MANUAL GENERATION RULES**:
- **Market Leaders Priority**: Start with Top 15 proven leaders from PLAN.md (VHM, SSI, VND, VPB, VIX, HDC, HDB, TCH, MWG, CTS, HPG, MSN, REE, MBS, VCI)
- **Manual signal confirmation**: Verify each leader has supportive signals in reports
- **Add exceptional new candidates**: Based on manual signal analysis from broader universe
- **Confidence Score Strategy**: Manual assessment (95% → 85% → 75%) based on signal strength
- **Vietnamese terminology**: Use proper financial terms throughout
- **REQUIRED FORMAT**: `[**TCB**](#TCB) (Ngân Hàng) - **95%** - Tín hiệu mạnh mẽ - [View Report](REPORT.md#TCB)`
- **Score Guidelines**: 
  - 95%: Perfect weekly/daily alignment with strong industry
  - 85%: Minor daily weakness but weekly trend intact
  - 75%: Temporary consolidation but fundamentally sound
- **MANDATORY ORGANIZED STRUCTURE**:
  ```markdown
  ## 2. Top [X] Cơ Hội Giao Dịch Chất Lượng
  
  ### Nhóm Tin Cậy Cao (85-95%) - Portfolio Core
  1. [**VHM**](#VHM) (Bất Động Sản) - **90%** - Description - [View Report](REPORT.md#VHM)
  2. [**VND**](#VND) (Chứng Khoán) - **90%** - Description - [View Report](REPORT.md#VND)
  
  ### Nhóm Tin Cậy Tốt (75-84%) - Strategic Holdings
  6. [**HDB**](#HDB) (Ngân Hàng) - **80%** - Description - [View Report](REPORT.md#HDB)
  
  ### Nhóm Quan Sát Cẩn Thận (65-74%) - Tactical Positions
  10. [**CTS**](#CTS) (Chứng Khoán) - **70%** - Description - [View Report](REPORT.md#CTS)
  ```

#### 5.3 Potential List Generation (Manual Signal Scanning)
**MANUAL GENERATION RULES**:
- **Manual signal identification**: Scan REPORT.md for strong signals from non-Top List tickers
- **Weekly foundation check**: Verify weekly context supports daily signals
- **Industry context**: Consider sector strength from LEADER.md analysis
- **Opportunity categorization**: Group by signal strength and timing
- **Vietnamese descriptions**: Emphasize weekly foundation + daily catalyst
- **Fast-track indicators**: Mark tickers ready for potential Top List promotion

#### 5.4 Downgraded List Generation (Manual Assessment)
**MANUAL GENERATION RULES**:
- **Check current Downgraded**: Review existing downgraded tickers in PLAN.md
- **Manual weakness identification**: Look for consistent bearish signals in proven leaders
- **Include reasoning**: Cite specific signals that triggered demotion
- **Monitor for recovery**: Track potential reversal signals

#### 5.5 Detailed Analysis for Top Tickers
**MINIMUM REQUIREMENT**: Provide detailed analysis for **ALL TOP LIST TICKERS** (not just 10)

**MANDATORY FORMAT** for EACH ticker analysis section:
```markdown
### **[TICKER] ([SECTOR])**
![Weekly Chart](reports_week/[TICKER]/[TICKER]_candlestick_chart.png) ![Daily Chart](reports/[TICKER]/[TICKER]_candlestick_chart.png)

* **Giá Hiện Tại:** [PRICE].000 VNĐ
* **Tín Hiệu VPA Tuần:** [Weekly VPA narrative with exact dates]
* **Tín Hiệu VPA Ngày:** [Daily VPA narrative with exact dates]
* **Bối Cảnh Ngành:** [Industry context from LEADER.md]
* **Phân Tích Thiết Lập:** [Synthesis explaining high-conviction setup]
* **Vùng Vào Tốt Nhất:** [Best entry zones with technical justification]
```

**CRITICAL REQUIREMENTS**:
- **Current Price Format**: MUST use thousand dot format (e.g., 72.200 VNĐ, 23.550 VNĐ)
- **Price Source**: Extract from latest CSV market data file using glob.glob(f'market_data/{TICKER}_*.csv') to find most recent file
- **All Top List Tickers**: Every ticker in Top List must have detailed section
- **Vietnamese Terms**: All analysis in professional Vietnamese financial terminology
- **Chart Links**: Verify paths exist for both weekly and daily charts

**Selection Priority**: **ALL TOP LIST TICKERS** must have detailed analysis sections

#### 5.6 Audit Log Creation
**Mandatory documentation** of ALL state changes with precise justifications:

```markdown
## 6. Nhật Ký Thay Đổi Kế Hoạch (AUDIT LOG)

### Cổ Phiếu Được Nâng Lên "Top 1x":
- **ABC**: Từ `Potential List`. Lý do: REPORT.md ghi nhận **'SOS' ngày YYYY-MM-DD**, xác nhận **'SOS' tuần kết thúc YYYY-MM-DD**. LEADER.md xác nhận ngành 'Dẫn dắt Đồng Thuận'.

### Cổ Phiếu Được Thêm Vào "Potential List":
- **XYZ**: Từ `Unlisted`. Lý do: **'SOS' ngày YYYY-MM-DD** với biểu đồ tuần trong vùng Tích Lũy.

### Cổ Phiếu Bị Giáng Xuống "Hạ Ưu Tiên":
- **FPT**: Từ `Top List`. Lý do: **'Sign of Weakness' ngày YYYY-MM-DD** sau 'Upthrust' tuần kết thúc YYYY-MM-DD.

### Cổ Phiếu Bị Loại Bỏ Hoàn Toàn:
- **GEX**: Từ `Downgraded`. Lý do: **'No Demand' ngày YYYY-MM-DD** xác nhận xu hướng giảm.
```

### Step 6: **CRITICAL DATA VERIFICATION** (Prevent Trading Errors)
**Objective**: Ensure PLAN.md accuracy and completeness through systematic data verification

**⚠️ MANDATORY DATA ACCURACY VERIFICATION** (Based on Real Error Patterns):

#### 6.1 **Price Data Verification** (Zero Tolerance for Errors)
```bash
# For EVERY ticker mentioned in PLAN.md, verify using most recent CSV file:
uv run -c "
import pandas as pd
import glob
ticker = 'TICKER_NAME'
try:
    # Find the most recent CSV file for this ticker
    csv_files = glob.glob(f'market_data/{ticker}_*.csv')
    if csv_files:
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        print(f'Using file: {latest_file}')
        print(f'Data range: {df.iloc[0][\"Date\"]} to {df.iloc[-1][\"Date\"]}')
        print('Last 5 rows for verification:')
        print(df.tail(5)[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']])
    else:
        print(f'No CSV files found for {ticker}')
except Exception as e:
    print(f'Error reading {ticker}: {e}')
"
```

**MANDATORY CURRENT PRICE EXTRACTION PROCESS**:
```bash
# For each Top List ticker, extract current price from most recent CSV:
uv run -c "
import pandas as pd
import glob

tickers = ['VHM', 'VND', 'VPB', 'VIX', 'SSI', 'HDB', 'MWG', 'REE', 'SHS', 'CTS', 'MBB', 'SHB', 'ACB', 'MSN', 'HDC', 'VCI', 'TCB', 'BSR']

for ticker in tickers:
    try:
        # Find the most recent CSV file for this ticker
        csv_files = glob.glob(f'market_data/{ticker}_*.csv')
        if csv_files:
            latest_file = max(csv_files)
            df = pd.read_csv(latest_file)
            latest = df.iloc[-1]  # Last row = most recent data
            price = float(latest['Close'])
            # Format with thousand dot: 72.2 becomes 72.200
            formatted_price = f'{price:.3f}'
            print(f'* **Giá Hiện Tại:** {formatted_price} VNĐ')
            print(f'  (Date: {latest[\"Date\"]}, File: {latest_file})')
        else:
            print(f'No CSV files found for {ticker}')
    except Exception as e:
        print(f'Error reading {ticker}: {e}')
"
```

**Critical Checks**:
- [ ] **Current Prices**: MUST be in thousand dot format (XXX.XXX VNĐ) for ALL Top List tickers
- [ ] **Daily Prices**: Open, High, Low, Close match CSV data exactly
- [ ] **Gap Claims**: "gap up X" must match actual Open vs Previous Close
- [ ] **Price Movements**: "từ X xuống Y" must match actual data
- [ ] **Price Ranges**: All claimed price ranges verified against CSV

#### 6.2 **Volume Data Verification** (⚠️ HIGHEST ERROR AREA)
```bash
# Volume verification process:
# 1. Read CSV volume column (actual units)
# 2. Convert to millions: actual_volume ÷ 1,000,000
# 3. Verify PLAN.md claims match calculated millions
```

**Critical Volume Checks**:
- [ ] **Volume Figures**: All "XM" claims verified against CSV (÷1M conversion)
- [ ] **Volume Comparisons**: "doubled", "increased 60%" calculated and verified
- [ ] **Volume Direction**: "volume tăng/giảm" matches actual direction
- [ ] **Volume Patterns**: VPA interpretations match actual volume behavior

#### 6.3 **Weekly Data Verification** (⚠️ COMMON ERROR AREA)
```bash
# For weekly claims, use most recent weekly data files:
uv run -c "
import pandas as pd
import glob
ticker = 'VHM'
try:
    # Find the most recent weekly CSV file
    csv_files = glob.glob(f'market_data_week/{ticker}_*.csv')
    if csv_files:
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        print(f'Using weekly file: {latest_file}')
        print(f'Weekly data range: {df.iloc[0][\"Date\"]} to {df.iloc[-1][\"Date\"]}')
        # Calculate actual weekly percentage changes
        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else df.iloc[-1]
        change_pct = ((latest[\"Close\"] - previous[\"Close\"]) / previous[\"Close\"]) * 100
        print(f'Weekly change: {change_pct:.1f}%')
    else:
        print(f'No weekly CSV files found for {ticker}')
except Exception as e:
    print(f'Error: {e}')
"
```

**Weekly Verification Checks**:
- [ ] **Weekly Percentages**: Calculate (Current-Previous)/Previous × 100
- [ ] **Weekly Performance Claims**: "+X%" verified against actual weekly data
- [ ] **Weekly Volume Claims**: Weekly volume patterns verified

#### 6.4 **VPA Signal Verification** (Critical for Trading Decisions)
```bash
# Cross-reference VPA claims with actual data:
# 1. Check volume direction matches claimed VPA signal
# 2. Verify "Test for Supply" has decreasing volume
# 3. Verify "SOS" has increasing volume
```

**VPA Consistency Checks**:
- [ ] **Test for Supply**: Must have decreasing volume, not increasing
- [ ] **Sign of Strength**: Must have increasing volume
- [ ] **Effort to Rise**: Volume pattern matches price action
- [ ] **No Supply**: Volume decreases as price rises

#### 6.5 **Mathematical Consistency Verification**
**Calculation Verification**:
- [ ] **Percentage Changes**: All % claims calculated and verified
- [ ] **Price Logic**: Open ≤ High, Low ≤ Close relationships maintained
- [ ] **Volume Units**: Consistent M (millions) usage throughout
- [ ] **Support/Resistance Logic**: Support < Current Price < Resistance

#### 6.6 **Cross-Reference Verification**
```bash
# Verify claims against VPA data files:
Read: /Volumes/data/workspace/aipriceaction/vpa_data/{TICKER}.md
# Check latest entries match PLAN.md claims
```

**Cross-Reference Checks**:
- [ ] **VPA Data Consistency**: Claims match latest vpa_data entries
- [ ] **Signal Dates**: All dates referenced exist and are accurate
- [ ] **Historical Context**: Previous signals correctly referenced

**⚠️ ERROR PREVENTION PRIORITIES** (Based on Actual Findings):
1. **Volume Errors** (BSR 100% error, GAS 43% error) - HIGHEST PRIORITY
2. **Weekly Percentage Errors** (VND +13.4% vs +14.0%) - HIGH PRIORITY
3. **VPA Signal Misinterpretation** (volume direction wrong) - CRITICAL
4. **New Opportunities Section** (higher error rate) - SPECIAL ATTENTION

**Manual Verification Checklist** (Enhanced):
- [ ] All assertions cite specific signals and dates from manual analysis
- [ ] **⚠️ ZERO price/volume errors** - every figure verified against CSV
- [ ] **⚠️ All VPA signals** match actual volume patterns
- [ ] **⚠️ Weekly percentages** calculated and verified
- [ ] No ticker appears in multiple categories
- [ ] **MANDATORY**: ALL TOP LIST TICKERS have detailed analysis sections
- [ ] **MANDATORY**: Current prices in thousand dot format (XXX.XXX VNĐ) for all detailed sections
- [ ] **MANDATORY**: Top List organized with numbered tiers and group headers
- [ ] Complete audit log documents every state change with manual justification
- [ ] VNINDEX analysis synthesizes both daily and weekly timeframes from reports
- [ ] Chart links use correct file paths
- [ ] Vietnamese financial terminology is accurate and professional
- [ ] Confidence scores are manually justified based on signal analysis
- [ ] Top List organized by confidence tiers (90-95%, 85-89%, 75-84%)
- [ ] Potential List categorized by opportunity type
- [ ] Strategic context and portfolio allocation included
- [ ] Actionable entry strategies provided
- [ ] Portfolio holdings from hold.md properly incorporated as market leaders

### Step 7: Complete Manual Protocol Summary
**Objective**: Execute the complete daily planning protocol using natural language analysis

**Complete Manual Execution Sequence**:
1. **Step 1**: Use LS tool to verify input files: `REPORT.md`, `REPORT_week.md`, `LEADER.md`, `GROUP.md`, `PLAN.md`, `vpa_data/`, `market_data/`

2. **Step 2**: Market leaders foundation analysis using Read tool on PLAN.md to identify Top 15 proven leaders

3. **Step 3**: Manual data analysis using natural language:
   - Read REPORT.md and REPORT_week.md manually for signals
   - Read individual vpa_data files for context
   - Use reliable Python only for CSV price data

4. **Step 4**: Manual ticker state assessment using VPA-Strategist methodology:
   - Proven leaders as TOP foundation
   - Manual signal scanning for POTENTIAL candidates
   - Manual identification of DOWNGRADED tickers

5. **Step 5**: Create new PLAN.md using manual analysis results:
   - Use Edit/Write tools to create complete new PLAN.md
   - Apply manual assessment results to categorize tickers
   - Include detailed analysis for top 10+ tickers
   - Provide complete audit trail with manual reasoning

**Final Output**: New `PLAN.md` file with:
- **Market leaders-based TOP list** with manual signal confirmation
- **Manually identified POTENTIAL opportunities** from signal scanning
- **Complete manual assessment** of all relevant tickers
- **Professional Vietnamese financial writing** throughout
- **Complete audit trail** documenting all manual reasoning
- **Exact template format** as specified

## Quality Control Standards

### Data Accuracy Requirements (⚠️ ENHANCED - PREVENT TRADING ERRORS)
- **ZERO TOLERANCE**: No price/volume assertions without CSV verification
- **ZERO TOLERANCE**: No VPA signals without volume pattern verification
- **Date Precision**: All signals must include exact dates from manual reading
- **Source Attribution**: Every claim must trace back to manually read input files
- **Cross-Verification**: Weekly and daily signals must align logically through manual analysis
- **Mathematical Verification**: All percentages and calculations verified
- **Volume Unit Consistency**: All volume figures in millions (M) with CSV verification
- **VPA Pattern Matching**: Volume behavior must match claimed VPA signals

### Vietnamese Language Standards
- Use proper Vietnamese financial terminology throughout
- Maintain professional tone and grammar
- Ensure decimal formatting uses dots (.), not commas (,)
- Use consistent industry naming from GROUP.md (verified manually)
- **NO English terms** - use Vietnamese equivalents for all financial concepts

### Technical Requirements
- **Chart Links**: Verify all image paths exist
- **Markdown Formatting**: Ensure proper headers, links, and structure
- **Confidence Scores**: Base on manual evaluation of signal strength and industry context
- **Audit Trail**: Document manual reasoning for every decision
- **Portfolio Foundation**: Ensure hold.md holdings properly incorporated as market leaders

## Error Handling

### Missing Input Files
- Document missing files in summary
- Use available data and note limitations
- Flag areas requiring manual review
- Continue with manual analysis where possible

### Data Inconsistencies  
- Cross-reference multiple sources manually
- Prioritize most recent and reliable data through manual verification
- Document conflicts in audit log with manual reasoning
- **⚠️ When price/volume conflicts found**: Always verify against CSV files (authoritative source)

### Signal Interpretation Disputes
- Apply conservative Wyckoff methodology manually
- Err on side of caution for state changes
- Provide detailed manual reasoning for controversial decisions
- Prioritize portfolio holdings as market leaders
- **⚠️ Volume Pattern Disputes**: Always check actual CSV volume data

### **⚠️ CRITICAL ERROR PREVENTION** (New Section)

#### Volume Error Prevention
```bash
# MANDATORY process for all volume claims:
uv run -c "
import pandas as pd
import glob
ticker = 'VHM'
try:
    # 1. Find and read the most recent CSV file
    csv_files = glob.glob(f'market_data/{ticker}_*.csv')
    latest_file = max(csv_files) if csv_files else None
    if latest_file:
        df = pd.read_csv(latest_file)
        # 2. Get actual volume from last row
        latest_volume = df.iloc[-1]['Volume']
        # 3. Convert to millions: volume ÷ 1,000,000
        volume_millions = latest_volume / 1_000_000
        # 4. Round to 2 decimal places
        volume_formatted = round(volume_millions, 2)
        # 5. Use this exact figure in PLAN.md
        print(f'{ticker} volume: {volume_formatted}M')
        print(f'Date: {df.iloc[-1][\"Date\"]}')
        print(f'Source: {latest_file}')
    else:
        print(f'No CSV files found for {ticker}')
except Exception as e:
    print(f'Error: {e}')
"
```

#### Weekly Percentage Error Prevention
```bash
# MANDATORY process for weekly % claims:  
uv run -c "
import pandas as pd
import glob
ticker = 'VHM'
try:
    # 1. Find and read the most recent weekly CSV file
    csv_files = glob.glob(f'market_data_week/{ticker}_*.csv')
    latest_file = max(csv_files) if csv_files else None
    if latest_file:
        df = pd.read_csv(latest_file)
        # 2. Get last two closes: current_close, previous_close
        current_close = df.iloc[-1]['Close']
        previous_close = df.iloc[-2]['Close'] if len(df) > 1 else current_close
        # 3. Calculate: (current - previous) / previous × 100
        change_pct = ((current_close - previous_close) / previous_close) * 100
        # 4. Round to 1 decimal place
        change_formatted = round(change_pct, 1)
        # 5. Use this exact percentage in PLAN.md
        print(f'{ticker} weekly change: {change_formatted:+.1f}%')
        print(f'Current week: {df.iloc[-1][\"Date\"]}')
        print(f'Source: {latest_file}')
    else:
        print(f'No weekly CSV files found for {ticker}')
except Exception as e:
    print(f'Error: {e}')
"
```

#### VPA Signal Error Prevention
- **Test for Supply**: Volume MUST decrease (verify in CSV)
- **Sign of Strength**: Volume MUST increase (verify in CSV)
- **No Supply**: Price rises, volume decreases (verify both)
- **If volume pattern doesn't match signal name**: Change the signal name, not the data

## Success Metrics (⚠️ ENHANCED - PREVENT TRADING ERRORS)

- **⚠️ ZERO DATA ERRORS**: No price/volume/percentage errors (verified against CSV)
- **⚠️ ZERO VPA ERRORS**: All VPA signals match actual volume patterns
- **Accuracy**: All manual analysis matches source data exactly
- **Completeness**: All relevant tickers assessed and categorized manually
- **Traceability**: All decisions can be verified from manual audit log
- **Actionability**: Top List provides clear trading opportunities based on portfolio foundation
- **Consistency**: Analysis follows Wyckoff methodology strictly through manual application
- **Vietnamese Quality**: Professional financial terminology throughout
- **Portfolio Integration**: hold.md holdings properly incorporated as market leader foundation
- **Mathematical Precision**: All calculations verified and accurate
- **Volume Unit Consistency**: All volumes properly converted to millions with CSV verification

## Templates for Manual Analysis

### Manual Analysis Workflow Template
```markdown
## Manual Ticker Analysis Workflow

### 1. Market Leaders Foundation Analysis (PLAN.md)
- Read PLAN.md completely for current Top 15 proven leaders
- Identify market leader status and performance  
- Note any underperforming leaders from previous assessment

### 2. Signal Verification Process
For each proven leader:
- Search REPORT.md manually for ticker signals
- Search REPORT_week.md manually for weekly context
- Read vpa_data/[TICKER].md for narrative context
- Use reliable Python only for price data from CSV

### 3. Opportunity Identification
- Manually scan REPORT.md for strong non-Top List signals
- Look for SOS, Effort to Rise patterns
- Verify weekly foundation in REPORT_week.md
- Check industry context in LEADER.md

### 4. Vietnamese Terminology Guidelines
- "Tín hiệu Sức mạnh" = Sign of Strength/SOS
- "Nỗ lực tăng giá" = Effort to Rise
- "Kiểm tra nguồn cung" = Test for Supply
- "Không có nguồn cung" = No Supply
- "Dẫn dắt Đồng thuận" = Leading Consensus
- NO English financial terms in final output
```

### Complete PLAN.md Structure Template (Manual Creation)
```markdown
# PLAN.md - Kế Hoạch Giao Dịch Hàng Ngày

*Cập nhật: [DATE] | Phân tích theo phương pháp VPA-Strategist*

## 1. Phân Tích Trạng Thái VNINDEX & Chiến Lược
[Manual synthesis from REPORT.md + REPORT_week.md]

## 2. Top [X] Cơ Hội Giao Dịch Chất Lượng
[Proven leaders + exceptional candidates from manual analysis]
### Nhóm Tin Cậy Cao (90-95%)
### Nhóm Tin Cậy Tốt (85-89%) 
### Nhóm Tin Cậy Trung Bình (75-84%)

## 3. Danh Sách Cổ Phiếu Tiềm Năng
[Manually identified opportunities from signal scanning]
### Cơ Hội Tăng Trưởng Mạnh
### Cơ Hội Theo Dõi Đặc Biệt
### Cơ Hội Cần Xác Nhận

## 4. Phân Tích Chi Tiết Các Cổ Phiếu Hàng Đầu
[Manual analysis for minimum 10 top tickers]

## 5. Nhật Ký Thay Đổi Kế Hoạch (AUDIT LOG)
[Complete manual reasoning for all changes]
### Cổ Phiếu Được Nâng Lên "Top List":
### Cổ Phiếu Được Thêm Vào "Danh Sách Tiềm Năng":
### Cổ Phiếu Bị Giáng Xuống "Hạ Ưu Tiên":

## 6. Chiến Lược Giao Dịch Tuần Tới
[Portfolio allocation based on manual analysis]
```

## Key Principles for Manual Protocol (⚠️ ENHANCED)

1. **NO AUTOMATED TEXT PARSING** - Human intelligence only
2. **Market Leaders Foundation First** - PLAN.md Top 15 are proven leaders
3. **Vietnamese Financial Terminology** - No English terms in output
4. **Manual Signal Verification** - Read reports directly with human understanding
5. **Reliable Python Only** - CSV, JSON, basic file operations only
6. **Complete Audit Trail** - Document all manual reasoning
7. **Professional Quality** - Maintain high Vietnamese financial writing standards
8. **⚠️ MANDATORY CSV VERIFICATION** - Every price/volume claim verified against CSV
9. **⚠️ VPA PATTERN VERIFICATION** - Volume behavior must match claimed signals
10. **⚠️ MATHEMATICAL VERIFICATION** - All percentages and calculations verified
11. **⚠️ ZERO TOLERANCE FOR DATA ERRORS** - Trading accuracy depends on data precision
