# VPA Analysis Generation Task

## Task Description
Generate VPA analysis for all tickers that need updates

## Task Prompt
I need to generate VPA analysis for [NUMBER] Vietnamese stock tickers for [DATE] using the Wyckoff methodology. For each ticker, I need you to:

1. Use reliable Python with glob.glob() to find and examine the most recent market_data/{TICKER}_*.csv file to get the latest available data and previous day's OHLCV data:
```python
import pandas as pd
import glob
ticker = 'TICKER_NAME'
csv_files = glob.glob(f'market_data/{ticker}_*.csv')
latest_file = max(csv_files) if csv_files else None
if latest_file:
    df = pd.read_csv(latest_file)
    latest_data = df.iloc[-1]  # Most recent data
    previous_data = df.iloc[-2] if len(df) > 1 else latest_data
    print(f'Latest date: {latest_data["Date"]}')
    print(f'File: {latest_file}')
```
2. Use Read tool to examine the existing vpa_data/{TICKER}.md file to get the latest VPA analysis context
3. Generate a new VPA analysis entry for the actual latest available date (not assumed date) following this EXACT format:

```markdown
- **Ngày [DATE]:** [Analysis of price movement from previous to current day]. [Description of candle characteristics]. [Volume analysis compared to previous day].
    - **Phân tích VPA/Wyckoff:** [Wyckoff interpretation: No Demand, Effort to Rise, Sign of Strength, etc.]. [Contextual explanation building on previous analysis].
```

CRITICAL REQUIREMENTS:
- Use DOT (.) as decimal separator, NEVER comma (,)
- Write in Vietnamese using proper financial terminology
- Must reference the previous VPA signal and build contextual continuity
- Apply proper Wyckoff VPA signals (No Demand, Effort to Rise, Sign of Strength, Test for Supply, etc.)
- Compare current bar to previous bar (price, spread, volume)
- Only generate analysis for [DATE] - do not modify any existing entries

**⚠️ CRITICAL FILE OPERATION REQUIREMENTS**:
- **⚠️ MANDATORY: ALWAYS use Write tool** to update `vpa_data/{TICKER}.md` files
- **⚠️ NEVER use bash, echo, or shell commands** for file operations
- **⚠️ ALWAYS use Read tool first** to get existing file content
- **⚠️ NO command line file operations** - they require approval prompts

**Correct Process for Each Ticker**:
1. **Use Read tool**: Read existing `vpa_data/{TICKER}.md` file completely
2. **Manual analysis**: Generate new VPA entry following the format
3. **Use Write tool**: Save complete updated content (existing + new entry)

**WRONG METHODS (NEVER DO THIS)**:
```bash
# NEVER USE THESE - THEY CAUSE APPROVAL PROMPTS:
echo "new content" >> vpa_data/{TICKER}.md
for file in vpa_data/*.md; do echo ...; done
cat >> vpa_data/{TICKER}.md << EOF
```

For each ticker, use the Write tool to append the new analysis entry to the existing content in vpa_data/{TICKER}.md files. Preserve all existing historical analysis.

Process all [NUMBER] tickers systematically and sequentially, ensuring each gets proper VPA analysis based on their individual context and recent signals. Complete each ticker before moving to the next one.

## Usage Instructions
1. Replace [NUMBER] with the actual number of tickers to process
2. Replace [DATE] with the target analysis date (format: YYYY-MM-DD)
3. Adjust the CSV file path pattern if needed for different date ranges
4. Use this task to generate VPA analysis for multiple tickers efficiently

## Common Wyckoff VPA Signals
- **Sign of Strength (SOS)** - Strong buying pressure
- **Sign of Weakness (SOW)** - Strong selling pressure  
- **Test for Supply** - Testing resistance levels
- **Test for Demand** - Testing support levels
- **No Demand** - Lack of buying interest
- **No Supply** - Lack of selling pressure
- **Effort to Rise** - Attempted upward movement
- **Effort to Fall** - Attempted downward movement
- **Secondary Test (ST)** - Retesting previous levels