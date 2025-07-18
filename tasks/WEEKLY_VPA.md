# Weekly VPA Analysis Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to perform weekly VPA (Volume Price Analysis) using the Wyckoff methodology. The agent must follow these steps sequentially to ensure accurate, contextual analysis.

## Important Weekly Date Logic
**CRITICAL**: Weekly data dates are always from Monday of each week. If today is Sunday 2025-07-13, the latest complete weekly data will be dated Monday 2025-07-07 (representing the week of July 7-11, 2025). Always analyze the most recent Monday-dated weekly data available.

## Execution Protocol

### Step 1: Dividend Adjustment Check
**Objective**: Ensure all VPA price references are accurate before analysis

Use LS tool to check for dividend-adjusted tickers:
- Path: market_data_check_dividends_week/
- If directory doesn't exist or is empty: proceed to Step 2

**Actions**:
- If `market_data_check_dividends_week/` directory exists and contains files:
  - Follow the dividend processing protocol in `tasks/dividends_plan.md`
  - Update all price references in affected VPA files using dividend ratios
  - Delete processed files from `market_data_check_dividends_week/` after completion
- If directory is empty or doesn't exist: proceed to Step 2

**Success Criteria**: All dividend adjustments completed, `market_data_check_dividends_week/` directory is empty

### Step 2: Individual Ticker VPA Analysis
**Objective**: Analyze each ticker using automated preparation and efficient generation

#### 2.1 Ticker Batch Preparation
**Split tickers into 8 batches for parallel processing**:

```bash
uv run utilities/split_tickers.py
```

This script automatically:
- Reads TICKERS.csv and splits into 8 batch files
- Creates utilities/data/batch_1.csv through batch_8.csv
- Each batch contains 14-15 tickers for optimal parallel processing

#### 2.2 Context Gathering (Automated)
**Use Python utility for data preparation**:

```bash
uv run utilities/vpa_analysis_prep_week.py
```

This script automatically:
- Scans all market_data_week CSV files for latest weekly data
- Reads existing VPA analysis from vpa_data_week/ directory
- Identifies tickers needing new analysis
- Extracts context data (current week OHLCV, last 4 weeks OHLCV, latest VPA signal)
- Provides summary of analysis requirements

**Reference**: See `tasks/task_vpa_prep_python_week.md` for detailed usage

#### 2.3 Context Gathering (Internal Processing)
**CRITICAL**: Use LS tool to check market_data_week/ directory and Read tool to examine CSV files directly.
**MANDATORY**: Always read both market_data_week CSV files AND existing vpa_data_week/*.md files to ensure accurate context.

For each ticker with new weekly data, create this internal context structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "new_data_date": "2025-07-07",
  "new_data_ohlcv": {
    "open": 64.4,
    "high": 64.9, 
    "low": 64.1,
    "close": 64.7,
    "volume": 12500000
  },
  "previous_data_ohlcv": {
    "open": 63.8,
    "high": 64.5,
    "low": 63.5, 
    "close": 64.4,
    "volume": 9800000
  },
  "previous_vpa_analysis": {
    "date": "2025-07-06",
    "signal": "No Demand",
    "context": "Previous analysis summary"
  },
  "analysis_mode": "NEW_ENTRY" // or "UPDATE_LAST" if current week exists in last 10 VPA entries
}
```

#### 2.4 Analysis Generation
**Use multiple Task tools for parallel processing**:

Based on the batch files created in Step 2.1, spawn exactly 8 sub-agents to process each batch concurrently.

**PARALLEL PROCESSING RULE**: 
- **ALWAYS launch exactly 8 Task tools concurrently** using a single message with multiple tool calls
- **Each Task tool reads from its assigned batch file** (utilities/data/batch_X.csv)
- **Each batch contains 14-15 tickers** for optimal parallel processing

**Key steps**:
1. Read the task template: `tasks/task_generate_vpa_analysis_week.md`
2. Create exactly 8 Task tool calls simultaneously, each with:
   - Customized prompt with current date and batch file assignment
   - Template from `tasks/task_generate_vpa_analysis_week.md`
   - Instruction to read from utilities/data/batch_X.csv (where X = 1-8)
3. Execute all 8 Task tools concurrently to maximize parallel processing
4. Each task tool will handle format requirements and Vietnamese VPA analysis for its assigned batch

**Reference**: See `tasks/task_generate_vpa_analysis_week.md` for:
- Complete task prompt template
- Vietnamese VPA format requirements
- Wyckoff methodology guidelines
- Number formatting rules (DOT separator)
- Common VPA signals reference

#### 2.5 Analysis Generation (Manual Mode)
**CRITICAL**: Only append new date entries - NEVER overwrite existing VPA analysis unless dividends require price adjustments

**Format Requirements**: Follow exact Vietnamese VPA format

```markdown
- **Ngày YYYY-MM-DD:** [Analysis of price movement from previous to current week]. [Description of weekly candle characteristics]. [Volume analysis compared to previous week].
    - **Phân tích VPA/Wyckoff:** [Wyckoff interpretation: No Demand, Effort to Rise, Sign of Strength, etc.]. [Contextual explanation building on previous analysis].
```

**Analysis Requirements**:
- **Contextual Continuity**: Must reference previous VPA signal from most recent existing entry
- **Comparative Analysis**: Explicitly compare new weekly bar to previous weekly bar (price, spread, volume)  
- **Wyckoff Methodology**: Apply proper VPA signals (No Demand, Effort to Rise, Sign of Strength, etc.)
- **Vietnamese Language**: Maintain natural Vietnamese financial terminology
- **Number Formatting**: ALWAYS use DOT (.) as decimal separator, NEVER comma (,)
- **Date Check**: Only generate analysis if new week doesn't already exist in VPA files
- **Weekly Perspective**: Focus on weekly trends and patterns, not intraday movements

**Example New Entry**:
```markdown
- **Ngày 2025-07-07:** Tiếp nối tín hiệu **No Demand** của tuần trước, tuần này SIP tăng từ 64.4 lên 64.7. Nến tuần tăng có biên độ hẹp. Khối lượng giao dịch tăng nhẹ (12.5 triệu đơn vị).
    - **Phân tích VPA/Wyckoff:** Đây là một tín hiệu **Effort to Rise**, phủ nhận tín hiệu yếu kém tuần trước. Lực cầu đã quay trở lại, cho thấy tiềm năng phục hồi trong xu hướng tuần.
```

**IMPORTANT NUMBER FORMATTING RULE**:
- **Always use DOT (.) as decimal separator** in all price and volume references
- **NEVER use comma (,) as decimal separator** 
- Examples: 64.4, 12.5, 123.45 (CORRECT)
- Examples: 64,4, 12,5, 123,45 (INCORRECT)

#### 2.6 File Output Processing
**Automatic handling by Task tool**:
- Task tool automatically appends new date entries to existing `vpa_data_week/{TICKER}.md` files
- Preserves all existing historical analysis
- Ensures proper UTF-8 encoding for Vietnamese text
- Skips tickers that already have current week's analysis

#### 2.7 File Output Processing (Manual Mode)
**APPEND-ONLY MODE** (Default - unless dividends processed):
- **MANDATORY**: Use Read tool to examine existing `vpa_data_week/{TICKER}.md` files to get current analysis 
- **MANDATORY**: Use LS tool to check if vpa_data_week/ directory exists, create it if needed
- Check if target week already exists in analysis
- If week exists: Skip ticker (no action needed)
- If week missing: Append new week entry to existing content
- Preserve all existing historical analysis
- Ensure proper UTF-8 encoding for Vietnamese text

**DIVIDEND ADJUSTMENT MODE** (Only when dividend files processed):
- Update all historical price references using dividend ratios
- Maintain analysis logic but adjust numerical values
- Preserve analysis structure and dates

### Step 3: VPA Verification
**Objective**: Validate analysis accuracy and consistency

```bash
uv run utilities/verify_vpa_week.py
```
**Note**: Use Bash tool to run this command

**What verify_vpa_week.py should check**:
- Logical VPA signal progression (e.g., "Test for Supply" after "Effort to Rise")
- Price data consistency with market_data_week CSV files
- Vietnamese language grammar and financial terminology
- Proper markdown formatting and structure
- Date continuity and chronological order
- Weekly timeframe appropriateness

**Expected Output**: List of problematic tickers with specific issues identified

### Step 4: Fix Problematic Analysis
**Objective**: Address all issues identified in verification

**Process**:
1. Review each flagged ticker from verify_vpa_week.py output
2. Re-analyze using corrected context and logic
3. Update the corresponding `vpa_data_week/{TICKER}.md` file
4. Re-run verification until all issues resolved

**Common Issues to Fix**:
- Illogical VPA signal transitions
- Price mismatches with CSV data
- Vietnamese grammar or terminology errors
- Missing contextual references to previous analysis
- Inappropriate daily vs weekly perspective

### Step 5: Merge Individual Files
**Objective**: Append new week entries from vpa_data_week/ to existing VPA_week.md structure

```bash
uv run merge_vpa.py --week
```
**Note**: Use Bash tool to run this command

**Process**:
- Reads all files from `vpa_data_week/` directory (contains only new week entries)
- Reads existing `VPA_week.md` to preserve historical analysis
- For each ticker: Appends new week entries to existing ticker section in VPA_week.md
- If ticker doesn't exist in VPA_week.md: Creates new ticker section
- Maintains alphabetical ticker ordering
- Preserves all existing historical analysis
- Backs up market_data_week to market_data_week_processed

### Step 6: Generate Final Report
**Objective**: Create comprehensive weekly market report with integrated VPA

```bash
uv run main.py --week
```
**Note**: Use Bash tool to run this command

**Process**:
- Integrates VPA analysis from `VPA_week.md` into weekly market report
- Generates weekly candlestick charts for all tickers
- Creates `REPORT_week.md` with comprehensive weekly market analysis
- Links VPA signals to weekly technical chart patterns

### Step 7: Summary Documentation
**Objective**: Document the analysis session for review

Create `tasks/report_vpa_week.md` with:

```markdown
# Weekly VPA Analysis Report - [DATE]

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
- [Notable weekly pattern changes]
- [Sector rotation observations]
- [Weekly volume anomalies]

## Issues Resolved
- [Description of verification issues and fixes]
- [Dividend adjustments made]

## Recommendations for Next Session
- [Tickers requiring close monitoring]
- [Potential weekly setup developments]
```

## Quality Control Checklist

Before completing the weekly VPA analysis, verify:

- [ ] All dividend adjustments processed and `market_data_check_dividends_week/` is empty
- [ ] Each ticker has logical VPA signal progression from previous weekly analysis
- [ ] Vietnamese text is grammatically correct and uses proper financial terminology
- [ ] All price references match market_data_week CSV files exactly
- [ ] VPA_week.md file is properly formatted with headers and separators
- [ ] REPORT_week.md successfully generated with integrated VPA analysis
- [ ] Summary report documents all analysis activities

## Error Handling

**If dividend processing fails**:
- Document the issue in summary report
- Continue with analysis using existing price data
- Flag affected tickers for manual review

**If verification fails**:
- Re-analyze problematic tickers with enhanced context
- Check for data inconsistencies in market_data_week
- Ensure proper Wyckoff methodology application

**If merge fails**:
- Check vpa_data_week directory permissions and file formats
- Verify all ticker files have proper UTF-8 encoding
- Ensure merge process is appending, not overwriting existing VPA_week.md content
- Manually append new entries if automated merge fails

## Success Metrics

- **Accuracy**: All VPA signals follow logical Wyckoff progression
- **Completeness**: Every ticker with new weekly data has updated analysis
- **Consistency**: Vietnamese terminology and formatting maintained
- **Integration**: Final report successfully incorporates all VPA analysis
- **Documentation**: Complete summary report generated

## Weekly Analysis Specific Notes

- **Timeframe Focus**: Analysis should focus on weekly trends, not daily noise
- **Volume Context**: Weekly volume should be compared to previous weeks, not daily averages
- **Signal Persistence**: Weekly signals carry more weight and should show clear trend changes
- **Pattern Recognition**: Look for weekly chart patterns like higher highs, higher lows, etc.
- **Market Context**: Consider broader market weekly trends when analyzing individual stocks