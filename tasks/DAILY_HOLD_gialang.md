# Daily Portfolio Management Task - AI Agent Protocol (Gialang Portfolio)

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `hold-gialang.md` file using the Portfolio-Strategist methodology. The agent must follow these steps sequentially to provide actionable portfolio management recommendations based on VPA analysis for the Gialang portfolio.

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current

```bash
# Check for required input files
ls hold-gialang.md REPORT.md REPORT_week.md LEADER.md GROUP.md PLAN.md
ls vpa_data/ market_data/
```

**Actions**:
- Verify existing `hold-gialang.md` contains portfolio data table ("Dữ Liệu Danh Mục")
- Verify `REPORT.md` exists with recent daily signals and prices
- Verify `vpa_data/` directory exists with individual ticker daily VPA files
- Verify `market_data/` directory exists with individual ticker CSV files
- Verify `REPORT_week.md` exists with weekly analysis
- Verify `LEADER.md` exists with industry context analysis
- **MANDATORY**: Verify `GROUP.md` exists with accurate ticker-to-industry mappings - cross-check all portfolio holdings
- Verify `PLAN.md` exists with overall market context (VNINDEX analysis)

**Success Criteria**: All core input files are present and accessible

### Step 2: Previous Portfolio State Analysis
**Objective**: Extract current holdings and previous recommendations

**Actions**:
- Read existing `hold-gialang.md` "Dữ Liệu Danh Mục" table to identify:
  - All held tickers with average buy prices
  - Quantity of shares held for each ticker
  - Previous recommendation for each ticker from "Hành Động Đề Xuất" sections

**Output**: Portfolio state mapping for Stage 0 processing

**Gialang Portfolio Holdings**:
- MWG: 55.38 avg price, 2,500 shares
- VNM: 61.41 avg price, 2,700 shares
- SSI: 25.71 avg price, 4,200 shares
- MSN: 65.58 avg price, 1,000 shares
- KBC: 27.76 avg price, 2,500 shares
- FUEVFVND: 32.01 avg price, 1,800 shares (Fund)
- NKG: 15.65 avg price, 4,100 shares
- TCB: 26.34 avg price, 1,200 shares
- AGG: 19.63 avg price, 1,950 shares

### Step 3: STAGE 0 - Data Verification & Fact Sheet Creation
**Objective**: Create verified internal fact sheets for ALL portfolio tickers

**Parallel Processing Approach**: Use Task tool to process portfolio tickers concurrently since portfolio is typically smaller (5-20 tickers).

**Critical Process**: For EVERY ticker in the portfolio holdings table, create this internal data structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "holding_info": {
    "avg_buy_price": 32.50,
    "quantity": 1000
  },
  "previous_recommendation": "Hold/Buy More/Sell/etc.",
  "current_price": "Latest close from market_data/{TICKER}_*.csv",
  "most_recent_daily_signal": {
    "signal": "Effort to Rise/No Demand/SOS/etc.",
    "date": "YYYY-MM-DD"
  },
  "daily_narrative_context": "1-sentence summary from vpa_data/{TICKER}.md last 3-5 days",
  "weekly_context": {
    "signal": "SOS Bar/Upthrust/etc.",
    "week_ending_date": "YYYY-MM-DD",
    "weekly_narrative": "Brief summary of weekly trend and context"
  },
  "industry_group": "Industry name from GROUP.md",
  "industry_status": "Dẫn dắt Đồng Thuận/Yếu/Phân Phối from LEADER.md",
  "overall_market_context": "1-sentence VNINDEX summary from PLAN.md"
}
```

**File Reading Strategy for Each Portfolio Ticker**:
1. Read `vpa_data/{TICKER}.md` for daily VPA narrative (last 10 entries)
2. Read `market_data/{TICKER}_*.csv` for current price (last row)
3. Cross-reference with `REPORT.md` and `REPORT_week.md` for signals
4. **CRITICAL**: Map industry using `GROUP.md` and cross-check accuracy - verify each ticker's industry classification
5. Get industry status from `LEADER.md`
6. Extract VNINDEX context from `PLAN.md`

**Data Extraction Rules**:
- Extract holding data ONLY from existing `hold-gialang.md` portfolio table
- Extract current prices from individual `market_data/{TICKER}_*.csv` files (most recent closing price)
- Extract daily signals ONLY from `REPORT.md` with exact dates
- Extract weekly signals ONLY from `REPORT_week.md` with week ending dates and weekly trend context
- Extract VPA narrative context from individual `vpa_data/{TICKER}.md` files
- **MANDATORY**: Map industries using exact matches from `GROUP.md` - ALWAYS cross-check ticker industry classification accuracy
- Get industry status from `LEADER.md` analysis
- Extract market context from `PLAN.md` VNINDEX analysis

**Parallel Processing Strategy**:
- Use Task tool to process multiple portfolio tickers concurrently
- Read only relevant ticker files for each holding (vpa_data/{TICKER}.md, market_data/{TICKER}_*.csv)
- Avoid reading large consolidated files for better performance and context focus

**Quality Control**: These fact sheets become the SOLE source of truth for all subsequent stages

**Example Task Tool Usage for Gialang Portfolio**:
```
Task 1: "Process portfolio tickers MWG,VNM,SSI from hold-gialang.md holdings table. For each: 1) Read vpa_data/{TICKER}.md last 10 entries 2) Read market_data/{TICKER}_*.csv current price 3) Extract signals from REPORT.md/REPORT_week.md 4) Map industry from GROUP.md 5) Get status from LEADER.md 6) Return complete fact sheet JSON"

Task 2: "For each holding ticker, identify top 3 alternative investments. Prioritize weekly signals from REPORT_week.md, then use GROUP.md for same-industry options, confirm with daily signals from REPORT.md, and consider LEADER.md industry status. Return ranked alternatives with specific VPA reasoning."

Task 3: "Select top 3 diversified portfolio expansion picks from different industry sectors. PRIMARY: Read REPORT_week.md for weekly bullish signals. CRITICAL: Assess entry point value - avoid overextended tickers from leading sectors unless at pullback levels. Look for 'Test for Supply', 'No Supply', early breakouts. Balance sector leadership with attractive entry points. Consider sector rotation opportunities. Ensure 3 different industries."
```

**Portfolio Processing Benefits**:
- Focused analysis on only held tickers (typically 5-20 vs 100+ total tickers)
- Individual files provide precise context without noise from non-held tickers
- Faster P&L calculations with direct price access
- Better risk assessment with focused VPA context

### Step 4: STAGE 1 - Ticker Action Assessment
**Objective**: Determine new recommended actions using state transition rules

**Process**: Apply action recommendation rules in exact order using ONLY fact sheet data:

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

### Step 5: P&L Calculation
**Objective**: Calculate current profit/loss for each holding

**Formula**: 
- P&L % = ((Current Price - Average Buy Price) / Average Buy Price) × 100
- P&L Amount = (Current Price - Average Buy Price) × Quantity

**Format**: Display as both percentage and monetary value (e.g., "+4.92% (+327.6)")

### Step 5.5: Alternative Ticker Selection
**Objective**: For each holding ticker, identify 3 best alternative investment options

**Selection Criteria** (in priority order):
1. **Weekly VPA Analysis Priority**: Prioritize tickers with strong weekly signals from `REPORT_week.md`
2. **Same Industry Group**: First consider tickers from same industry group (from `GROUP.md`)
3. **Daily VPA Confirmation**: Use daily signals from `REPORT.md` to confirm weekly analysis
4. **Industry Leadership**: Prefer tickers from "Dẫn dắt" or "Đồng Thuận" industries (from `LEADER.md`)

**Data Sources for Alternative Analysis**:
- Read `REPORT_week.md` for weekly VPA signals of all available tickers
- Read `REPORT.md` for daily VPA confirmation signals
- Use `GROUP.md` to identify same-industry alternatives
- Use `LEADER.md` to prioritize strong industry groups
- Cross-reference with `vpa_data/{TICKER}.md` files for detailed analysis

**Selection Process**:
1. **Industry Matching**: Find all tickers in same industry group as holding ticker - **MANDATORY**: Use `GROUP.md` to verify exact industry classification
2. **Weekly Signal Filtering**: From available tickers, prioritize those with strong weekly bullish signals (SOS Bar, Effort to Rise, etc.)
3. **Daily Confirmation**: Confirm weekly signals with supportive daily VPA analysis
4. **Cross-Industry Options**: If insufficient same-industry options, expand to strong tickers from leading industry groups
5. **Ranking Logic**: Rank by weekly signal strength first, then daily confirmation, then industry leadership status
6. **CRITICAL VERIFICATION**: Always cross-check alternatives are from the SAME industry group in `GROUP.md` - never mix industries in same-sector alternatives

**Output Format**: For each alternative, provide specific reasoning citing:
- Weekly VPA signal and date (PRIORITY)
- Daily VPA confirmation (if available)
- Industry group and leadership status
- Comparative advantage over current holding

### Step 5.6: Diversified Portfolio Expansion Selection
**Objective**: Select top 3 tickers from different industry sectors for portfolio diversification

**Priority Data Sources** (in order):
1. **Weekly VPA Analysis (PRIMARY)**: `REPORT_week.md` - prioritize strong weekly signals
2. **Daily VPA Confirmation (SECONDARY)**: `REPORT.md` - confirm weekly signals only
3. **Market Context**: `PLAN.md` top recommendations and market analysis
4. **Industry Leadership**: `LEADER.md` for sector rotation strategy

**Selection Criteria** (in priority order):
1. **Cross-Sector Diversification**: Must select from 3 different industry groups
2. **Weekly Signal Strength**: Prioritize "Sign of Strength" and "Effort to Rise" from weekly analysis
3. **Entry Point Valuation**: Avoid overextended tickers - prefer pullbacks, consolidations, or early breakouts
4. **PLAN.md Integration**: Consider tickers from "Top 1x Cơ Hội Giao Dịch" section but evaluate entry points
5. **Industry Balance**: Mix leading sectors with emerging/recovering sectors for better value
6. **Risk-Reward Ratio**: Prioritize favorable entry points over pure sector leadership

**Selection Process**:
1. **Industry Mapping**: Read `PLAN.md` to identify sectors and picks, noting current price levels
2. **Weekly Signal Analysis**: From `REPORT_week.md`, filter tickers with strongest weekly bullish signals
3. **Entry Point Assessment**: Identify tickers with:
   - Recent pullbacks to support levels ("Test for Supply" or "No Supply")
   - Early-stage breakouts with room for growth
   - Consolidation patterns near key support levels
   - Avoid extended moves without healthy corrections
4. **Value vs. Leadership Balance**: 
   - Don't exclusively pick from "Dẫn dắt" sectors if overextended
   - Consider "Đồng Thuận" or recovering sectors with better entry points
   - Look for rotation opportunities from expensive to undervalued sectors
5. **Sector Diversification**: Ensure 3 picks from different major industry groups
6. **Daily Confirmation**: Use `REPORT.md` to confirm weekly signals and assess short-term entry timing
7. **Risk-Reward Evaluation**: Calculate potential upside vs. current extension from key levels

**Output Requirements**:
- 3 tickers from 3 different industry sectors
- Each selection must cite weekly VPA signal and date as primary justification
- **Entry Point Analysis**: Specific reasoning why current levels offer good value
- **Risk-Reward Assessment**: Compare current price to key support/resistance levels
- Include reasoning for diversification benefit beyond just sector leadership
- Avoid overextended picks from leading sectors unless at attractive re-entry points
- Consider sector rotation opportunities and value plays in emerging sectors

### Step 6: hold-gialang.md Generation
**Objective**: Generate complete hold-gialang.md using verified fact sheets and final actions

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
* **P&L (Lợi Nhuận/Thua Lỗ Chưa Thực Hiện):** [Calculated P&L]
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

### Step 7: Quality Verification
**Objective**: Ensure hold-gialang.md accuracy and completeness

**CRITICAL BUG PREVENTION**: Verify correct section structure to avoid heading misalignment:
- [ ] **Section 1**: Tóm Tắt Danh Mục Hiện Tại (summary and action table)
- [ ] **Section 2**: Kế Hoạch Giao Dịch Chi Tiết (detailed analysis of CURRENT holdings with charts, P&L, VPA analysis, recommendations, stop-loss, take-profit, alternatives)
- [ ] **Section 3**: Kế Hoạch Gia Tăng Chi Tiết (detailed analysis of NEW diversification picks with same format as Section 2: charts, buy prices, quantities, VPA analysis, stop-loss, take-profit)
- [ ] **Section 4**: Nhật Ký Thay Đổi Kế Hoạch (change log)

**STRUCTURAL VERIFICATION**:
- [ ] Section 2 contains individual ### ticker analyses for ALL current holdings
- [ ] Section 3 contains individual ### ticker analyses for ALL diversification picks with full detail (not just summary table)
- [ ] Section 3 uses identical format to Section 2: charts, prices, quantities, VPA analysis (including separate Bối Cảnh Tuần and Bối Cảnh Ngày), stop-loss, take-profit
- [ ] No content appears between section headers without proper subsection organization

**Verification Checklist**:
- [ ] All portfolio holdings from previous hold-gialang.md are processed
- [ ] P&L calculations are mathematically correct
- [ ] All assertions cite specific signals and dates from fact sheets
- [ ] Action recommendations follow state transition rules correctly
- [ ] Change log documents every recommendation change with justification
- [ ] Chart links use correct file paths
- [ ] Vietnamese text is grammatically correct
- [ ] Industry classifications match GROUP.md exactly
- [ ] **CRITICAL**: All "Top 3 Cổ Phiếu Thay Thế" alternatives are from the SAME industry group as the holding ticker per GROUP.md

### Step 8: File Output
**Objective**: Generate final hold-gialang.md file

```bash
# Generate new hold-gialang.md (git handles version control)
# [Output complete hold-gialang.md content]
```

## Quality Control Standards

### Data Accuracy Requirements
- **Zero Tolerance**: No assertions without fact sheet verification
- **Price Accuracy**: Current prices must match market_data.txt exactly
- **Date Precision**: All signals must include exact dates
- **P&L Accuracy**: Mathematical calculations must be precise
- **State Tracking**: Previous recommendations must be accurately captured

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
- Ensure decimal formatting uses dots (.), not commas (,)
- Use consistent industry naming from GROUP.md
- **EXAMPLES OF CORRECT USAGE**:
  - Good: "Điểm vào tốt sau điều chỉnh lành mạnh, tỷ lệ rủi ro-lợi nhuận 3:1 thuận lợi"
  - Bad: "Excellent entry point sau healthy pullback, favorable 3:1 risk-reward ratio"
  - Good: "Ngành ngân hàng dẫn dắt chu kỳ phục hồi kinh tế"
  - Bad: "Banking sector leads recovery, momentum breakout"

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
  "weekly_context": {"signal": "", "week_ending_date": "", "weekly_narrative": ""},
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

## Gialang Portfolio Specific Notes

**Current Holdings Overview**:
- Total portfolio: 9 positions including 1 fund (FUEVFVND)
- Sector exposure: Retail (MWG), Food (VNM, MSN), Securities (SSI), Banking (TCB), Steel (NKG), Real Estate (KBC), Fund (FUEVFVND), Other (AGG)
- Portfolio value range: ~400-500k based on holding sizes
- Key positions: SSI (4,200 shares), NKG (4,100 shares), VNM (2,700 shares)

**Special Considerations**:
- FUEVFVND is a fund and requires separate NAV analysis
- AGG may not be tracked in current system - requires status verification
- High concentration in SSI and NKG requires careful risk management
- Strong exposure to leading sectors (Securities, Food, Banking) per LEADER.md