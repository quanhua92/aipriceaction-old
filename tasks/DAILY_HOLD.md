# Daily Portfolio Management Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `hold.md` file using the Portfolio-Strategist methodology with **manual natural language analysis only**. No unreliable Python text parsing utilities.

**⚠️ CRITICAL: ALWAYS USE ACTUAL DATA DATES**
- Never assume "today's date" for analysis
- Always get the actual last available date from CSV files using `df.iloc[-1]["Date"]`
- Use `glob.glob()` to find the most recent CSV file for each ticker
- Compare actual data dates with existing analysis dates to determine if new analysis is needed

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current

**Use LS tool to check for required input files:**
- Verify paths: `hold.md`, `REPORT.md`, `REPORT_week.md`, `LEADER.md`, `GROUP.md`, `PLAN.md`
- Verify directories: `vpa_data/`, `market_data/`

**Manual Verification Actions**:
- **Use Read tool** to verify existing `hold.md` contains portfolio data table ("Dữ Liệu Danh Mục")
- **Use Read tool** to verify `REPORT.md` exists with recent daily signals and prices
- **Use LS tool** to verify `vpa_data/` directory exists with individual ticker daily VPA files
- **Use LS tool** to verify `market_data/` directory exists with individual ticker CSV files
- **Use Read tool** to verify `REPORT_week.md` exists with weekly analysis
- **Use Read tool** to verify `LEADER.md` exists with industry context analysis
- **MANDATORY**: **Use Read tool** to verify `GROUP.md` exists with accurate ticker-to-industry mappings - manually cross-check all portfolio holdings
- **Use Read tool** to verify `PLAN.md` exists with overall market context (VNINDEX analysis)

**Success Criteria**: All core input files are present and accessible through manual verification

### Step 2: Manual Portfolio State Analysis
**Objective**: Extract current holdings and previous recommendations using manual natural language analysis

**Manual Analysis Actions**:
- **Use Read tool** to read existing `hold.md` "Dữ Liệu Danh Mục" table and manually identify:
  - All held tickers with average buy prices
  - Quantity of shares held for each ticker
  - Previous recommendation for each ticker from "Hành Động Đề Xuất" sections
- **Manual data extraction** using human intelligence to parse table data
- **NO automated text parsing** - read and understand using natural language

**Output**: Manual portfolio state mapping for next stage processing

### Step 3: STAGE 0 - Manual Data Analysis & Fact Sheet Creation
**Objective**: Create verified internal fact sheets for ALL portfolio tickers using manual analysis

**Manual Processing Approach**: Use Task tools to process portfolio tickers with **manual natural language analysis guidance** since portfolio is typically smaller (5-20 tickers).

**Critical Manual Process**: For EVERY ticker in the portfolio holdings table, manually create this internal data structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "holding_info": {
    "avg_buy_price": 32.50,
    "quantity": 1000
  },
  "previous_recommendation": "Hold/Buy More/Sell/etc.",
  "current_price": "Latest close from most recent market_data/{TICKER}_*.csv using reliable Python with glob.glob()",
  "most_recent_daily_signal": {
    "signal": "Effort to Rise/No Demand/SOS/etc. - manually identified",
    "date": "YYYY-MM-DD"
  },
  "daily_narrative_context": "1-sentence summary from vpa_data/{TICKER}.md last 3-5 days - manual analysis",
  "weekly_context": {
    "signal": "SOS Bar/Upthrust/etc. - manually identified",
    "week_ending_date": "YYYY-MM-DD",
    "weekly_narrative": "Brief summary of weekly trend and context - manual analysis"
  },
  "industry_group": "Industry name from GROUP.md - manually verified",
  "industry_status": "Dẫn dắt Đồng Thuận/Yếu/Phân Phối from LEADER.md - manually identified",
  "overall_market_context": "1-sentence VNINDEX summary from PLAN.md - manually extracted"
}
```

**Manual File Reading Strategy for Each Portfolio Ticker**:
1. **Use Read tool** to read `vpa_data/{TICKER}.md` for daily VPA narrative (last 10 entries) - manual analysis
2. **Use reliable Python script** to read the most recent `market_data/{TICKER}_*.csv` file for current price (last row):
```python
# CRITICAL: Use calculate_pnl_correct.py script for accurate P&L calculations
# This script:
# 1. Reads portfolio from hold.md table automatically 
# 2. Gets current prices from last row of the most recent CSV file for each ticker using glob.glob()
# 3. Calculates accurate P&L with proper formulas
python3 calculate_pnl_correct.py
```
3. **Manual cross-reference** with `REPORT.md` and `REPORT_week.md` for signals using Read tool
4. **CRITICAL**: **Manual industry mapping** using `GROUP.md` and cross-check accuracy - manually verify each ticker's industry classification
5. **Manual extraction** of industry status from `LEADER.md` using Read tool
6. **Manual extraction** of VNINDEX context from `PLAN.md` using Read tool

**Manual Data Extraction Rules**:
- **Manual extraction** of holding data from existing `hold.md` portfolio table using Read tool
- **Use calculate_pnl_correct.py script** for current prices from individual `market_data/{TICKER}_*.csv` files (script automatically finds most recent file using glob.glob())
- **Manual signal identification** from `REPORT.md` with exact dates using Read tool
- **Manual weekly signal extraction** from `REPORT_week.md` using Read tool  
- **Manual VPA narrative analysis** from individual `vpa_data/{TICKER}.md` files using Read tool
- **MANDATORY**: **Manual industry mapping** using exact matches from `GROUP.md` - ALWAYS manually cross-check ticker industry classification accuracy
- **Manual status extraction** from `LEADER.md` analysis using Read tool
- **Manual market context extraction** from `PLAN.md` VNINDEX analysis using Read tool

**Manual Processing Strategy**:
- Use Task tools to process multiple portfolio tickers with **manual analysis instructions**
- **NO automated text parsing** - all signal identification through human intelligence
- Each Task tool reads only relevant ticker files for each holding using Read tool
- **Manual verification** of all extracted data

**Quality Control**: These manually created fact sheets become the SOLE source of truth for all subsequent stages

**Example Manual Task Tool Usage for Portfolio**:
```
Task 1: "MANUAL ANALYSIS ONLY - Process portfolio tickers TCB,VND from hold.md holdings table. For each: 1) Use Read tool to manually read vpa_data/{TICKER}.md last 10 entries 2) Use reliable Python to read market_data/{TICKER}_*.csv current price 3) Manually extract signals from REPORT.md/REPORT_week.md using Read tool 4) Manually map industry from GROUP.md using Read tool 5) Manually get status from LEADER.md using Read tool 6) Return complete manually-created fact sheet JSON. NO automated text parsing."

Task 2: "MANUAL ANALYSIS ONLY - For each holding ticker, manually identify top 3 alternative investments. Use Read tool to prioritize weekly signals from REPORT_week.md, then manually use GROUP.md for same-industry options, manually confirm with daily signals from REPORT.md, and manually consider LEADER.md industry status. Return ranked alternatives with specific VPA reasoning. NO automated signal detection."

Task 3: "MANUAL ANALYSIS ONLY - Select top 3 diversified portfolio expansion picks from different industry sectors. PRIMARY: Use Read tool to manually read REPORT_week.md for weekly bullish signals. CRITICAL: Manually assess entry point value - avoid overextended tickers from leading sectors unless at pullback levels. Manually look for 'Test for Supply', 'No Supply', early breakouts through human intelligence. Balance sector leadership with attractive entry points. Consider sector rotation opportunities. Ensure 3 different industries. NO automated analysis."
```

**Manual Portfolio Processing Benefits**:
- **Manual focus** on only held tickers (typically 5-20 vs 100+ total tickers)
- **Individual file reading** provides precise context without noise from non-held tickers
- **Manual P&L calculations** with direct price access using reliable Python
- **Better manual risk assessment** with focused VPA context through human intelligence

### Step 4: STAGE 1 - Manual Ticker Action Assessment
**Objective**: Determine new recommended actions using manual analysis and state transition rules

**Manual Process**: Apply action recommendation rules in exact order using ONLY manually created fact sheet data and human intelligence:

### Step 4.5: Portfolio Sector Peer Analysis

**CRITICAL PROTOCOL**: Before making any sell recommendations for portfolio holdings, MUST conduct comprehensive sector peer analysis to prevent premature selling due to isolated weakness signals.

#### 4.5.1 Portfolio-Focused Sector Analysis
For each holding ticker showing bearish/weak signals:
1. **Identify Sector**: Use @GROUP.md for ticker's sector classification
2. **Gather Major Sector Peers**: List 3-5 major players in same sector
3. **VPA Signal Assessment**: Check recent VPA signals for each peer
4. **Sector Strength Classification**: Determine if weakness is isolated or sector-wide

#### 4.5.2 Sell Decision Matrix for Portfolio Holdings

| Individual Signal | Sector Context | Recommended Action | Risk Level |
|------------------|----------------|-------------------|------------|
| Bearish VPA | 70%+ Peers Weak | SELL | Low Risk - Sector rotation confirmed |
| Bearish VPA | 30-60% Peers Mixed | HOLD/MONITOR | Medium Risk - Sector mixed |
| Bearish VPA | <30% Peers Weak | HOLD/BUY DIP | High Risk - Likely temporary weakness |
| Strong Bearish VPA | Isolated Weakness | REDUCE POSITION | Medium Risk - Partial exit |

#### 4.5.3 Special Portfolio Considerations
- **Securities Holdings (SHS, VND, SSI, VIX, CTS, MBS)**: Always cross-reference all sector peers
- **Banking Holdings**: Check systemic vs individual bank issues  
- **Real Estate Holdings**: Verify sector-wide vs company-specific weakness
- **Never sell based on isolated signals** when sector remains strong

#### 4.5.4 Documentation for Portfolio Decisions
```markdown
**[TICKER] Portfolio Decision Analysis**
- Current Holding: [Avg Price, Quantity, P&L]
- Individual Signal: [Recent VPA signal and date]
- Sector Peers Analysis: [List peers and their recent signals]
- Sector Context: [Strong/Weak/Mixed - % breakdown]
- Risk Assessment: [Isolated weakness vs sector rotation]
- Final Decision: [Hold/Sell/Reduce with specific reasoning]
```

#### For Previous "Hold" Recommendations:
- **Check Strong Bullish Continuation**:
  - Daily signal is bullish (SOS, Effort to Rise, Backing Up) AND weekly context supportive AND daily narrative confirms strength
- **Check Minor Weakness/Consolidation**:
  - Daily signal neutral/minor bearish (No Demand low volume) AND daily narrative shows sideways movement AND weekly context remains bullish
- **Check Significant Weakness/Breakdown**:
  - Daily signal major bearish (Sign of Weakness, Effort to Fall high volume) OR weekly bearish confirmed by daily
- **Decisions**: Buy More → Hold/Prepare to Buy → Sell/Panic Sell

#### For Previous "Buy More" Recommendations:
- **Check Confirmation/Continuation**: Further bullish signals, price moving up
- **Check Failure to Confirm**: Weak/neutral signals, stagnant/down price
- **Decisions**: Hold/Buy Fast → Hold/Prepare to Buy

#### For Previous "Sell" Recommendations:
- **Check Further Decline**: Continued bearish signals and decline
- **Check Rebound/False Breakdown**: Strong bullish reversal signals (SOS)
- **Decisions**: Panic Sell/Avoid → Re-evaluate

#### For Previous "Prepare to Buy" Recommendations:
- **Check Entry Signal Confirmed**: Classic entry signals (Test for Supply, No Supply pullback, small SOS)
- **Check Entry Failed**: Bearish signals instead of expected entry
- **Decisions**: Buy → Hold/Avoid

#### Action Types Summary:
- **Buy More**: Strong bullish continuation on existing holdings
- **Sell**: Significant weakness or breakdown
- **Hold**: Default when no strong buy/sell signals
- **Panic Sell**: Accelerated bearish trends
- **Prepare to Buy**: VPA entry setup forming
- **Buy**: Execute purchase when setup confirmed
- **Buy Fast**: Accelerating bullish moves
- **Re-evaluate**: Previous bearish thesis invalidated
- **Avoid**: Stay away due to bearish signals

### Step 5: Accurate P&L Calculation Using calculate_pnl_correct.py
**Objective**: Calculate current profit/loss for each holding using the verified calculation script

**CRITICAL CALCULATION PROCESS**:
1. **ALWAYS use calculate_pnl_correct.py script** - this script automatically:
   - Reads portfolio from hold.md table 
   - Gets current prices from last row of the most recent CSV file for each ticker using glob.glob() pattern matching
   - Calculates accurate P&L with verified formulas
   - **Formats all numbers using Vietnamese dot separators** (28.085.600)
   - Provides formatted output for hold.md updates

**Never use hardcoded prices or manual calculations** - always run:
```bash
python3 calculate_pnl_correct.py
```

**Script Output Provides**:
- Current prices from actual market data CSV files
- Accurate P&L calculations for each position using Vietnamese dot formatting (e.g., 28.085.600)
- Total portfolio P&L summary with consistent Vietnamese number formatting
- Formatted P&L lines ready for hold.md insertion with proper dot separators

**Formula Verification**: 
- P&L % = ((Current Price - Average Buy Price) / Average Buy Price) × 100
- P&L Amount = (Current Price - Average Buy Price) × Quantity
- All calculations verified by the script

**CRITICAL VIETNAMESE NUMBER FORMATTING**: Display as both percentage and monetary value using Vietnamese dot separators (e.g., "+4.92% (+2.885.000)")

**Data Sources**: 
- Portfolio holdings: From hold.md "Dữ Liệu Danh Mục" table
- Current prices: From most recent market_data/{TICKER}_*.csv last row (automatically detected using glob.glob())
- All processed automatically by calculate_pnl_correct.py

### Step 5.1: Manual Sector Allocation Calculation
**Objective**: Calculate portfolio allocation by sector for the "Phân Bổ Danh Mục Theo Ngành" table

**Manual Calculation Process**:
1. **Sector Classification**: **Use Read tool** to manually read `GROUP.md` and classify each portfolio ticker by industry sector
2. **Market Value Calculation**: For each ticker, calculate market value = Current Price × Quantity
3. **Sector Aggregation**: Sum market values for all tickers within each sector
4. **Percentage Calculation**: (Sector Total Value / Portfolio Total Value) × 100
5. **Ticker Listing**: Group tickers by sector for display

**Manual Calculation Formula**:
- Sector Value = Σ(Current Price × Quantity) for all tickers in sector
- Sector Percentage = (Sector Value / Total Portfolio Value) × 100
- Round percentages to 1 decimal place (e.g., 45.6%)

**Manual Table Format**:
```markdown
| Ngành | Các Mã Cổ Phiếu | Tỷ Trọng Danh Mục |
| :---- | :-------------- | :---------------- |
| Chứng Khoán | CTS, SSI, VIX, VND | 45.6% |
| Ngân Hàng | HDB, SHB, VPB | 25.5% |
| Bất Động Sản | HDC, TCH, VHM | 23.4% |
| Bán Lẻ | MWG | 5.5% |
```

**Manual Data Sources**:
- **Current prices**: From calculate_pnl_correct.py script output (reads actual CSV files)
- **Holdings quantities**: From existing hold.md "Dữ Liệu Danh Mục" table
- **Sector classifications**: **Use Read tool** to manually verify against `GROUP.md`

**CRITICAL MANUAL VERIFICATION**: 
- **Always manually cross-check** sector classifications against `GROUP.md`
- **Manually verify** percentage calculations sum to 100%
- **Display percentages only** - no VND amounts in the table

### Step 5.5: Manual Alternative Ticker Selection
**Objective**: For each holding ticker, manually identify 3 best alternative investment options

**Manual Selection Criteria** (in priority order):
1. **Manual Weekly VPA Analysis Priority**: **Use Read tool** to manually prioritize tickers with strong weekly signals from `REPORT_week.md`
2. **Manual Same Industry Group**: **Use Read tool** to manually consider tickers from same industry group (from `GROUP.md`)
3. **Manual Daily VPA Confirmation**: **Use Read tool** to manually confirm weekly analysis with daily signals from `REPORT.md`
4. **Manual Industry Leadership**: **Use Read tool** to manually prefer tickers from "Dẫn dắt" or "Đồng Thuận" industries (from `LEADER.md`)

**Manual Data Sources for Alternative Analysis**:
- **Use Read tool** to manually read `REPORT_week.md` for weekly VPA signals of all available tickers
- **Use Read tool** to manually read `REPORT.md` for daily VPA confirmation signals
- **Use Read tool** to manually use `GROUP.md` to identify same-industry alternatives
- **Use Read tool** to manually use `LEADER.md` to prioritize strong industry groups
- **Use Read tool** to manually cross-reference with `vpa_data/{TICKER}.md` files for detailed analysis

**Manual Selection Process**:
1. **Manual Industry Matching**: **Use Read tool** to manually find all tickers in same industry group as holding ticker - **MANDATORY**: Manually use `GROUP.md` to verify exact industry classification
2. **Manual Weekly Signal Filtering**: **Manual analysis** to prioritize those with strong weekly bullish signals (SOS Bar, Effort to Rise, etc.)
3. **Manual Daily Confirmation**: **Manual verification** to confirm weekly signals with supportive daily VPA analysis
4. **Manual Cross-Industry Options**: If insufficient same-industry options, manually expand to strong tickers from leading industry groups
5. **Manual Ranking Logic**: **Human intelligence** to rank by weekly signal strength first, then daily confirmation, then industry leadership status
6. **⚠️ CRITICAL INDUSTRY VERIFICATION**: **MANDATORY manual cross-check** - alternatives MUST be from the SAME industry group in `GROUP.md`
   - **Zero tolerance**: Never mix industries in same-ticker alternatives  
   - **Manual verification required**: Read GROUP.md for every alternative ticker
   - **Error prevention**: Cross-industry mixing is a critical bug that leads to poor portfolio advice

**Manual Output Format**: For each alternative, provide specific reasoning citing:
- Weekly VPA signal and date (PRIORITY) - manually identified
- Daily VPA confirmation (if available) - manually verified
- Industry group and leadership status - manually checked
- Comparative advantage over current holding - manually assessed

### Step 5.6: Manual Diversified Portfolio Expansion Selection
**Objective**: Manually select top 3 tickers from different industry sectors for portfolio diversification

**Manual Priority Data Sources** (in order):
1. **Manual Weekly VPA Analysis (PRIMARY)**: **Use Read tool** to manually read `REPORT_week.md` - prioritize strong weekly signals
2. **Manual Daily VPA Confirmation (SECONDARY)**: **Use Read tool** to manually read `REPORT.md` - confirm weekly signals only
3. **Manual Market Context**: **Use Read tool** to manually read `PLAN.md` top recommendations and market analysis
4. **Manual Industry Leadership**: **Use Read tool** to manually read `LEADER.md` for sector rotation strategy

**Manual Selection Criteria** (in priority order):
1. **Manual Cross-Sector Diversification**: Must manually select from 3 different industry groups
2. **Manual Weekly Signal Strength**: **Human intelligence** to prioritize "Sign of Strength" and "Effort to Rise" from weekly analysis
3. **Manual Entry Point Valuation**: **Manual assessment** to avoid overextended tickers - prefer pullbacks, consolidations, or early breakouts
4. **Manual PLAN.md Integration**: **Manual analysis** to consider tickers from "Top 1x Cơ Hội Giao Dịch" section but evaluate entry points
5. **Manual Industry Balance**: **Human judgment** to mix leading sectors with emerging/recovering sectors for better value
6. **Manual Risk-Reward Ratio**: **Manual evaluation** to prioritize favorable entry points over pure sector leadership

**Manual Selection Process**:
1. **Manual Industry Mapping**: **Use Read tool** to manually read `PLAN.md` to identify sectors and picks, noting current price levels
2. **Manual Weekly Signal Analysis**: **Use Read tool** to manually analyze `REPORT_week.md`, filter tickers with strongest weekly bullish signals through human intelligence
3. **Manual Entry Point Assessment**: **Manual identification** of tickers with:
   - Recent pullbacks to support levels ("Test for Supply" or "No Supply") - manually identified
   - Early-stage breakouts with room for growth - manually assessed
   - Consolidation patterns near key support levels - manually analyzed
   - Avoid extended moves without healthy corrections - manual judgment
4. **Manual Value vs. Leadership Balance**: **Human decision-making** to:
   - Don't exclusively pick from "Dẫn dắt" sectors if overextended - manual assessment
   - Consider "Đồng Thuận" or recovering sectors with better entry points - manual evaluation
   - Look for rotation opportunities from expensive to undervalued sectors - manual analysis
5. **Manual Sector Diversification**: **Manual verification** to ensure 3 picks from different major industry groups
6. **Manual Daily Confirmation**: **Use Read tool** to manually confirm weekly signals and assess short-term entry timing
7. **Manual Risk-Reward Evaluation**: **Manual calculation** of potential upside vs. current extension from key levels

**Manual Output Requirements**:
- 3 tickers from 3 different industry sectors - manually verified
- Each selection must cite weekly VPA signal and date as primary justification - manually identified
- **Manual Entry Point Analysis**: Specific reasoning why current levels offer good value - manual assessment
- **Manual Risk-Reward Assessment**: Compare current price to key support/resistance levels - manual analysis
- Include reasoning for diversification benefit beyond just sector leadership - manual evaluation
- Avoid overextended picks from leading sectors unless at attractive re-entry points - manual judgment
- Consider sector rotation opportunities and value plays in emerging sectors - manual strategy

### Step 6: Manual hold.md Generation (SECTION-BY-SECTION)
**Objective**: Generate complete hold.md using manually verified fact sheets and manually determined final actions

**🔄 SECTION-BY-SECTION GENERATION PROCESS** (To avoid long output messages):

**CRITICAL IMPLEMENTATION APPROACH**:
- **Generate hold.md in multiple separate sections** to prevent output truncation
- **Each section must be complete and properly formatted**
- **Agent must explicitly state which section is being generated**
- **Use Write tool for initial file creation, Edit tool for subsequent sections**

**📋 SECTION GENERATION ORDER** (Generate one section at a time):

1. **SECTION 1 - File Header & Portfolio Summary**: Generate header, portfolio data table, and summary analysis
2. **SECTION 2 - Individual Holdings Analysis Part 1**: Generate first 3-4 detailed ticker analyses for current holdings
3. **SECTION 3 - Individual Holdings Analysis Part 2**: Generate next 3-4 detailed ticker analyses for current holdings
4. **SECTION 4 - Individual Holdings Analysis Part 3**: Generate remaining detailed ticker analyses for current holdings
5. **SECTION 5 - Diversification Expansion Analysis**: Generate detailed analysis for 3 diversified picks
6. **SECTION 6 - Change Log & 5-Day Forecast**: Generate change log and market forecast sections

#### 6.1 File Header
```markdown
# Kế Hoạch Quản Lý Danh Mục

**Cập Nhật Lần Cuối:** [Current Date]

## Dữ Liệu Danh Mục

| Mã Cổ Phiếu | Giá Mua Trung Bình | Số Lượng Nắm Giữ |
| :---------- | :----------------- | :--------------- |
[Portfolio holdings table using fact sheet data]
```

#### 6.2 Portfolio Analysis Section
```markdown
## Phân tích

**1. Tóm Tắt Danh Mục Hiện Tại**

[Concise overview based on collective actions and market context]

* **Phân Bổ Danh Mục Theo Ngành:**
  | Ngành | Các Mã Cổ Phiếu | Tỷ Trọng Danh Mục |
  | :---- | :-------------- | :---------------- |
  [Sector allocation table showing sector name, ticker list, and percentage allocation calculated from price × quantity for each sector]

* **Tóm Tắt Hành Động Đề Xuất:**
  | Mã Cổ Phiếu | Trạng Thái Hiện Tại | Hành Động Đề Xuất Ngắn Gọn |
  | :---------- | :------------------ | :------------------------- |
  [Summary table of new recommendations]

**2. Kế Hoạch Giao Dịch Chi Tiết**

**3. Kế Hoạch Gia Tăng Chi Tiết**

*Top 3 cổ phiếu đa dạng ngành để mở rộng danh mục - giảm rủi ro, tăng lợi nhuận*

| Mã Cổ Phiếu | Ngành | Tín Hiệu VPA Chính | Lý Do Lựa Chọn |
| :---------- | :---- | :----------------- | :-------------- |
[Top 3 diversified recommendations with cross-sector analysis]
```

#### 6.2-6.4: Individual Ticker Analysis (SPLIT BY SECTIONS)
**🔄 SPLIT GENERATION APPROACH**: For EVERY ticker, provide detailed breakdown across multiple sections

**SECTION 2-4 Distribution Strategy**:
- **SECTION 2**: First 3-4 current holdings (alphabetical order)  
- **SECTION 3**: Next 3-4 current holdings (continue alphabetical)
- **SECTION 4**: Remaining current holdings (complete alphabetical)

**MANDATORY FORMAT** for EACH ticker analysis:
```markdown
### **[TICKER] ([INDUSTRY])**
![Weekly Chart](./reports_week/[TICKER]/[TICKER]_candlestick_chart.png)
![Daily Chart](./reports/[TICKER]/[TICKER]_candlestick_chart.png)

* **Giá Mua Trung Bình:** [From fact sheet]
* **Số Lượng Nắm Giữ:** [From fact sheet]
* **Giá Hiện Tại:** [From fact sheet]
* **P&L (Lợi Nhuận/Thua Lỗ Chưa Thực Hiện):** [Calculated P&L using Vietnamese dot format - e.g., +9.27% (+2.885.000)]
* **VPA Phân Tích Hiện Tại:** 
  * **Bối Cảnh Tuần:** [Weekly context from fact sheet - weekly signals, week ending date, and weekly narrative]
  * **Bối Cảnh Ngày:** [Daily context from fact sheet - daily signals, recent narrative, and short-term trend analysis]
* **Hành Động Đề Xuất:** [Final decision from Stage 1]
  * **Giá Đề Xuất:** [Specific price range if buy/sell action]
  * **Số Lượng Đề Xuất:** [Specific quantity in multiples of 100 shares (e.g., 100, 200, 300) or ratio if buy/sell action]
  * **Lý Do Hành Động:** [VPA logic explaining the decision]
* **Điểm Dừng Lỗ:** [Specific stop-loss level]
* **Điểm Chốt Lời:** [Specific take-profit level(s)]
* **Top 3 Cổ Phiếu Thay Thế:** [3 best alternative tickers with reasoning]
  * **[TICKER1]**: [Reason based on weekly/daily VPA analysis]
  * **[TICKER2]**: [Reason based on weekly/daily VPA analysis]  
  * **[TICKER3]**: [Reason based on weekly/daily VPA analysis]
```

#### 6.5: Diversification Expansion Analysis (SECTION 5)
**🔄 SECTION 5 GENERATION**: Generate complete detailed analysis for 3 diversified picks with SAME format as current holdings

**MANDATORY FORMAT** for EACH diversified pick (identical to current holdings format):
```markdown
### **[TICKER] ([INDUSTRY])**
![Weekly Chart](./reports_week/[TICKER]/[TICKER]_candlestick_chart.png)
![Daily Chart](./reports/[TICKER]/[TICKER]_candlestick_chart.png)

* **Giá Mua Đề Xuất:** [Recommended entry price range]
* **Số Lượng Đề Xuất:** [Specific quantity in multiples of 100 shares]
* **VPA Phân Tích Hiện Tại:** 
  * **Bối Cảnh Tuần:** [Weekly VPA analysis from REPORT_week.md]
  * **Bối Cảnh Ngày:** [Daily VPA analysis from REPORT.md]
* **Phân Tích Thiết Lập:** [Entry point analysis and setup reasoning]
* **Vùng Vào Tốt Nhất:** [Best entry zones with technical justification]
* **Điểm Dừng Lỗ:** [Specific stop-loss level]
* **Điểm Chốt Lời:** [Specific take-profit level(s)]
```

#### 6.6: Change Log & Forecast (SECTION 6)
**🔄 SECTION 6 GENERATION**: Generate change log and 5-day market forecast

```markdown
**4. Nhật Ký Thay Đổi Kế Hoạch**

* **Chuyển Từ Hold sang Buy/Buy More/Buy Fast/Prepare to Buy:**
  * [Document upgrades with specific protocol conditions and signals]

* **Chuyển Từ Hold sang Sell/Panic Sell:**
  * [Document downgrades with specific protocol conditions and signals]

* **Thay Đổi Trạng Thái Khác:**
  * [Document other significant changes with justifications]

* **Loại Bỏ/Thêm Mới Ticker:**
  * [Document additions or removals from portfolio]

## 5. Dự Đoán 5 Ngày Kế Tiếp
[Complete 5-day forecast with scenarios]
```

### Step 7: Manual Quality Verification
**Objective**: Ensure hold.md accuracy and completeness through manual verification

**CRITICAL MANUAL BUG PREVENTION**: Manually verify correct section structure to avoid heading misalignment:
- [ ] **Section 1**: Tóm Tắt Danh Mục Hiện Tại (summary and action table) - manually verified
- [ ] **Section 2**: Kế Hoạch Giao Dịch Chi Tiết (detailed analysis of CURRENT holdings with charts, P&L, VPA analysis, recommendations, stop-loss, take-profit, alternatives) - manually verified
- [ ] **Section 3**: Kế Hoạch Gia Tăng Chi Tiết (detailed analysis of NEW diversification picks with same format as Section 2: charts, buy prices, quantities, VPA analysis, stop-loss, take-profit) - manually verified
- [ ] **Section 4**: Nhật Ký Thay Đổi Kế Hoạch (change log) - manually verified

**MANUAL STRUCTURAL VERIFICATION**:
- [ ] Section 2 contains individual ### ticker analyses for ALL current holdings - manually counted and verified
- [ ] Section 3 contains individual ### ticker analyses for ALL diversification picks with full detail (not just summary table) - manually verified
- [ ] Section 3 uses identical format to Section 2: charts, prices, quantities, VPA analysis (including separate Bối Cảnh Tuần and Bối Cảnh Ngày), stop-loss, take-profit - manually checked
- [ ] No content appears between section headers without proper subsection organization - manually inspected

**Manual Verification Checklist**:
- [ ] All portfolio holdings from previous hold.md are processed - manually cross-checked
- [ ] P&L calculations are mathematically correct - manually verified
- [ ] All assertions cite specific signals and dates from manually created fact sheets
- [ ] Action recommendations follow state transition rules correctly - manually verified
- [ ] Change log documents every recommendation change with manual justification
- [ ] Chart links use correct file paths - manually checked
- [ ] Vietnamese text is grammatically correct - manually reviewed
- [ ] Industry classifications match GROUP.md exactly - manually cross-verified
- [ ] **CRITICAL**: All "Top 3 Cổ Phiếu Thay Thế" alternatives are from the SAME industry group as the holding ticker per GROUP.md - manually verified

### Step 8: 5-Day Market Forecast Generation
**Objective**: Create detailed 5-day forward-looking analysis with scenario-based action plans

**Manual Forecast Process**:
- **Use Read tool** to analyze current market conditions from PLAN.md VNINDEX analysis
- **Manual assessment** of post-climax market behavior patterns using VPA methodology  
- **Scenario-based planning** for Up/Sideway/Down outcomes with specific probabilities
- **Dynamic action plans** for each scenario based on portfolio holdings and market context

**5-Day Forecast Structure**:
```markdown
## 5. Dự Đoán 5 Ngày Kế Tiếp

### **Ngày [X] ([DATE])**

**Tình Huống UP ([PROBABILITY]%)**
- **Mô tả**: [Market scenario description]
- **Điều kiện**: [Technical conditions required]
- **Hành động**: [Specific portfolio actions]

**Tình Huống SIDEWAY ([PROBABILITY]%)**
- **Mô tả**: [Market scenario description]  
- **Điều kiện**: [Technical conditions required]
- **Hành động**: [Specific portfolio actions]

**Tình Huống DOWN ([PROBABILITY]%)**
- **Mô tả**: [Market scenario description]
- **Điều kiện**: [Technical conditions required]
- **Hành động**: [Specific portfolio actions]
```

**Manual Forecast Guidelines**:
- **Day 1**: Focus on immediate post-climax reaction (conservative probabilities)
- **Day 2-3**: Consider trend development and institutional response
- **Day 4-5**: Account for weekly close and monthly patterns
- **Probabilities**: Must sum to 100%, reflect VPA-based market structure analysis
- **Actions**: Specific to current portfolio holdings with exact price levels and quantities

**Key Forecast Elements**:
- **VNINDEX levels**: Specific support/resistance levels for each scenario
- **Portfolio actions**: Exact share quantities and price triggers for holdings
- **Cash management**: Dynamic cash allocation based on market conditions
- **Risk management**: Clear stop-loss and emergency procedures
- **Strategic summary**: 5-day overview with core principles and key levels

### Step 9: Manual File Output
**Objective**: Generate final hold.md file using manual compilation

**Manual Output Process**:
- **Use Write tool** to create complete hold.md content based on manual analysis
- **Manual compilation** of all sections using manually verified data
- **Manual formatting** to ensure proper Vietnamese structure
- **Manual verification** of all content before writing

## Manual Quality Control Standards

### Manual Data Accuracy Requirements
- **Zero Tolerance**: No assertions without manual fact sheet verification
- **Price Accuracy**: Current prices must match market_data CSV files exactly - verified using calculate_pnl_correct.py
- **Date Precision**: All signals must include exact dates - manually verified
- **P&L Accuracy**: Mathematical calculations must be manually verified as precise using Vietnamese dot formatting for ALL individual ticker P&L amounts
- **Number Formatting**: ALL monetary amounts must use Vietnamese dot separators (28.085.600 VND)
- **State Tracking**: Previous recommendations must be accurately captured through manual analysis

### 🚨 MANDATORY DATA INTEGRITY RULES

#### **RULE 1: NO DATE MIXING (CRITICAL)**
- **NEVER mix VPA analysis from different dates** in the same recommendation
- **ALWAYS verify VPA signal dates match the analysis context date**
- **Example of FORBIDDEN practice**: Using 2025-08-05 "Sign of Strength" analysis for 2025-08-07 recommendations
- **Verification Required**: Cross-check all VPA claims against actual dates in vpa_data/{TICKER}.md files
- **Red Flag Detection**: Look for explosive volume claims (e.g., "3.4x bùng nổ") that may be from previous days

#### **RULE 2: CURRENT STATE ONLY**
- **Use ONLY the most recent VPA analysis date** for current recommendations
- **Distinguish between historical significant events and current state**
- **Example**: "Previous breakout on Aug 5 with 3.4x volume, currently in continuation phase" (CORRECT) vs. "Sign of Strength breakout with 3.4x volume" when describing current state (INCORRECT)

#### **RULE 3: RISK-REWARD RATIO MINIMUM**
- **ALL recommendations must have Risk:Reward ratio ≥ 2:1**
- **Take-profit targets must be at least 2x the stop-loss distance**
- **Formula verification**: (Target Price - Current Price) ÷ (Current Price - Stop Loss) ≥ 2.0
- **Immediate rejection**: Any recommendation with R:R < 2:1 must be revised or rejected

#### **RULE 4: ENTRY PRICE REALITY CHECK**
- **NEVER recommend entry prices more than 10% below current market price**
- **Flag any diversification pick where recommended entry vs current price shows >15% gap**
- **Example of FORBIDDEN**: Recommending FRT entry at 67-70 when current price is 152 (+117%)
- **Mandatory verification**: Compare ALL recommended entry prices against current market data

#### **RULE 5: VPA SIGNAL ACCURACY**
- **MANDATORY cross-verification**: All claimed VPA signals must match exactly with vpa_data files**
- **Zero tolerance for signal misstatement**: "No Supply" vs "No Demand" are different signals
- **Daily verification**: Check latest 3 entries in vpa_data/{TICKER}.md for current signal accuracy
- **Flag mismatches immediately**: Any discrepancy requires investigation and correction

#### **RULE 6: POSITION SIZING COMPLIANCE**
- **ALL position recommendations must be multiples of 100 shares minimum**
- **Forbidden quantities**: 50, 150, 75, any number not divisible by 100 and <100
- **Correct examples**: 100, 200, 300, 400, 500 shares
- **Automatic rejection**: Any position size recommendation violating this rule

#### **RULE 7: INDUSTRY CLASSIFICATION VERIFICATION**
- **MANDATORY**: All "Top 3 Cổ Phiếu Thay Thế" must be from SAME industry group per GROUP.md
- **Zero tolerance for cross-industry mixing** in alternatives
- **Verification process**: Read GROUP.md and manually confirm every alternative ticker's industry
- **Example of FORBIDDEN**: Banking alternatives (ACB, VCB) for Securities holding (SHS)
- **Error detection**: Any alternative from different industry triggers immediate correction

#### **RULE 8: OVEREXTENSION DETECTION**
- **Automatic flagging**: Any ticker >30% above its recommended entry price range**
- **Immediate review required**: Tickers showing recent "No Demand" or "Sign of Weakness" signals
- **Risk assessment mandatory**: Evaluate if overextended tickers should be removed from recommendations
- **Conservative approach**: When in doubt, exclude overextended candidates

### 🔍 MANDATORY PRE-SUBMISSION VERIFICATION CHECKLIST

**Before finalizing hold.md, EVERY AI agent must verify:**

- [ ] **Date Integrity**: No VPA analysis mixed from different dates
- [ ] **Signal Accuracy**: All VPA signals match vpa_data files exactly  
- [ ] **Price Reality**: All entry recommendations within 10% of current prices
- [ ] **R:R Ratios**: All recommendations have ≥2:1 risk-reward ratios
- [ ] **Position Sizes**: All quantities are multiples of 100 shares (minimum 100)
- [ ] **Industry Match**: All alternatives from same industry group per GROUP.md
- [ ] **Volume Claims**: All volume statistics verified against actual CSV data
- [ ] **Current State**: Analysis reflects most recent data date, not historical events
- [ ] **Overextension Check**: No recommendations for tickers >30% above suggested entry
- [ ] **Signal Consistency**: Daily and weekly VPA signals align logically

### 🚨 AUTOMATIC REJECTION TRIGGERS

**Any hold.md with the following issues must be REJECTED and regenerated:**

1. **Date mixing detected** (different VPA dates in same analysis)
2. **Risk-reward ratios <2:1** for any ticker
3. **Entry prices >15% gap** from current market prices  
4. **Cross-industry alternatives** detected
5. **Position sizes not multiples of 100** or below 100 shares
6. **VPA signal mismatches** with source data
7. **Volume claims unverified** against CSV files
8. **Overextended tickers** without proper risk warnings

### 📊 VALIDATION PROTOCOLS

#### **Daily Validation Process**:
1. **Run calculate_pnl_correct.py** to verify all prices
2. **Spot-check 3 random tickers** for VPA signal accuracy  
3. **Verify all R:R ratios** meet minimum standards
4. **Check top 3 most recent VPA entries** for date consistency
5. **Cross-reference alternatives** with GROUP.md classifications

#### **Weekly Deep Audit**:
1. **Full portfolio VPA verification** against source files
2. **Complete R:R ratio audit** for all recommendations  
3. **Entry price reality check** for all diversification picks
4. **Alternative industry classification** comprehensive review
5. **Position sizing compliance** across entire portfolio

### Action Logic Standards
- **Protocol Adherence**: All decisions must follow state transition rules
- **Signal Confirmation**: Bullish/bearish assessments must be evidence-based
- **Risk Management**: Stop-loss and take-profit levels must be technically justified
- **Position Sizing**: Quantity recommendations must be proportional and reasonable

### Vietnamese Language Standards
- **PRIORITY VIETNAMESE**: Use Vietnamese language for all analysis and explanations - VPA signal names in English are acceptable
- **NO MIXED LANGUAGE**: Never mix English and Vietnamese in same sentence (e.g. avoid "Banking sector leads recovery, momentum breakout", "Excellent entry point sau healthy pullback")
- Use proper Vietnamese financial terminology for all descriptions
- Maintain professional tone and grammar in Vietnamese
- **CRITICAL NUMBER FORMATTING**: Use Vietnamese dot separators for thousands (e.g., 28.085.600 VND, not 28,085,600 VND). Decimal points still use dots (e.g., 42.5 price)
- Use consistent industry naming from GROUP.md
- **EXAMPLES OF CORRECT USAGE**:
  - Good: "Điểm vào tốt sau điều chỉnh lành mạnh, tỷ lệ rủi ro-lợi nhuận 3:1 thuận lợi"
  - Bad: "Excellent entry point sau healthy pullback, favorable 3:1 risk-reward ratio"
  - Good: "Ngành ngân hàng dẫn dắt chu kỳ phục hồi kinh tế"
  - Bad: "Banking sector leads recovery, momentum breakout"
  - Good (Numbers): "Tổng P&L: +28.085.600 VND (+8.35%)"
  - Bad (Numbers): "Tổng P&L: +28,085,600 VND (+8.35%)"
  - Good (Individual P&L): "+9.27% (+2.885.000)"
  - Bad (Individual P&L): "+9.27% (+2,885)"

### Technical Requirements
- **Chart Links**: Verify all image paths exist (reports/ and reports_week/)
- **Report Links**: Ensure links to REPORT.md work with correct anchors
- **Markdown Formatting**: Proper headers, tables, and structure
- **Data Consistency**: Holdings table must match individual analyses

## Error Handling

### Missing Portfolio Data
- Document missing tickers in summary
- Use available data and note limitations
- Flag areas requiring manual review

### Price Data Issues
- Cross-reference multiple sources for current prices
- Use most recent available data with timestamp
- Document any data quality concerns

### Signal Interpretation Conflicts
- Apply conservative VPA methodology
- Prioritize risk management over aggressive positioning
- Provide detailed reasoning for controversial decisions

## Success Metrics

- **Accuracy**: All fact sheets match source data exactly
- **Completeness**: Every portfolio ticker assessed and recommended
- **Traceability**: All decisions can be verified from audit log
- **Actionability**: Recommendations provide clear trading instructions
- **Risk Management**: Appropriate stop-loss and position sizing

## Templates

### Fact Sheet Template
```json
{
  "ticker": "",
  "holding_info": {"avg_buy_price": 0, "quantity": 0},
  "previous_recommendation": "",
  "current_price": 0,
  "most_recent_daily_signal": {"signal": "", "date": ""},
  "daily_narrative_context": "",
  "weekly_context": {"signal": "", "week_ending_date": ""},
  "industry_group": "",
  "industry_status": "",
  "overall_market_context": ""
}
```

### Action Justification Templates
- **Buy More**: "Tín hiệu [SIGNAL] ngày [DATE] xác nhận xu hướng tăng mạnh, đáp ứng điều kiện #1A"
- **Sell**: "Tín hiệu [SIGNAL] ngày [DATE] phá vỡ cấu trúc tăng giá với khối lượng lớn, đáp ứng điều kiện #1C"
- **Hold**: "Tín hiệu [SIGNAL] ngày [DATE] cho thấy giai đoạn tích lũy, cần quan sát thêm"

## Risk Management Notes

- **Position Sizing**: Consider portfolio balance when recommending quantity changes. **CRITICAL**: All buying suggestions must specify quantities as multiples of 100 shares (100, 200, 300, etc.) - never suggest quantities below 100 shares
- **Stop-Loss Placement**: Use technical levels, not arbitrary percentages
- **Take-Profit Strategy**: Consider partial profit-taking at multiple levels
- **Market Context**: Factor in overall VNINDEX trend for individual decisions