# Daily Portfolio Management Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `hold.md` file using the Portfolio-Strategist methodology with **manual natural language analysis only**. No unreliable Python text parsing utilities.

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
  "current_price": "Latest close from market_data/{TICKER}_*.csv using reliable Python",
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
2. **Use reliable Python script** to read `market_data/{TICKER}_2025-01-02_to_2025-07-28.csv` for current price (last row):
```python
# CRITICAL: Use calculate_pnl_correct.py script for accurate P&L calculations
# This script:
# 1. Reads portfolio from hold.md table automatically 
# 2. Gets current prices from last row of each ticker's CSV in market_data/
# 3. Calculates accurate P&L with proper formulas
python3 calculate_pnl_correct.py
```
3. **Manual cross-reference** with `REPORT.md` and `REPORT_week.md` for signals using Read tool
4. **CRITICAL**: **Manual industry mapping** using `GROUP.md` and cross-check accuracy - manually verify each ticker's industry classification
5. **Manual extraction** of industry status from `LEADER.md` using Read tool
6. **Manual extraction** of VNINDEX context from `PLAN.md` using Read tool

**Manual Data Extraction Rules**:
- **Manual extraction** of holding data from existing `hold.md` portfolio table using Read tool
- **Use calculate_pnl_correct.py script** for current prices from individual `market_data/{TICKER}_2025-01-02_to_2025-07-28.csv` files
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
   - Gets current prices from last row of each ticker's CSV in market_data/
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
- Current prices: From market_data/{TICKER}_2025-01-02_to_2025-07-28.csv last row
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
6. **CRITICAL MANUAL VERIFICATION**: **Always manually cross-check** alternatives are from the SAME industry group in `GROUP.md` - never mix industries in same-sector alternatives

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

### Step 6: Manual hold.md Generation
**Objective**: Generate complete hold.md using manually verified fact sheets and manually determined final actions

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

#### 6.3 Individual Ticker Analysis (A-Z Order)
For EVERY ticker, provide detailed breakdown:

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

### Step 8: Manual File Output
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