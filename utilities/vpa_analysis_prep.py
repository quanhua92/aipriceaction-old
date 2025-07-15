#!/usr/bin/env python3
"""
Script to analyze VPA data preparation for current date
"""

import csv
import os
import re
from datetime import datetime, timedelta

def read_csv_data(ticker, market_data_dir, target_date):
    """Read OHLCV data for a ticker"""
    csv_file = os.path.join(market_data_dir, f"{ticker}_2025-01-02_to_{target_date}.csv")
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
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get all tickers from market_data
    tickers = []
    for filename in os.listdir(market_data_dir):
        if filename.endswith('.csv'):
            ticker = filename.split('_')[0]
            tickers.append(ticker)
    
    tickers.sort()
    
    print(f"=== VPA Analysis Preparation Report for {today} ===")
    print(f"Total tickers found: {len(tickers)}")
    print()
    
    # Check each ticker
    need_analysis = []
    up_to_date = []
    missing_vpa = []
    
    for ticker in tickers:
        # Read market data
        market_data = read_csv_data(ticker, market_data_dir, today)
        if not market_data:
            continue
            
        # Check if today's data exists
        has_today_data = any(row['date'] == today for row in market_data)
        if not has_today_data:
            continue
            
        # Get latest VPA signal
        vpa_signal = get_latest_vpa_signal(ticker, vpa_data_dir)
        if not vpa_signal:
            missing_vpa.append(ticker)
            continue
            
        # Check if already has today's analysis
        if vpa_signal['date'] == today:
            up_to_date.append(ticker)
        else:
            # Extract today's and last 7 days of data
            today_data = next((row for row in market_data if row['date'] == today), None)
            
            # Get last 7 days of data
            last_7_days = []
            today_date = datetime.strptime(today, '%Y-%m-%d')
            for i in range(1, 8):  # Get previous 7 days
                target_date = (today_date - timedelta(days=i)).strftime('%Y-%m-%d')
                day_data = next((row for row in market_data if row['date'] == target_date), None)
                if day_data:
                    last_7_days.append(day_data)
            
            need_analysis.append({
                'ticker': ticker,
                'today_data': today_data,
                'last_7_days': last_7_days,
                'latest_vpa': vpa_signal
            })
    
    print(f"SUMMARY:")
    print(f"- Tickers needing new VPA analysis: {len(need_analysis)}")
    print(f"- Tickers up-to-date: {len(up_to_date)}")
    print(f"- Tickers missing VPA files: {len(missing_vpa)}")
    print()
    
    if up_to_date:
        print(f"Tickers already up-to-date (have {today} entry):")
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
        today_data = item['today_data']
        last_7_days = item['last_7_days']
        vpa = item['latest_vpa']
        
        print(f"=== {ticker} ===")
        print(f"Today's data ({today}): O={today_data['open']}, H={today_data['high']}, L={today_data['low']}, C={today_data['close']}, V={today_data['volume']:,}")
        
        print("Last 7 days data:")
        for day_data in last_7_days:
            print(f"  {day_data['date']}: O={day_data['open']}, H={day_data['high']}, L={day_data['low']}, C={day_data['close']}, V={day_data['volume']:,}")
        
        print(f"Latest VPA signal ({vpa['date']}): {vpa['signal']}")
        print()
    
    print(f"Total tickers needing analysis: {len(need_analysis)}")

if __name__ == "__main__":
    main()