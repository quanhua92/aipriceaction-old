# CHECK_HOLD_us_crypto.md - Task Template for US & Crypto Portfolio Holdings Verification

## Purpose
Systematic verification of price data, P&L calculations, and VPA analysis mentioned in hold_us_crypto.md against actual market data to ensure accuracy and prevent portfolio management errors in US indices and cryptocurrency positions.

## When to Execute
- After hold_us_crypto.md is generated or updated
- Before making portfolio trading decisions based on hold_us_crypto.md
- When price discrepancies or P&L errors are suspected in US/crypto positions
- As part of regular US & crypto portfolio quality control process

## Step-by-Step Process

### 1. Initial Setup
```bash
# Create todo list for systematic tracking
TodoWrite: Create tasks for US & crypto portfolio verification process
```

### 2. **Portfolio Holdings Verification** (Critical Foundation)

#### A. Extract Current Holdings from hold_us_crypto.md
- Read "Dữ Liệu Danh Mục" table for all US index and crypto positions
- Extract ticker symbols (DJI, INX, BTC, ETH, etc.), average buy prices, quantities held
- Identify previous recommendations from detailed analysis sections
- Verify asset class classification (US indices vs cryptocurrencies)

#### B. Verify Market Data Availability
```bash
# For each portfolio ticker, verify market data exists:
LS: /Volumes/data/workspace/aipriceaction/market_data_us_crypto/
# Check for {TICKER}_2025-01-02_to_2025-08-08.csv files
```

### 3. **Critical Data Verification Process**

#### 3.1 **Current Price Verification** (⚠️ HIGH ERROR AREA - USD Pricing)
```bash
# For EVERY ticker in US/crypto portfolio, verify current price using most recent CSV file
uv run -c "
import pandas as pd
import glob
ticker = 'TICKER_NAME'  # DJI, BTC, ETH, etc.
try:
    # Find the most recent CSV file for this ticker
    csv_files = glob.glob(f'market_data_us_crypto/{ticker}_*.csv')
    if csv_files:
        latest_file = max(csv_files)
        df = pd.read_csv(latest_file)
        latest = df.iloc[-1]  # Last row = most recent data
        print(f'{ticker}: Latest date={latest[\"time\"]}, Close={latest[\"close\"]}')
        print(f'Using file: {latest_file}')
        print(f'Asset type: {\"US Index\" if ticker in [\"DJI\", \"INX\", \"COMP\", \"RUT\", \"NYA\", \"RUI\", \"RUA\"] else \"Crypto\"}')
    else:
        print(f'No CSV files found for {ticker}')
except Exception as e:
    print(f'Error reading {ticker}: {e}')
"
```

**Critical Checks:**
- [ ] **Current Prices**: All "Giá Hiện Tại" match CSV close prices exactly (USD format)
- [ ] **Date Consistency**: Latest price dates match expected trading day
- [ ] **Price Format**: USD decimal format with appropriate precision (indices vs crypto)
- [ ] **Asset Classification**: Proper identification of US indices vs cryptocurrency assets

#### 3.2 **P&L Calculation Verification** (⚠️ CRITICAL FOR US/CRYPTO TRADING)
```bash
# Use verified calculation script for US/crypto assets:
python3 calculate_pnl_correct_us_crypto.py
# Cross-reference output with hold_us_crypto.md P&L claims
```

**P&L Verification Formula:**
- **P&L %** = ((Current Price - Average Buy Price) / Average Buy Price) × 100
- **P&L Amount** = (Current Price - Average Buy Price) × Quantity
- **USD Format**: +X.XX% (+$X,XXX.XX) using proper USD formatting

**Critical P&L Checks:**
- [ ] **Percentage Accuracy**: All P&L percentages calculated correctly for each asset class
- [ ] **Amount Accuracy**: All P&L amounts calculated correctly in USD
- [ ] **USD Formatting**: All amounts use proper USD formatting ($X,XXX.XX)
- [ ] **Sign Consistency**: Positive/negative signs match actual performance
- [ ] **Portfolio Total**: Overall P&L summary matches individual positions across asset classes
- [ ] **Cross-Asset Calculation**: Proper handling of different price scales (indices vs crypto)

#### 3.3 **VPA Analysis Verification** 
```bash
# Cross-reference VPA claims with actual analysis files
Read: /Volumes/data/workspace/aipriceaction/vpa_data_us_crypto/{TICKER}.md
# Check latest entries match hold_us_crypto.md VPA claims
```

**VPA Verification Checks:**
- [ ] **Daily Signals**: Latest daily VPA signals match vpa_data_us_crypto files
- [ ] **Weekly Context**: Weekly analysis claims match REPORT_us_crypto_week.md
- [ ] **Signal Dates**: All VPA signal dates are accurate and recent
- [ ] **Volume Claims**: Volume patterns support claimed VPA signals
- [ ] **Asset-Specific Analysis**: Proper VPA methodology adapted for global markets

### 4. **Asset Class Allocation Verification**

#### 4.1 **Asset Classification Check**
```bash
# Verify asset classifications against GROUP_us_crypto.md
Read: /Volumes/data/workspace/aipriceaction/GROUP_us_crypto.md
# Manual verification of each ticker's asset class assignment
```

#### 4.2 **Portfolio Allocation Calculation**
**Manual Verification Process:**
1. Calculate market value for each ticker: Current Price × Quantity
2. Group tickers by asset class (US_INDICES, MAJOR_CRYPTO, etc.)
3. Calculate asset class percentages: (Class Value / Total Portfolio Value) × 100
4. Verify percentages sum to 100%

**Critical Allocation Checks:**
- [ ] **Asset Class Accuracy**: All tickers classified correctly per GROUP_us_crypto.md
- [ ] **Percentage Math**: All asset class percentages calculated correctly  
- [ ] **Total Verification**: All percentages sum to 100%
- [ ] **Market Values**: Individual position values calculated correctly in USD
- [ ] **Cross-Asset Balance**: Appropriate diversification between US indices and crypto

### 5. **Action Recommendation Verification**

#### 5.1 **Signal-Action Consistency**
**Verification Logic:**
- **Strong Bullish Signals** (SOS, Effort to Rise) → Buy More/Hold recommendations
- **Strong Bearish Signals** (SOW, Effort to Fall) → Sell/Panic Sell recommendations  
- **Neutral/Mixed Signals** → Hold recommendations
- **Climactic Patterns** → Appropriate caution in recommendations
- **Asset-Specific Considerations**: Different volatility expectations for crypto vs indices

#### 5.2 **Stop Loss & Take Profit Verification**
**Technical Level Checks:**
- [ ] **Stop Loss Logic**: Below support levels for long positions
- [ ] **Take Profit Logic**: At resistance levels or technical targets
- [ ] **Risk-Reward Ratio**: Appropriate risk management ratios for each asset class
- [ ] **Price Relationship**: Stop < Current < Target for long positions
- [ ] **Volatility Adjustment**: Crypto stops/targets account for higher volatility

### 6. **Alternative Recommendations Verification**

#### 6.1 **Asset Class Matching Verification**
```bash
# Verify all "Top 3 Tài Sản Thay Thế" are from same asset class
Read: /Volumes/data/workspace/aipriceaction/GROUP_us_crypto.md
# Cross-check each alternative ticker's asset class classification
```

**Critical Alternative Checks:**
- [ ] **Same Asset Class Rule**: All 3 alternatives from SAME asset class as holding
- [ ] **Signal Verification**: Alternative recommendations have supporting VPA signals
- [ ] **Logic Consistency**: Alternatives offer better risk-reward than current holding
- [ ] **Diversification Logic**: Appropriate alternatives within US indices or crypto space

### 7. **Error Documentation & Correction Priority**

#### 7.1 **Error Classification System**
```markdown
**Critical Errors (Fix Immediately):**
- P&L calculation errors >1% on any position
- Wrong current prices for US indices or crypto assets
- Incorrect buy/sell recommendations based on wrong data
- Asset class misclassification affecting alternatives
- USD formatting errors affecting portfolio values

**High Priority Errors:**
- VPA signal misinterpretation for global markets
- Stop loss/take profit level errors
- Asset class allocation calculation errors
- Cross-asset correlation misunderstanding

**Medium Priority Errors:**
- Formatting inconsistencies in USD amounts
- Minor date discrepancies
- Vietnamese language/formatting issues in global context
```

#### 7.2 **Correction Process**
```bash
# Use MultiEdit for efficient batch corrections
MultiEdit: /Volumes/data/workspace/aipriceaction/hold_us_crypto.md
# Update all instances of incorrect data simultaneously
```

### 8. **Quality Assurance Final Checklist**

#### Portfolio Integrity Verification
- [ ] **Complete Coverage**: All US index and crypto holdings analyzed and verified
- [ ] **Data Accuracy**: All prices and P&L calculations verified against CSV data
- [ ] **Signal Consistency**: All VPA claims match source analysis files
- [ ] **Action Logic**: All recommendations follow proper VPA methodology for global markets
- [ ] **Risk Management**: All stop/target levels technically justified for each asset class

#### Format & Language Verification  
- [ ] **USD Formatting**: All monetary amounts use proper USD formatting
- [ ] **Decimal Consistency**: Prices use appropriate precision for asset type
- [ ] **Language Standards**: Vietnamese financial terminology adapted for global markets
- [ ] **Chart Links**: All image paths verified to exist in reports_us_crypto directories

### 9. **Error Prevention Guidelines**

#### Common Error Patterns in US/Crypto Portfolio Management
- **P&L Miscalculations**: Most common error - always use calculate_pnl_correct_us_crypto.py
- **Stale Price Data**: Using outdated prices - always check latest CSV entries
- **Asset Class Mismatching**: Wrong alternatives due to GROUP_us_crypto.md misreading
- **VPA Signal Lag**: Using old signals instead of most recent analysis
- **USD Formatting**: Incorrect currency formatting for international assets
- **Volatility Misjudgment**: Not accounting for crypto vs index volatility differences

#### Prevention Best Practices
1. **Always run P&L script** before making US/crypto portfolio decisions
2. **Cross-reference dates** between market data and VPA analysis
3. **Manually verify asset classifications** against GROUP_us_crypto.md for every ticker
4. **Check volume patterns** to support VPA signal claims
5. **Verify mathematical consistency** across all calculations
6. **Account for asset class differences** in risk management

### 10. **Success Metrics**

#### Accuracy Standards
- **Zero P&L calculation errors** (verified against script output)
- **Zero current price errors** (verified against CSV data)
- **100% asset class accuracy** (verified against GROUP_us_crypto.md)
- **All VPA signals current** (within 1-2 trading days)
- **All recommendations logically consistent** with supporting data
- **Proper USD formatting** throughout all monetary references

#### Risk Management Standards
- **All stop losses below current prices** for long positions
- **All targets above current prices** for long positions  
- **Risk-reward ratios 1:2 or better** where applicable
- **Position sizing appropriate** for portfolio balance across asset classes
- **Volatility-adjusted risk levels** for crypto vs index positions

### 11. **Tools Required**
- Read tool for CSV and MD files
- calculate_pnl_correct_us_crypto.py script for P&L verification
- MultiEdit tool for batch corrections
- TodoWrite tool for progress tracking
- Basic calculator for percentage verification
- LS tool for file existence verification

### 12. **Emergency Procedures**

If **ANY of these critical issues found**:
- **>2 P&L calculation errors >1%** on US/crypto positions
- **>1 current price error** for any asset
- **>3 asset class classification errors**
- **VPA signals >3 days old**
- **Major USD formatting inconsistencies**

**EMERGENCY ACTIONS:**
1. **STOP all US/crypto portfolio trading** based on current hold_us_crypto.md
2. **Run complete verification** using calculate_pnl_correct_us_crypto.py
3. **Update all market data** files if needed
4. **Re-verify all VPA analysis** against source files
5. **Regenerate hold_us_crypto.md** with corrected data if errors are systematic
6. **Review asset class allocation** for appropriate diversification

---
*This template ensures systematic, thorough verification of US index and cryptocurrency portfolio management accuracy to prevent costly trading errors and protect investment capital in global markets.*