# Daily Portfolio Management Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to generate a high-quality `hold.md` file using the Portfolio-Strategist methodology. The agent must follow these steps sequentially to provide actionable portfolio management recommendations based on VPA analysis.

## Execution Protocol

### Step 1: Input File Verification
**Objective**: Ensure all required source files are available and current

```bash
# Check for required input files
ls hold.md REPORT.md REPORT_week.md LEADER.md GROUP.md PLAN.md
ls vpa_data/ market_data/
```

**Actions**:
- Verify existing `hold.md` contains portfolio data table ("Dữ Liệu Danh Mục")
- Verify `REPORT.md` exists with recent daily signals and prices
- Verify `vpa_data/` directory exists with individual ticker daily VPA files
- Verify `market_data/` directory exists with individual ticker CSV files
- Verify `REPORT_week.md` exists with weekly analysis
- Verify `LEADER.md` exists with industry context analysis
- Verify `GROUP.md` exists with ticker-to-industry mappings
- Verify `PLAN.md` exists with overall market context (VNINDEX analysis)

**Success Criteria**: All core input files are present and accessible

### Step 2: Previous Portfolio State Analysis
**Objective**: Extract current holdings and previous recommendations

**Actions**:
- Read existing `hold.md` "Dữ Liệu Danh Mục" table to identify:
  - All held tickers with average buy prices
  - Quantity of shares held for each ticker
  - Previous recommendation for each ticker from "Hành Động Đề Xuất" sections

**Output**: Portfolio state mapping for Stage 0 processing

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
    "week_ending_date": "YYYY-MM-DD"
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
4. Map industry using `GROUP.md` and get status from `LEADER.md`
5. Extract VNINDEX context from `PLAN.md`

**Data Extraction Rules**:
- Extract holding data ONLY from existing `hold.md` portfolio table
- Extract current prices from individual `market_data/{TICKER}_*.csv` files (most recent closing price)
- Extract daily signals ONLY from `REPORT.md` with exact dates
- Extract weekly signals ONLY from `REPORT_week.md` with week ending dates
- Extract VPA narrative context from individual `vpa_data/{TICKER}.md` files
- Map industries using exact matches from `GROUP.md`
- Get industry status from `LEADER.md` analysis
- Extract market context from `PLAN.md` VNINDEX analysis

**Parallel Processing Strategy**:
- Use Task tool to process multiple portfolio tickers concurrently
- Read only relevant ticker files for each holding (vpa_data/{TICKER}.md, market_data/{TICKER}_*.csv)
- Avoid reading large consolidated files for better performance and context focus

**Quality Control**: These fact sheets become the SOLE source of truth for all subsequent stages

**Example Task Tool Usage for Portfolio**:
```
Task 1: "Process portfolio tickers TCB,VND from hold.md holdings table. For each: 1) Read vpa_data/{TICKER}.md last 10 entries 2) Read market_data/{TICKER}_*.csv current price 3) Extract signals from REPORT.md/REPORT_week.md 4) Map industry from GROUP.md 5) Get status from LEADER.md 6) Return complete fact sheet JSON"
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

### Step 6: hold.md Generation
**Objective**: Generate complete hold.md using verified fact sheets and final actions

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
* **VPA Phân Tích Hiện Tại:** [Synthesis from fact sheet - weekly context, daily signals, narrative, industry status]
* **Hành Động Đề Xuất:** [Final decision from Stage 1]
  * **Giá Đề Xuất:** [Specific price range if buy/sell action]
  * **Số Lượng Đề Xuất:** [Specific quantity or ratio if buy/sell action]
  * **Lý Do Hành Động:** [VPA logic explaining the decision]
* **Điểm Dừng Lỗ:** [Specific stop-loss level]
* **Điểm Chốt Lời:** [Specific take-profit level(s)]
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
**Objective**: Ensure hold.md accuracy and completeness

**Verification Checklist**:
- [ ] All portfolio holdings from previous hold.md are processed
- [ ] P&L calculations are mathematically correct
- [ ] All assertions cite specific signals and dates from fact sheets
- [ ] Action recommendations follow state transition rules correctly
- [ ] Change log documents every recommendation change with justification
- [ ] Chart links use correct file paths
- [ ] Vietnamese text is grammatically correct
- [ ] Industry classifications match GROUP.md

### Step 8: File Output
**Objective**: Generate final hold.md file

```bash
# Generate new hold.md (git handles version control)
# [Output complete hold.md content]
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
- Use proper financial terminology
- Maintain professional tone and grammar
- Ensure decimal formatting uses dots (.), not commas (,)
- Use consistent industry naming from GROUP.md

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

- **Position Sizing**: Consider portfolio balance when recommending quantity changes
- **Stop-Loss Placement**: Use technical levels, not arbitrary percentages
- **Take-Profit Strategy**: Consider partial profit-taking at multiple levels
- **Market Context**: Factor in overall VNINDEX trend for individual decisions