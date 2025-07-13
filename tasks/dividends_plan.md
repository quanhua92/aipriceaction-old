# Dividend Processing Plan for AI

## Overview
This document explains how to process dividend-adjusted VPA files that have been flagged by the dividend detection system.

## Directory Structure

### Daily Mode
- `market_data/` - Current/new market data
- `market_data_backup/` - Temporary backup (gets cleaned up)
- `market_data_check_dividends/` - Contains dividend-affected files (YOUR TASK)

### Weekly Mode  
- `market_data_week/` - Current/new market data
- `market_data_week_backup/` - Temporary backup (gets cleaned up)
- `market_data_week_check_dividends/` - Contains dividend-affected files (YOUR TASK)

## How Dividend Detection Works

1. **GitHub Actions** moves `market_data/` → `market_data_backup/`
2. **main.py --check-dividend** downloads fresh data and compares:
   - If dividend detected → copies old CSV to `market_data_check_dividends/`
   - Always deletes backup file (cleanup)
3. **Result**: Only dividend-affected files remain in `market_data_check_dividends/`

## Your AI Processing Task

### Input Files (in market_data_check_dividends/)
For each dividend-detected ticker, you'll find:
- `{TICKER}_{date_range}.csv` - The OLD CSV data (before dividend adjustment)
- `{TICKER}_dividend_info.txt` - Metadata with dividend ratio

### What You Need to Do
1. **Read dividend info**: Get the dividend ratio from `{TICKER}_dividend_info.txt`
2. **Process VPA files**: Update VPA analysis for that ticker using the dividend ratio
3. **Update price references**: Intelligently adjust Vietnamese price text in VPA files
4. **Delete processed files**: Remove both CSV and metadata files when done

### VPA File Locations
- Daily: `vpa_data/{TICKER}.md` or `VPA.md` (main file)
- Weekly: `vpa_data/{TICKER}.md` or `VPA_week.md` (main file)

### Example Dividend Info File
```
Ticker: SIP
Dividend Ratio: 1.250000
Detected: 2025-07-13 14:30:25
CSV File: SIP_2025-01-02_to_2025-07-13.csv
```

### Price Update Logic
When dividend ratio is 1.25, it means:
- OLD prices in VPA were 25% higher than NEW prices
- You need to divide all price references in VPA by 1.25
- Example: "từ 64.4 lên 64.9" → "từ 51.5 lên 51.9"

### Vietnamese Price Patterns to Update
```
- "từ X lên Y" (from X to Y)
- "từ X xuống Y" (from X down to Y)  
- "tăng từ X lên Y" (increased from X to Y)
- "giảm từ X xuống Y" (decreased from X to Y)
- "đóng cửa ở mức X" (closed at level X)
- "mở cửa ở X" (opened at X)
```

### Processing Steps
1. **Scan directory**: Check `market_data_check_dividends/` for `*_dividend_info.txt` files
2. **For each dividend ticker**:
   - Read dividend ratio from metadata file
   - Load corresponding VPA file for that ticker
   - Update all price references using the ratio
   - Preserve Vietnamese grammar and context
   - Save updated VPA file
   - Delete the CSV and metadata files from check_dividends directory

### Important Notes
- **Preserve context**: Don't just replace numbers - maintain Vietnamese sentence structure
- **Round appropriately**: Use reasonable decimal places for Vietnamese currency
- **Delete after processing**: Always clean up processed files to prevent reprocessing
- **Handle both daily and weekly modes**: Check file paths based on context
- **Graceful failures**: If processing fails, log error but don't crash

### Success Criteria
- ✅ All price references in VPA updated with dividend-adjusted values
- ✅ Vietnamese text remains natural and grammatically correct
- ✅ Processed files removed from `market_data_check_dividends/`
- ✅ No files left behind in check_dividends directory
- ✅ VPA analysis context and meaning preserved

### Error Handling
- If dividend ratio is invalid (≤0 or >10), skip and log error
- If VPA file not found, log warning and clean up dividend files
- If price parsing fails, attempt manual patterns or skip problematic entries
- Always delete processed files even if updates fail (prevent infinite loops)

## Testing
To test your dividend processing:
1. Create test files in `market_data_check_dividends/`
2. Run your dividend processor
3. Verify VPA files are updated correctly
4. Confirm check_dividends directory is empty after processing