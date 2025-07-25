# VPA Analysis Generation Task

## Task Description
Generate VPA analysis for all tickers that need updates

## Task Prompt
I need to generate VPA analysis for [NUMBER] Vietnamese stock tickers for [DATE] using the Wyckoff methodology. For each ticker, I need you to:

1. Use Read tool to examine market_data/{TICKER}_2025-01-02_to_2025-07-14.csv file to get today's and previous day's OHLCV data
2. Use Read tool to examine the existing vpa_data/{TICKER}.md file to get the latest VPA analysis context
3. Generate a new VPA analysis entry for [DATE] following this EXACT format:

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

For each ticker, use the Write tool to append the new analysis entry to the existing content in vpa_data/{TICKER}.md files. NEVER use echo or bash commands to update markdown files. Always use the Write tool to preserve proper file encoding and avoid formatting issues. Preserve all existing historical analysis.

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