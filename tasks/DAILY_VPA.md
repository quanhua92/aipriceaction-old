# Daily VPA Analysis Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to perform daily VPA (Volume Price Analysis) using the Wyckoff methodology. The agent must follow these steps sequentially to ensure accurate, contextual analysis.

## Execution Protocol

### Step 1: Dividend Adjustment Check
**Objective**: Ensure all VPA price references are accurate before analysis

**Use LS tool to check for dividend-adjusted tickers:**
- Path: `market_data_check_dividends/`
- If directory doesn't exist or is empty: proceed to Step 2

**Actions**:
- If `market_data_check_dividends/` directory exists and contains files:
  - Follow the dividend processing protocol in `tasks/dividends_plan.md`
  - Update all price references in affected VPA files using dividend ratios
  - Delete processed files from `market_data_check_dividends/` after completion
  - **CRITICAL**: Must complete ALL dividend processing before continuing to Step 2
- If directory is empty or doesn't exist: proceed to Step 2

**Success Criteria**: All dividend adjustments completed, `market_data_check_dividends/` directory is empty

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
uv run utilities/vpa_analysis_prep.py
```

This script automatically:
- Scans all market_data CSV files for today's data
- Reads existing VPA analysis from vpa_data/ directory
- Identifies tickers needing new analysis
- Extracts context data (today's OHLCV, last 7 days OHLCV, latest VPA signal)
- Provides summary of analysis requirements

**Reference**: See `tasks/task_vpa_prep_python.md` for detailed usage

#### 2.3 Analysis Generation
**Use multiple Task tools for parallel processing**:

Based on the batch files created in Step 2.1, spawn exactly 8 sub-agents to process each batch concurrently.

**PARALLEL PROCESSING RULE**: 
- **ALWAYS launch exactly 8 Task tools concurrently** using a single message with multiple tool calls
- **Each Task tool reads from its assigned batch file** (utilities/data/batch_X.csv)
- **Each batch contains 14-15 tickers** for optimal parallel processing
- **All Task tool calls are non-interactive** and run automatically without confirmation

**Key steps**:
1. Read the task template: `tasks/task_generate_vpa_analysis.md`
2. Create exactly 8 Task tool calls simultaneously, each with:
   - Customized prompt with current date and batch file assignment
   - Template from `tasks/task_generate_vpa_analysis.md`
   - Instruction to read from utilities/data/batch_X.csv (where X = 1-8)
3. Execute all 8 Task tools concurrently to maximize parallel processing
4. Each task tool will handle format requirements and Vietnamese VPA analysis for its assigned batch

**Reference**: See `tasks/task_generate_vpa_analysis.md` for:
- Complete task prompt template
- Vietnamese VPA format requirements
- Wyckoff methodology guidelines
- Number formatting rules (DOT separator)
- Common VPA signals reference

#### 2.3 File Output Processing
**Automatic handling by Task tool**:
- Task tool automatically appends new date entries to existing `vpa_data/{TICKER}.md` files
- Preserves all existing historical analysis
- Ensures proper UTF-8 encoding for Vietnamese text
- Skips tickers that already have today's analysis

**DIVIDEND ADJUSTMENT MODE** (Only when dividend files processed):
- Update all historical price references using dividend ratios
- Maintain analysis logic but adjust numerical values
- Preserve analysis structure and dates

### Step 3: VPA Verification
**Objective**: Validate analysis accuracy and consistency

```bash
uv run utilities/verify_vpa.py
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
**Objective**: Append new date entries from vpa_data/ to existing VPA.md structure

```bash
uv run merge_vpa.py
```

**Process**:
- Reads all files from `vpa_data/` directory (contains only new date entries)
- Reads existing `VPA.md` to preserve historical analysis
- For each ticker: Appends new date entries to existing ticker section in VPA.md
- If ticker doesn't exist in VPA.md: Creates new ticker section
- Maintains alphabetical ticker ordering
- Preserves all existing historical analysis
- Backs up market_data to market_data_processed

### Step 6: Summary Documentation
**Objective**: Document the analysis session for review

**Use Write tool to create** `tasks/report_vpa.md` with:

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
- [ ] VPA analysis completed and merged successfully
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
- Ensure merge process is appending, not overwriting existing VPA.md content
- Manually append new entries if automated merge fails

## Success Metrics

- **Accuracy**: All VPA signals follow logical Wyckoff progression
- **Completeness**: Every ticker with new data has updated analysis
- **Consistency**: Vietnamese terminology and formatting maintained
- **Integration**: Final report successfully incorporates all VPA analysis
- **Documentation**: Complete summary report generated