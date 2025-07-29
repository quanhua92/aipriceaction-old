#!/usr/bin/env python3

import pandas as pd
import os
import math

# Portfolio data from hold.md
portfolio = {
    'CTS': {'avg_buy': 39.228, 'quantity': 900},
    'HDB': {'avg_buy': 27.560, 'quantity': 1500},
    'HDC': {'avg_buy': 33.320, 'quantity': 500},
    'SHB': {'avg_buy': 15.514, 'quantity': 1800},
    'SSI': {'avg_buy': 32.994, 'quantity': 1700},
    'TCH': {'avg_buy': 25.719, 'quantity': 400},
    'VIX': {'avg_buy': 24.109, 'quantity': 900},
    'VND': {'avg_buy': 19.731, 'quantity': 3500},
    'VPB': {'avg_buy': 23.368, 'quantity': 2000}
}

# Claims from hold.md to verify
hold_claims = {
    'CTS': {'current_price': 39.55, 'pnl_pct': 0.82, 'pnl_amount': 289000},
    'HDB': {'current_price': 26.50, 'pnl_pct': -3.85, 'pnl_amount': -1590000},
    'HDC': {'current_price': 32.35, 'pnl_pct': -2.91, 'pnl_amount': -485000},
    'SHB': {'current_price': 15.05, 'pnl_pct': -2.99, 'pnl_amount': -835000},
    'SSI': {'current_price': 33.30, 'pnl_pct': 0.93, 'pnl_amount': 520000},
    'TCH': {'current_price': 24.60, 'pnl_pct': -4.35, 'pnl_amount': -447000},
    'VIX': {'current_price': 23.95, 'pnl_pct': -0.66, 'pnl_amount': -143000},
    'VND': {'current_price': 21.05, 'pnl_pct': 6.68, 'pnl_amount': 4616000},
    'VPB': {'current_price': 23.60, 'pnl_pct': 0.99, 'pnl_amount': 464000}
}

def get_latest_price(ticker):
    """Get latest closing price from CSV"""
    try:
        file_path = f"market_data/{ticker}_2025-01-02_to_2025-07-29.csv"
        df = pd.read_csv(file_path)
        return df.iloc[-1]['close']
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

print("=== COMPREHENSIVE VERIFICATION OF hold.md ===\n")
print("Portfolio Holdings Verification:")
print("================================")

errors = []
total_errors = 0

for ticker, data in portfolio.items():
    print(f"\n{ticker}:")
    print(f"  Average Buy Price: {data['avg_buy']}")
    print(f"  Quantity: {data['quantity']}")
    
    # Get actual current price
    actual_price = get_latest_price(ticker)
    claimed_price = hold_claims[ticker]['current_price']
    
    print(f"  Claimed Current Price: {claimed_price}")
    print(f"  Actual Current Price: {actual_price}")
    
    if actual_price != claimed_price:
        error_msg = f"PRICE ERROR - {ticker}: Claimed {claimed_price}, Actual {actual_price}"
        errors.append(error_msg)
        print(f"  ❌ {error_msg}")
        total_errors += 1
    else:
        print("  ✅ Current price matches")
    
    # Calculate actual P&L
    actual_pnl_pct, actual_pnl_amount = calculate_pnl(data['avg_buy'], actual_price, data['quantity'])
    claimed_pnl_pct = hold_claims[ticker]['pnl_pct']
    claimed_pnl_amount = hold_claims[ticker]['pnl_amount']
    
    print(f"  Claimed P&L: {claimed_pnl_pct:+.2f}% ({format_vnd(claimed_pnl_amount)})")
    print(f"  Actual P&L: {actual_pnl_pct:+.2f}% ({format_vnd(actual_pnl_amount)})")
    
    # Check P&L percentage (allow small rounding differences)
    if abs(actual_pnl_pct - claimed_pnl_pct) > 0.05:
        error_msg = f"P&L PCT ERROR - {ticker}: Claimed {claimed_pnl_pct:+.2f}%, Actual {actual_pnl_pct:+.2f}%"
        errors.append(error_msg)
        print(f"  ❌ {error_msg}")
        total_errors += 1
    else:
        print("  ✅ P&L percentage matches")
    
    # Check P&L amount (allow small rounding differences for VND formatting)
    if abs(actual_pnl_amount - claimed_pnl_amount) > 1000:
        error_msg = f"P&L AMOUNT ERROR - {ticker}: Claimed {format_vnd(claimed_pnl_amount)}, Actual {format_vnd(actual_pnl_amount)}"
        errors.append(error_msg)
        print(f"  ❌ {error_msg}")
        total_errors += 1
    else:
        print("  ✅ P&L amount matches")

print(f"\n=== SUMMARY ===")
print(f"Total Errors Found: {total_errors}")
if errors:
    print("\nAll Errors:")
    for i, error in enumerate(errors, 1):
        print(f"{i}. {error}")
else:
    print("✅ All basic portfolio data verified correctly!")

# Now check volume claims and other specific claims
print(f"\n=== VOLUME AND OTHER CLAIMS VERIFICATION ===")

# Volume checks for July 29, 2025
volume_claims = {
    'CTS': {'claimed_volume': '8.72 triệu', 'claimed_change': '+100%'},
    'SHB': {'claimed_volume': '152.87M', 'claimed_change': None},
    'HDC': {'claimed_volume': '16.74 triệu', 'claimed_change': '+156%'},
    'SSI': {'claimed_volume': '104.97M', 'claimed_change': None},
    'TCH': {'claimed_volume': None, 'claimed_change': '+103%'},
    'VIX': {'claimed_volume': '118.78M', 'claimed_change': '+260%'},
    'VND': {'claimed_volume': None, 'claimed_change': '+142%'}
}

print("\nVolume Claims Verification:")
for ticker in ['CTS', 'HDB', 'HDC', 'SHB', 'SSI', 'TCH', 'VIX', 'VND', 'VPB']:
    try:
        df = pd.read_csv(f"market_data/{ticker}_2025-01-02_to_2025-07-29.csv")
        latest_volume = df.iloc[-1]['volume']
        previous_volume = df.iloc[-2]['volume'] if len(df) > 1 else 0
        
        volume_change_pct = ((latest_volume - previous_volume) / previous_volume * 100) if previous_volume > 0 else 0
        
        print(f"{ticker}: Volume {latest_volume:,} (+{volume_change_pct:.0f}%)")
        
        if ticker in volume_claims and volume_claims[ticker]['claimed_volume']:
            claimed_vol_str = volume_claims[ticker]['claimed_volume']
            # Convert claimed volume to number
            if 'triệu' in claimed_vol_str:
                claimed_vol = float(claimed_vol_str.split()[0]) * 1_000_000
            elif 'M' in claimed_vol_str:
                claimed_vol = float(claimed_vol_str.replace('M', '')) * 1_000_000
            else:
                claimed_vol = 0
                
            if claimed_vol > 0 and abs(latest_volume - claimed_vol) > 100000:
                error_msg = f"VOLUME ERROR - {ticker}: Claimed {claimed_vol_str}, Actual {latest_volume:,}"
                errors.append(error_msg)
                print(f"  ❌ {error_msg}")
                total_errors += 1
                
    except Exception as e:
        print(f"Error checking {ticker}: {e}")

print(f"\n=== FINAL SUMMARY ===") 
print(f"Total Errors Found: {total_errors}")