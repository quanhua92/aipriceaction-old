# CHECK_HOLD.md - Task Template for Portfolio Holdings Verification

## Purpose
Systematic verification of price data, P&L calculations, and VPA analysis mentioned in hold.md against actual market data to ensure accuracy and prevent portfolio management errors.

## When to Execute
- After hold.md is generated or updated
- Before making portfolio trading decisions based on hold.md
- When price discrepancies or P&L errors are suspected
- As part of regular portfolio quality control process

## Step-by-Step Process

### 1. Initial Setup
```bash
# Create todo list for systematic tracking
TodoWrite: Create tasks for portfolio verification process
```

### 2. **Portfolio Holdings Verification** (Critical Foundation)

#### A. Extract Current Holdings from hold.md
- Read "Dữ Liệu Danh Mục" table for all portfolio positions
- Extract ticker symbols, average buy prices, quantities held
- Identify previous recommendations from detailed analysis sections

#### B. Verify Market Data Availability
```bash
# For each portfolio ticker, verify market data exists:
LS: /Volumes/data/workspace/aipriceaction/market_data/
# Check for {TICKER}_2025-01-02_to_2025-07-29.csv files
```

### 3. **Critical Data Verification Process**

#### 3.1 **Current Price Verification** (⚠️ HIGH ERROR AREA)
```bash
# For EVERY ticker in portfolio, verify current price using most recent CSV file
uv run -c "
import pandas as pd
import glob
ticker = 'TICKER_NAME'
try:
    # Find the most recent CSV file for this ticker
    csv_files = glob.glob(f'market_data/{ticker}_*.csv')
    if csv_files:
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        latest = df.iloc[-1]  # Last row = most recent data
        print(f'{ticker}: Latest date={latest[\"Date\"]}, Close={latest[\"Close\"]}')
        print(f'Using file: {latest_file}')
    else:
        print(f'No CSV files found for {ticker}')
except Exception as e:
    print(f'Error reading {ticker}: {e}')
"
```

**Critical Checks:**
- [ ] **Current Prices**: All "Giá Hiện Tại" match CSV close prices exactly
- [ ] **Date Consistency**: Latest price dates match expected trading day
- [ ] **Price Format**: Vietnamese decimal format (dots for decimals, no thousands separators)

#### 3.2 **P&L Calculation Verification** (⚠️ CRITICAL FOR TRADING)
```bash
# Use verified calculation script:
python3 calculate_pnl_correct.py
# Cross-reference output with hold.md P&L claims
```

**P&L Verification Formula:**
- **P&L %** = ((Current Price - Average Buy Price) / Average Buy Price) × 100
- **P&L Amount** = (Current Price - Average Buy Price) × Quantity
- **Vietnamese Format**: +X.XX% (+X.XXX.000) using dot separators

**Critical P&L Checks:**
- [ ] **Percentage Accuracy**: All P&L percentages calculated correctly
- [ ] **Amount Accuracy**: All P&L amounts calculated correctly  
- [ ] **Vietnamese Formatting**: All amounts use dot separators (2.885.000)
- [ ] **Sign Consistency**: Positive/negative signs match actual performance
- [ ] **Portfolio Total**: Overall P&L summary matches individual positions

#### 3.3 **VPA Analysis Verification** 
```bash
# Cross-reference VPA claims with actual analysis files
Read: /Volumes/data/workspace/aipriceaction/vpa_data/{TICKER}.md
# Check latest entries match hold.md VPA claims
```

**VPA Verification Checks:**
- [ ] **Daily Signals**: Latest daily VPA signals match vpa_data files
- [ ] **Weekly Context**: Weekly analysis claims match REPORT_week.md
- [ ] **Signal Dates**: All VPA signal dates are accurate and recent
- [ ] **Volume Claims**: Volume patterns support claimed VPA signals

### 4. **Sector Allocation Verification**

#### 4.1 **Industry Classification Check**
```bash
# Verify sector classifications against GROUP.md
Read: /Volumes/data/workspace/aipriceaction/GROUP.md
# Manual verification of each ticker's industry assignment
```

#### 4.2 **Portfolio Allocation Calculation**
**Manual Verification Process:**
1. Calculate market value for each ticker: Current Price × Quantity
2. Group tickers by industry sector
3. Calculate sector percentages: (Sector Value / Total Portfolio Value) × 100
4. Verify percentages sum to 100%

**Critical Allocation Checks:**
- [ ] **Industry Accuracy**: All tickers classified correctly per GROUP.md
- [ ] **Percentage Math**: All sector percentages calculated correctly  
- [ ] **Total Verification**: All percentages sum to 100%
- [ ] **Market Values**: Individual position values calculated correctly

### 5. **Action Recommendation Verification**

#### 5.1 **Signal-Action Consistency**
**Verification Logic:**
- **Strong Bullish Signals** (SOS, Effort to Rise) → Buy More/Hold recommendations
- **Strong Bearish Signals** (SOW, Effort to Fall) → Sell/Panic Sell recommendations  
- **Neutral/Mixed Signals** → Hold recommendations
- **Climactic Patterns** → Appropriate caution in recommendations

#### 5.2 **Stop Loss & Take Profit Verification**
**Technical Level Checks:**
- [ ] **Stop Loss Logic**: Below support levels for long positions
- [ ] **Take Profit Logic**: At resistance levels or technical targets
- [ ] **Risk-Reward Ratio**: Appropriate risk management ratios
- [ ] **Price Relationship**: Stop < Current < Target for long positions

### 6. **Alternative Recommendations Verification**

#### 6.1 **Industry Matching Verification**
```bash
# Verify all "Top 3 Cổ Phiếu Thay Thế" are from same industry
Read: /Volumes/data/workspace/aipriceaction/GROUP.md
# Cross-check each alternative ticker's industry classification
```

**Critical Alternative Checks:**
- [ ] **Same Industry Rule**: All 3 alternatives from SAME industry as holding
- [ ] **Signal Verification**: Alternative recommendations have supporting VPA signals
- [ ] **Logic Consistency**: Alternatives offer better risk-reward than current holding

### 7. **Error Documentation & Correction Priority**

#### 7.1 **Error Classification System**
```markdown
**Critical Errors (Fix Immediately):**
- P&L calculation errors >1%
- Wrong current prices
- Incorrect buy/sell recommendations based on wrong data
- Industry misclassification affecting alternatives

**High Priority Errors:**
- VPA signal misinterpretation
- Stop loss/take profit level errors
- Sector allocation calculation errors

**Medium Priority Errors:**
- Formatting inconsistencies
- Minor date discrepancies
- Vietnamese language/formatting issues
```

#### 7.2 **Correction Process**
```bash
# Use MultiEdit for efficient batch corrections
MultiEdit: /Volumes/data/workspace/aipriceaction/hold.md
# Update all instances of incorrect data simultaneously
```

### 8. **Quality Assurance Final Checklist**

#### Portfolio Integrity Verification
- [ ] **Complete Coverage**: All portfolio holdings analyzed and verified
- [ ] **Data Accuracy**: All prices and P&L calculations verified against CSV data
- [ ] **Signal Consistency**: All VPA claims match source analysis files
- [ ] **Action Logic**: All recommendations follow proper VPA methodology
- [ ] **Risk Management**: All stop/target levels technically justified

#### Format & Language Verification  
- [ ] **Vietnamese Formatting**: All monetary amounts use dot separators
- [ ] **Decimal Consistency**: Prices use proper decimal formatting
- [ ] **Language Standards**: Pure Vietnamese financial terminology
- [ ] **Chart Links**: All image paths verified to exist

### 9. **Error Prevention Guidelines**

#### Common Error Patterns in Portfolio Management
- **P&L Miscalculations**: Most common error - always use calculate_pnl_correct.py
- **Stale Price Data**: Using outdated prices - always check latest CSV entries
- **Industry Mismatching**: Wrong alternatives due to GROUP.md misreading
- **VPA Signal Lag**: Using old signals instead of most recent analysis
- **Vietnamese Number Format**: Using commas instead of dots for thousands

#### Prevention Best Practices
1. **Always run P&L script** before making portfolio decisions
2. **Cross-reference dates** between market data and VPA analysis
3. **Manually verify industry classifications** against GROUP.md for every ticker
4. **Check volume patterns** to support VPA signal claims
5. **Verify mathematical consistency** across all calculations

### 10. **Success Metrics**

#### Accuracy Standards
- **Zero P&L calculation errors** (verified against script output)
- **Zero current price errors** (verified against CSV data)
- **100% industry classification accuracy** (verified against GROUP.md)
- **All VPA signals current** (within 1-2 trading days)
- **All recommendations logically consistent** with supporting data

#### Risk Management Standards
- **All stop losses below current prices** for long positions
- **All targets above current prices** for long positions  
- **Risk-reward ratios 1:2 or better** where applicable
- **Position sizing appropriate** for portfolio balance

### 11. **Tools Required**
- Read tool for CSV and MD files
- calculate_pnl_correct.py script for P&L verification
- MultiEdit tool for batch corrections
- TodoWrite tool for progress tracking
- Basic calculator for percentage verification
- LS tool for file existence verification

### 12. **Emergency Procedures**

If **ANY of these critical issues found**:
- **>2 P&L calculation errors >1%**
- **>1 current price error**
- **>3 industry classification errors**
- **VPA signals >3 days old**

**EMERGENCY ACTIONS:**
1. **STOP all portfolio trading** based on current hold.md
2. **Run complete verification** using calculate_pnl_correct.py
3. **Update all market data** files if needed
4. **Re-verify all VPA analysis** against source files
5. **Regenerate hold.md** with corrected data if errors are systematic

---
*This template ensures systematic, thorough verification of portfolio management accuracy to prevent costly trading errors and protect investment capital.*