#!/usr/bin/env python3
"""
Weekly VPA Verification Script
Validates VPA analysis accuracy and consistency for weekly data.
"""

import os
import re
import csv
import glob
from datetime import datetime
from typing import List, Dict, Set, Tuple

class VPAVerifier:
    def __init__(self):
        self.vpa_dir = "vpa_data_week"
        self.market_data_dir = "market_data_week"
        self.issues = []
        
        # VPA signals for validation
        self.valid_signals = {
            "Sign of Strength", "Sign of Weakness", "No Demand", "No Supply",
            "Effort to Rise", "Effort to Fall", "Test for Supply", "Test for Demand",
            "Stopping Volume", "Climax", "Upthrust", "Spring"
        }
        
        # Vietnamese financial terms
        self.vn_terms = {
            "tăng", "giảm", "nến", "tuần", "khối lượng", "giao dịch", 
            "biên độ", "lực cầu", "lực bán", "xu hướng", "phục hồi",
            "tiếp nối", "tín hiệu", "phân tích", "triệu", "đơn vị"
        }

    def verify_all_tickers(self) -> List[str]:
        """Verify all VPA files and return list of issues."""
        self.issues = []
        
        if not os.path.exists(self.vpa_dir):
            self.issues.append(f"ERROR: VPA directory {self.vpa_dir} does not exist")
            return self.issues
        
        vpa_files = glob.glob(f"{self.vpa_dir}/*.md")
        
        if not vpa_files:
            self.issues.append(f"WARNING: No VPA files found in {self.vpa_dir}")
            return self.issues
        
        print(f"Verifying {len(vpa_files)} VPA files...")
        
        for vpa_file in vpa_files:
            ticker = os.path.basename(vpa_file).replace('.md', '')
            self.verify_ticker(ticker, vpa_file)
        
        return self.issues
    
    def verify_ticker(self, ticker: str, vpa_file: str):
        """Verify individual ticker VPA analysis."""
        try:
            with open(vpa_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if file is empty
            if not content.strip():
                self.issues.append(f"{ticker}: Empty VPA file")
                return
            
            # Verify date format and chronological order
            self.verify_dates(ticker, content)
            
            # Verify VPA signals
            self.verify_vpa_signals(ticker, content)
            
            # Verify price data consistency
            self.verify_price_data(ticker, content)
            
            # Verify Vietnamese language usage
            self.verify_vietnamese_usage(ticker, content)
            
            # Verify number formatting
            self.verify_number_formatting(ticker, content)
            
        except Exception as e:
            self.issues.append(f"{ticker}: Error reading file - {str(e)}")
    
    def verify_dates(self, ticker: str, content: str):
        """Verify date formatting and chronological order."""
        date_pattern = r'\*\*Ngày (\d{4}-\d{2}-\d{2}):\*\*'
        dates = re.findall(date_pattern, content)
        
        if not dates:
            self.issues.append(f"{ticker}: No valid date entries found")
            return
        
        # Check date format and order
        parsed_dates = []
        for date_str in dates:
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                parsed_dates.append((date_str, date_obj))
            except ValueError:
                self.issues.append(f"{ticker}: Invalid date format: {date_str}")
        
        # Check chronological order
        for i in range(1, len(parsed_dates)):
            if parsed_dates[i][1] <= parsed_dates[i-1][1]:
                self.issues.append(f"{ticker}: Dates not in chronological order: {parsed_dates[i-1][0]} -> {parsed_dates[i][0]}")
    
    def verify_vpa_signals(self, ticker: str, content: str):
        """Verify VPA/Wyckoff signals are valid."""
        signal_pattern = r'\*\*Phân tích VPA/Wyckoff:\*\*.*?\*\*([^*]+)\*\*'
        signals = re.findall(signal_pattern, content, re.DOTALL)
        
        for signal in signals:
            signal_clean = signal.strip()
            if signal_clean not in self.valid_signals:
                # Check if it's a partial match
                found_valid = False
                for valid_signal in self.valid_signals:
                    if valid_signal.lower() in signal_clean.lower():
                        found_valid = True
                        break
                
                if not found_valid:
                    self.issues.append(f"{ticker}: Invalid VPA signal: '{signal_clean}'")
    
    def verify_price_data(self, ticker: str, content: str):
        """Verify price data consistency with market data CSV."""
        market_file = None
        for file in glob.glob(f"{self.market_data_dir}/{ticker}_*.csv"):
            market_file = file
            break
        
        if not market_file:
            self.issues.append(f"{ticker}: No market data file found")
            return
        
        try:
            # Read market data
            market_dates = {}
            with open(market_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    date = row['time']
                    market_dates[date] = {
                        'open': float(row['open']),
                        'high': float(row['high']),
                        'low': float(row['low']),
                        'close': float(row['close']),
                        'volume': int(row['volume'])
                    }
            
            # Extract dates and prices from VPA content
            date_pattern = r'\*\*Ngày (\d{4}-\d{2}-\d{2}):\*\*'
            price_pattern = r'(\d+\.?\d*)'
            
            vpa_dates = re.findall(date_pattern, content)
            
            for vpa_date in vpa_dates:
                if vpa_date not in market_dates:
                    self.issues.append(f"{ticker}: VPA date {vpa_date} not found in market data")
        
        except Exception as e:
            self.issues.append(f"{ticker}: Error verifying price data - {str(e)}")
    
    def verify_vietnamese_usage(self, ticker: str, content: str):
        """Verify Vietnamese language usage."""
        # Check for basic Vietnamese terms
        has_vn_terms = any(term in content.lower() for term in self.vn_terms)
        
        if not has_vn_terms:
            self.issues.append(f"{ticker}: Missing Vietnamese financial terminology")
        
        # Check for required Vietnamese structure
        if "Phân tích VPA/Wyckoff:" not in content:
            self.issues.append(f"{ticker}: Missing 'Phân tích VPA/Wyckoff:' section")
    
    def verify_number_formatting(self, ticker: str, content: str):
        """Verify numbers use dots as decimal separators, not commas."""
        # Check for comma decimal separators (should be dots)
        comma_decimals = re.findall(r'\d+,\d+', content)
        
        if comma_decimals:
            self.issues.append(f"{ticker}: Found comma decimal separators (should be dots): {comma_decimals}")
        
        # Check for proper price formatting
        price_pattern = r'(\d+\.\d+|\d+)'
        prices = re.findall(price_pattern, content)
        
        if not prices:
            self.issues.append(f"{ticker}: No price values found in analysis")

def main():
    verifier = VPAVerifier()
    issues = verifier.verify_all_tickers()
    
    if not issues:
        print("✅ All VPA files passed verification!")
        return 0
    
    print(f"❌ Found {len(issues)} issues:")
    print("-" * 50)
    
    for issue in issues:
        print(f"• {issue}")
    
    return 1

if __name__ == "__main__":
    exit(main())