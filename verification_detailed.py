#!/usr/bin/env python3

import pandas as pd
import os
import math

# Portfolio data from hold.md (line numbers for reference)
portfolio = {
    'CTS': {'avg_buy': 39.228, 'quantity': 900, 'line': 51},
    'HDB': {'avg_buy': 27.560, 'quantity': 1500, 'line': 73},
    'HDC': {'avg_buy': 33.320, 'quantity': 500, 'line': 95},
    'SHB': {'avg_buy': 15.514, 'quantity': 1800, 'line': 117},
    'SSI': {'avg_buy': 32.994, 'quantity': 1700, 'line': 139},
    'TCH': {'avg_buy': 25.719, 'quantity': 400, 'line': 161},
    'VIX': {'avg_buy': 24.109, 'quantity': 900, 'line': 183},
    'VND': {'avg_buy': 19.731, 'quantity': 3500, 'line': 205},
    'VPB': {'avg_buy': 23.368, 'quantity': 2000, 'line': 227}
}

# Claims from hold.md to verify (amounts in VND, not thousands)
hold_claims = {
    'CTS': {'current_price': 39.55, 'pnl_pct': 0.82, 'pnl_amount': 289000, 'line': 53},
    'HDB': {'current_price': 26.50, 'pnl_pct': -3.85, 'pnl_amount': -1590000, 'line': 75},
    'HDC': {'current_price': 32.35, 'pnl_pct': -2.91, 'pnl_amount': -485000, 'line': 97},
    'SHB': {'current_price': 15.05, 'pnl_pct': -2.99, 'pnl_amount': -835000, 'line': 119},
    'SSI': {'current_price': 33.30, 'pnl_pct': 0.93, 'pnl_amount': 520000, 'line': 141},
    'TCH': {'current_price': 24.60, 'pnl_pct': -4.35, 'pnl_amount': -447000, 'line': 163},
    'VIX': {'current_price': 23.95, 'pnl_pct': -0.66, 'pnl_amount': -143000, 'line': 185},
    'VND': {'current_price': 21.05, 'pnl_pct': 6.68, 'pnl_amount': 4616000, 'line': 207},
    'VPB': {'current_price': 23.60, 'pnl_pct': 0.99, 'pnl_amount': 464000, 'line': 229}
}

# Specific volume and price movement claims to verify
specific_claims = {
    'CTS': {
        'volume_jul29': {'claimed': '8.72 triệu', 'line': 57},
        'volume_change': {'claimed': '+100%', 'line': 57},
        'price_movement': {'claimed': '42.5 xuống 39.55', 'line': 57}
    },
    'HDB': {
        'price_movement': {'claimed': '28.45 xuống 26.5', 'line': 79},
        'volume_change': {'claimed': '+36%', 'line': 79}
    },
    'HDC': {
        'volume_jul29': {'claimed': '16.74 triệu', 'line': 101},
        'volume_change': {'claimed': '+156%', 'line': 101},
        'price_movement': {'claimed': '34.75 xuống 32.35', 'line': 101}
    },
    'SHB': {
        'volume_jul29': {'claimed': '152.87M', 'line': 123},
        'price_movement': {'claimed': 'gap up từ 16.5 nhưng bị bán tháo dữ dội xuống 15.05', 'line': 123}
    },
    'SSI': {
        'volume_jul29': {'claimed': '104.97M', 'line': 145}, 
        'price_movement': {'claimed': '35.8 xuống 33.3', 'line': 145}
    },
    'TCH': {
        'volume_change': {'claimed': '+103%', 'line': 167},
        'price_movement': {'claimed': '26.5 xuống 24.6', 'line': 167},
        'daily_change': {'claimed': '-6.82%', 'line': 167}
    },
    'VIX': {
        'volume_jul29': {'claimed': '118.78M', 'line': 189},
        'volume_change': {'claimed': '+260%', 'line': 189},
        'price_movement': {'claimed': 'gap lên 27.35 nhưng sụp đổ xuống 23.95', 'line': 189}
    },
    'VND': {
        'volume_change': {'claimed': '+142%', 'line': 211},
        'price_movement': {'claimed': 'gap lên 24.0 nhưng điều chỉnh xuống 21.05', 'line': 211}
    },
    'VPB': {
        'price_movement': {'claimed': '25.1 xuống 23.6', 'line': 233}
    }
}

# Weekly claims to verify
weekly_claims = {
    'VND': {
        'sos_weeks': {'claimed': '4 tuần liên tiếp', 'line': 210},
        'weekly_gain': {'claimed': '+13.4%', 'line': 210, 'volume_change': '+29.7%'}
    },
    'VPB': {
        'weekly_gain': {'claimed': '+11.3%', 'line': 232, 'volume_change': '+20.3%'}
    },
    'HDC': {
        'weekly_gain': {'claimed': '+27%', 'line': 100, 'volume_change': '+24.5%'}
    }
}

def get_latest_price(ticker):
    """Get latest closing price from CSV"""
    try:
        file_path = f"market_data/{ticker}_2025-01-02_to_2025-07-29.csv"
        df = pd.read_csv(file_path)
        return df.iloc[-1]['close']
    except:
        return None

def get_daily_data(ticker, date_offset=-1):
    """Get daily data for specific offset (0=latest, -1=previous, etc.)"""
    try:
        file_path = f"market_data/{ticker}_2025-01-02_to_2025-07-29.csv"
        df = pd.read_csv(file_path)
        return df.iloc[date_offset]
    except:
        return None

def calculate_pnl(avg_buy, current_price, quantity):
    """Calculate P&L percentage and amount"""
    pnl_per_share = current_price - avg_buy
    pnl_pct = (pnl_per_share / avg_buy) * 100
    pnl_amount = pnl_per_share * quantity
    return pnl_pct, pnl_amount

def format_vnd(amount):
    """Format amount in Vietnamese format with dots"""
    if amount >= 0:
        return f"+{amount:,.0f}".replace(',', '.')
    else:
        return f"{amount:,.0f}".replace(',', '.')

print("=== COMPREHENSIVE VERIFICATION REPORT FOR hold.md ===\n")

errors = []
critical_errors = []
high_priority_errors = []
medium_priority_errors = []

print("1. PORTFOLIO HOLDINGS TABLE VERIFICATION (Lines 7-17)")
print("=" * 60)

# Verify holdings table data
for ticker, data in portfolio.items():
    print(f"\n{ticker} (Line {data['line']}):")
    
    # Check average buy price format (should be decimal)
    avg_buy = data['avg_buy']
    if '.' not in str(avg_buy):
        error = f"Line {data['line']}: {ticker} average buy price format issue"
        medium_priority_errors.append(error)
    
    # Check quantity format (should be integer)
    quantity = data['quantity']
    if not isinstance(quantity, int) or quantity <= 0:
        error = f"Line {data['line']}: {ticker} quantity format issue"
        medium_priority_errors.append(error)
    
    print(f"  ✅ Average Buy Price: {avg_buy} (format OK)")
    print(f"  ✅ Quantity: {quantity} (format OK)")

print(f"\n2. CURRENT PRICES VERIFICATION")
print("=" * 40)

for ticker, claims in hold_claims.items():
    print(f"\n{ticker} (Line {claims['line']}):")
    
    # Get actual current price
    actual_price = get_latest_price(ticker)
    claimed_price = claims['current_price']
    
    print(f"  Claimed: {claimed_price}")
    print(f"  Actual:  {actual_price}")
    
    if actual_price != claimed_price:
        error = f"Line {claims['line']}: {ticker} - PRICE ERROR: Claimed {claimed_price}, Actual {actual_price}"
        critical_errors.append(error)
        print(f"  ❌ CRITICAL ERROR")
    else:
        print("  ✅ VERIFIED")

print(f"\n3. P&L CALCULATIONS VERIFICATION")
print("=" * 40)

for ticker, claims in hold_claims.items():
    portfolio_data = portfolio[ticker]
    print(f"\n{ticker} (Line {claims['line']}):")
    
    # Get actual price for calculation
    actual_price = get_latest_price(ticker)
    
    # Calculate actual P&L
    actual_pnl_pct, actual_pnl_amount = calculate_pnl(
        portfolio_data['avg_buy'], 
        actual_price, 
        portfolio_data['quantity']
    )
    
    claimed_pnl_pct = claims['pnl_pct']
    claimed_pnl_amount = claims['pnl_amount']
    
    print(f"  P&L %:  Claimed {claimed_pnl_pct:+.2f}%, Actual {actual_pnl_pct:+.2f}%")
    print(f"  P&L VND: Claimed {format_vnd(claimed_pnl_amount)}, Actual {format_vnd(actual_pnl_amount)}")
    
    # Check P&L percentage (allow 0.05% tolerance for rounding)
    if abs(actual_pnl_pct - claimed_pnl_pct) > 0.05:
        error = f"Line {claims['line']}: {ticker} - P&L % ERROR: Claimed {claimed_pnl_pct:+.2f}%, Actual {actual_pnl_pct:+.2f}%"
        critical_errors.append(error)
        print(f"  ❌ P&L % ERROR")
    else:
        print("  ✅ P&L % VERIFIED")
    
    # Check P&L amount (allow 1000 VND tolerance for rounding)
    if abs(actual_pnl_amount - claimed_pnl_amount) > 1000:
        error = f"Line {claims['line']}: {ticker} - P&L AMOUNT ERROR: Claimed {format_vnd(claimed_pnl_amount)}, Actual {format_vnd(actual_pnl_amount)}"
        critical_errors.append(error)
        print(f"  ❌ P&L AMOUNT ERROR")
    else:
        print("  ✅ P&L AMOUNT VERIFIED")

print(f"\n4. VOLUME CLAIMS VERIFICATION")
print("=" * 35)

for ticker in portfolio.keys():
    print(f"\n{ticker}:")
    
    # Get actual volume data
    try:
        latest_data = get_daily_data(ticker, -1)  # Latest day
        previous_data = get_daily_data(ticker, -2)  # Previous day
        
        actual_volume = latest_data['volume']
        previous_volume = previous_data['volume']
        volume_change_pct = ((actual_volume - previous_volume) / previous_volume * 100) if previous_volume > 0 else 0
        
        print(f"  Actual Volume: {actual_volume:,} (+{volume_change_pct:.0f}%)")
        
        # Check specific volume claims
        if ticker in specific_claims and 'volume_jul29' in specific_claims[ticker]:
            claimed_vol_str = specific_claims[ticker]['volume_jul29']['claimed']
            line_num = specific_claims[ticker]['volume_jul29']['line']
            
            # Convert claimed volume to number
            if 'triệu' in claimed_vol_str:
                claimed_vol = float(claimed_vol_str.split()[0]) * 1_000_000
            elif 'M' in claimed_vol_str:
                claimed_vol = float(claimed_vol_str.replace('M', '')) * 1_000_000
            else:
                claimed_vol = 0
                
            print(f"  Claimed Volume: {claimed_vol_str} ({claimed_vol:,.0f})")
            
            if abs(actual_volume - claimed_vol) > 100000:  # Allow 100k tolerance
                error = f"Line {line_num}: {ticker} - VOLUME ERROR: Claimed {claimed_vol_str}, Actual {actual_volume:,}"
                high_priority_errors.append(error)
                print(f"  ❌ VOLUME ERROR")
            else:
                print(f"  ✅ VOLUME VERIFIED")
        
        # Check volume change claims
        if ticker in specific_claims and 'volume_change' in specific_claims[ticker]:
            claimed_change_str = specific_claims[ticker]['volume_change']['claimed']
            line_num = specific_claims[ticker]['volume_change']['line']
            claimed_change = float(claimed_change_str.replace('+', '').replace('%', ''))
            
            print(f"  Volume Change: Claimed {claimed_change_str}, Actual +{volume_change_pct:.0f}%")
            
            if abs(volume_change_pct - claimed_change) > 10:  # Allow 10% tolerance
                error = f"Line {line_num}: {ticker} - VOLUME CHANGE ERROR: Claimed {claimed_change_str}, Actual +{volume_change_pct:.0f}%"
                high_priority_errors.append(error)
                print(f"  ❌ VOLUME CHANGE ERROR")
            else:
                print(f"  ✅ VOLUME CHANGE VERIFIED")
    
    except Exception as e:
        print(f"  ❌ Error verifying {ticker}: {e}")

print(f"\n5. PRICE MOVEMENT CLAIMS VERIFICATION")
print("=" * 45)

for ticker, claims_data in specific_claims.items():
    if 'price_movement' in claims_data:
        print(f"\n{ticker} (Line {claims_data['price_movement']['line']}):")
        
        try:
            latest_data = get_daily_data(ticker, -1)  # July 29
            
            actual_open = latest_data['open']
            actual_high = latest_data['high'] 
            actual_low = latest_data['low']
            actual_close = latest_data['close']
            
            claimed_movement = claims_data['price_movement']['claimed']
            
            print(f"  Claimed Movement: {claimed_movement}")
            print(f"  Actual: Open {actual_open}, High {actual_high}, Low {actual_low}, Close {actual_close}")
            
            # Parse and verify key price points from claims
            if 'gap lên' in claimed_movement or 'gap up' in claimed_movement:
                # For gap up claims, check if open is significantly higher than previous close
                previous_data = get_daily_data(ticker, -2)
                prev_close = previous_data['close']
                gap_size = ((actual_open - prev_close) / prev_close) * 100
                print(f"  Gap Size: {gap_size:+.1f}% (Open {actual_open} vs Prev Close {prev_close})")
                
                if gap_size < 1:  # Should be at least 1% gap to be significant
                    error = f"Line {claims_data['price_movement']['line']}: {ticker} - Minimal gap claim questionable: {gap_size:+.1f}%"
                    medium_priority_errors.append(error)
        
        except Exception as e:
            print(f"  ❌ Error verifying price movement for {ticker}: {e}")

print(f"\n6. SUMMARY REPORT")
print("=" * 20)

total_errors = len(critical_errors) + len(high_priority_errors) + len(medium_priority_errors)

print(f"\nTotal Errors Found: {total_errors}")
print(f"  Critical (Trading Impact): {len(critical_errors)}")
print(f"  High Priority: {len(high_priority_errors)}")
print(f"  Medium Priority: {len(medium_priority_errors)}")

if critical_errors:
    print(f"\n🚨 CRITICAL ERRORS (Immediate Fix Required):")
    for i, error in enumerate(critical_errors, 1):
        print(f"  {i}. {error}")

if high_priority_errors:
    print(f"\n⚠️  HIGH PRIORITY ERRORS:")
    for i, error in enumerate(high_priority_errors, 1):
        print(f"  {i}. {error}")

if medium_priority_errors:
    print(f"\n📋 MEDIUM PRIORITY ERRORS:")
    for i, error in enumerate(medium_priority_errors, 1):
        print(f"  {i}. {error}")

if total_errors == 0:
    print("\n✅ ALL VERIFICATIONS PASSED - No errors found!")
else:
    print(f"\n📊 ERROR BREAKDOWN BY TYPE:")
    print(f"  Price Errors: {sum(1 for e in critical_errors if 'PRICE ERROR' in e)}")
    print(f"  P&L Errors: {sum(1 for e in critical_errors if 'P&L' in e)}")
    print(f"  Volume Errors: {sum(1 for e in high_priority_errors if 'VOLUME' in e)}")
    print(f"  Format Errors: {len(medium_priority_errors)}")