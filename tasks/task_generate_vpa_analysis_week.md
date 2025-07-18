# Weekly VPA Analysis Generation Task

## Task Description
Generate weekly VPA analysis for all tickers that need updates

## Task Prompt
I need to generate weekly VPA analysis for [NUMBER] Vietnamese stock tickers for [MONDAY_DATE] using the Wyckoff methodology. For each ticker, I need you to:

1. Read the market_data_week/{TICKER}_2025-01-02_to_[MONDAY_DATE].csv file to get current week's and previous weeks' OHLCV data
2. Read the existing vpa_data_week/{TICKER}.md file to get the latest VPA analysis context
3. Generate a new weekly VPA analysis entry for [MONDAY_DATE] following this EXACT format:

```markdown
- **Ngày [MONDAY_DATE]:** [Analysis of weekly price movement from previous to current week]. [Description of weekly candle characteristics]. [Volume analysis compared to previous week].
    - **Phân tích VPA/Wyckoff:** [Wyckoff interpretation: No Demand, Effort to Rise, Sign of Strength, etc.]. [Contextual explanation building on previous weekly analysis].
```

CRITICAL REQUIREMENTS:
- **WEEKLY PERSPECTIVE**: Focus on weekly trends, not daily noise
- **MONDAY DATES**: All weekly data is Monday-dated (e.g., 2025-07-07 represents the week of July 7-11)
- **DOT DECIMAL SEPARATOR**: Use DOT (.) as decimal separator, NEVER comma (,)
- **VIETNAMESE LANGUAGE**: Write in Vietnamese using proper financial terminology
- **CONTEXTUAL CONTINUITY**: Must reference the previous weekly VPA signal and build upon it
- **WEEKLY WYCKOFF SIGNALS**: Apply proper weekly VPA signals with greater significance than daily
- **WEEKLY COMPARISON**: Compare current weekly bar to previous weekly bar (price spread, volume)
- **WEEKLY VOLUME CONTEXT**: Weekly volume should be compared to previous weeks, not daily averages
- **DATE VERIFICATION**: Only generate analysis for [MONDAY_DATE] if it doesn't already exist

## Weekly Analysis Focus Areas
- **Weekly Price Spread**: Compare weekly high-low range to previous weeks
- **Weekly Closing**: Position of weekly close within the weekly range
- **Weekly Volume**: Total volume for the week compared to previous weeks
- **Weekly Patterns**: Higher highs, higher lows, weekly support/resistance
- **Weekly Trends**: Multi-week trend analysis, not daily fluctuations

For each ticker, append the new weekly analysis entry to the existing content in vpa_data_week/{TICKER}.md files. Preserve all existing historical analysis.

Process all [NUMBER] tickers systematically, ensuring each gets proper weekly VPA analysis based on their individual context and recent weekly signals.

## Usage Instructions
1. Replace [NUMBER] with the actual number of tickers to process
2. Replace [MONDAY_DATE] with the target Monday date (format: YYYY-MM-DD)
3. Adjust the CSV file path pattern if needed for different date ranges
4. Use this task to generate weekly VPA analysis for multiple tickers efficiently
5. Read from the assigned batch file: utilities/data/batch_X.csv

## Common Weekly Wyckoff VPA Signals
- **Sign of Strength (SOS)** - Strong weekly buying pressure with high volume
- **Sign of Weakness (SOW)** - Strong weekly selling pressure with high volume
- **Test for Supply** - Weekly testing of resistance levels with lower volume
- **Test for Demand** - Weekly testing of support levels with lower volume
- **No Demand** - Weak weekly advance on low volume
- **No Supply** - Weak weekly decline on low volume
- **Effort to Rise** - Attempted weekly upward movement with increased volume
- **Effort to Fall** - Attempted weekly downward movement with increased volume
- **Secondary Test (ST)** - Weekly retest of previous significant levels

## Weekly Number Formatting Examples
- **CORRECT**: 64.4, 12.5, 123.45, 1.234.567 (for millions)
- **INCORRECT**: 64,4, 12,5, 123,45, 1,234,567

## Weekly Analysis Template Example
```markdown
- **Ngày 2025-07-07:** Tiếp nối tín hiệu **No Demand** của tuần trước, tuần này SIP tăng từ 64.4 lên 64.7 với biên độ hẹp. Nến tuần tăng nhẹ với khối lượng 12.5 triệu đơn vị, tăng so với tuần trước.
    - **Phân tích VPA/Wyckoff:** Đây là một tín hiệu **Effort to Rise** trên khung thời gian tuần, phủ nhận tín hiệu yếu kém tuần trước. Lực cầu tuần đã quay trở lại, cho thấy tiềm năng phục hồi trong xu hướng tuần tới.
```