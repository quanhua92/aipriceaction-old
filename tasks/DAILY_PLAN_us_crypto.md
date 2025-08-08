# Daily US & Crypto Planning Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `PLAN_us_crypto.md` file using VPA-Strategist methodology adapted for US indices and cryptocurrency markets. The agent must follow these steps sequentially to ensure accurate, verifiable analysis using natural language processing and reliable Python operations only.

**⚠️ CRITICAL: ALWAYS USE ACTUAL DATA DATES**
- Never assume "today's date" for analysis
- Always get the actual last available date from CSV files using `df.iloc[-1]["Date"]`
- Use `glob.glob()` to find the most recent CSV file for each ticker
- Compare actual data dates with existing analysis dates to determine if new analysis is needed

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current

**Use LS tool to check for required input files:**
- Verify paths: `REPORT_us_crypto.md`, `REPORT_us_crypto_week.md`, `LEADER_us_crypto.md`, `GROUP_us_crypto.md`, `PLAN_us_crypto.md`
- Verify directories: `vpa_data_us_crypto/`, `market_data_us_crypto/`

**Actions**:
- Verify `REPORT_us_crypto.md` exists and contains recent daily signals
- Verify `REPORT_us_crypto_week.md` exists with weekly analysis (reflects last completed trading week)
- Verify `vpa_data_us_crypto/` directory exists with individual ticker VPA files
- Verify `market_data_us_crypto/` directory exists with individual ticker CSV files
- Verify `LEADER_us_crypto.md` exists with industry context analysis
- Verify `GROUP_us_crypto.md` exists with ticker-to-industry mappings
- Verify `PLAN_us_crypto.md` exists with current Top List (market leaders foundation)

**Success Criteria**: All core input files are present and accessible

### Step 1.5: Asset Classification Validation
**Objective**: Ensure all ticker asset classifications match GROUP_us_crypto.md using reliable Python operations

```bash
# Only use reliable Python for CSV/JSON reading
uv run -c "
import pandas as pd
import json

# Read GROUP_us_crypto.md using reliable text operations
with open('GROUP_us_crypto.md', 'r', encoding='utf-8') as f:
    group_content = f.read()
    print('GROUP_us_crypto.md loaded successfully')
    print(f'File size: {len(group_content)} characters')
"
```

**Critical Validation Process**:
- **MANUAL NATURAL LANGUAGE ANALYSIS ONLY** - read GROUP_us_crypto.md directly with Read tool
- Compare ticker asset classifications manually by reading and analyzing text
- Identify mismatched asset classifications through human-readable analysis
- Ensure consistent Vietnamese asset naming conventions for global markets
- NO automated text parsing - use human intelligence for text understanding

**Required Actions**:
- Fix any asset mismatches found manually (e.g., BTC should be "Tiền Điện Tử" not "Chỉ Số")
- Update Vietnamese asset names to match GROUP_us_crypto.md conventions through manual analysis
- Add missing tickers to GROUP_us_crypto.md if needed
- Document any classification changes in audit log

**Success Criteria**: All ticker asset classifications are accurate and consistent

### Step 2: Global Market Leaders Foundation Analysis
**Objective**: Use current Top List from PLAN_us_crypto.md as proven global market leaders foundation

**Actions**:
- **Read PLAN_us_crypto.md using Read tool** to understand current Top List holdings
- Identify the proven US & crypto leaders from existing Top 15 list as foundation
- **Use these leaders as the starting point for the new TOP list**
- Analyze performance and VPA signals for each leader
- **NATURAL LANGUAGE ANALYSIS ONLY** - no Python text parsing

**Proven Global Market Leaders from PLAN_us_crypto.md Top List**:
- **DJI (Chỉ Số Mỹ)**: Proven US market leader, confidence 95%
- **INX (Chỉ Số Mỹ)**: Proven US market leader, confidence 95%
- **BTC (Tiền Điện Tử)**: Proven crypto leader, confidence 90%
- **ETH (Tiền Điện Tử)**: Proven crypto leader, confidence 85%

**Foundation Principle**: These proven global leaders start as TOP candidates unless signals severely deteriorate

**Output**: Proven foundation for creating new TOP, POTENTIAL, and DOWNGRADED lists

### Step 3: STAGE 0 - Manual Data Analysis Using Natural Language
**Objective**: Analyze US & crypto ticker data using natural language processing and reliable Python operations only

**MANUAL ANALYSIS APPROACH - NO TEXT PARSING UTILITIES**:

**For Global Market Leaders (Top List from PLAN_us_crypto.md)**:
1. **Read REPORT_us_crypto.md** using Read tool - manually identify signals for each Top List ticker
2. **Read REPORT_us_crypto_week.md** using Read tool - manually identify weekly signals for each leader
3. **For each leader, read individual vpa_data_us_crypto/{TICKER}.md** using Read tool - extract recent VPA context
4. **Use reliable Python ONLY for CSV operations**:
```bash
# Example reliable Python for price data - gets the most recent CSV file
uv run -c "
import pandas as pd
import glob
ticker = 'DJI'
try:
    # Find the most recent CSV file for this ticker
    csv_files = glob.glob(f'market_data_us_crypto/{ticker}_*.csv')
    if not csv_files:
        print(f'No CSV files found for {ticker}')
    else:
        # Get the most recent file by modification time or filename
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        latest = df.iloc[-1]  # Last row = most recent data
        print(f'{ticker}: Latest date={latest[\"time\"]}, Close={latest[\"close\"]}')
        print(f'CSV file: {latest_file}')
        print(f'Data date range: {df.iloc[0][\"time\"]} to {df.iloc[-1][\"time\"]}')
except Exception as e:
    print(f'Could not read CSV for {ticker}: {e}')
"
```

**For Potential Candidates (Beyond Top List)**:
1. **Read TICKERS_US.csv and TICKERS_CRYPTO.csv using reliable Python**:
```bash
uv run -c "
import pandas as pd
us_tickers = pd.read_csv('TICKERS_US.csv')
crypto_tickers = pd.read_csv('TICKERS_CRYPTO.csv')
print(f'US tickers to analyze: {len(us_tickers)}')
print(f'Crypto tickers to analyze: {len(crypto_tickers)}')
print('Sample US tickers:', us_tickers.head().to_list())
print('Sample crypto tickers:', crypto_tickers.head().to_list())
"
```
2. **Manually scan REPORT_us_crypto.md for strong signals (SOS, Effort to Rise)** from non-Top List tickers
3. **Use Read tool to check individual vpa_data_us_crypto files** for promising candidates
4. **Manual analysis of weekly patterns** from REPORT_us_crypto_week.md
5. **Review current Potential List** from PLAN_us_crypto.md for promotion candidates

**Data Analysis Rules**:
- **NO automated text parsing or regex operations**
- **Use natural language understanding to read reports**
- **Use reliable Python ONLY for CSV, JSON, basic file operations**
- **Extract signals manually by reading and understanding context**
- **Cross-reference findings using human intelligence, not automation**

**Quality Control**: Manual verification ensures accuracy over automation

### Step 3.5: Mandatory Asset Class Context Analysis

**CRITICAL PROTOCOL**: Before making any sell recommendations or negative assessments, MUST conduct comprehensive asset class peer analysis to prevent isolated signal interpretation errors.

#### 3.5.1 Asset Class Peer Identification
For each ticker showing negative signals:
1. **Identify Asset Class**: Check @GROUP_us_crypto.md for ticker's asset classification
2. **List All Peers**: Gather all tickers in same asset class (US Indices vs Crypto)
3. **Priority Peers**: Focus on major players with similar market significance

#### 3.5.2 Peer VPA Signal Analysis
For each asset class peer:
1. **Read Recent VPA**: Check last 3-5 entries in vpa_data_us_crypto/[TICKER].md
2. **Signal Classification**: Categorize as Bullish/Bearish/Neutral
3. **Volume Trends**: Compare volume patterns across peers
4. **Price Performance**: Check relative strength within asset class

#### 3.5.3 Asset Class Strength Assessment
**Asset Class Classification Rules**:
- **Asset Rotation OUT**: If 70%+ of peers show weakness (bearish VPA signals)
- **Asset Rotation IN**: If 70%+ of peers show strength (bullish VPA signals)  
- **Asset Mixed/Consolidating**: If 40-60% mixed signals
- **Isolated Weakness**: If <30% show weakness (target ticker may be laggard)
- **Isolated Strength**: If <30% show strength (target ticker may be leader)

#### 3.5.4 Context-Adjusted Recommendations
**Decision Matrix**:

| Individual Signal | Asset Class Context | Action | Rationale |
|------------------|----------------|--------|--------------|
| Bearish VPA | Asset Rotation OUT | SELL/REDUCE | Confirmed asset weakness |
| Bearish VPA | Asset Strong/Mixed | HOLD/MONITOR | Likely temporary weakness |
| Bearish VPA | Isolated Weakness | HOLD/BUY DIP | Laggard catch-up opportunity |
| Bullish VPA | Asset Rotation IN | BUY/INCREASE | Asset momentum confirmed |
| Bullish VPA | Asset Weak/Mixed | CAUTION | May be false breakout |

#### 3.5.5 Asset Class Analysis Documentation
For each ticker analysis, document:
```markdown
**[TICKER] Asset Analysis ([ASSET_CLASS])**
- Asset Peers: [List major peers in same class]
- Peer Signals: [Count bullish/bearish/neutral]
- Asset Strength: [Strong/Weak/Mixed/Rotation]
- Context Rating: [High confidence/Low confidence]
- Recommendation Adjustment: [None/Hold instead of Sell/etc.]
```

#### 3.5.6 Special Cases Requiring Extra Scrutiny
- **US Indices**: DJI, INX, COMP, RUT - economic sentiment indicators
- **Major Crypto**: BTC, ETH - crypto market leaders with systemic implications
- **Stable Crypto**: USDT, USDC - stability and liquidity indicators

### Step 4: STAGE 1 - Manual Ticker State Assessment Using VPA-Strategist Methodology
**Objective**: Determine new state for each US & crypto ticker using manual analysis and VPA principles

**MANUAL ASSESSMENT PROCESS - NO AUTOMATED UTILITIES**:

**Foundation Principle**: Top proven leaders from PLAN_us_crypto.md are global market leaders and form the core TOP list unless severely compromised

**Assessment Categories**:

#### For Global Market Leaders (Current Top List):
**MANUAL ANALYSIS APPROACH**:
1. **Read PLAN_us_crypto.md Top List** - understand current proven leaders and their VPA status
2. **Cross-reference with REPORT_us_crypto.md** - manually find daily signals for each leader
3. **Cross-reference with REPORT_us_crypto_week.md** - manually find weekly signals for each leader
4. **Apply VPA-Strategist methodology manually**

**Assessment Rules for Global Market Leaders**:
- **DJI, INX, BTC, ETH**: Start as TOP candidates (proven leaders)
- **High threshold for removing proven leaders** - they have demonstrated consistent performance
- **Weekly signals dominate** - daily signals fine-tune confidence levels
- **Confidence scoring**: 95% (strong weekly+daily), 85% (weekly strong, daily mixed), 75% (weekly neutral, daily strong)

#### For Non-Top List Strong Signal Candidates:
**MANUAL IDENTIFICATION PROCESS**:
1. **Scan REPORT_us_crypto.md manually** - look for strong daily signals (SOS, Effort to Rise) from non-Top List tickers
2. **Check weekly context in REPORT_us_crypto_week.md** - confirm weekly foundation for candidates
3. **Read individual vpa_data_us_crypto files** for context on promising tickers
4. **Apply manual VPA assessment** - evaluate for POTENTIAL list inclusion

**Promotion Criteria**:
- **Daily SOS + Weekly supportive**: Strong POTENTIAL candidate
- **Daily Effort to Rise + Asset class strength**: Consider for POTENTIAL
- **Multiple day patterns**: Higher confidence for POTENTIAL inclusion
- **New breakouts**: Fast-track evaluation for opportunities

#### For Previously Downgraded Tickers:
**RECOVERY ASSESSMENT**:
- **Manual scan for recovery signals** in daily and weekly reports
- **Fast recovery on strong signals** - daily SOS can promote to POTENTIAL quickly
- **Patient approach** - allow time for signal confirmation
- **Asset class context matters** - asset class improvement supports recovery

#### For Unlisted Ticker Universe:
**OPPORTUNITY SCANNING**:
- **Manual review of strong signals** from entire ticker universe in reports
- **Focus on SOS and Effort to Rise** patterns for new opportunities
- **Asset class rotation opportunities** - look for emerging asset strength
- **Don't miss breakouts** - prioritize capturing new trends early

**MANUAL ASSESSMENT OUTPUT**:
- **New TOP List**: Proven leaders + any exceptional new candidates (manual assessment)
- **New POTENTIAL List**: Strong signal candidates not yet in TOP (manual assessment)  
- **New DOWNGRADED List**: Weakening tickers requiring monitoring (manual assessment)
- **Confidence scores**: Based on manual evaluation of signal strength and context
- **Complete audit trail**: Document all reasoning for state changes

### Step 5: STAGE 2 - PLAN_us_crypto.md Creation Using Manual Natural Language Analysis
**Objective**: Create new PLAN_us_crypto.md using manual analysis and natural language understanding

**MANUAL CREATION PROCESS - NO AUTOMATED UTILITIES**:

**Key Requirements**:
- **Create completely new PLAN_us_crypto.md** based on manual analysis results
- **Use portfolio holdings from hold_us_crypto.md as foundation** for TOP list
- **Apply manual VPA assessment results** to categorize all tickers appropriately
- **Maintain professional Vietnamese financial writing style** with global market context
- **Include proper audit trail** documenting all changes and reasoning
- **EXACT OUTPUT FORMAT** as specified in template

**Quality Standards**:
- Organize Top List by confidence tiers (90-95%, 85-89%, 75-84%)
- Categorize Potential List by opportunity type (Strong Growth, Special Watch, Need Confirmation)
- Add strategic context and portfolio allocation recommendations for global markets
- Include actionable entry strategies and risk management guidance
- Provide comprehensive global market analysis with both weekly and daily synthesis

**Data Sources for Manual Analysis**:
- `PLAN_us_crypto.md`: Global market leaders foundation from proven Top List
- `REPORT_us_crypto.md` and `REPORT_us_crypto_week.md`: Market analysis and ticker signals (manual reading)
- `LEADER_us_crypto.md` and `GROUP_us_crypto.md`: Asset context and classification analysis (manual reading)
- Individual `vpa_data_us_crypto/*.md` files: Ticker-specific VPA context (manual reading)
- Reliable Python for CSV price data only

#### 5.1 Global Market Analysis Section
```markdown
## 1. Phân Tích Trạng Thái Thị Trường Toàn Cầu & Chiến Lược

![US Weekly Chart](reports_us_crypto_week/DJI/DJI_candlestick_chart.png) ![US Daily Chart](reports_us_crypto/DJI/DJI_candlestick_chart.png)
![Crypto Weekly Chart](reports_us_crypto_week/BTC/BTC_candlestick_chart.png) ![Crypto Daily Chart](reports_us_crypto/BTC/BTC_candlestick_chart.png)

**Bối Cảnh Tuần Chỉ Số Mỹ**: [Synthesize US weekly context from REPORT_us_crypto_week.md]

**Bối Cảnh Tuần Tiền Điện Tử**: [Synthesize crypto weekly context from REPORT_us_crypto_week.md]

**Hành Động Gần Đây**: [Describe how recent daily action from REPORT_us_crypto.md confirms/contradicts weekly picture]

**Vùng Tốt Nhất Để Gia Tăng Tỷ Trọng**: [Define specific support/resistance levels with justification]
```

#### 5.2 Top List Generation (Global Market Leaders Foundation + Strong Signals)
**MANUAL GENERATION RULES**:
- **Global Market Leaders Priority**: Start with proven leaders from PLAN_us_crypto.md (DJI, INX, BTC, ETH)
- **Manual signal confirmation**: Verify each leader has supportive signals in reports
- **Add exceptional new candidates**: Based on manual signal analysis from broader universe
- **Confidence Score Strategy**: Manual assessment (95% → 85% → 75%) based on signal strength
- **Vietnamese terminology**: Use proper financial terms with global market context
- **REQUIRED FORMAT**: `[**DJI**](#DJI) (Chỉ Số Mỹ) - **95%** - Tín hiệu mạnh mẽ - [View Report](REPORT_us_crypto.md#DJI)`
- **Score Guidelines**: 
  - 95%: Perfect weekly/daily alignment with strong asset class
  - 85%: Minor daily weakness but weekly trend intact
  - 75%: Temporary consolidation but fundamentally sound
- **MANDATORY ORGANIZED STRUCTURE**:
  ```markdown
  ## 2. Top [X] Cơ Hội Giao Dịch Chất Lượng Toàn Cầu
  
  ### Nhóm Tin Cậy Cao (85-95%) - Portfolio Core
  1. [**DJI**](#DJI) (Chỉ Số Mỹ) - **90%** - Description - [View Report](REPORT_us_crypto.md#DJI)
  2. [**BTC**](#BTC) (Tiền Điện Tử) - **90%** - Description - [View Report](REPORT_us_crypto.md#BTC)
  
  ### Nhóm Tin Cậy Tốt (75-84%) - Strategic Holdings
  3. [**INX**](#INX) (Chỉ Số Mỹ) - **80%** - Description - [View Report](REPORT_us_crypto.md#INX)
  
  ### Nhóm Quan Sát Cẩn Thận (65-74%) - Tactical Positions
  4. [**ETH**](#ETH) (Tiền Điện Tử) - **70%** - Description - [View Report](REPORT_us_crypto.md#ETH)
  ```

#### 5.3 Potential List Generation (Manual Signal Scanning)
**MANUAL GENERATION RULES**:
- **Manual signal identification**: Scan REPORT_us_crypto.md for strong signals from non-Top List tickers
- **Weekly foundation check**: Verify weekly context supports daily signals
- **Asset class context**: Consider asset strength from LEADER_us_crypto.md analysis
- **Opportunity categorization**: Group by signal strength and timing
- **Vietnamese descriptions**: Emphasize weekly foundation + daily catalyst
- **Fast-track indicators**: Mark tickers ready for potential Top List promotion

#### 5.4 Downgraded List Generation (Manual Assessment)
**MANUAL GENERATION RULES**:
- **Check current Downgraded**: Review existing downgraded tickers in PLAN_us_crypto.md
- **Manual weakness identification**: Look for consistent bearish signals in proven leaders
- **Include reasoning**: Cite specific signals that triggered demotion
- **Monitor for recovery**: Track potential reversal signals

#### 5.5 Detailed Analysis for Top Tickers
**MINIMUM REQUIREMENT**: Provide detailed analysis for **ALL TOP LIST TICKERS** (not just 10)

**MANDATORY FORMAT** for EACH ticker analysis section:
```markdown
### **[TICKER] ([ASSET_CLASS])**
![Weekly Chart](reports_us_crypto_week/[TICKER]/[TICKER]_candlestick_chart.png) ![Daily Chart](reports_us_crypto/[TICKER]/[TICKER]_candlestick_chart.png)

* **Giá Hiện Tại:** [PRICE] USD
* **Tín Hiệu VPA Tuần:** [Weekly VPA narrative with exact dates]
* **Tín Hiệu VPA Ngày:** [Daily VPA narrative with exact dates]
* **Bối Cảnh Tài Sản:** [Asset class context from LEADER_us_crypto.md]
* **Phân Tích Thiết Lập:** [Synthesis explaining high-conviction setup]
* **Vùng Vào Tốt Nhất:** [Best entry zones with technical justification]
```

**CRITICAL REQUIREMENTS**:
- **Current Price Format**: MUST use standard USD format (e.g., 44,250.00 USD, 95,420.50 USD)
- **Price Source**: Extract from latest CSV market data file using glob.glob(f'market_data_us_crypto/{TICKER}_*.csv') to find most recent file
- **All Top List Tickers**: Every ticker in Top List must have detailed section
- **Vietnamese Terms**: All analysis in professional Vietnamese financial terminology
- **Chart Links**: Verify paths exist for both weekly and daily charts

**Selection Priority**: **ALL TOP LIST TICKERS** must have detailed analysis sections

#### 5.6 Audit Log Creation
**Mandatory documentation** of ALL state changes with precise justifications:

```markdown
## 6. Nhật Ký Thay Đổi Kế Hoạch (AUDIT LOG)

### Tài Sản Được Nâng Lên "Top List":
- **ABC**: Từ `Potential List`. Lý do: REPORT_us_crypto.md ghi nhận **'SOS' ngày YYYY-MM-DD**, xác nhận **'SOS' tuần kết thúc YYYY-MM-DD**. LEADER_us_crypto.md xác nhận tài sản 'Dẫn dắt Đồng Thuận'.

### Tài Sản Được Thêm Vào "Potential List":
- **XYZ**: Từ `Unlisted`. Lý do: **'SOS' ngày YYYY-MM-DD** với biểu đồ tuần trong vùng Tích Lũy.

### Tài Sản Bị Giáng Xuống "Hạ Ưu Tiên":
- **BTC**: Từ `Top List`. Lý do: **'Sign of Weakness' ngày YYYY-MM-DD** sau 'Upthrust' tuần kết thúc YYYY-MM-DD.

### Tài Sản Bị Loại Bỏ Hoàn Toàn:
- **ETH**: Từ `Downgraded`. Lý do: **'No Demand' ngày YYYY-MM-DD** xác nhận xu hướng giảm.
```

### Step 6: **CRITICAL DATA VERIFICATION** (Prevent Trading Errors)
**Objective**: Ensure PLAN_us_crypto.md accuracy and completeness through systematic data verification

**⚠️ MANDATORY DATA ACCURACY VERIFICATION** (Based on Real Error Patterns):

#### 6.1 **Price Data Verification** (Zero Tolerance for Errors)
```bash
# For EVERY ticker mentioned in PLAN_us_crypto.md, verify using most recent CSV file:
uv run -c "
import pandas as pd
import glob
ticker = 'DJI'
try:
    # Find the most recent CSV file for this ticker
    csv_files = glob.glob(f'market_data_us_crypto/{ticker}_*.csv')
    if csv_files:
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        print(f'Using file: {latest_file}')
        print(f'Data range: {df.iloc[0][\"time\"]} to {df.iloc[-1][\"time\"]}')
        print('Last 5 rows for verification:')
        print(df.tail(5)[['time', 'open', 'high', 'low', 'close', 'volume']])
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

tickers = ['DJI', 'INX', 'BTC', 'ETH']

for ticker in tickers:
    try:
        # Find the most recent CSV file for this ticker
        csv_files = glob.glob(f'market_data_us_crypto/{ticker}_*.csv')
        if csv_files:
            latest_file = max(csv_files)
            df = pd.read_csv(latest_file)
            latest = df.iloc[-1]  # Last row = most recent data
            price = float(latest['close'])
            # Format for global markets: 44,250.00 USD
            formatted_price = f'{price:,.2f}'
            print(f'* **Giá Hiện Tại:** {formatted_price} USD')
            print(f'  (Date: {latest[\"time\"]}, File: {latest_file})')
        else:
            print(f'No CSV files found for {ticker}')
    except Exception as e:
        print(f'Error reading {ticker}: {e}')
"
```

**Critical Checks**:
- [ ] **Current Prices**: MUST be in USD format (XXX,XXX.XX USD) for ALL Top List tickers
- [ ] **Daily Prices**: Open, High, Low, Close match CSV data exactly
- [ ] **Gap Claims**: "gap up X" must match actual Open vs Previous Close
- [ ] **Price Movements**: "từ X xuống Y" must match actual data
- [ ] **Price Ranges**: All claimed price ranges verified against CSV

#### 6.2 **Volume Data Verification** (⚠️ HIGHEST ERROR AREA)
```bash
# Volume verification process:
# 1. Read CSV volume column (actual units)
# 2. Convert to appropriate display format for asset class
# 3. Verify PLAN_us_crypto.md claims match calculated values
```

**Critical Volume Checks**:
- [ ] **Volume Figures**: All volume claims verified against CSV
- [ ] **Volume Comparisons**: "doubled", "increased 60%" calculated and verified
- [ ] **Volume Direction**: "volume tăng/giảm" matches actual direction
- [ ] **Volume Patterns**: VPA interpretations match actual volume behavior

#### 6.3 **Weekly Data Verification** (⚠️ COMMON ERROR AREA)
```bash
# For weekly claims, use most recent weekly data files:
uv run -c "
import pandas as pd
import glob
ticker = 'DJI'
try:
    # Find the most recent weekly CSV file
    csv_files = glob.glob(f'market_data_us_crypto_week/{ticker}_*.csv')
    if csv_files:
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        print(f'Using weekly file: {latest_file}')
        print(f'Weekly data range: {df.iloc[0][\"time\"]} to {df.iloc[-1][\"time\"]}')
        # Calculate actual weekly percentage changes
        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else df.iloc[-1]
        change_pct = ((latest[\"close\"] - previous[\"close\"]) / previous[\"close\"]) * 100
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
- [ ] **Volume Consistency**: Consistent volume reporting throughout
- [ ] **Support/Resistance Logic**: Support < Current Price < Resistance

#### 6.6 **Cross-Reference Verification**
```bash
# Verify claims against VPA data files:
Read: /Volumes/data/workspace/aipriceaction/vpa_data_us_crypto/{TICKER}.md
# Check latest entries match PLAN_us_crypto.md claims
```

**Cross-Reference Checks**:
- [ ] **VPA Data Consistency**: Claims match latest vpa_data_us_crypto entries
- [ ] **Signal Dates**: All dates referenced exist and are accurate
- [ ] **Historical Context**: Previous signals correctly referenced

**⚠️ ERROR PREVENTION PRIORITIES** (Based on Actual Findings):
1. **Volume Errors** - HIGHEST PRIORITY
2. **Weekly Percentage Errors** - HIGH PRIORITY  
3. **VPA Signal Misinterpretation** - CRITICAL
4. **New Opportunities Section** - SPECIAL ATTENTION

**Manual Verification Checklist** (Enhanced):
- [ ] All assertions cite specific signals and dates from manual analysis
- [ ] **⚠️ ZERO price/volume errors** - every figure verified against CSV
- [ ] **⚠️ All VPA signals** match actual volume patterns
- [ ] **⚠️ Weekly percentages** calculated and verified
- [ ] No ticker appears in multiple categories
- [ ] **MANDATORY**: ALL TOP LIST TICKERS have detailed analysis sections
- [ ] **MANDATORY**: Current prices in USD format for all detailed sections
- [ ] **MANDATORY**: Top List organized with numbered tiers and group headers
- [ ] Complete audit log documents every state change with manual justification
- [ ] Global market analysis synthesizes both daily and weekly timeframes from reports
- [ ] Chart links use correct file paths
- [ ] Vietnamese financial terminology is accurate and professional
- [ ] Confidence scores are manually justified based on signal analysis
- [ ] Top List organized by confidence tiers (90-95%, 85-89%, 75-84%)
- [ ] Potential List categorized by opportunity type
- [ ] Strategic context and portfolio allocation included
- [ ] Actionable entry strategies provided
- [ ] Portfolio holdings from hold_us_crypto.md properly incorporated as global market leaders

### Step 7: Complete Manual Protocol Summary
**Objective**: Execute the complete US & crypto planning protocol using natural language analysis

**Complete Manual Execution Sequence**:
1. **Step 1**: Use LS tool to verify input files: `REPORT_us_crypto.md`, `REPORT_us_crypto_week.md`, `LEADER_us_crypto.md`, `GROUP_us_crypto.md`, `PLAN_us_crypto.md`, `vpa_data_us_crypto/`, `market_data_us_crypto/`

2. **Step 2**: Global market leaders foundation analysis using Read tool on PLAN_us_crypto.md to identify proven leaders

3. **Step 3**: Manual data analysis using natural language:
   - Read REPORT_us_crypto.md and REPORT_us_crypto_week.md manually for signals
   - Read individual vpa_data_us_crypto files for context
   - Use reliable Python only for CSV price data

4. **Step 4**: Manual ticker state assessment using VPA-Strategist methodology:
   - Proven leaders as TOP foundation
   - Manual signal scanning for POTENTIAL candidates
   - Manual identification of DOWNGRADED tickers

5. **Step 5**: Create new PLAN_us_crypto.md using manual analysis results:
   - Use Edit/Write tools to create complete new PLAN_us_crypto.md
   - Apply manual assessment results to categorize tickers
   - Include detailed analysis for all top tickers
   - Provide complete audit trail with manual reasoning

**Final Output**: New `PLAN_us_crypto.md` file with:
- **Global market leaders-based TOP list** with manual signal confirmation
- **Manually identified POTENTIAL opportunities** from signal scanning
- **Complete manual assessment** of all relevant tickers
- **Professional Vietnamese financial writing** with global market context
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
- **Volume Consistency**: All volume figures properly verified with CSV
- **VPA Pattern Matching**: Volume behavior must match claimed VPA signals

### Vietnamese Language Standards
- Use proper Vietnamese financial terminology throughout with global market context
- Maintain professional tone and grammar
- Ensure decimal formatting uses appropriate format for asset class
- Use consistent asset naming from GROUP_us_crypto.md (verified manually)
- **NO English terms** - use Vietnamese equivalents for all financial concepts

### Technical Requirements
- **Chart Links**: Verify all image paths exist
- **Markdown Formatting**: Ensure proper headers, links, and structure
- **Confidence Scores**: Base on manual evaluation of signal strength and asset context
- **Audit Trail**: Document manual reasoning for every decision
- **Portfolio Foundation**: Ensure hold_us_crypto.md holdings properly incorporated as global market leaders

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
- Prioritize portfolio holdings as global market leaders
- **⚠️ Volume Pattern Disputes**: Always check actual CSV volume data

## Success Metrics (⚠️ ENHANCED - PREVENT TRADING ERRORS)

- **⚠️ ZERO DATA ERRORS**: No price/volume/percentage errors (verified against CSV)
- **⚠️ ZERO VPA ERRORS**: All VPA signals match actual volume patterns
- **Accuracy**: All manual analysis matches source data exactly
- **Completeness**: All relevant tickers assessed and categorized manually
- **Traceability**: All decisions can be verified from manual audit log
- **Actionability**: Top List provides clear trading opportunities based on portfolio foundation
- **Consistency**: Analysis follows Wyckoff methodology strictly through manual application
- **Vietnamese Quality**: Professional financial terminology throughout with global context
- **Portfolio Integration**: hold_us_crypto.md holdings properly incorporated as global market leader foundation
- **Mathematical Precision**: All calculations verified and accurate
- **Volume Consistency**: All volumes properly verified with CSV

## Templates for Manual Analysis

### Manual Analysis Workflow Template
```markdown
## Manual US & Crypto Ticker Analysis Workflow

### 1. Global Market Leaders Foundation Analysis (PLAN_us_crypto.md)
- Read PLAN_us_crypto.md completely for current proven leaders
- Identify global market leader status and performance  
- Note any underperforming leaders from previous assessment

### 2. Signal Verification Process
For each proven leader:
- Search REPORT_us_crypto.md manually for ticker signals
- Search REPORT_us_crypto_week.md manually for weekly context
- Read vpa_data_us_crypto/[TICKER].md for narrative context
- Use reliable Python only for price data from CSV

### 3. Opportunity Identification
- Manually scan REPORT_us_crypto.md for strong non-Top List signals
- Look for SOS, Effort to Rise patterns
- Verify weekly foundation in REPORT_us_crypto_week.md
- Check asset context in LEADER_us_crypto.md

### 4. Vietnamese Terminology Guidelines
- "Tín hiệu Sức mạnh" = Sign of Strength/SOS
- "Nỗ lực tăng giá" = Effort to Rise
- "Kiểm tra nguồn cung" = Test for Supply
- "Không có nguồn cung" = No Supply
- "Chỉ Số Mỹ" = US Index
- "Tiền Điện Tử" = Cryptocurrency
- "Dẫn dắt Đồng thuận" = Leading Consensus
- NO English financial terms in final output
```

### Complete PLAN_us_crypto.md Structure Template (Manual Creation)
```markdown
# PLAN_us_crypto.md - Kế Hoạch Giao Dịch Toàn Cầu Hàng Ngày

*Cập nhật: [DATE] | Phân tích theo phương pháp VPA-Strategist cho Thị Trường Toàn Cầu*

## 1. Phân Tích Trạng Thái Thị Trường Toàn Cầu & Chiến Lược
[Manual synthesis from REPORT_us_crypto.md + REPORT_us_crypto_week.md]

## 2. Top [X] Cơ Hội Giao Dịch Chất Lượng Toàn Cầu
[Proven leaders + exceptional candidates from manual analysis]
### Nhóm Tin Cậy Cao (90-95%)
### Nhóm Tin Cậy Tốt (85-89%) 
### Nhóm Tin Cậy Trung Bình (75-84%)

## 3. Danh Sách Tài Sản Tiềm Năng Toàn Cầu
[Manually identified opportunities from signal scanning]
### Cơ Hội Tăng Trưởng Mạnh
### Cơ Hội Theo Dõi Đặc Biệt
### Cơ Hội Cần Xác Nhận

## 4. Phân Tích Chi Tiết Các Tài Sản Hàng Đầu
[Manual analysis for all top tickers]

## 5. Nhật Ký Thay Đổi Kế Hoạch (AUDIT LOG)
[Complete manual reasoning for all changes]
### Tài Sản Được Nâng Lên "Top List":
### Tài Sản Được Thêm Vào "Danh Sách Tiềm Năng":
### Tài Sản Bị Giáng Xuống "Hạ Ưu Tiên":

## 6. Chiến Lược Giao Dịch Tuần Tới
[Portfolio allocation based on manual analysis]
```

## Key Principles for Manual Protocol (⚠️ ENHANCED)

1. **NO AUTOMATED TEXT PARSING** - Human intelligence only
2. **Global Market Leaders Foundation First** - PLAN_us_crypto.md proven leaders
3. **Vietnamese Financial Terminology** - No English terms in output, with global context
4. **Manual Signal Verification** - Read reports directly with human understanding
5. **Reliable Python Only** - CSV, JSON, basic file operations only
6. **Complete Audit Trail** - Document all manual reasoning
7. **Professional Quality** - Maintain high Vietnamese financial writing standards for global markets
8. **⚠️ MANDATORY CSV VERIFICATION** - Every price/volume claim verified against CSV
9. **⚠️ VPA PATTERN VERIFICATION** - Volume behavior must match claimed signals
10. **⚠️ MATHEMATICAL VERIFICATION** - All percentages and calculations verified
11. **⚠️ ZERO TOLERANCE FOR DATA ERRORS** - Trading accuracy depends on data precision
12. **Asset Class Context** - Consider US vs crypto market dynamics in all analysis