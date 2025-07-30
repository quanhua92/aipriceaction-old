# VPA Analysis Fix Protocol

This document outlines the exact steps to verify and fix VPA (Volume Price Analysis) analyses on a daily basis.

## Overview

The VPA verification and fixing process involves:
1. Running verification to identify problematic tickers
2. Deploying specialized sub-agents to fix individual tickers
3. Re-verifying to confirm improvements
4. Committing changes to git

## Prerequisites

- Python environment with required packages (vnstock, mplfinance, etc.)
- Access to `market_data/` directory with CSV files
- Access to `vpa_data/` directory with markdown analysis files
- `verify_vpa.py` script for verification

## Step-by-Step Process

### 1. Initial Verification

```bash
uv run verify_vpa.py
```

This will generate a comprehensive report showing:
- Total analyses verified
- Accuracy percentages (correct, incorrect, warnings, errors)
- List of problematic tickers (more incorrect than correct analyses)

**Expected Output Example:**
```
Total analyses verified: 1,808
Correct: 824 (45.6%)
Incorrect: 199 (11.0%)
Warnings: 785 (43.4%)
Errors: 0 (0.0%)

Problematic tickers: AAA, ACB, BCM, BSI, CII, CMG, CTD, DBC, DGC, DGW, DPM, etc.
```

### 2. Deploy Sub-Agents for Ticker Fixes

For each problematic ticker identified in step 1, create a specialized sub-agent to fix the VPA analysis:

**Sub-Agent Task Template:**
```
Fix VPA analysis for ticker [TICKER] by:

1. Use reliable Python with glob.glob() to find and read the most recent market data CSV file: market_data/[TICKER]_*.csv
```python
import pandas as pd
import glob
ticker = '[TICKER]'
csv_files = glob.glob(f'market_data/{ticker}_*.csv')
latest_file = max(csv_files) if csv_files else None
if latest_file:
    df = pd.read_csv(latest_file)
    print(f'Using file: {latest_file}')
    print(f'Data range: {df.iloc[0]["Date"]} to {df.iloc[-1]["Date"]}')
```
2. Read the current VPA analysis file: vpa_data/[TICKER].md
3. Compare the VPA analysis statements with actual market data
4. Fix any incorrect price directions (tăng/giảm/đi ngang)
5. Update volume amounts to match CSV data (format with commas)
6. Preserve all VPA signal analysis (SOS, SOW, No Demand, Test for Supply, etc.)
7. Ensure Vietnamese terminology is correct and consistent
8. Update the vpa_data/[TICKER].md file with accurate analysis

Key requirements:
- Price directions must match actual open/close data
- Volume amounts must match CSV data (converted to millions with commas)
- Preserve VPA signal interpretations (don't change SOS, SOW, etc.)
- Use proper Vietnamese stock market terminology
- Fix any contradictory statements
- Maintain markdown formatting
```

**Example Sub-Agent Deployment:**
```bash
# Deploy multiple agents in parallel for efficiency
Task 1: Fix VPA analysis for AAA
Task 2: Fix VPA analysis for ACB  
Task 3: Fix VPA analysis for BCM
# ... continue for all problematic tickers
```

### 3. Common VPA Analysis Issues to Fix

**Price Direction Errors:**
- "tăng từ X xuống Y" → should be "giảm từ X xuống Y"
- "giảm từ X lên Y" → should be "tăng từ X lên Y"
- Direction doesn't match actual CSV open/close data

**Volume Formatting Issues:**
- Inconsistent number formatting (missing commas)
- Incorrect volume amounts vs CSV data
- Wrong volume direction (tăng/giảm)

**File Organization Issues:**
- Mixed ticker analyses in same file
- Incorrect ticker headers
- Missing or malformed markdown structure

### 4. Re-Verification

After sub-agents complete their fixes, run verification again:

```bash
uv run verify_vpa.py
```

**Success Criteria:**
- Increased accuracy percentage (target: >60% correct)
- Reduced number of incorrect analyses
- Elimination of problematic tickers (0% incorrect preferred)

### 5. Git Commit

Once verification shows improvements, commit the changes:

```bash
git add vpa_data/
git commit -m "Fix VPA analysis accuracy improvements

- Fixed price direction errors across [X] tickers
- Updated volume amounts to match market data
- Improved accuracy from [X]% to [Y]%
- Resolved [X] incorrect analyses
- [Specific major fixes, e.g., CTG: 41.2% to 0% incorrect]"
```

## Quality Assurance Checklist

Before committing changes, ensure:

- [ ] Overall accuracy increased by at least 5%
- [ ] No new problematic tickers introduced
- [ ] All price directions match CSV data
- [ ] Volume amounts are properly formatted
- [ ] VPA signals preserved (SOS, SOW, etc.)
- [ ] Vietnamese terminology is correct
- [ ] Markdown formatting maintained
- [ ] No contradictory statements remain

## Daily Workflow

1. **Morning:** Run `uv run verify_vpa.py` to check current status
2. **Identify:** Note any new problematic tickers from overnight data updates
3. **Deploy:** Create sub-agents for new problematic tickers
4. **Monitor:** Track sub-agent progress and completion
5. **Verify:** Re-run verification to confirm improvements
6. **Commit:** Save improvements to git with detailed commit message

## Performance Targets

- **Accuracy Target:** >60% correct analyses
- **Error Rate:** <10% incorrect analyses
- **Warning Rate:** <40% warnings (aim to convert to correct analyses)
- **Problematic Tickers:** 0 tickers with more incorrect than correct

## File Structure

```
market_data/
├── [TICKER]_2025-01-02_to_2025-07-13.csv  # Source CSV data
└── ...

vpa_data/
├── [TICKER].md                             # VPA analysis files
└── ...

verify_vpa.py                               # Verification script
tasks/
└── FIX_VPA.md                             # This protocol document
```

## Notes

- Each sub-agent should focus on one ticker for optimal results
- Preserve VPA signal interpretations while fixing factual errors
- Use parallel deployment for efficiency (12+ agents recommended)
- Always verify improvements before committing
- Document major improvements in commit messages