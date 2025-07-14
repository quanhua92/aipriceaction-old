#!/usr/bin/env python3
"""
Script to analyze VPA data preparation for 2025-07-14
"""

import csv
import os
import re
from datetime import datetime, timedelta

def read_csv_data(ticker, market_data_dir):
    """Read OHLCV data for a ticker"""
    csv_file = os.path.join(market_data_dir, f"{ticker}_2025-01-02_to_2025-07-14.csv")
    if not os.path.exists(csv_file):
        return None
    
    data = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 6:
                ticker_name, date, open_price, high, low, close, volume = row
                # Skip header row
                if open_price == 'open':
                    continue
                data.append({
                    'ticker': ticker_name,
                    'date': date,
                    'open': float(open_price),
                    'high': float(high),
                    'low': float(low),
                    'close': float(close),
                    'volume': int(volume)
                })
    return data

def get_latest_vpa_signal(ticker, vpa_data_dir):
    """Extract the latest VPA signal from a ticker's VPA file"""
    vpa_file = os.path.join(vpa_data_dir, f"{ticker}.md")
    if not os.path.exists(vpa_file):
        return None
    
    with open(vpa_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the latest date entry
    date_pattern = r'- \*\*Ngày (\d{4}-\d{2}-\d{2}):\*\*'
    dates = re.findall(date_pattern, content)
    if not dates:
        return None
    
    latest_date = max(dates)
    
    # Extract the analysis for the latest date
    # Find the section starting with the latest date
    latest_section_pattern = rf'- \*\*Ngày {re.escape(latest_date)}:\*\*.*?(?=- \*\*Ngày|\Z)'
    match = re.search(latest_section_pattern, content, re.DOTALL)
    if not match:
        return None
    
    section_content = match.group(0)
    
    # Extract VPA signal from the analysis
    vpa_pattern = r'\*\*([^*]+)\*\*'
    vpa_signals = re.findall(vpa_pattern, section_content)
    
    # Filter for known VPA signals
    known_signals = [
        'Sign of Strength', 'SOS', 'Sign of Weakness', 'SOW',
        'Test for Supply', 'Test for Demand', 'Effort to Rise',
        'Effort to Fall', 'No Demand', 'No Supply', 'Stopping Volume',
        'Climax', 'Absorption', 'Support', 'Resistance'
    ]
    
    main_signal = None
    for signal in vpa_signals:
        if any(known in signal for known in known_signals):
            main_signal = signal
            break
    
    return {
        'date': latest_date,
        'signal': main_signal,
        'full_analysis': section_content.strip()
    }

def main():
    base_dir = '/Volumes/data/workspace/aipriceaction'
    market_data_dir = os.path.join(base_dir, 'market_data')
    vpa_data_dir = os.path.join(base_dir, 'vpa_data')
    
    # Get all tickers from market_data
    tickers = []
    for filename in os.listdir(market_data_dir):
        if filename.endswith('.csv') and not filename.startswith('VNINDEX'):
            ticker = filename.split('_')[0]
            tickers.append(ticker)
    
    tickers.sort()
    
    print(f"=== VPA Analysis Preparation Report for 2025-07-14 ===")
    print(f"Total tickers found: {len(tickers)}")
    print()
    
    # Check each ticker
    need_analysis = []
    up_to_date = []
    missing_vpa = []
    
    for ticker in tickers:
        # Read market data
        market_data = read_csv_data(ticker, market_data_dir)
        if not market_data:
            continue
            
        # Check if 2025-07-14 data exists
        has_today_data = any(row['date'] == '2025-07-14' for row in market_data)
        if not has_today_data:
            continue
            
        # Get latest VPA signal
        vpa_signal = get_latest_vpa_signal(ticker, vpa_data_dir)
        if not vpa_signal:
            missing_vpa.append(ticker)
            continue
            
        # Check if already has 2025-07-14 analysis
        if vpa_signal['date'] == '2025-07-14':
            up_to_date.append(ticker)
        else:
            # Extract today's and previous day's data
            today_data = next((row for row in market_data if row['date'] == '2025-07-14'), None)
            prev_data = next((row for row in reversed(market_data) if row['date'] < '2025-07-14'), None)
            
            need_analysis.append({
                'ticker': ticker,
                'today_data': today_data,
                'prev_data': prev_data,
                'latest_vpa': vpa_signal
            })
    
    print(f"SUMMARY:")
    print(f"- Tickers needing new VPA analysis: {len(need_analysis)}")
    print(f"- Tickers up-to-date: {len(up_to_date)}")
    print(f"- Tickers missing VPA files: {len(missing_vpa)}")
    print()
    
    if up_to_date:
        print("Tickers already up-to-date (have 2025-07-14 entry):")
        for ticker in up_to_date:
            print(f"  - {ticker}")
        print()
    
    if missing_vpa:
        print("Tickers missing VPA files:")
        for ticker in missing_vpa:
            print(f"  - {ticker}")
        print()
    
    print("TICKERS NEEDING ANALYSIS:")
    print()
    
    for item in need_analysis:  # Show all tickers
        ticker = item['ticker']
        today = item['today_data']
        prev = item['prev_data']
        vpa = item['latest_vpa']
        
        print(f"=== {ticker} ===")
        print(f"Today's data (2025-07-14): O={today['open']}, H={today['high']}, L={today['low']}, C={today['close']}, V={today['volume']:,}")
        print(f"Previous data ({prev['date']}): O={prev['open']}, H={prev['high']}, L={prev['low']}, C={prev['close']}, V={prev['volume']:,}")
        print(f"Latest VPA signal ({vpa['date']}): {vpa['signal']}")
        print()
    
    print(f"Total tickers needing analysis: {len(need_analysis)}")

if __name__ == "__main__":
    main()