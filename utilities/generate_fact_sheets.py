#!/usr/bin/env python3
"""
Fact Sheet Generator for Daily Planning Protocol

This utility generates verified fact sheets for all tickers mentioned in PLAN.md,
following the exact protocol defined in tasks/DAILY_PLAN.md.

Usage:
    python generate_fact_sheets.py
    
Output:
    fact_sheets.json - JSON file containing all ticker fact sheets
"""

import json
import os
import csv
import re
from datetime import datetime
from pathlib import Path

def read_plan_md():
    """Extract all tickers from existing PLAN.md and their current states"""
    try:
        with open('PLAN.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        tickers = {}
        
        # Extract Top List tickers
        top_section = re.search(r'## 2\. Top 1[0-9x]+ Cơ Hội Giao Dịch.*?(?=##|\Z)', content, re.DOTALL)
        if top_section:
            top_matches = re.findall(r'\*\*([A-Z]{3})\*\*', top_section.group(0))
            for ticker in top_matches:
                tickers[ticker] = "Top List"
        
        # Extract Potential List tickers
        potential_section = re.search(r'## 3\. Danh Sách Cổ Phiếu Tiềm Năng.*?(?=##|\Z)', content, re.DOTALL)
        if potential_section:
            potential_matches = re.findall(r'\*\*([A-Z]{3})\*\*', potential_section.group(0))
            for ticker in potential_matches:
                tickers[ticker] = "Potential List"
        
        # Extract Downgraded tickers
        downgraded_section = re.search(r'## 4\. Danh Sách Cổ Phiếu Bị Hạ Ưu Tiên.*?(?=##|\Z)', content, re.DOTALL)
        if downgraded_section:
            downgraded_matches = re.findall(r'\*\*([A-Z]{3})\*\*', downgraded_section.group(0))
            for ticker in downgraded_matches:
                tickers[ticker] = "Downgraded"
        
        return tickers
    
    except FileNotFoundError:
        print("PLAN.md not found, treating all tickers as Unlisted")
        return {}

def get_current_price(ticker):
    """Get current price from market_data CSV file"""
    try:
        # Find the CSV file for this ticker
        market_files = list(Path('market_data').glob(f'{ticker}_*.csv'))
        if not market_files:
            return None
        
        # Read the last row of the most recent file
        csv_file = market_files[0]  # Should be only one file per ticker
        
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            if rows:
                return float(rows[-1]['Close'])
        
        return None
    except:
        return None

def extract_daily_signal(ticker, report_content):
    """Extract most recent daily signal for ticker from REPORT.md"""
    try:
        # Find ticker section
        ticker_pattern = rf'### {ticker}\n(.*?)(?=### [A-Z]{{3}}|\Z)'
        ticker_match = re.search(ticker_pattern, report_content, re.DOTALL)
        
        if not ticker_match:
            return {"signal": "No Signal", "date": "N/A"}
        
        ticker_section = ticker_match.group(1)
        
        # Look for signal patterns with dates
        signal_patterns = [
            r'(\d{4}-\d{2}-\d{2}): (SOS|Sign of Strength|Effort to Rise|No Demand|Sign of Weakness|SOW|Test for Supply|No Supply)',
            r'(\d{4}-\d{2}-\d{2}).*?(SOS|Sign of Strength|Effort to Rise|No Demand|Sign of Weakness|SOW|Test for Supply|No Supply)'
        ]
        
        latest_date = None
        latest_signal = "No Signal"
        
        for pattern in signal_patterns:
            matches = re.findall(pattern, ticker_section, re.IGNORECASE)
            for match in matches:
                date_str = match[0]
                signal = match[1]
                
                if not latest_date or date_str > latest_date:
                    latest_date = date_str
                    latest_signal = signal
        
        return {
            "signal": latest_signal,
            "date": latest_date if latest_date else "N/A"
        }
    
    except:
        return {"signal": "No Signal", "date": "N/A"}

def extract_weekly_context(ticker, report_week_content):
    """Extract weekly context for ticker from REPORT_week.md"""
    try:
        # Find ticker section
        ticker_pattern = rf'### {ticker}\n(.*?)(?=### [A-Z]{{3}}|\Z)'
        ticker_match = re.search(ticker_pattern, report_week_content, re.DOTALL)
        
        if not ticker_match:
            return {"signal": "No Signal", "week_ending_date": "N/A"}
        
        ticker_section = ticker_match.group(1)
        
        # Look for weekly signal patterns
        signal_patterns = [
            r'Week ending (\d{4}-\d{2}-\d{2}): (SOS Bar|Upthrust|Effort to Rise|No Demand|Test for Supply|No Supply)',
            r'(\d{4}-\d{2}-\d{2}).*?(SOS Bar|Upthrust|Effort to Rise|No Demand|Test for Supply|No Supply)'
        ]
        
        latest_date = None
        latest_signal = "No Signal"
        
        for pattern in signal_patterns:
            matches = re.findall(pattern, ticker_section, re.IGNORECASE)
            for match in matches:
                date_str = match[0]
                signal = match[1]
                
                if not latest_date or date_str > latest_date:
                    latest_date = date_str
                    latest_signal = signal
        
        return {
            "signal": latest_signal,
            "week_ending_date": latest_date if latest_date else "N/A"
        }
    
    except:
        return {"signal": "No Signal", "week_ending_date": "N/A"}

def get_daily_narrative(ticker):
    """Get daily narrative context from vpa_data ticker file"""
    try:
        vpa_file = Path(f'vpa_data/{ticker}.md')
        if not vpa_file.exists():
            return "No VPA data available"
        
        with open(vpa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Get last 10 entries (lines that start with date)
        lines = content.split('\n')
        date_lines = [line for line in lines if re.match(r'^\d{4}-\d{2}-\d{2}:', line)]
        
        if len(date_lines) >= 3:
            recent_entries = date_lines[-5:]  # Last 5 entries
            return " ".join(recent_entries)
        elif date_lines:
            return " ".join(date_lines)
        else:
            return "No recent VPA entries"
    
    except:
        return "Error reading VPA data"

def get_industry_info(ticker):
    """Get industry group and status from GROUP.md and LEADER.md"""
    try:
        # Read GROUP.md to get industry mapping
        with open('GROUP.md', 'r', encoding='utf-8') as f:
            group_content = f.read()
        
        # Find which industry group contains this ticker
        industry_group = "Unknown"
        group_matches = re.findall(r'## ([^#\n]+)\n(.*?)(?=## |\Z)', group_content, re.DOTALL)
        
        for group_name, group_content in group_matches:
            if ticker in group_content:
                industry_group = group_name.strip()
                break
        
        # Read LEADER.md to get industry status
        with open('LEADER.md', 'r', encoding='utf-8') as f:
            leader_content = f.read()
        
        industry_status = "Unknown"
        # Look for status patterns in LEADER.md
        status_patterns = [
            rf'{re.escape(industry_group)}.*?(Dẫn dắt|Đồng Thuận|Yếu|Phân Phối)',
            rf'{re.escape(industry_group)}.*?(Leading|Consensus|Weak|Distribution)'
        ]
        
        for pattern in status_patterns:
            match = re.search(pattern, leader_content, re.IGNORECASE)
            if match:
                industry_status = match.group(1)
                break
        
        return industry_group, industry_status
    
    except:
        return "Unknown", "Unknown"

def generate_fact_sheet(ticker, previous_state, report_content, report_week_content):
    """Generate fact sheet for a single ticker"""
    fact_sheet = {
        "ticker": ticker,
        "previous_state": previous_state,
        "current_price": get_current_price(ticker),
        "most_recent_daily_signal": extract_daily_signal(ticker, report_content),
        "daily_narrative_context": get_daily_narrative(ticker),
        "weekly_context": extract_weekly_context(ticker, report_week_content),
        "industry_group": None,
        "industry_status": None
    }
    
    # Get industry information
    industry_group, industry_status = get_industry_info(ticker)
    fact_sheet["industry_group"] = industry_group
    fact_sheet["industry_status"] = industry_status
    
    return fact_sheet

def main():
    """Main function to generate all fact sheets"""
    print("Generating fact sheets for daily planning protocol...")
    
    # Read existing ticker states from PLAN.md
    existing_tickers = read_plan_md()
    
    # Read ALL tickers from TICKERS.csv
    all_tickers = set()
    try:
        with open('TICKERS.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ticker = row['ticker'].strip()
                if ticker != 'VNINDEX':  # Skip VNINDEX from ticker processing
                    all_tickers.add(ticker)
    except FileNotFoundError:
        print("ERROR: TICKERS.csv not found")
        return
    
    # Read report contents
    try:
        with open('REPORT.md', 'r', encoding='utf-8') as f:
            report_content = f.read()
    except FileNotFoundError:
        print("ERROR: REPORT.md not found")
        return
    
    try:
        with open('REPORT_week.md', 'r', encoding='utf-8') as f:
            report_week_content = f.read()
    except FileNotFoundError:
        print("ERROR: REPORT_week.md not found")
        return
    
    # Generate fact sheets for ALL tickers from TICKERS.csv
    fact_sheets = {}
    
    for ticker in sorted(all_tickers):
        # Determine previous state (default to "Unlisted" if not in PLAN.md)
        previous_state = existing_tickers.get(ticker, "Unlisted")
        
        print(f"Processing {ticker} (Previous: {previous_state})")
        fact_sheet = generate_fact_sheet(ticker, previous_state, report_content, report_week_content)
        fact_sheets[ticker] = fact_sheet
    
    # Write fact sheets to JSON file
    output_file = 'utilities/fact_sheets.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fact_sheets, f, indent=2, ensure_ascii=False)
    
    print(f"\nFact sheets generated successfully!")
    print(f"Total tickers processed: {len(fact_sheets)}")
    print(f"Output file: {output_file}")
    
    # Print summary
    states = {}
    for ticker, fact_sheet in fact_sheets.items():
        state = fact_sheet['previous_state']
        if state not in states:
            states[state] = []
        states[state].append(ticker)
    
    print("\nSummary by previous state:")
    for state, tickers in states.items():
        print(f"  {state}: {len(tickers)} tickers - {', '.join(tickers)}")

if __name__ == "__main__":
    main()