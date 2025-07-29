# Daily VPA Analysis Task - AI Agent Protocol

## Overview
This document outlines the complete protocol for AI agents to perform daily VPA (Volume Price Analysis) using the Wyckoff methodology with **manual natural language analysis only**. No unreliable Python text parsing utilities.

## Execution Protocol

### Step 1: Dividend Adjustment Check
**Objective**: Ensure all VPA price references are accurate before analysis

**Use LS tool to check for dividend-adjusted tickers:**
- Path: `market_data_check_dividends/`
- If directory doesn't exist or is empty: proceed to Step 2

**Manual Dividend Processing Actions**:
- If `market_data_check_dividends/` directory exists and contains files:
  - **MANUAL PROCESSING ONLY** - Follow the dividend processing protocol in `tasks/dividends_plan.md`
  - **Use reliable Python only for CSV operations** to read dividend ratios
  - **Manual price adjustment** using Read/Edit tools for affected VPA files
  - Delete processed files from `market_data_check_dividends/` after completion
  - **CRITICAL**: Must complete ALL dividend processing before continuing to Step 2
- If directory is empty or doesn't exist: proceed to Step 2

**Success Criteria**: All dividend adjustments completed manually, `market_data_check_dividends/` directory is empty

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

**For each ticker, manually gather context using**:
1. **Read latest market data CSV** using reliable Python:
```bash
# Example reliable Python for price data
uv run -c "
import pandas as pd
ticker = 'VHM'
try:
    df = pd.read_csv(f'market_data/{ticker}_*.csv')
    latest = df.iloc[-1]
    print(f'{ticker}: Close={latest["Close"]}, Volume={latest["Volume"]}')
    print(f'Last 7 days OHLCV data available: {len(df.tail(7))} rows')
except Exception as e:
    print(f'Could not read CSV for {ticker}: {e}')
"
```

2. **Read existing VPA analysis manually** using Read tool:
   - Read `vpa_data/{TICKER}.md` to understand previous analysis context
   - Manually identify latest VPA signal from previous entries
   - Understand historical pattern progression

3. **Manual assessment of new analysis needs**:
   - Compare latest market data date with last VPA analysis date
   - Determine if new analysis is required based on data availability
   - NO automated text parsing or signal extraction

**Context Sources (Manual Reading Only)**:
- **Market data**: Use reliable Python CSV operations only
- **Previous VPA**: Manual reading with Read tool
- **Signal identification**: Human intelligence, no automation

#### 2.3 Manual VPA Analysis Generation
**Use multiple Task tools for parallel processing with manual guidance**:

Based on the batch files created in Step 2.1, spawn exactly 8 sub-agents to process each batch concurrently using **manual natural language analysis**.

**⚠️ CRITICAL PARALLEL PROCESSING RULES**: 
- **ALWAYS launch exactly 8 Task tools concurrently** using a single message with multiple tool calls
- **Each Task tool reads from its assigned batch file** (utilities/data/batch_X.csv) using reliable CSV operations
- **Each batch contains 14-15 tickers** for optimal parallel processing
- **⚠️ MANDATORY: Each Task tool MUST use Write tools ONLY** - no bash/echo commands
- **⚠️ EXPLICIT INSTRUCTION: Tell each subagent to use Read/Write tools** for file operations
- **All Task tool calls use MANUAL ANALYSIS ONLY** - no automated text parsing
- **Each Task tool applies Wyckoff methodology manually** with human intelligence

**⚠️ CRITICAL Task Tool Instructions**:
1. Read the task template: `tasks/task_generate_vpa_analysis.md`
2. Create exactly 8 Task tool calls simultaneously, each with:
   - **⚠️ MANDATORY Write Tool Usage**: "Use ONLY Read/Write tools for file operations. NEVER use bash, echo, or shell commands."
   - **⚠️ File Operation Instruction**: "Use Read tool first to get existing file content, then use Write tool to save updated content."
   - **Manual analysis instructions** emphasizing natural language understanding
   - **Vietnamese VPA terminology requirements** (no English terms)
   - **Reliable Python guidance** for CSV operations only
   - Instruction to read from utilities/data/batch_X.csv (where X = 1-8)
   - **Manual context gathering** from existing vpa_data files
3. Execute all 8 Task tools concurrently with manual analysis approach
4. **⚠️ Each task tool EXPLICITLY instructed** to avoid command line file operations
5. Each task tool applies Wyckoff methodology manually without automated signal detection

**Reference**: See `tasks/task_generate_vpa_analysis.md` for:
- **Manual analysis methodology** (updated to remove automation)
- **Vietnamese VPA format requirements** (proper financial terminology)
- **Wyckoff methodology guidelines** (manual application)
- **Number formatting rules** (DOT separator)
- **Common VPA signals reference** (for manual identification)

#### 2.4 **⚠️ CRITICAL File Output Processing** - USE WRITE TOOLS ONLY
**MANDATORY Write Tool Usage**:
- **⚠️ NEVER use bash, echo, or shell commands** for file operations
- **⚠️ ALWAYS use Write tool** to create/update `vpa_data/{TICKER}.md` files
- **⚠️ ALWAYS use Read tool first** to preserve existing historical analysis
- **⚠️ NO command line file operations** - they require approval prompts

**Correct File Processing Approach**:
```
# CORRECT METHOD:
1. Read: /Volumes/data/workspace/aipriceaction/vpa_data/{TICKER}.md
2. Analyze existing content
3. Write: /Volumes/data/workspace/aipriceaction/vpa_data/{TICKER}.md (with new content appended)

# WRONG METHOD (NEVER DO THIS):
# echo "new content" >> vpa_data/{TICKER}.md  # CREATES APPROVAL PROMPTS
# for file in ...; do echo ...; done          # CREATES APPROVAL PROMPTS
```

**Manual File Update Process**:
- Use **Read tool** to get existing file content
- **Manually append** new VPA analysis to existing content
- Use **Write tool** to save complete updated content
- Ensures proper UTF-8 encoding for Vietnamese text
- **Manual checking** to skip tickers that already have today's analysis

**DIVIDEND ADJUSTMENT MODE** (Only when dividend files processed):
- **Manual update** of historical price references using dividend ratios
- **Preserve analysis logic** while manually adjusting numerical values
- **Maintain analysis structure and dates** through careful editing

### Step 3: Manual VPA Verification
**Objective**: Validate analysis accuracy and consistency through manual review

**❌ NO AUTOMATED VERIFICATION UTILITIES** - Manual verification only

**Manual Verification Process**:
1. **Sample-based manual review** of generated VPA analysis
2. **Use Read tool** to check key tickers from each batch
3. **Manual validation checklist** applied to each reviewed ticker
4. **Human intelligence** to assess logical progression

**Manual Verification Checklist**:
- **Logical VPA signal progression** (e.g., "Kiểm tra nguồn cung" after "Nỗ lực tăng giá")
- **Price data consistency** - manually compare with market_data CSV using reliable Python
- **Vietnamese language** grammar and proper financial terminology
- **Proper markdown formatting** and structure
- **Date continuity** and chronological order
- **Wyckoff methodology** correctly applied manually

**Manual Price Verification Example**:
```bash
# Use reliable Python to verify price consistency
uv run -c "
import pandas as pd
ticker = 'VHM'
df = pd.read_csv(f'market_data/{ticker}_*.csv')
latest = df.iloc[-1]
print(f'Market data for {ticker}: {latest["Date"]} Close={latest["Close"]}')
print('Now manually compare with VPA analysis using Read tool')
"
```

**Expected Output**: Manual assessment notes of problematic tickers with specific issues identified

### Step 4: Manual Fix of Problematic Analysis
**Objective**: Address all issues identified in manual verification

**⚠️ CRITICAL Manual Fix Process**:
1. **Review each flagged ticker** from manual verification notes
2. **Re-analyze manually** using corrected context and logic with human intelligence
3. **⚠️ Use Read tool first** to get existing content from `vpa_data/{TICKER}.md`
4. **⚠️ Use Write tool** to save updated content (NEVER use bash/echo)
5. **Re-verify manually** until all issues resolved through human assessment

**Common Issues to Fix Manually**:
- **Illogical VPA signal transitions** - apply Wyckoff methodology correctly by hand
- **Price mismatches with CSV data** - verify using reliable Python and correct manually
- **Vietnamese grammar or terminology errors** - fix language manually
- **Missing contextual references** to previous analysis - read historical context and add manually
- **Format inconsistencies** - ensure proper Vietnamese VPA format manually

### Step 5: Manual Merge of Individual Files ✅ RELIABLE UTILITY AVAILABLE
**Objective**: Append new date entries from vpa_data/ to existing VPA.md structure

```bash
uv run merge_vpa.py
```

**This utility is reliable** because:
- **Merge operation** is structural file manipulation, not text parsing
- **File concatenation** using standard file operations
- **No complex text analysis** or signal interpretation required
- **Simple append logic** that doesn't require understanding VPA content

**Process**:
- Reads all files from `vpa_data/` directory (contains only new date entries)
- Reads existing `VPA.md` to preserve historical analysis
- For each ticker: Appends new date entries to existing ticker section in VPA.md
- If ticker doesn't exist in VPA.md: Creates new ticker section
- Maintains alphabetical ticker ordering
- Preserves all existing historical analysis
- Backs up market_data to market_data_processed

**⚠️ Alternative Manual Approach** (if merge_vpa.py unavailable):
- **⚠️ Use Read tool** to read existing VPA.md content
- **⚠️ Use Read tool** to read individual vpa_data files
- **⚠️ Use Write tool** to save updated VPA.md (NEVER use bash append operations)
- **Preserve formatting** and structure manually

### Step 6: Manual Summary Documentation
**Objective**: Document the analysis session for review using manual assessment

**Use Write tool to create** `tasks/report_vpa.md` with manual analysis summary:

```markdown
# Daily VPA Analysis Report - [DATE]

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
- [Notable pattern changes - manually observed]
- [Sector rotation observations - manually analyzed]
- [Volume anomalies - manually detected]

## Issues Resolved (Manual Fixes)
- [Description of manual verification issues and fixes]
- [Manual dividend adjustments made]
- [Manual corrections applied]

## Recommendations for Next Session (Manual Assessment)
- [Tickers requiring close monitoring - manually identified]
- [Potential setup developments - manually assessed]
- [Areas requiring manual attention]
```

**Vietnamese Terminology Requirements**:
- Use proper Vietnamese financial terms throughout
- NO English VPA terminology in the report
- Manual verification of all Vietnamese language accuracy

## Manual Quality Control Checklist

Before completing the daily VPA analysis, manually verify:

- [ ] All dividend adjustments processed manually and `market_data_check_dividends/` is empty
- [ ] Each ticker has logical VPA signal progression from previous analysis (manually verified)
- [ ] Vietnamese text is grammatically correct and uses proper financial terminology (manually checked)
- [ ] All price references match market_data CSV files exactly (verified using reliable Python)
- [ ] VPA.md file is properly formatted with headers and separators (manually inspected)
- [ ] VPA analysis completed and merged successfully (manually confirmed)
- [ ] Summary report documents all analysis activities (manually compiled)
- [ ] NO English VPA terminology used anywhere (manually verified)
- [ ] All Vietnamese VPA terms are accurate (manually validated)

## **⚠️ Error Handling** (Manual Approach - Write Tools Only)

**If dividend processing fails**:
- Document the issue in manual summary report
- Continue with analysis using existing price data
- Flag affected tickers for manual review
- **NO automated recovery** - handle manually

**If manual verification fails**:
- Re-analyze problematic tickers manually with enhanced context
- Check for data inconsistencies in market_data using reliable Python
- Ensure proper Wyckoff methodology application through human intelligence
- **NO automated re-verification** - assess manually

**If merge fails**:
- Check vpa_data directory permissions and file formats manually
- Verify all ticker files have proper UTF-8 encoding manually
- Ensure merge process is appending, not overwriting existing VPA.md content
- **⚠️ Manual fallback**: Use Read tool to get existing content, then Write tool to save updated content (NEVER use bash operations)

## Success Metrics (Manual Assessment)

- **Accuracy**: All VPA signals follow logical Wyckoff progression (manually verified)
- **Completeness**: Every ticker with new data has updated analysis (manually counted)
- **Consistency**: Vietnamese terminology and formatting maintained (manually checked)
- **Integration**: Final report successfully incorporates all VPA analysis (manually confirmed)
- **Documentation**: Complete manual summary report generated
- **Language Quality**: Proper Vietnamese financial terminology throughout (manually validated)
- **No Automation Dependencies**: All analysis done through manual natural language understanding