# VPA Analysis Preparation Task - Python Version

## Task Description
Use the Python utility to analyze which tickers need VPA updates

## Usage
**Non-interactive command - runs automatically without confirmation:**
```bash
uv run utilities/vpa_analysis_prep.py
```

## What this script does
1. Scans all CSV files in market_data/ directory
2. Identifies tickers with data for 2025-07-14 (or current date)
3. Reads corresponding vpa_data/{TICKER}.md files
4. Checks if 2025-07-14 analysis already exists
5. Extracts context data for tickers needing analysis:
   - Today's OHLCV data
   - Previous day's OHLCV data  
   - Latest VPA signal and analysis

## Output
- Summary of tickers needing analysis vs up-to-date
- List of tickers missing VPA files
- Detailed context data for each ticker needing analysis

## Advantages over Task tool
- Much faster execution
- Consistent data parsing
- No token/context limitations
- Reliable CSV and markdown parsing
- Can be run repeatedly for verification

## Next Steps
After running this script, use the output to:
1. Identify which tickers need VPA analysis
2. Get the context data needed for each ticker
3. Either use Task tool for VPA generation or create another Python script

## Related Files
- Source script: `utilities/vpa_analysis_prep.py`
- VPA generation task: `tasks/task_generate_vpa_analysis.md`
- Main protocol: `tasks/DAILY_VPA.md`