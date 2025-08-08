# Weekly US & Crypto Leader Analysis Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `LEADER_us_crypto.md` file using the VPA-AssetLead methodology with **manual natural language analysis only**. No unreliable Python text parsing utilities.

**⚠️ CRITICAL: ALWAYS USE ACTUAL DATA DATES**
- Never assume "today's date" or "this week" for analysis
- Always get the actual last available date from CSV files using `df.iloc[-1]["time"]`
- Use `glob.glob()` to find the most recent CSV file for each ticker
- Compare actual data dates with existing analysis dates to determine if new analysis is needed

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current

**Use LS tool to check for required input files:**
- Verify paths: `GROUP_us_crypto.md`, `REPORT_us_crypto_week.md`
- Verify directories: `vpa_data_us_crypto_week/`, `market_data_us_crypto_week/`

**Manual Verification Actions**:
- **Use Read tool** to verify `GROUP_us_crypto.md` exists with asset-class-to-ticker mappings
- **Use LS tool** to verify `vpa_data_us_crypto_week/` directory exists with individual ticker weekly VPA files
- **Use Read tool** to verify `REPORT_us_crypto_week.md` exists with weekly analysis and signals
- **Use LS tool** to verify `market_data_us_crypto_week/` directory exists with individual ticker weekly CSV files (last 6 months)

**Success Criteria**: All core input files are present and accessible through manual verification

### Step 2: STAGE 0 - Manual Ticker Profile Creation
**Objective**: Create verified internal ticker profiles for ALL tickers using manual natural language analysis

**Manual Processing Approach**: Use Task tools to process asset classes with **manual natural language analysis guidance**, with each asset class processing its tickers through human intelligence.

**Critical Manual Process**: For EVERY ticker from GROUP_us_crypto.md, manually create this internal data structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "asset_class": "Asset class name from GROUP_us_crypto.md - manually verified",
  "full_vpa_story_summary": "Concise summary from vpa_data_us_crypto_week/{TICKER}.md - manually analyzed",
  "recent_vpa_signals": [
    {"signal": "SOS Bar - manually identified", "date": "2025-07-07"},
    {"signal": "Test for Supply - manually identified", "date": "2025-06-30"}
  ],
  "price_history_data": "Raw weekly OHLCV from most recent market_data_us_crypto_week/{TICKER}_*.csv using reliable Python with glob.glob()",
  "base_period_start": "Asset class base period start date - manually determined",
  "base_period_end": "Asset class base period end date - manually determined"
}
```

**Manual File Reading Strategy for Each Ticker**:
1. **Use Read tool** to manually read `vpa_data_us_crypto_week/{TICKER}.md` for complete weekly VPA story - manual analysis
2. **Use reliable Python** to read the most recent `market_data_us_crypto_week/{TICKER}_*.csv` file for price history and calculations:
```bash
# Example reliable Python for weekly price data - gets most recent CSV file
uv run -c "
import pandas as pd
import glob
ticker = 'DJI'
try:
    # Find the most recent weekly CSV file for this ticker
    csv_files = glob.glob(f'market_data_us_crypto_week/{ticker}_*.csv')
    if not csv_files:
        print(f'No weekly CSV files found for {ticker}')
    else:
        # Get the most recent file by modification time or filename
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        latest = df.iloc[-1]  # Last row = most recent week
        print(f'{ticker}: Latest week ending {latest[\"time\"]}, Close={latest[\"close\"]}')
        print(f'CSV file: {latest_file}')
        print(f'Weekly data range: {df.iloc[0][\"time\"]} to {df.iloc[-1][\"time\"]}')
        print(f'Performance: {((df.iloc[-1][\"close\"] / df.iloc[0][\"close\"]) - 1) * 100:.2f}%')
except Exception as e:
    print(f'Could not read CSV for {ticker}: {e}')
"
```
3. **Manual extraction** of recent VPA signals from ticker file (last 2-3 significant signals) using human intelligence
4. **Manual calculation** of performance from asset class base period to latest close

**Manual Data Extraction Rules**:
- **Manual extraction** of asset class mappings from `GROUP_us_crypto.md` using Read tool
- **Manual extraction** of VPA story summaries from individual `vpa_data_us_crypto_week/{TICKER}.md` files using Read tool
- **Manual extraction** of recent signals from both individual VPA files and `REPORT_us_crypto_week.md` using Read tool
- **Reliable Python only** for price data from individual `market_data_us_crypto_week/{TICKER}_*.csv` files

**Manual Processing Strategy**:
- Use Task tools to process multiple tickers with **manual analysis instructions**
- **NO automated text parsing** - all VPA signal identification through human intelligence
- Read ticker-specific files using Read tool for VPA data and reliable Python for CSV data
- **Manual verification** of all extracted information

**Quality Control**: These manually created ticker profiles become the SOLE source of truth for all subsequent stages

**Example Manual Task Tool Usage by Asset Class**:
```
Task 1: "MANUAL ANALYSIS ONLY - Process US_INDICES asset class tickers (DJI,INX,COMP,RUT,NYA,RUI,RUA) for weekly leader analysis. For each: 1) Use Read tool to manually read vpa_data_us_crypto_week/{TICKER}.md full story and manually analyze VPA narrative 2) Use reliable Python to read market_data_us_crypto_week/{TICKER}_*.csv for price history 3) Manually identify recent VPA signals using human intelligence 4) Return manually-created ticker profile JSON with VPA summary and recent signals. NO automated text parsing."

Task 2: "MANUAL ANALYSIS ONLY - Process MAJOR_CRYPTO asset class tickers (BTC,ETH) for weekly leader analysis. Same manual process as Task 1. Use Read tool for VPA analysis, reliable Python for CSV data, manual signal identification."
```

### Step 3: STAGE 1 - Manual Asset Class Strength Assessment
**Objective**: Categorize each asset class based on manually analyzed ticker profiles

**Manual Assessment Categories**:

#### **Dẫn Dắt Đồng Thuận (Leading Consensus)**
- **70%+ tickers** showing strong VPA signals (SOS, Effort to Rise, Strong Weekly Bar)
- **Manual verification**: Most tickers manually confirmed with bullish weekly patterns
- **Asset class momentum**: Clear directional bias confirmed through manual analysis
- **Vietnamese description**: "Tài sản dẫn dắt thị trường với tín hiệu mạnh mẽ"

#### **Hỗn Hợp Tín Hiệu (Mixed Signals)**  
- **40-70% tickers** with mixed or conflicting signals
- **Manual verification**: Some strength, some weakness identified manually
- **Vietnamese description**: "Tài sản có tín hiệu hỗn hợp, cần theo dõi"

#### **Yếu Kém (Weakness)**
- **70%+ tickers** showing weakness (SOW, Effort to Fall, Supply)
- **Manual verification**: Broad-based weakness confirmed through manual analysis
- **Vietnamese description**: "Tài sản đang yếu kém, thận trọng"

#### **Không Xác Định (Undefined)**
- **Insufficient data** or **contradictory patterns** identified through manual analysis
- **Manual assessment**: Requires more time to develop clear picture
- **Vietnamese description**: "Cần thêm thời gian để xác định xu hướng"

**Manual Assessment Process**:
- **Use only manually created ticker profiles** from Stage 0
- **Manual evaluation** of VPA signal patterns across asset class
- **Manual calculation** of percentage of tickers in each signal category
- **NO automated signal categorization** - human intelligence only

**Success Criteria**: Each asset class manually assigned to appropriate category with Vietnamese description

### Step 4: STAGE 2 - Manual Individual Asset Leaders Identification
**Objective**: Identify standout individual assets within each asset class using manual analysis

**Manual Leader Identification Criteria**:
1. **Strong VPA Signals**: SOS, Strong Weekly Bar, Effort to Rise (manually verified)
2. **Asset Class Context**: Outperforming peers within same asset class (manually compared)
3. **Volume Confirmation**: Volume supporting price action (manually verified from CSV)
4. **Trend Quality**: Clean, consistent weekly trend (manually assessed)

**Manual Analysis Process for Each Asset Class**:

#### For US Indices:
```bash
# Manual assessment framework for US indices
1. Read vpa_data_us_crypto_week/DJI.md - manually analyze VPA story
2. Read vpa_data_us_crypto_week/INX.md - manually analyze VPA story  
3. Manual comparison of recent signals and performance
4. Manual identification of leader based on:
   - Strongest VPA signals (manually verified)
   - Best relative performance (calculated via reliable Python)
   - Clearest weekly trend (manually assessed)
```

#### For Cryptocurrency Assets:
```bash
# Manual assessment framework for crypto assets
1. Read vpa_data_us_crypto_week/BTC.md - manually analyze VPA story
2. Read vpa_data_us_crypto_week/ETH.md - manually analyze VPA story
3. Manual comparison of recent signals and performance
4. Manual identification of leader based on:
   - Strongest VPA signals (manually verified)
   - Best relative performance (calculated via reliable Python)
   - Clearest weekly trend (manually assessed)
```

**Manual Leader Selection Rules**:
- **Maximum 2-3 leaders per asset class** - manually selected for quality
- **Must have recent strong signals** - manually verified from VPA files
- **Must outperform asset class peers** - manually compared performance
- **Must have volume confirmation** - manually verified from CSV data

**Success Criteria**: Clear individual leaders identified for each asset class through manual analysis

### Step 5: STAGE 3 - LEADER_us_crypto.md Creation Using Manual Natural Language Analysis
**Objective**: Create comprehensive LEADER_us_crypto.md using manual analysis results

**Manual Creation Process - NO AUTOMATED UTILITIES**:

**Document Structure Requirements**:
```markdown
# LEADER_us_crypto.md - Phân Tích Dẫn Dắt Tài Sản Toàn Cầu Tuần

*Cập nhật: [DATE] | Phân tích theo phương pháp VPA-AssetLead*

## 1. Tóm Tắt Tình Hình Tài Sản Toàn Cầu
[Manual synthesis of global asset class health from manual assessment]

## 2. Xếp Hạng Tài Sản Theo Sức Mạnh
[Manual ranking based on manual strength assessment]

### Dẫn Dắt Đồng Thuận
- **Asset Class**: [Manual description of leading asset classes]

### Hỗn Hợp Tín Hiệu  
- **Asset Class**: [Manual description of mixed asset classes]

### Yếu Kém
- **Asset Class**: [Manual description of weak asset classes]

## 3. Tài Sản Dẫn Dắt Cá Biệt
[Manual analysis of individual leaders from manual identification]

### Chỉ Số Mỹ
#### **[TICKER] - [Asset Description]**
- **Tín Hiệu VPA Gần Đây**: [Recent signals manually extracted]
- **Bối Cảnh Tuần**: [Weekly context manually analyzed]  
- **Hiệu Suất**: [Performance manually calculated]
- **Nhận Định**: [Manual assessment in Vietnamese]

### Tiền Điện Tử
#### **[TICKER] - [Asset Description]**
- **Tín Hiệu VPA Gần Đây**: [Recent signals manually extracted]
- **Bối Cảnh Tuần**: [Weekly context manually analyzed]
- **Hiệu Suất**: [Performance manually calculated] 
- **Nhận Định**: [Manual assessment in Vietnamese]

## 4. Chiến Lược Giao Dịch Tuần Tới
[Manual strategic recommendations based on leader analysis]

## 5. Theo Dõi Tài Sản Cần Chú Ý
[Manual identification of assets requiring attention]
```

**Manual Content Creation Guidelines**:
- **ALL content from manual analysis** of ticker profiles and assessments
- **Vietnamese financial terminology** with global market context
- **NO automated text generation** - human intelligence for all descriptions
- **Manual verification** of all claims against source data
- **Professional tone** suitable for trading decisions

**Critical Manual Requirements**:
- [ ] **Asset class strength percentages** manually calculated from ticker profiles
- [ ] **Individual leader selections** manually justified with VPA signals
- [ ] **Performance figures** manually calculated using reliable Python for CSV data
- [ ] **Vietnamese descriptions** manually written with proper financial terminology
- [ ] **Trading recommendations** manually developed from comprehensive analysis

**Data Verification Process**:
- **Manual cross-reference** all VPA claims with individual ticker VPA files using Read tool
- **Reliable Python verification** for all performance and price claims from CSV files
- **Manual consistency check** between asset class assessments and individual leader selections

**Success Criteria**: Complete LEADER_us_crypto.md file created entirely through manual analysis

### Step 6: **CRITICAL DATA VERIFICATION** (Prevent Trading Errors)
**Objective**: Ensure LEADER_us_crypto.md accuracy through systematic verification

**⚠️ MANDATORY DATA ACCURACY VERIFICATION**:

#### 6.1 **Performance Calculation Verification**
```bash
# For EVERY asset mentioned in LEADER_us_crypto.md, verify using most recent CSV file:
uv run -c "
import pandas as pd
import glob
ticker = 'DJI'
try:
    # Find the most recent weekly CSV file for this ticker
    csv_files = glob.glob(f'market_data_us_crypto_week/{ticker}_*.csv')
    if csv_files:
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        print(f'Using file: {latest_file}')
        print(f'Data range: {df.iloc[0][\"time\"]} to {df.iloc[-1][\"time\"]}')
        print('Last 5 weeks for verification:')
        print(df.tail(5)[['time', 'open', 'high', 'low', 'close', 'volume']])
        # Calculate performance from start to end
        start_price = df.iloc[0]['close']
        end_price = df.iloc[-1]['close']
        performance = ((end_price - start_price) / start_price) * 100
        print(f'Period performance: {performance:.2f}%')
    else:
        print(f'No weekly CSV files found for {ticker}')
except Exception as e:
    print(f'Error reading {ticker}: {e}')
"
```

#### 6.2 **VPA Signal Verification**
```bash
# Cross-reference VPA claims with actual VPA files:
Read: /Volumes/data/workspace/aipriceaction/vpa_data_us_crypto_week/{TICKER}.md
# Check latest entries match LEADER_us_crypto.md claims
```

**Critical Verification Checks**:
- [ ] **Performance Percentages**: All % claims calculated and verified against CSV
- [ ] **VPA Signal Claims**: All signals exist in corresponding VPA files
- [ ] **Date References**: All dates mentioned are accurate and exist
- [ ] **Asset Class Percentages**: Manual calculations verified for strength assessments
- [ ] **Volume Claims**: Volume patterns verified against CSV data
- [ ] **Price Movements**: Weekly price action claims verified against CSV

#### 6.3 **Manual Consistency Verification**
**Consistency Checks**:
- [ ] **Asset Class vs Individual Leaders**: Leaders align with asset class strength
- [ ] **Signal Timing**: Recent signals align with performance claims
- [ ] **Vietnamese Terminology**: Consistent use of proper financial terms
- [ ] **Global Market Context**: Appropriate context for international assets

### Step 7: Complete Manual Protocol Summary
**Objective**: Execute the complete weekly US & crypto leader analysis protocol

**Complete Manual Execution Sequence**:
1. **Step 1**: Use LS and Read tools to verify input files: `GROUP_us_crypto.md`, `REPORT_us_crypto_week.md`, directories
2. **Step 2**: Manual ticker profile creation using Task tools with manual analysis guidance
3. **Step 3**: Manual asset class strength assessment using ticker profiles
4. **Step 4**: Manual individual leader identification within asset classes  
5. **Step 5**: Create LEADER_us_crypto.md using Write tool with manual content
6. **Step 6**: Complete data verification using reliable Python for calculations

**Final Output**: New `LEADER_us_crypto.md` file with:
- **Manual asset class strength analysis** based on comprehensive ticker assessment
- **Manually identified individual leaders** with VPA signal justification
- **Complete manual analysis** of global market leadership
- **Professional Vietnamese financial writing** with global market context
- **Verified data accuracy** for all performance and signal claims

## Quality Control Standards

### Data Accuracy Requirements
- **ZERO TOLERANCE**: No performance claims without CSV verification
- **ZERO TOLERANCE**: No VPA signals without file verification  
- **Manual Analysis Only**: All assessments through human intelligence
- **Source Attribution**: Every claim traceable to manual analysis
- **Vietnamese Quality**: Professional terminology with global context

### Technical Requirements
- **Manual Creation**: Use Write tool for document creation
- **Data Verification**: Use reliable Python only for CSV calculations
- **File References**: Use Read tool for VPA file verification
- **Consistency**: Asset class assessments align with individual selections

## Error Handling

### Missing Input Files
- Document missing files and continue with available data
- Flag areas requiring manual review when complete data becomes available

### Data Inconsistencies
- Cross-reference multiple sources manually
- Document conflicts with manual reasoning
- **⚠️ When conflicts found**: Always verify against CSV files (authoritative)

### Signal Interpretation Disputes
- Apply conservative VPA methodology manually
- Provide detailed manual reasoning for all assessments
- **⚠️ Volume Pattern Disputes**: Always check actual CSV volume data

## Success Metrics

- **⚠️ ZERO DATA ERRORS**: No performance/volume/signal errors (verified against CSV)
- **Accuracy**: All manual analysis matches source data exactly
- **Completeness**: All asset classes and leaders assessed manually
- **Traceability**: All decisions verified from manual analysis
- **Actionability**: Clear trading guidance based on leadership analysis
- **Vietnamese Quality**: Professional financial terminology with global context
- **Manual Integrity**: All content created through human intelligence

## Key Principles for Manual Protocol

1. **NO AUTOMATED TEXT PARSING** - Human intelligence only
2. **Manual Asset Class Assessment** - Strength analysis through manual ticker evaluation
3. **Vietnamese Financial Terminology** - Professional global market context
4. **Manual Signal Verification** - Read VPA files directly with human understanding
5. **Reliable Python Only** - CSV calculations and data extraction only
6. **Complete Manual Verification** - Document all manual reasoning
7. **Global Market Focus** - Appropriate context for US indices and cryptocurrency assets
8. **⚠️ MANDATORY CSV VERIFICATION** - Every performance claim verified against CSV
9. **⚠️ VPA FILE VERIFICATION** - Every signal claim verified against VPA files
10. **⚠️ ZERO TOLERANCE FOR DATA ERRORS** - Trading accuracy depends on data precision