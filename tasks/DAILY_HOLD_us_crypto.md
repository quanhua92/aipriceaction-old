# Daily US & Crypto Portfolio Management Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `hold_us_crypto.md` file using the Portfolio-Strategist methodology adapted for US indices and cryptocurrency assets with **manual natural language analysis only**. No unreliable Python text parsing utilities.

**⚠️ CRITICAL: ALWAYS USE ACTUAL DATA DATES**
- Never assume "today's date" for analysis
- Always get the actual last available date from CSV files using `df.iloc[-1]["time"]`
- Use `glob.glob()` to find the most recent CSV file for each ticker
- Compare actual data dates with existing analysis dates to determine if new analysis is needed

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current for US/crypto analysis

**Use LS tool to check for required input files:**
- Verify paths: `hold_us_crypto.md`, `REPORT_us_crypto.md`, `REPORT_us_crypto_week.md`, `LEADER_us_crypto.md`, `GROUP_us_crypto.md`
- Verify directories: `vpa_data_us_crypto/`, `market_data_us_crypto/`

**Manual Verification Actions**:
- **Use Read tool** to verify existing `hold_us_crypto.md` contains portfolio data table ("Dữ Liệu Danh Mục")
- **Use Read tool** to verify `REPORT_us_crypto.md` exists with recent daily signals and USD prices
- **Use LS tool** to verify `vpa_data_us_crypto/` directory exists with individual ticker daily VPA files
- **Use LS tool** to verify `market_data_us_crypto/` directory exists with individual ticker CSV files
- **Use Read tool** to verify `REPORT_us_crypto_week.md` exists with weekly analysis
- **Use Read tool** to verify `LEADER_us_crypto.md` exists with asset class context analysis
- **MANDATORY**: **Use Read tool** to verify `GROUP_us_crypto.md` exists with accurate ticker-to-asset-class mappings - manually cross-check all portfolio holdings
- **Use Read tool** to verify any available market context files for global market analysis

**Success Criteria**: All core input files are present and accessible through manual verification

### Step 2: Manual Portfolio State Analysis
**Objective**: Extract current US/crypto holdings and previous recommendations using manual natural language analysis

**Manual Analysis Actions**:
- **Use Read tool** to read existing `hold_us_crypto.md` "Dữ Liệu Danh Mục" table and manually identify:
  - All held tickers (DJI, BTC, ETH, etc.) with average buy prices in USD
  - Quantity of shares/units held for each ticker
  - Previous recommendation for each ticker from "Hành Động Đề Xuất" sections
- **Manual data extraction** using human intelligence to parse table data
- **NO automated text parsing** - read and understand using natural language

**Output**: Manual portfolio state mapping for next stage processing

### Step 3: STAGE 0 - Manual Data Analysis & Fact Sheet Creation
**Objective**: Create verified internal fact sheets for ALL US/crypto portfolio tickers using manual analysis

**Manual Processing Approach**: Use Task tools to process portfolio tickers with **manual natural language analysis guidance** since portfolio is typically smaller (5-20 tickers).

**Critical Manual Process**: For EVERY ticker in the portfolio holdings table, manually create this internal data structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "asset_type": "US_INDEX or CRYPTO",
  "holding_info": {
    "avg_buy_price": 32500.00,
    "quantity": 0.5
  },
  "previous_recommendation": "Hold/Buy More/Sell/etc.",
  "current_price": "Latest close from most recent market_data_us_crypto/{TICKER}_*.csv using reliable Python with glob.glob()",
  "most_recent_daily_signal": {
    "signal": "Effort to Rise/No Demand/SOS/etc. - manually identified",
    "date": "YYYY-MM-DD"
  },
  "daily_narrative_context": "1-sentence summary from vpa_data_us_crypto/{TICKER}.md last 3-5 days - manual analysis",
  "weekly_context": {
    "signal": "SOS Bar/Upthrust/etc. - manually identified",
    "week_ending_date": "YYYY-MM-DD",
    "weekly_narrative": "Brief summary of weekly trend and context - manual analysis"
  },
  "asset_class": "Asset class name from GROUP_us_crypto.md - manually verified",
  "asset_class_status": "Leading Consensus/Mixed Signals/Weakness from LEADER_us_crypto.md - manually identified",
  "overall_market_context": "1-sentence global market summary from available sources - manually extracted"
}
```

**Manual File Reading Strategy for Each Portfolio Ticker**:
1. **Use Read tool** to read `vpa_data_us_crypto/{TICKER}.md` for daily VPA narrative (last 10 entries) - manual analysis
2. **Use reliable Python script** to read the most recent `market_data_us_crypto/{TICKER}_*.csv` file for current price (last row):
```python
# CRITICAL: Use calculate_pnl_correct_us_crypto.py script for accurate P&L calculations
# This script:
# 1. Reads portfolio from hold_us_crypto.md table automatically 
# 2. Gets current USD prices from last row of the most recent CSV file for each ticker using glob.glob()
# 3. Calculates accurate P&L with proper formulas for US/crypto assets
python3 calculate_pnl_correct_us_crypto.py
```
3. **Manual cross-reference** with `REPORT_us_crypto.md` and `REPORT_us_crypto_week.md` for signals using Read tool
4. **CRITICAL**: **Manual asset class mapping** using `GROUP_us_crypto.md` and cross-check accuracy - manually verify each ticker's asset class classification
5. **Manual extraction** of asset class status from `LEADER_us_crypto.md` using Read tool
6. **Manual extraction** of global market context from available sources using Read tool

**Manual Data Extraction Rules**:
- **Manual extraction** of holding data from existing `hold_us_crypto.md` portfolio table using Read tool
- **Use calculate_pnl_correct_us_crypto.py script** for current USD prices from individual `market_data_us_crypto/{TICKER}_*.csv` files (script automatically finds most recent file using glob.glob())
- **Manual signal identification** from `REPORT_us_crypto.md` with exact dates using Read tool
- **Manual weekly signal extraction** from `REPORT_us_crypto_week.md` using Read tool  
- **Manual VPA narrative analysis** from individual `vpa_data_us_crypto/{TICKER}.md` files using Read tool
- **MANDATORY**: **Manual asset class mapping** using exact matches from `GROUP_us_crypto.md` - ALWAYS manually cross-check ticker asset class accuracy
- **Manual status extraction** from `LEADER_us_crypto.md` analysis using Read tool
- **Manual market context extraction** from available global market sources using Read tool

**Manual Processing Strategy**:
- Use Task tools to process multiple portfolio tickers with **manual analysis instructions**
- **NO automated text parsing** - all signal identification through human intelligence
- Each Task tool reads only relevant ticker files for each holding using Read tool
- **Manual verification** of all extracted data

**Quality Control**: These manually created fact sheets become the SOLE source of truth for all subsequent stages

**Example Manual Task Tool Usage for US/Crypto Portfolio**:
```
Task 1: "MANUAL ANALYSIS ONLY - Process US/crypto portfolio tickers DJI,BTC from hold_us_crypto.md holdings table. For each: 1) Use Read tool to manually read vpa_data_us_crypto/{TICKER}.md last 10 entries 2) Use reliable Python to read market_data_us_crypto/{TICKER}_*.csv current price 3) Manually extract signals from REPORT_us_crypto.md/REPORT_us_crypto_week.md using Read tool 4) Manually map asset class from GROUP_us_crypto.md using Read tool 5) Manually get status from LEADER_us_crypto.md using Read tool 6) Return complete manually-created fact sheet JSON. NO automated text parsing."

Task 2: "MANUAL ANALYSIS ONLY - For each US/crypto holding ticker, manually identify top 3 alternative investments. Use Read tool to prioritize weekly signals from REPORT_us_crypto_week.md, then manually use GROUP_us_crypto.md for same-asset-class options, manually confirm with daily signals from REPORT_us_crypto.md, and manually consider LEADER_us_crypto.md asset class status. Return ranked alternatives with specific VPA reasoning. NO automated signal detection."

Task 3: "MANUAL ANALYSIS ONLY - Select top 3 diversified portfolio expansion picks from different asset classes. PRIMARY: Use Read tool to manually read REPORT_us_crypto_week.md for weekly bullish signals. CRITICAL: Manually assess entry point value - avoid overextended tickers from leading asset classes unless at pullback levels. Manually look for 'Test for Supply', 'No Supply', early breakouts through human intelligence. Balance asset class leadership with attractive entry points. Consider rotation opportunities. Ensure 3 different asset classes. NO automated analysis."
```

**Manual Portfolio Processing Benefits**:
- **Manual focus** on only held tickers (typically 5-20 vs 100+ total tickers)
- **Individual file reading** provides precise context without noise from non-held tickers
- **Manual P&L calculations** with direct USD price access using reliable Python
- **Better manual risk assessment** with focused VPA context through human intelligence

### Step 4: STAGE 1 - Manual Ticker Action Assessment
**Objective**: Determine new recommended actions using manual analysis and state transition rules adapted for US/crypto markets

**Manual Process**: Apply action recommendation rules in exact order using ONLY manually created fact sheet data and human intelligence:

### Step 4.5: Portfolio Asset Class Peer Analysis

**CRITICAL PROTOCOL**: Before making any sell recommendations for portfolio holdings, MUST conduct comprehensive asset class peer analysis to prevent premature selling due to isolated weakness signals.

#### 4.5.1 Portfolio-Focused Asset Class Analysis
For each holding ticker showing bearish/weak signals:
1. **Identify Asset Class**: Use GROUP_us_crypto.md for ticker's asset class classification
2. **Gather Major Asset Class Peers**: List 3-5 major players in same asset class
3. **VPA Signal Assessment**: Check recent VPA signals for each peer
4. **Asset Class Strength Classification**: Determine if weakness is isolated or class-wide

#### 4.5.2 Sell Decision Matrix for US/Crypto Portfolio Holdings

| Individual Signal | Asset Class Context | Recommended Action | Risk Level |
|------------------|----------------|-------------------|------------|
| Bearish VPA | 70%+ Peers Weak | SELL | Low Risk - Asset class rotation confirmed |
| Bearish VPA | 30-60% Peers Mixed | HOLD/MONITOR | Medium Risk - Asset class mixed |
| Bearish VPA | <30% Peers Weak | HOLD/BUY DIP | High Risk - Likely temporary weakness |
| Strong Bearish VPA | Isolated Weakness | REDUCE POSITION | Medium Risk - Partial exit |

#### 4.5.3 Special US/Crypto Portfolio Considerations
- **US Index Holdings (DJI, INX, COMP, etc.)**: Always cross-reference all major US index peers
- **Crypto Holdings (BTC, ETH)**: Check correlation vs individual crypto issues  
- **Cross-Asset Analysis**: Verify global market context affects both asset classes similarly
- **Never sell based on isolated signals** when asset class remains strong

#### 4.5.4 Documentation for Portfolio Decisions
```markdown
**[TICKER] Portfolio Decision Analysis**
- Current Holding: [Avg Price USD, Quantity, P&L]
- Individual Signal: [Recent VPA signal and date]
- Asset Class Peers Analysis: [List peers and their recent signals]
- Asset Class Context: [Strong/Weak/Mixed - % breakdown]
- Risk Assessment: [Isolated weakness vs asset class rotation]
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

### Step 5: Accurate P&L Calculation Using calculate_pnl_correct_us_crypto.py
**Objective**: Calculate current profit/loss for each US/crypto holding using the verified calculation script

**CRITICAL CALCULATION PROCESS**:
1. **ALWAYS use calculate_pnl_correct_us_crypto.py script** - this script automatically:
   - Reads US/crypto portfolio from hold_us_crypto.md table 
   - Gets current USD prices from last row of the most recent CSV file for each ticker using glob.glob() pattern matching
   - Calculates accurate P&L with verified formulas for different asset types
   - **Formats all numbers using proper USD formatting** ($XX,XXX.XX)
   - Provides formatted output for hold_us_crypto.md updates

**Never use hardcoded prices or manual calculations** - always run:
```bash
python3 calculate_pnl_correct_us_crypto.py
```

**Script Output Provides**:
- Current USD prices from actual market data CSV files
- Accurate P&L calculations for each position using proper USD formatting (e.g., $28,085.60)
- Total portfolio P&L summary with consistent USD number formatting
- Formatted P&L lines ready for hold_us_crypto.md insertion with proper USD separators

**Formula Verification**: 
- P&L % = ((Current Price - Average Buy Price) / Average Buy Price) × 100
- P&L Amount = (Current Price - Average Buy Price) × Quantity
- All calculations verified by the script

**CRITICAL USD NUMBER FORMATTING**: Display as both percentage and monetary value using USD formatting (e.g., "+4.92% (+$2,885.00)")

**Data Sources**: 
- Portfolio holdings: From hold_us_crypto.md "Dữ Liệu Danh Mục" table
- Current prices: From most recent market_data_us_crypto/{TICKER}_*.csv last row (automatically detected using glob.glob())
- All processed automatically by calculate_pnl_correct_us_crypto.py

### Step 5.1: Manual Asset Class Allocation Calculation
**Objective**: Calculate portfolio allocation by asset class for the "Phân Bổ Danh Mục Theo Loại Tài Sản" table

**Manual Calculation Process**:
1. **Asset Class Classification**: **Use Read tool** to manually read `GROUP_us_crypto.md` and classify each portfolio ticker by asset class
2. **Market Value Calculation**: For each ticker, calculate market value = Current Price × Quantity
3. **Asset Class Aggregation**: Sum market values for all tickers within each asset class
4. **Percentage Calculation**: (Asset Class Total Value / Portfolio Total Value) × 100
5. **Ticker Listing**: Group tickers by asset class for display

**Manual Calculation Formula**:
- Asset Class Value = Σ(Current Price × Quantity) for all tickers in asset class
- Asset Class Percentage = (Asset Class Value / Total Portfolio Value) × 100
- Round percentages to 1 decimal place (e.g., 45.6%)

**Manual Table Format**:
```markdown
| Loại Tài Sản | Các Mã Tài Sản | Tỷ Trọng Danh Mục |
| :----------- | :------------- | :---------------- |
| Chỉ Số Mỹ | DJI, INX, COMP | 45.6% |
| Tiền Điện Tử | BTC, ETH | 54.4% |
```

**Manual Data Sources**:
- **Current prices**: From calculate_pnl_correct_us_crypto.py script output (reads actual CSV files)
- **Holdings quantities**: From existing hold_us_crypto.md "Dữ Liệu Danh Mục" table
- **Asset class classifications**: **Use Read tool** to manually verify against `GROUP_us_crypto.md`

**CRITICAL MANUAL VERIFICATION**: 
- **Always manually cross-check** asset class classifications against `GROUP_us_crypto.md`
- **Manually verify** percentage calculations sum to 100%
- **Display percentages only** - no USD amounts in the table

### Step 5.5: Manual Alternative Ticker Selection
**Objective**: For each holding ticker, manually identify 3 best alternative investment options within same asset class

**Manual Selection Criteria** (in priority order):
1. **Manual Weekly VPA Analysis Priority**: **Use Read tool** to manually prioritize tickers with strong weekly signals from `REPORT_us_crypto_week.md`
2. **Manual Same Asset Class Group**: **Use Read tool** to manually consider tickers from same asset class (from `GROUP_us_crypto.md`)
3. **Manual Daily VPA Confirmation**: **Use Read tool** to manually confirm weekly analysis with daily signals from `REPORT_us_crypto.md`
4. **Manual Asset Class Leadership**: **Use Read tool** to manually prefer tickers from "Leading Consensus" asset classes (from `LEADER_us_crypto.md`)

**Manual Data Sources for Alternative Analysis**:
- **Use Read tool** to manually read `REPORT_us_crypto_week.md` for weekly VPA signals of all available tickers
- **Use Read tool** to manually read `REPORT_us_crypto.md` for daily VPA confirmation signals
- **Use Read tool** to manually use `GROUP_us_crypto.md` to identify same-asset-class alternatives
- **Use Read tool** to manually use `LEADER_us_crypto.md` to prioritize strong asset class groups
- **Use Read tool** to manually cross-reference with `vpa_data_us_crypto/{TICKER}.md` files for detailed analysis

**Manual Selection Process**:
1. **Manual Asset Class Matching**: **Use Read tool** to manually find all tickers in same asset class as holding ticker - **MANDATORY**: Manually use `GROUP_us_crypto.md` to verify exact asset class classification
2. **Manual Weekly Signal Filtering**: **Manual analysis** to prioritize those with strong weekly bullish signals (SOS Bar, Effort to Rise, etc.)
3. **Manual Daily Confirmation**: **Manual verification** to confirm weekly signals with supportive daily VPA analysis
4. **Manual Cross-Asset Class Options**: If insufficient same-asset-class options, manually expand to strong tickers from leading asset classes
5. **Manual Ranking Logic**: **Human intelligence** to rank by weekly signal strength first, then daily confirmation, then asset class leadership status
6. **⚠️ CRITICAL ASSET CLASS VERIFICATION**: **MANDATORY manual cross-check** - alternatives MUST be from the SAME asset class in `GROUP_us_crypto.md`
   - **Zero tolerance**: Never mix asset classes in same-ticker alternatives  
   - **Manual verification required**: Read GROUP_us_crypto.md for every alternative ticker
   - **Error prevention**: Cross-asset-class mixing is a critical bug that leads to poor portfolio advice

**Manual Output Format**: For each alternative, provide specific reasoning citing:
- Weekly VPA signal and date (PRIORITY) - manually identified
- Daily VPA confirmation (if available) - manually verified
- Asset class and leadership status - manually checked
- Comparative advantage over current holding - manually assessed

### Step 5.6: Manual Diversified Portfolio Expansion Selection
**Objective**: Manually select top 3 tickers from different asset classes for portfolio diversification

**Manual Priority Data Sources** (in order):
1. **Manual Weekly VPA Analysis (PRIMARY)**: **Use Read tool** to manually read `REPORT_us_crypto_week.md` - prioritize strong weekly signals
2. **Manual Daily VPA Confirmation (SECONDARY)**: **Use Read tool** to manually read `REPORT_us_crypto.md` - confirm weekly signals only
3. **Manual Market Context**: **Use Read tool** to manually read available global market analysis for context
4. **Manual Asset Class Leadership**: **Use Read tool** to manually read `LEADER_us_crypto.md` for asset class rotation strategy

**Manual Selection Criteria** (in priority order):
1. **Manual Cross-Asset Class Diversification**: Must manually select from different asset classes
2. **Manual Weekly Signal Strength**: **Human intelligence** to prioritize "Sign of Strength" and "Effort to Rise" from weekly analysis
3. **Manual Entry Point Valuation**: **Manual assessment** to avoid overextended tickers - prefer pullbacks, consolidations, or early breakouts
4. **Manual Asset Class Balance**: **Human judgment** to mix leading asset classes with emerging/recovering classes for better value
5. **Manual Risk-Reward Ratio**: **Manual evaluation** to prioritize favorable entry points over pure asset class leadership

**Manual Selection Process**:
1. **Manual Asset Class Mapping**: **Use Read tool** to manually identify available asset classes and top picks, noting current price levels
2. **Manual Weekly Signal Analysis**: **Use Read tool** to manually analyze `REPORT_us_crypto_week.md`, filter tickers with strongest weekly bullish signals through human intelligence
3. **Manual Entry Point Assessment**: **Manual identification** of tickers with:
   - Recent pullbacks to support levels ("Test for Supply" or "No Supply") - manually identified
   - Early-stage breakouts with room for growth - manually assessed
   - Consolidation patterns near key support levels - manually analyzed
   - Avoid extended moves without healthy corrections - manual judgment
4. **Manual Value vs. Leadership Balance**: **Human decision-making** to:
   - Don't exclusively pick from "Leading Consensus" asset classes if overextended - manual assessment
   - Consider "Mixed Signals" or recovering asset classes with better entry points - manual evaluation
   - Look for rotation opportunities from expensive to undervalued asset classes - manual analysis
5. **Manual Asset Class Diversification**: **Manual verification** to ensure 3 picks from different major asset classes
6. **Manual Daily Confirmation**: **Use Read tool** to manually confirm weekly signals and assess short-term entry timing
7. **Manual Risk-Reward Evaluation**: **Manual calculation** of potential upside vs. current extension from key levels

**Manual Output Requirements**:
- 3 tickers from 3 different asset classes - manually verified
- Each selection must cite weekly VPA signal and date as primary justification - manually identified
- **Manual Entry Point Analysis**: Specific reasoning why current levels offer good value - manual assessment
- **Manual Risk-Reward Assessment**: Compare current price to key support/resistance levels - manual analysis
- Include reasoning for diversification benefit beyond just asset class leadership - manual evaluation
- Avoid overextended picks from leading asset classes unless at attractive re-entry points - manual judgment
- Consider asset class rotation opportunities and value plays in emerging classes - manual strategy

### Step 6: Manual hold_us_crypto.md Generation
**Objective**: Generate complete hold_us_crypto.md using manually verified fact sheets and manually determined final actions

#### 6.1 File Header
```markdown
# Kế Hoạch Quản Lý Danh Mục Tài Sản Toàn Cầu

**Cập Nhật Lần Cuối:** [Current Date]

## Dữ Liệu Danh Mục

| Mã Tài Sản | Giá Mua Trung Bình (USD) | Số Lượng Nắm Giữ |
| :--------- | :---------------------- | :--------------- |
[US/crypto portfolio holdings table using fact sheet data]
```

#### 6.2 Portfolio Analysis Section
```markdown
## Phân tích

**1. Tóm Tắt Danh Mục Hiện Tại**

[Concise overview based on collective actions and global market context]

* **Phân Bổ Danh Mục Theo Loại Tài Sản:**
  | Loại Tài Sản | Các Mã Tài Sản | Tỷ Trọng Danh Mục |
  | :----------- | :------------- | :---------------- |
  [Asset class allocation table showing asset class name, ticker list, and percentage allocation calculated from price × quantity for each class]

* **Tóm Tắt Hành Động Đề Xuất:**
  | Mã Tài Sản | Trạng Thái Hiện Tại | Hành Động Đề Xuất Ngắn Gọn |
  | :--------- | :------------------ | :------------------------- |
  [Summary table of new recommendations]

**2. Kế Hoạch Giao Dịch Chi Tiết**

**3. Kế Hoạch Gia Tăng Chi Tiết**

*Top 3 tài sản đa dạng loại để mở rộng danh mục - giảm rủi ro, tăng lợi nhuận*

| Mã Tài Sản | Loại Tài Sản | Tín Hiệu VPA Chính | Lý Do Lựa Chọn |
| :--------- | :----------- | :----------------- | :-------------- |
[Top 3 diversified recommendations with cross-asset-class analysis]
```

#### 6.3 Individual Ticker Analysis (A-Z Order)
For EVERY ticker, provide detailed breakdown:

```markdown
### **[TICKER] ([ASSET_CLASS])**
![Weekly Chart](./reports_us_crypto_week/[TICKER]/[TICKER]_candlestick_chart.png)
![Daily Chart](./reports_us_crypto/[TICKER]/[TICKER]_candlestick_chart.png)

* **Giá Mua Trung Bình:** [From fact sheet] USD
* **Số Lượng Nắm Giữ:** [From fact sheet]
* **Giá Hiện Tại:** [From fact sheet] USD
* **P&L (Lợi Nhuận/Thua Lỗ Chưa Thực Hiện):** [Calculated P&L using USD format - e.g., +9.27% (+$2,885.00)]
* **VPA Phân Tích Hiện Tại:** 
  * **Bối Cảnh Tuần:** [Weekly context from fact sheet - weekly signals, week ending date, and weekly narrative]
  * **Bối Cảnh Ngày:** [Daily context from fact sheet - daily signals, recent narrative, and short-term trend analysis]
* **Hành Động Đề Xuất:** [Final decision from Stage 1]
  * **Giá Đề Xuất:** [Specific USD price range if buy/sell action]
  * **Số Lượng Đề Xuất:** [Specific quantity appropriate for asset type (whole shares for indices, fractional for crypto) if buy/sell action]
  * **Lý Do Hành Động:** [VPA logic explaining the decision]
* **Điểm Dừng Lỗ:** [Specific stop-loss level in USD]
* **Điểm Chốt Lời:** [Specific take-profit level(s) in USD]
* **Top 3 Tài Sản Thay Thế:** [3 best alternative tickers with reasoning]
  * **[TICKER1]**: [Reason based on weekly/daily VPA analysis]
  * **[TICKER2]**: [Reason based on weekly/daily VPA analysis]  
  * **[TICKER3]**: [Reason based on weekly/daily VPA analysis]
```

#### 6.4 Change Log Section
```markdown
**3. Nhật Ký Thay Đổi Kế Hoạch**

* **Chuyển Từ Hold sang Buy/Buy More/Buy Fast/Prepare to Buy:**
  * [Document upgrades with specific protocol conditions and signals]

* **Chuyển Từ Hold sang Sell/Panic Sell:**
  * [Document downgrades with specific protocol conditions and signals]

* **Thay Đổi Trạng Thái Khác:**
  * [Document other significant changes with justifications]

* **Loại Bỏ/Thêm Mới Ticker:**
  * [Document additions or removals from portfolio]
```

### Step 7: Manual Quality Verification
**Objective**: Ensure hold_us_crypto.md accuracy and completeness through manual verification

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
- [ ] All portfolio holdings from previous hold_us_crypto.md are processed - manually cross-checked
- [ ] P&L calculations are mathematically correct in USD - manually verified
- [ ] All assertions cite specific signals and dates from manually created fact sheets
- [ ] Action recommendations follow state transition rules correctly - manually verified
- [ ] Change log documents every recommendation change with manual justification
- [ ] Chart links use correct file paths (reports_us_crypto/) - manually checked
- [ ] Vietnamese text is grammatically correct - manually reviewed
- [ ] Asset class classifications match GROUP_us_crypto.md exactly - manually cross-verified
- [ ] **CRITICAL**: All "Top 3 Tài Sản Thay Thế" alternatives are from the SAME asset class as the holding ticker per GROUP_us_crypto.md - manually verified

### Step 8: 5-Day Market Forecast Generation
**Objective**: Create detailed 5-day forward-looking analysis with scenario-based action plans for US/crypto markets

**Manual Forecast Process**:
- **Use Read tool** to analyze current global market conditions from available sources
- **Manual assessment** of post-climax market behavior patterns using VPA methodology adapted for US/crypto markets  
- **Scenario-based planning** for Up/Sideway/Down outcomes with specific probabilities
- **Dynamic action plans** for each scenario based on US/crypto portfolio holdings and market context

**5-Day Forecast Structure**:
```markdown
## 5. Dự Đoán 5 Ngày Kế Tiếp

### **Ngày [X] ([DATE])**

**Tình Huống UP ([PROBABILITY]%)**
- **Mô tả**: [Global market scenario description]
- **Điều kiện**: [Technical conditions required for US/crypto assets]
- **Hành động**: [Specific portfolio actions for US/crypto holdings]

**Tình Huống SIDEWAY ([PROBABILITY]%)**
- **Mô tả**: [Global market scenario description]  
- **Điều kiện**: [Technical conditions required for US/crypto assets]
- **Hành động**: [Specific portfolio actions for US/crypto holdings]

**Tình Huống DOWN ([PROBABILITY]%)**
- **Mô tả**: [Global market scenario description]
- **Điều kiện**: [Technical conditions required for US/crypto assets]
- **Hành động**: [Specific portfolio actions for US/crypto holdings]
```

**Manual Forecast Guidelines**:
- **Day 1**: Focus on immediate post-climax reaction (conservative probabilities)
- **Day 2-3**: Consider trend development and institutional response in global markets
- **Day 4-5**: Account for weekly close and monthly patterns for both US and crypto
- **Probabilities**: Must sum to 100%, reflect VPA-based global market structure analysis
- **Actions**: Specific to current US/crypto portfolio holdings with exact USD price levels and quantities

**Key Forecast Elements**:
- **US Index levels**: Specific support/resistance levels for each scenario
- **Crypto price levels**: Key technical levels for major cryptocurrencies
- **Portfolio actions**: Exact quantities and USD price triggers for holdings
- **Cash management**: Dynamic cash allocation based on global market conditions
- **Risk management**: Clear stop-loss and emergency procedures
- **Strategic summary**: 5-day overview with core principles and key USD levels

### Step 9: Manual File Output
**Objective**: Generate final hold_us_crypto.md file using manual compilation

**Manual Output Process**:
- **Use Write tool** to create complete hold_us_crypto.md content based on manual analysis
- **Manual compilation** of all sections using manually verified data
- **Manual formatting** to ensure proper Vietnamese structure adapted for global markets
- **Manual verification** of all content before writing

## Manual Quality Control Standards

### Manual Data Accuracy Requirements
- **Zero Tolerance**: No assertions without manual fact sheet verification
- **Price Accuracy**: Current USD prices must match market_data_us_crypto CSV files exactly - verified using calculate_pnl_correct_us_crypto.py
- **Date Precision**: All signals must include exact dates - manually verified
- **P&L Accuracy**: Mathematical calculations must be manually verified as precise using USD formatting for ALL individual ticker P&L amounts
- **Number Formatting**: ALL monetary amounts must use USD formatting ($XX,XXX.XX)
- **State Tracking**: Previous recommendations must be accurately captured through manual analysis

### 🚨 MANDATORY DATA INTEGRITY RULES

#### **RULE 1: NO DATE MIXING (CRITICAL)**
- **NEVER mix VPA analysis from different dates** in the same recommendation
- **ALWAYS verify VPA signal dates match the analysis context date**
- **Example of FORBIDDEN practice**: Using 2025-08-05 "Sign of Strength" analysis for 2025-08-07 recommendations
- **Verification Required**: Cross-check all VPA claims against actual dates in vpa_data_us_crypto/{TICKER}.md files
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
- **Example of FORBIDDEN**: Recommending BTC entry at $30,000 when current price is $65,000 (+117%)
- **Mandatory verification**: Compare ALL recommended entry prices against current market data

#### **RULE 5: VPA SIGNAL ACCURACY**
- **MANDATORY cross-verification**: All claimed VPA signals must match exactly with vpa_data_us_crypto files**
- **Zero tolerance for signal misstatement**: "No Supply" vs "No Demand" are different signals
- **Daily verification**: Check latest 3 entries in vpa_data_us_crypto/{TICKER}.md for current signal accuracy
- **Flag mismatches immediately**: Any discrepancy requires investigation and correction

#### **RULE 6: POSITION SIZING COMPLIANCE**
- **US Index positions must be whole shares minimum 1 share**
- **Crypto positions can be fractional but must be reasonable amounts (0.01 BTC minimum, 0.1 ETH minimum)**
- **Correct examples**: 10 shares DJI, 0.5 BTC, 2.5 ETH
- **Automatic rejection**: Any position size recommendation violating logical constraints

#### **RULE 7: ASSET CLASS VERIFICATION**
- **MANDATORY**: All "Top 3 Tài Sản Thay Thế" must be from SAME asset class per GROUP_us_crypto.md
- **Zero tolerance for cross-asset-class mixing** in alternatives
- **Verification process**: Read GROUP_us_crypto.md and manually confirm every alternative ticker's asset class
- **Example of FORBIDDEN**: Crypto alternatives (BTC, ETH) for US Index holding (DJI)
- **Error detection**: Any alternative from different asset class triggers immediate correction

#### **RULE 8: OVEREXTENSION DETECTION**
- **Automatic flagging**: Any ticker >30% above its recommended entry price range**
- **Immediate review required**: Tickers showing recent "No Demand" or "Sign of Weakness" signals
- **Risk assessment mandatory**: Evaluate if overextended tickers should be removed from recommendations
- **Conservative approach**: When in doubt, exclude overextended candidates

### 🔍 MANDATORY PRE-SUBMISSION VERIFICATION CHECKLIST

**Before finalizing hold_us_crypto.md, EVERY AI agent must verify:**

- [ ] **Date Integrity**: No VPA analysis mixed from different dates
- [ ] **Signal Accuracy**: All VPA signals match vpa_data_us_crypto files exactly  
- [ ] **Price Reality**: All entry recommendations within 10% of current USD prices
- [ ] **R:R Ratios**: All recommendations have ≥2:1 risk-reward ratios
- [ ] **Position Sizes**: All quantities are appropriate for asset type
- [ ] **Asset Class Match**: All alternatives from same asset class per GROUP_us_crypto.md
- [ ] **Volume Claims**: All volume statistics verified against actual CSV data
- [ ] **Current State**: Analysis reflects most recent data date, not historical events
- [ ] **Overextension Check**: No recommendations for tickers >30% above suggested entry
- [ ] **Signal Consistency**: Daily and weekly VPA signals align logically

### 🚨 AUTOMATIC REJECTION TRIGGERS

**Any hold_us_crypto.md with the following issues must be REJECTED and regenerated:**

1. **Date mixing detected** (different VPA dates in same analysis)
2. **Risk-reward ratios <2:1** for any ticker
3. **Entry prices >15% gap** from current market prices  
4. **Cross-asset-class alternatives** detected
5. **Position sizes violating asset type constraints**
6. **VPA signal mismatches** with source data
7. **Volume claims unverified** against CSV files
8. **Overextended tickers** without proper risk warnings

### 📊 VALIDATION PROTOCOLS

#### **Daily Validation Process**:
1. **Run calculate_pnl_correct_us_crypto.py** to verify all USD prices
2. **Spot-check 3 random tickers** for VPA signal accuracy  
3. **Verify all R:R ratios** meet minimum standards
4. **Check top 3 most recent VPA entries** for date consistency
5. **Cross-reference alternatives** with GROUP_us_crypto.md classifications

#### **Weekly Deep Audit**:
1. **Full portfolio VPA verification** against source files
2. **Complete R:R ratio audit** for all recommendations  
3. **Entry price reality check** for all diversification picks
4. **Alternative asset class classification** comprehensive review
5. **Position sizing compliance** across entire US/crypto portfolio

### Action Logic Standards
- **Protocol Adherence**: All decisions must follow state transition rules
- **Signal Confirmation**: Bullish/bearish assessments must be evidence-based
- **Risk Management**: Stop-loss and take-profit levels must be technically justified for global markets
- **Position Sizing**: Quantity recommendations must be proportional and reasonable for each asset type

### Vietnamese Language Standards
- **PRIORITY VIETNAMESE**: Use Vietnamese language for all analysis and explanations - VPA signal names in English are acceptable
- **NO MIXED LANGUAGE**: Never mix English and Vietnamese in same sentence (e.g. avoid "US Index sector leads recovery, momentum breakout", "Excellent entry point sau healthy pullback")
- Use proper Vietnamese financial terminology adapted for global markets
- Maintain professional tone and grammar in Vietnamese
- **CRITICAL USD FORMATTING**: Use proper USD formatting for all amounts (e.g., $28,085.60, not $28.085.600). Use commas for thousands separator in USD amounts
- Use consistent asset class naming from GROUP_us_crypto.md
- **EXAMPLES OF CORRECT USAGE**:
  - Good: "Điểm vào tốt sau điều chỉnh lành mạnh, tỷ lệ rủi ro-lợi nhuận 3:1 thuận lợi"
  - Bad: "Excellent entry point sau healthy pullback, favorable 3:1 risk-reward ratio"
  - Good: "Chỉ số Mỹ dẫn dắt chu kỳ phục hồi kinh tế toàn cầu"
  - Bad: "US Index leads recovery, momentum breakout"
  - Good (Numbers): "Tổng P&L: +$28,085.60 (+8.35%)"
  - Bad (Numbers): "Tổng P&L: +28.085.600 USD (+8.35%)"
  - Good (Individual P&L): "+9.27% (+$2,885.00)"
  - Bad (Individual P&L): "+9.27% (+2.885 USD)"

### Technical Requirements
- **Chart Links**: Verify all image paths exist (reports_us_crypto/ and reports_us_crypto_week/)
- **Report Links**: Ensure links to REPORT_us_crypto.md work with correct anchors
- **Markdown Formatting**: Proper headers, tables, and structure
- **Data Consistency**: Holdings table must match individual analyses

## Error Handling

### Missing Portfolio Data
- Document missing tickers in summary
- Use available data and note limitations
- Flag areas requiring manual review

### Price Data Issues
- Cross-reference multiple sources for current USD prices
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
- **Actionability**: Recommendations provide clear trading instructions in USD
- **Risk Management**: Appropriate stop-loss and position sizing for US/crypto assets

## Templates

### Fact Sheet Template
```json
{
  "ticker": "",
  "asset_type": "US_INDEX or CRYPTO",
  "holding_info": {"avg_buy_price": 0, "quantity": 0},
  "previous_recommendation": "",
  "current_price": 0,
  "most_recent_daily_signal": {"signal": "", "date": ""},
  "daily_narrative_context": "",
  "weekly_context": {"signal": "", "week_ending_date": ""},
  "asset_class": "",
  "asset_class_status": "",
  "overall_market_context": ""
}
```

### Action Justification Templates
- **Buy More**: "Tín hiệu [SIGNAL] ngày [DATE] xác nhận xu hướng tăng mạnh, đáp ứng điều kiện #1A"
- **Sell**: "Tín hiệu [SIGNAL] ngày [DATE] phá vỡ cấu trúc tăng giá với khối lượng lớn, đáp ứng điều kiện #1C"
- **Hold**: "Tín hiệu [SIGNAL] ngày [DATE] cho thấy giai đoạn tích lũy, cần quan sát thêm"

## Risk Management Notes

- **Position Sizing**: Consider portfolio balance when recommending quantity changes for different asset types. **CRITICAL**: All US index buying suggestions must specify whole share quantities (1, 5, 10, etc.), crypto positions can be fractional but reasonable (0.01 BTC minimum, 0.1 ETH minimum)
- **Stop-Loss Placement**: Use technical levels appropriate for each asset type, not arbitrary percentages
- **Take-Profit Strategy**: Consider partial profit-taking at multiple levels adapted for volatility differences
- **Market Context**: Factor in overall global market trend for individual US/crypto decisions