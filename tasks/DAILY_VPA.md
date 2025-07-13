# Daily VPA Analysis Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to perform daily VPA (Volume Price Analysis) using the Wyckoff methodology. The agent must follow these steps sequentially to ensure accurate, contextual analysis.

## Execution Protocol

### Step 1: Dividend Adjustment Check
**Objective**: Ensure all VPA price references are accurate before analysis

```bash
# Check for dividend-adjusted tickers
ls market_data_check_dividends/
```

**Actions**:
- If `market_data_check_dividends/` directory exists and contains files:
  - Follow the dividend processing protocol in `tasks/dividends_plan.md`
  - Update all price references in affected VPA files using dividend ratios
  - Delete processed files from `market_data_check_dividends/` after completion
- If directory is empty or doesn't exist: proceed to Step 2

**Success Criteria**: All dividend adjustments completed, `market_data_check_dividends/` directory is empty

### Step 2: Individual Ticker VPA Analysis
**Objective**: Analyze each ticker using parallel agents for efficiency

#### 2.1 Context Gathering (Internal Processing)
For each ticker with new data, create this internal context structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "new_data_date": "2025-07-13",
  "new_data_ohlcv": {
    "open": 64.4,
    "high": 64.9, 
    "low": 64.1,
    "close": 64.7,
    "volume": 1250000
  },
  "previous_data_ohlcv": {
    "open": 63.8,
    "high": 64.5,
    "low": 63.5, 
    "close": 64.4,
    "volume": 980000
  },
  "previous_vpa_analysis": {
    "date": "2025-07-12",
    "signal": "No Demand",
    "context": "Previous analysis summary"
  },
  "analysis_mode": "NEW_ENTRY" // or "UPDATE_LAST" if today exists in last 10 VPA entries
}
```

#### 2.2 Analysis Generation
**Format Requirements**: Follow exact Vietnamese VPA format

```markdown
# TICKER

- **Ngày YYYY-MM-DD:** [Analysis of price movement from previous to current day]. [Description of candle characteristics]. [Volume analysis compared to previous day].
    - **Phân tích VPA/Wyckoff:** [Wyckoff interpretation: No Demand, Effort to Rise, Sign of Strength, etc.]. [Contextual explanation building on previous analysis].
```

**Analysis Requirements**:
- **Contextual Continuity**: Must reference previous VPA signal and build logical progression
- **Comparative Analysis**: Explicitly compare new bar to previous bar (price, spread, volume)
- **Wyckoff Methodology**: Apply proper VPA signals (No Demand, Effort to Rise, Sign of Strength, etc.)
- **Vietnamese Language**: Maintain natural Vietnamese financial terminology

**Example Entry**:
```markdown
# SIP

- **Ngày 2025-07-13:** Tiếp nối tín hiệu **No Demand** của phiên trước, phiên hôm nay SIP tăng từ 64.4 lên 64.7. Nến tăng có biên độ hẹp. Khối lượng giao dịch tăng nhẹ (1.25 triệu đơn vị).
    - **Phân tích VPA/Wyckoff:** Đây là một tín hiệu **Effort to Rise**, phủ nhận tín hiệu yếu kém trước đó. Lực cầu đã quay trở lại, cho thấy tiềm năng phục hồi.
```

#### 2.3 File Output
- Save each ticker analysis to `vpa_data/{TICKER}.md`
- Overwrite existing content (each file contains complete analysis for that ticker)
- Ensure proper UTF-8 encoding for Vietnamese text

### Step 3: VPA Verification
**Objective**: Validate analysis accuracy and consistency

```bash
uv run verify_vpa.py
```

**What verify_vpa.py should check**:
- Logical VPA signal progression (e.g., "Test for Supply" after "Effort to Rise")
- Price data consistency with market_data CSV files
- Vietnamese language grammar and financial terminology
- Proper markdown formatting and structure
- Date continuity and chronological order

**Expected Output**: List of problematic tickers with specific issues identified

### Step 4: Fix Problematic Analysis
**Objective**: Address all issues identified in verification

**Process**:
1. Review each flagged ticker from verify_vpa.py output
2. Re-analyze using corrected context and logic
3. Update the corresponding `vpa_data/{TICKER}.md` file
4. Re-run verification until all issues resolved

**Common Issues to Fix**:
- Illogical VPA signal transitions
- Price mismatches with CSV data
- Vietnamese grammar or terminology errors
- Missing contextual references to previous analysis

### Step 5: Merge Individual Files
**Objective**: Combine all ticker analyses into main VPA file

```bash
uv run merge_vpa.py
```

**Process**:
- Reads all files from `vpa_data/` directory
- Combines into single `VPA.md` file with proper structure
- Maintains alphabetical ticker ordering
- Adds proper headers and separators
- Backs up market_data to market_data_processed

### Step 6: Generate Final Report
**Objective**: Create comprehensive market report with integrated VPA

```bash
uv run main.py
```

**Process**:
- Integrates VPA analysis from `VPA.md` into market report
- Generates candlestick charts for all tickers
- Creates `REPORT.md` with comprehensive market analysis
- Links VPA signals to technical chart patterns

### Step 7: Summary Documentation
**Objective**: Document the analysis session for review

Create `tasks/report_vpa.md` with:

```markdown
# Daily VPA Analysis Report - [DATE]

## Summary
- **Tickers Analyzed**: [NUMBER]
- **New Entries**: [NUMBER] 
- **Updated Entries**: [NUMBER]
- **Dividend Adjustments**: [NUMBER]

## VPA Signal Distribution
- **Sign of Strength**: [LIST OF TICKERS]
- **Sign of Weakness**: [LIST OF TICKERS] 
- **No Demand**: [LIST OF TICKERS]
- **Effort to Rise**: [LIST OF TICKERS]
- **Test for Supply**: [LIST OF TICKERS]

## Key Market Observations
- [Notable pattern changes]
- [Sector rotation observations]
- [Volume anomalies]

## Issues Resolved
- [Description of verification issues and fixes]
- [Dividend adjustments made]

## Recommendations for Next Session
- [Tickers requiring close monitoring]
- [Potential setup developments]
```

## Quality Control Checklist

Before completing the daily VPA analysis, verify:

- [ ] All dividend adjustments processed and `market_data_check_dividends/` is empty
- [ ] Each ticker has logical VPA signal progression from previous analysis
- [ ] Vietnamese text is grammatically correct and uses proper financial terminology
- [ ] All price references match market_data CSV files exactly
- [ ] VPA.md file is properly formatted with headers and separators
- [ ] REPORT.md successfully generated with integrated VPA analysis
- [ ] Summary report documents all analysis activities

## Error Handling

**If dividend processing fails**:
- Document the issue in summary report
- Continue with analysis using existing price data
- Flag affected tickers for manual review

**If verification fails**:
- Re-analyze problematic tickers with enhanced context
- Check for data inconsistencies in market_data
- Ensure proper Wyckoff methodology application

**If merge fails**:
- Check vpa_data directory permissions and file formats
- Verify all ticker files have proper UTF-8 encoding
- Manually combine files if automated merge fails

## Success Metrics

- **Accuracy**: All VPA signals follow logical Wyckoff progression
- **Completeness**: Every ticker with new data has updated analysis
- **Consistency**: Vietnamese terminology and formatting maintained
- **Integration**: Final report successfully incorporates all VPA analysis
- **Documentation**: Complete summary report generated