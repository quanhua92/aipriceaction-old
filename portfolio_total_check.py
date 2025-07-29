#!/usr/bin/env python3

import pandas as pd

def check_portfolio_total():
    """Check the total portfolio P&L claim on line 23"""
    
    print("=== PORTFOLIO TOTAL P&L VERIFICATION ===\n")
    
    # Portfolio holdings
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
    
    def get_latest_price(ticker):
        try:
            df = pd.read_csv(f"market_data/{ticker}_2025-01-02_to_2025-07-29.csv")
            return df.iloc[-1]['close']
        except:
            return None
    
    total_cost = 0
    total_current_value = 0
    total_pnl = 0
    
    print("Individual P&L Breakdown:")
    print("=" * 40)
    
    for ticker, data in portfolio.items():
        current_price = get_latest_price(ticker)
        cost = data['avg_buy'] * data['quantity']
        current_value = current_price * data['quantity']
        pnl = current_value - cost
        pnl_pct = (pnl / cost) * 100
        
        total_cost += cost
        total_current_value += current_value
        total_pnl += pnl
        
        print(f"{ticker}: {pnl:+,.0f} VND ({pnl_pct:+.2f}%)")
    
    total_pnl_pct = (total_pnl / total_cost) * 100
    
    print(f"\nCalculated Portfolio Total:")
    print(f"Total Cost: {total_cost:,.0f} VND")
    print(f"Total Current Value: {total_current_value:,.0f} VND")
    print(f"Total P&L: {total_pnl:+,.0f} VND ({total_pnl_pct:+.2f}%)")
    
    # Claimed on line 23: +2.389.000 VND (+0.74%)
    claimed_pnl = 2389000
    claimed_pct = 0.74
    
    print(f"\nClaimed (Line 23): +{claimed_pnl:,} VND (+{claimed_pct}%)")
    
    if abs(total_pnl - claimed_pnl) > 10000:
        print(f"❌ TOTAL P&L ERROR: Claimed +{claimed_pnl:,}, Actual {total_pnl:+,.0f}")
    else:
        print("✅ Total P&L amount verified")
        
    if abs(total_pnl_pct - claimed_pct) > 0.1:
        print(f"❌ TOTAL P&L % ERROR: Claimed +{claimed_pct}%, Actual {total_pnl_pct:+.2f}%")
    else:
        print("✅ Total P&L percentage verified")

if __name__ == "__main__":
    check_portfolio_total()