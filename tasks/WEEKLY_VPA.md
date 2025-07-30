# Weekly VPA Analysis Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to perform weekly VPA (Volume Price Analysis) using the Wyckoff methodology with **manual natural language analysis only**. No unreliable Python text parsing utilities.

**⚠️ CRITICAL: ALWAYS USE ACTUAL DATA DATES**
- Never assume "today's date" or "this week" for analysis
- Always get the actual last available date from CSV files using `df.iloc[-1]["Date"]`
- Use `glob.glob()` to find the most recent CSV file for each ticker
- Compare actual data dates with existing analysis dates to determine if new analysis is needed

## Important Weekly Date Logic
**CRITICAL**: Weekly data dates are always from Monday of each week. Always analyze the most recent Monday-dated weekly data available by checking the actual last row of the CSV file, not assumed dates.

## Execution Protocol

### Step 1: Dividend Adjustment Check
**Objective**: Ensure all VPA price references are accurate before analysis

**Use LS tool to check for dividend-adjusted tickers:**
- Path: market_data_check_dividends_week/
- If directory doesn't exist or is empty: proceed to Step 2

**Manual Dividend Processing Actions**:
- If `market_data_check_dividends_week/` directory exists and contains files:
  - **MANUAL PROCESSING ONLY** - Follow the dividend processing protocol in `tasks/dividends_plan.md`
  - **Use reliable Python only for CSV operations** to read dividend ratios
  - **Manual price adjustment** using Read/Edit tools for affected VPA files
  - Delete processed files from `market_data_check_dividends_week/` after completion
- If directory is empty or doesn't exist: proceed to Step 2

**Success Criteria**: All dividend adjustments completed manually, `market_data_check_dividends_week/` directory is empty

### Step 2: Individual Ticker VPA Analysis
**Objective**: Analyze each ticker using manual natural language analysis with reliable Python support only

#### 2.1 Ticker Batch Preparation ✅ RELIABLE
**Split tickers into 8 batches for parallel processing**:

```bash
uv run utilities/split_tickers.py
```

This script is reliable (pure CSV operations):
- Reads TICKERS.csv and splits into 8 batch files using standard csv module
- Creates utilities/data/batch_1.csv through batch_8.csv
- Each batch contains 14-15 tickers for optimal parallel processing
- **NO text parsing** - only CSV reading/writing

#### 2.2 Manual Context Gathering - NO AUTOMATED UTILITIES
**MANUAL APPROACH ONLY - NO AUTOMATED TEXT PARSING**:

**❌ REMOVED**: `vpa_analysis_prep_week.py` - unreliable text parsing utility

**For each ticker, manually gather context using**:
1. **Read latest weekly market data CSV** using reliable Python:
```bash
# Example reliable Python for weekly price data - gets most recent CSV file
uv run -c "
import pandas as pd
import glob
ticker = 'VHM'
try:
    # Find the most recent weekly CSV file for this ticker
    csv_files = glob.glob(f'market_data_week/{ticker}_*.csv')
    if not csv_files:
        print(f'No weekly CSV files found for {ticker}')
    else:
        # Get the most recent file by modification time or filename
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        latest = df.iloc[-1]  # Last row = most recent week
        previous = df.iloc[-2] if len(df) > 1 else df.iloc[-1]
        print(f'{ticker}: Latest week ending {latest[\"Date\"]}, Close={latest[\"Close\"]}, Volume={latest[\"Volume\"]}')
        print(f'Previous week ending {previous[\"Date\"]}, Close={previous[\"Close\"]}, Volume={previous[\"Volume\"]}')
        print(f'CSV file: {latest_file}')
        print(f'Weekly data available: {len(df)} weeks')
        print(f'Weekly data range: {df.iloc[0][\"Date\"]} to {df.iloc[-1][\"Date\"]}')
except Exception as e:
    print(f'Could not read CSV for {ticker}: {e}')
"
```

2. **Read existing VPA analysis manually** using Read tool:
   - Read `vpa_data_week/{TICKER}.md` to understand previous weekly analysis context
   - Manually identify latest VPA signal from previous entries
   - Understand historical weekly pattern progression

3. **Manual assessment of new analysis needs**:
   - Compare the actual last available week ending date from CSV (df.iloc[-1]["Date"]) with last VPA analysis date
   - Determine if new analysis is required based on actual weekly data availability (not assumed dates)
   - NO automated text parsing or signal extraction

**Context Sources (Manual Reading Only)**:
- **Market data**: Use reliable Python CSV operations only
- **Previous VPA**: Manual reading with Read tool
- **Signal identification**: Human intelligence, no automation

#### 2.3 Manual Context Gathering (Internal Processing)
**MANUAL APPROACH**: Use LS tool to check market_data_week/ directory and Read tool to examine CSV files directly.
**MANDATORY**: Always manually read both market_data_week CSV files AND existing vpa_data_week/*.md files to ensure accurate context.

For each ticker with new weekly data, manually create this internal context structure:

```json
{
  "ticker": "TICKER_SYMBOL",
  "new_data_date": "2025-07-07 - manually verified",
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
    "signal": "No Demand - manually identified",
    "context": "Previous analysis summary - manually extracted"
  },
  "analysis_mode": "NEW_ENTRY or UPDATE_LAST - manually determined"
}
```

**Manual Data Sources**:
- **Weekly OHLCV data**: Using reliable Python CSV operations
- **Previous VPA analysis**: Manual reading using Read tool
- **Signal identification**: Human intelligence only
- **Analysis mode determination**: Manual assessment of existing entries

#### 2.4 Manual VPA Analysis Generation
**Use multiple Task tools for parallel processing with manual guidance**:

Based on the batch files created in Step 2.1, spawn exactly 8 sub-agents to process each batch concurrently using **manual natural language analysis**.

**PARALLEL PROCESSING RULE**: 
- **ALWAYS launch exactly 8 Task tools concurrently** using a single message with multiple tool calls
- **Each Task tool reads from its assigned batch file** (utilities/data/batch_X.csv) using reliable CSV operations
- **Each batch contains 14-15 tickers** for optimal parallel processing
- **All Task tool calls use MANUAL ANALYSIS ONLY** - no automated text parsing
- **Each Task tool applies Wyckoff methodology manually** with human intelligence

**Key steps**:
1. Read the task template: `tasks/task_generate_vpa_analysis_week.md`
2. Create exactly 8 Task tool calls simultaneously, each with:
   - **Manual analysis instructions** emphasizing natural language understanding
   - **Vietnamese VPA terminology requirements** (no English terms)
   - **Reliable Python guidance** for CSV operations only
   - Instruction to read from utilities/data/batch_X.csv (where X = 1-8)
   - **Manual context gathering** from existing vpa_data_week files
3. Execute all 8 Task tools concurrently with manual analysis approach
4. Each task tool applies Wyckoff methodology manually without automated signal detection

**Reference**: See `tasks/task_generate_vpa_analysis_week.md` for:
- **Manual analysis methodology** (updated to remove automation)
- **Vietnamese VPA format requirements** (proper financial terminology)
- **Wyckoff methodology guidelines** (manual application)
- **Number formatting rules** (DOT separator)
- **Common VPA signals reference** (for manual identification)

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
- If week missing: **Use Write tool to append** new week entry to existing content
- Preserve all existing historical analysis
- Ensure proper UTF-8 encoding for Vietnamese text
- **NEVER use echo or bash append commands** - always use Write tool

**DIVIDEND ADJUSTMENT MODE** (Only when dividend files processed):
- Update all historical price references using dividend ratios
- Maintain analysis logic but adjust numerical values
- Preserve analysis structure and dates

### Step 3: Manual VPA Verification
**Objective**: Validate analysis accuracy and consistency through manual review

**❌ NO AUTOMATED VERIFICATION UTILITIES** - Manual verification only

**Manual Verification Process**:
1. **Sample-based manual review** of generated weekly VPA analysis
2. **Use Read tool** to check key tickers from each batch
3. **Manual validation checklist** applied to each reviewed ticker
4. **Human intelligence** to assess logical progression

**Manual Verification Checklist**:
- **Logical VPA signal progression** (e.g., "Kiểm tra nguồn cung" after "Nỗ lực tăng giá") - weekly timeframe appropriate
- **Price data consistency** - manually compare with market_data_week CSV using reliable Python
- **Vietnamese language** grammar and proper financial terminology
- **Proper markdown formatting** and structure
- **Date continuity** and chronological order
- **Weekly timeframe appropriateness** - focus on weekly trends, not daily noise
- **Wyckoff methodology** correctly applied manually

**Manual Price Verification Example**:
```bash
# Use reliable Python to verify weekly price consistency with actual latest data
uv run -c "
import pandas as pd
import glob
ticker = 'VHM'
try:
    # Get the most recent weekly CSV file for this ticker
    csv_files = glob.glob(f'market_data_week/{ticker}_*.csv')
    latest_file = max(csv_files) if csv_files else None
    if latest_file:
        df = pd.read_csv(latest_file)
        latest = df.iloc[-1]  # Last row = most recent week
        print(f'Weekly data for {ticker}: Week ending {latest[\"Date\"]} Close={latest[\"Close\"]}')
        print(f'Using file: {latest_file}')
        print('Now manually compare with VPA analysis using Read tool')
    else:
        print(f'No weekly CSV files found for {ticker}')
except Exception as e:
    print(f'Error reading weekly data for {ticker}: {e}')
"
```

**Expected Output**: Manual assessment notes of problematic tickers with specific issues identified

### Step 4: Manual Fix of Problematic Analysis
**Objective**: Address all issues identified in manual verification

**Manual Fix Process**:
1. **Review each flagged ticker** from manual verification notes
2. **Re-analyze manually** using corrected context and logic with human intelligence
3. **Use Edit tool** to update the corresponding `vpa_data_week/{TICKER}.md` file
4. **Re-verify manually** until all issues resolved through human assessment

**Common Issues to Fix Manually**:
- **Illogical VPA signal transitions** - apply weekly Wyckoff methodology correctly by hand
- **Price mismatches with CSV data** - verify using reliable Python and correct manually
- **Vietnamese grammar or terminology errors** - fix language manually
- **Missing contextual references** to previous analysis - read historical context and add manually
- **Inappropriate daily vs weekly perspective** - ensure weekly timeframe focus manually
- **Format inconsistencies** - ensure proper Vietnamese VPA format manually

### Step 5: Manual Merge of Individual Files ✅ RELIABLE UTILITY AVAILABLE
**Objective**: Append new week entries from vpa_data_week/ to existing VPA_week.md structure

```bash
uv run merge_vpa.py --week
```

**This utility is reliable** because:
- **Merge operation** is structural file manipulation, not text parsing
- **File concatenation** using standard file operations
- **No complex text analysis** or signal interpretation required
- **Simple append logic** that doesn't require understanding VPA content

**Process**:
- Reads all files from `vpa_data_week/` directory (contains only new week entries)
- Reads existing `VPA_week.md` to preserve historical analysis
- For each ticker: Appends new week entries to existing ticker section in VPA_week.md
- If ticker doesn't exist in VPA_week.md: Creates new ticker section
- Maintains alphabetical ticker ordering
- Preserves all existing historical analysis
- Backs up market_data_week to market_data_week_processed

**Alternative Manual Approach** (if merge_vpa.py unavailable):
- **Use Read/Edit tools** to manually append new analysis to VPA_week.md
- **Read vpa_data_week files** individually and manually copy to VPA_week.md
- **Preserve formatting** and structure manually

### Step 6: Generate Final Report ✅ RELIABLE UTILITY AVAILABLE
**Objective**: Create comprehensive weekly market report with integrated VPA

```bash
uv run main.py --week
```

**This utility is reliable** because:
- **Chart generation** using standard plotting libraries
- **Report generation** using template-based approach
- **VPA integration** through file reading, not text parsing
- **Standard data processing** without complex text analysis

**Process**:
- Integrates VPA analysis from `VPA_week.md` into weekly market report
- Generates weekly candlestick charts for all tickers
- Creates `REPORT_week.md` with comprehensive weekly market analysis
- Links VPA signals to weekly technical chart patterns

### Step 7: Manual Summary Documentation
**Objective**: Document the analysis session for review using manual assessment

**Use Write tool to create** `tasks/report_vpa_week.md` with manual analysis summary:

```markdown
# Weekly VPA Analysis Report - [DATE]

## Summary (Manual Count)
- **Tickers Analyzed**: [NUMBER - counted manually]
- **New Entries**: [NUMBER - manually verified] 
- **Updated Entries**: [NUMBER - manually tracked]
- **Dividend Adjustments**: [NUMBER - manually processed]

## VPA Signal Distribution (Manual Classification)
- **Tín hiệu Sức mạnh (Sign of Strength)**: [LIST OF TICKERS - manually identified]
- **Tín hiệu Yếu (Sign of Weakness)**: [LIST OF TICKERS - manually identified] 
- **Không có nhu cầu (No Demand)**: [LIST OF TICKERS - manually identified]
- **Nỗ lực tăng giá (Effort to Rise)**: [LIST OF TICKERS - manually identified]
- **Kiểm tra nguồn cung (Test for Supply)**: [LIST OF TICKERS - manually identified]

## Key Market Observations (Manual Analysis)
- [Notable weekly pattern changes - manually observed]
- [Sector rotation observations - manually analyzed]
- [Weekly volume anomalies - manually detected]

## Issues Resolved (Manual Fixes)
- [Description of manual verification issues and fixes]
- [Manual dividend adjustments made]
- [Manual corrections applied]

## Recommendations for Next Session (Manual Assessment)
- [Tickers requiring close monitoring - manually identified]
- [Potential weekly setup developments - manually assessed]
- [Areas requiring manual attention]
```

**Vietnamese Terminology Requirements**:
- Use proper Vietnamese financial terms throughout
- NO English VPA terminology in the report
- Manual verification of all Vietnamese language accuracy

## Manual Quality Control Checklist

Before completing the weekly VPA analysis, manually verify:

- [ ] All dividend adjustments processed manually and `market_data_check_dividends_week/` is empty
- [ ] Each ticker has logical VPA signal progression from previous weekly analysis (manually verified)
- [ ] Vietnamese text is grammatically correct and uses proper financial terminology (manually checked)
- [ ] All price references match market_data_week CSV files exactly (verified using reliable Python)
- [ ] VPA_week.md file is properly formatted with headers and separators (manually inspected)
- [ ] REPORT_week.md successfully generated with integrated VPA analysis (manually confirmed)
- [ ] Summary report documents all analysis activities (manually compiled)
- [ ] NO English VPA terminology used anywhere (manually verified)
- [ ] All Vietnamese VPA terms are accurate (manually validated)
- [ ] Weekly timeframe focus maintained throughout analysis (manually checked)

## Error Handling (Manual Approach)

**If dividend processing fails**:
- Document the issue in manual summary report
- Continue with analysis using existing price data
- Flag affected tickers for manual review
- **NO automated recovery** - handle manually

**If manual verification fails**:
- Re-analyze problematic tickers manually with enhanced context
- Check for data inconsistencies in market_data_week using reliable Python
- Ensure proper Wyckoff methodology application through human intelligence
- **NO automated re-verification** - assess manually

**If merge fails**:
- Check vpa_data_week directory permissions and file formats manually
- Verify all ticker files have proper UTF-8 encoding manually
- Ensure merge process is appending, not overwriting existing VPA_week.md content
- **Manual fallback**: Use Read/Edit tools to manually append new entries

## Success Metrics (Manual Assessment)

- **Accuracy**: All VPA signals follow logical Wyckoff progression (manually verified)
- **Completeness**: Every ticker with new weekly data has updated analysis (manually counted)
- **Consistency**: Vietnamese terminology and formatting maintained (manually checked)
- **Integration**: Final report successfully incorporates all VPA analysis (manually confirmed)
- **Documentation**: Complete manual summary report generated
- **Language Quality**: Proper Vietnamese financial terminology throughout (manually validated)
- **No Automation Dependencies**: All analysis done through manual natural language understanding

## Weekly Analysis Specific Notes

- **Timeframe Focus**: Analysis should focus on weekly trends, not daily noise
- **Volume Context**: Weekly volume should be compared to previous weeks, not daily averages
- **Signal Persistence**: Weekly signals carry more weight and should show clear trend changes
- **Pattern Recognition**: Look for weekly chart patterns like higher highs, higher lows, etc.
- **Market Context**: Consider broader market weekly trends when analyzing individual stocks