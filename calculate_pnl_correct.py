#!/usr/bin/env python3
"""
Correct P&L calculation script that:
1. Reads portfolio from hold.md table
2. Gets current prices from last row of each ticker's CSV in market_data/
"""

import re
import csv
import os
from pathlib import Path

def format_vnd(amount):
    """Format VND amount with Vietnamese dot separators (e.g., 28.085.600)"""
    if amount == 0:
        return "0"
    
    # Convert to integer for formatting
    amount_int = int(abs(amount))
    
    # Convert to string and reverse for easier processing
    amount_str = str(amount_int)[::-1]
    
    # Add dots every 3 digits
    formatted_parts = []
    for i in range(0, len(amount_str), 3):
        formatted_parts.append(amount_str[i:i+3])
    
    # Join with dots and reverse back
    formatted = '.'.join(formatted_parts)[::-1]
    
    # Add sign if negative
    if amount < 0:
        formatted = '-' + formatted
    
    return formatted

def read_portfolio_from_hold_md():
    """Read portfolio data from hold.md table"""
    hold_path = Path('hold.md')
    
    if not hold_path.exists():
        print("Error: hold.md not found")
        return []
    
    with open(hold_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract table data using regex - more precise pattern
    table_pattern = r'\| ([A-Z]{3})\s+\| ([0-9.]+)\s+\| ([0-9]+)\s+\|'
    matches = re.findall(table_pattern, content)
    
    portfolio = []
    for match in matches:
        ticker = match[0].strip()
        avg_price = float(match[1])
        quantity = int(match[2])
        portfolio.append({
            'ticker': ticker,
            'avg_price': avg_price,
            'quantity': quantity
        })
    
    return portfolio

def get_current_price_from_csv(ticker):
    """Get current price from last row of ticker's CSV file"""
    csv_path = Path(f'market_data/{ticker}_2025-01-02_to_2025-07-28.csv')
    
    if not csv_path.exists():
        print(f"Warning: CSV file not found for {ticker}")
        return None
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            last_row = None
            for row in reader:
                last_row = row
            
            if last_row:
                return float(last_row['close'])
            else:
                print(f"Warning: No data found in CSV for {ticker}")
                return None
                
    except Exception as e:
        print(f"Error reading CSV for {ticker}: {e}")
        return None

def calculate_portfolio_pnl(portfolio):
    """Calculate P&L for entire portfolio"""
    print("=" * 90)
    print("CORRECT PORTFOLIO P&L CALCULATION")
    print("=" * 90)
    print(f"{'Ticker':<6} | {'Avg Price':<9} | {'Qty':<6} | {'Current':<8} | {'Investment':<12} | {'Current Val':<12} | {'P&L VND':<12} | {'P&L %':<8}")
    print("-" * 90)
    
    total_investment = 0
    total_current_value = 0
    results = []
    
    for position in portfolio:
        ticker = position['ticker']
        avg_price = position['avg_price']
        quantity = position['quantity']
        
        # Get current price from CSV
        current_price = get_current_price_from_csv(ticker)
        
        if current_price is None:
            print(f"Skipping {ticker} - no current price available")
            continue
        
        # Calculate values
        investment_value = avg_price * quantity
        current_value = current_price * quantity
        pnl_vnd = current_value - investment_value
        pnl_pct = (pnl_vnd / investment_value) * 100
        
        total_investment += investment_value
        total_current_value += current_value
        
        results.append({
            'ticker': ticker,
            'avg_price': avg_price,
            'quantity': quantity,
            'current_price': current_price,
            'investment_value': investment_value,
            'current_value': current_value,
            'pnl_vnd': pnl_vnd,
            'pnl_pct': pnl_pct
        })
        
        print(f"{ticker:<6} | {avg_price:>9.3f} | {quantity:>6} | {current_price:>8.2f} | {format_vnd(investment_value):>12} | {format_vnd(current_value):>12} | {format_vnd(pnl_vnd):>12} | {pnl_pct:>7.2f}%")
    
    total_pnl = total_current_value - total_investment
    total_pnl_pct = (total_pnl / total_investment) * 100 if total_investment > 0 else 0
    
    print("-" * 90)
    print(f"TOTAL INVESTMENT:     {format_vnd(total_investment):>15} VND")
    print(f"CURRENT VALUE:        {format_vnd(total_current_value):>15} VND")
    print(f"TOTAL P&L:            {format_vnd(total_pnl):>15} VND ({total_pnl_pct:>6.2f}%)")
    print("=" * 90)
    
    return results, {
        'total_investment': total_investment,
        'total_current_value': total_current_value,
        'total_pnl': total_pnl,
        'total_pnl_pct': total_pnl_pct
    }

def generate_hold_md_format(results):
    """Generate formatted P&L lines for hold.md"""
    print("\n" + "=" * 90)
    print("FORMATTED OUTPUT FOR hold.md UPDATE")
    print("=" * 90)
    
    for result in results:
        ticker = result['ticker']
        pnl_pct = result['pnl_pct']
        pnl_vnd = result['pnl_vnd']
        current_price = result['current_price']
        
        sign = "+" if pnl_vnd >= 0 else ""
        print(f"{ticker}: Current Price = {current_price:.2f}")
        print(f"* **P&L (Lợi Nhuận/Thua Lỗ Chưa Thực Hiện):** {sign}{pnl_pct:.2f}% ({sign}{format_vnd(pnl_vnd)}.000)")
        print()

def main():
    # Read portfolio from hold.md
    portfolio = read_portfolio_from_hold_md()
    
    if not portfolio:
        print("No portfolio data found!")
        return
    
    print(f"Found {len(portfolio)} positions in portfolio:")
    for p in portfolio:
        print(f"  {p['ticker']}: {p['quantity']} shares @ {p['avg_price']:.3f}")
    
    print()
    
    # Calculate P&L
    results, summary = calculate_portfolio_pnl(portfolio)
    
    # Generate hold.md format
    generate_hold_md_format(results)

if __name__ == "__main__":
    main()