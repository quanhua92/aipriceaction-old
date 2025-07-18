# Weekly VPA Analysis Preparation Task - Python Version

## Task Description
Use the Python utility to analyze which tickers need weekly VPA updates

## Usage
```bash
uv run utilities/vpa_analysis_prep_week.py
```

## What this script does
1. Scans all CSV files in market_data_week/ directory
2. Determines the latest Monday date for weekly analysis
3. Identifies tickers with data for the latest Monday
4. Reads corresponding vpa_data_week/{TICKER}.md files
5. Checks if latest Monday analysis already exists
6. Extracts context data for tickers needing analysis:
   - Current week's OHLCV data (Monday-dated)
   - Previous 4 weeks' OHLCV data  
   - Latest VPA signal and analysis

## Weekly Date Logic
**CRITICAL**: Weekly data dates are always from Monday of each week. The script automatically:
- Calculates the most recent Monday as the target analysis date
- If today is Monday before market close (4 PM), uses previous Monday
- If today is Monday after market close, uses current Monday
- For other days, uses the Monday of the current week

## Output
- Summary of tickers needing weekly analysis vs up-to-date
- List of tickers missing VPA files
- Detailed context data for each ticker needing analysis
- Clear indication of which Monday date is being targeted

## Advantages over Task tool
- Much faster execution for weekly data processing
- Consistent weekly date logic handling
- No token/context limitations
- Reliable CSV and markdown parsing
- Automatic Monday date calculation
- Can be run repeatedly for verification

## Next Steps
After running this script, use the output to:
1. Identify which tickers need weekly VPA analysis
2. Get the context data needed for each ticker
3. Use Task tool for weekly VPA generation with proper Monday dates
4. Ensure weekly perspective (trends, not daily noise)

## Related Files
- Source script: `utilities/vpa_analysis_prep_week.py`
- VPA generation task: `tasks/task_generate_vpa_analysis_week.md`
- Main protocol: `tasks/WEEKLY_VPA.md`