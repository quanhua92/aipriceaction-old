# CHECK_PLAN.md - Task Template for Price Verification

## Purpose
Systematic verification of price data mentioned in PLAN.md against actual market data to ensure accuracy and prevent trading errors.

## When to Execute
- After PLAN.md is generated or updated
- Before making trading decisions based on PLAN.md
- When price discrepancies are suspected
- As part of regular quality control process

## Step-by-Step Process

### 1. Initial Setup
```bash
# Create todo list for systematic tracking
TodoWrite: Create tasks for price verification process
```

### 2. Identify ALL Data Claims in PLAN.md
- **VNINDEX Analysis** (critical market context)
- **Top 12 Trading Opportunities** section
- **New Opportunities/Potential Lists** section (often contains errors)
- **Weekly Analysis Claims** (percentage gains)
- **Key Levels section** (support/resistance)
- **Audit Log changes** (volume and price claims)
- Extract ALL ticker symbols with ANY data mentions

### 3. Daily Price Verification Process

For each ticker mentioned in PLAN.md:

#### A. Extract ALL Claims from PLAN.md
- Daily price movements (open → close)
- **Volume figures (in millions) - HIGH ERROR RATE**
- Price ranges mentioned in analysis
- Support/resistance levels
- Target prices
- **Weekly percentage gains - OFTEN INCORRECT**
- **VPA signal interpretations (volume up/down claims)**
- Gap up/down claims
- Volume comparisons ("doubled", "increased 60%", etc.)

#### B. Cross-Reference Market Data
```bash
# Read latest market data
Read: /Volumes/data/workspace/aipriceaction/market_data/{TICKER}_2025-01-02_to_2025-07-29.csv
# Focus on last 5-10 lines for most recent data
```

#### C. Cross-Reference VPA Analysis
```bash
# Read VPA analysis for context
Read: /Volumes/data/workspace/aipriceaction/vpa_data/{TICKER}.md
# Check latest analysis entries
```

### 4. Critical Verification Points

#### Daily Analysis Verification
- **Open Price**: Does gap up/down claim match actual open?
- **Close Price**: Is final closing price accurate?
- **Volume**: Are volume figures correct (millions vs actual units)? **⚠️ HIGH ERROR AREA**
- **Volume Direction Claims**: Does "volume increased/decreased" match reality?
- **Volume Percentage Claims**: Calculate actual % changes ("doubled", "60% increase")
- **Price Range**: High-Low range accuracy
- **Percentage Changes**: Calculate and verify claimed % moves
- **VPA Signal Consistency**: Do volume patterns match claimed VPA signals?

#### Weekly Analysis Verification **⚠️ CRITICAL ERROR AREA**
- Check weekly data files in `market_data_week/` directory
- **Calculate actual weekly % changes from CSV data**
- **Cross-reference claimed vs actual weekly performance**
- Verify weekly volume patterns
- **Common Error**: Off by 0.5-1.5 percentage points

### 5. Error Documentation Standards

For each discrepancy found:
```markdown
**{TICKER} Error Found:**
- **Location**: PLAN.md line {X}
- **Claimed**: {incorrect_data}
- **Actual**: {correct_data_with_source}
- **Error Magnitude**: {percentage_difference}%
- **Risk Level**: {High/Medium/Low}
```

### 6. Priority Correction Sequence **⭐ UPDATED BASED ON FINDINGS**

1. **Critical Errors (Immediate Fix Required)**
   - **VPA signal interpretations** (volume direction wrong = wrong trading signal)
   - **Volume errors >50%** (BSR: 100% error, GAS: 43% error)
   - Top 3 confidence tickers price/volume data
   - Weekly percentage claims (affects trend analysis)

2. **High Priority Errors (Fix Before Trading)**
   - **Volume errors 15-50%** (TCB: 18% error)
   - Support/resistance levels
   - Target prices
   - "New Opportunities" section data

3. **Medium Priority Errors (5-15% discrepancy)**
   - Secondary volume figures
   - Historical price references

4. **Minor Errors (<5% discrepancy)**
   - Contextual price mentions
   - Rounding differences

### 7. Update Process

For confirmed errors:
```bash
# Use MultiEdit for efficient batch corrections
MultiEdit: /Volumes/data/workspace/aipriceaction/PLAN.md
# Update all instances of incorrect data simultaneously
```

### 8. Quality Assurance Checks

#### Post-Correction Verification
- Verify mathematical consistency (percentages match price moves)
- Check that support < current price < resistance logic holds
- Ensure volume units are consistent (M vs actual numbers)

#### Risk Assessment
- **High Risk**: Top-ranked tickers with >20% price errors
- **Medium Risk**: Price errors affecting entry/exit strategies  
- **Low Risk**: Minor volume or historical data errors

### 9. Documentation for Future Prevention

#### Common Error Patterns to Watch **⚠️ BASED ON ACTUAL FINDINGS**
- **Volume reporting errors (most common)**: Wrong figures, wrong units
- **Weekly percentage calculation errors**: Off by 0.5-1.5pp consistently
- **VPA signal misinterpretation**: Volume direction claims wrong
- **"New Opportunities" section errors**: Higher error rate than top stocks
- Copy-paste errors between tickers
- Volume comparison errors ("doubled" claims incorrect)
- Wrong date references (using old data)
- Confusion between adjusted vs unadjusted prices

#### Data Source Validation
- Ensure CSV files are from correct date range
- Verify data freshness (latest trading day)
- Check for data corruption or incomplete downloads

### 10. Final Checklist

Before marking verification complete:
- [ ] All top 12 tickers verified
- [ ] Critical price levels corrected
- [ ] Volume figures standardized
- [ ] Support/resistance levels logical
- [ ] Target prices achievable
- [ ] Mathematical consistency confirmed
- [ ] Risk levels appropriate for corrected data

## Emergency Procedures

If **ANY of these critical issues found**:
- **>2 volume errors >50%**
- **>1 VPA signal interpretation error** 
- **>2 tickers have >20% price errors**
- **>3 weekly percentage errors >1pp**

**EMERGENCY ACTIONS:**
1. **STOP trading based on current PLAN.md**
2. Investigate data pipeline integrity
3. Check for systematic data source issues
4. **Focus on "New Opportunities" section** (higher error rate)
5. Consider regenerating entire PLAN.md from fresh data
6. Implement additional quality controls

## Success Metrics **⭐ UPDATED BASED ON ACTUAL PERFORMANCE**
- **Zero VPA signal interpretation errors** (volume direction must be correct)
- **Zero volume errors >20%** in any ticker
- **Zero critical errors** (>15% price discrepancy) in top 3 tickers
- **<5% error rate** across all data mentions (realistic based on findings)
- **100% mathematical consistency** in percentage calculations
- **Complete price chain validation** (open → high → low → close logic)
- **Weekly percentage accuracy within 0.5pp** (previous errors were 0.6-1.3pp)

## Tools Required
- Read tool for CSV and MD files
- **Task tool for comprehensive verification** (use when >10 data points to check)
- MultiEdit tool for batch corrections
- TodoWrite tool for progress tracking
- Basic calculator for percentage verification
- **Volume conversion calculator** (actual units ÷ 1M for millions)

---
*This template ensures systematic, thorough verification of trading plan accuracy to prevent costly errors in real trading scenarios.*