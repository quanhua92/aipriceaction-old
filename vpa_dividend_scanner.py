#!/usr/bin/env python3
"""
VPA Dividend Scanner - Multi-Agent System

This script deploys multiple agents to scan VPA analysis files and compare
price references with CSV data to identify tickers that need dividend adjustment.
When discrepancies are found, it copies relevant files to check_dividends folder.

Usage: python vpa_dividend_scanner.py [--week]
"""

import os
import re
import pandas as pd
import shutil
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import json

class VPADividendAgent:
    """Individual agent responsible for checking one ticker for dividend issues."""
    
    def __init__(self, ticker: str, vpa_file: str, market_data_dir: str, is_week: bool = False):
        self.ticker = ticker
        self.vpa_file = vpa_file
        self.market_data_dir = market_data_dir
        self.is_week = is_week
        self.results = {}
        
    def extract_vpa_prices(self, limit_entries: int = 10) -> List[Tuple[str, List[float]]]:
        """Extract price references from the first few VPA entries."""
        if not os.path.exists(self.vpa_file):
            return []
        
        try:
            with open(self.vpa_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find ticker section
            ticker_pattern = f"# {self.ticker}\\n(.*?)(?=\\n# [A-Z0-9]+\\n|\\Z)"
            ticker_match = re.search(ticker_pattern, content, re.DOTALL)
            
            if not ticker_match:
                return []
            
            ticker_content = ticker_match.group(1)
            
            # Extract daily entries (limit to first few)
            date_pattern = r'-\s+\*\*Ngày (\d{4}-\d{2}-\d{2}):\*\* (.+?)(?=-\s+\*\*Ngày|\Z)'
            date_matches = re.findall(date_pattern, ticker_content, re.DOTALL)
            
            vpa_data = []
            for i, (date, analysis_text) in enumerate(date_matches[:limit_entries]):
                prices = self._extract_prices_from_text(analysis_text)
                if prices:
                    vpa_data.append((date, prices))
            
            return vpa_data
            
        except Exception as e:
            print(f"   Agent {self.ticker}: Error reading VPA file: {e}")
            return []
    
    def _extract_prices_from_text(self, text: str) -> List[float]:
        """Extract numerical prices from Vietnamese VPA text."""
        prices = []
        
        # Price patterns to match
        patterns = [
            r'từ\s+([\d.]+)\s+(?:lên|xuống|đến)\s+([\d.]+)',  # từ X lên/xuống Y
            r'(?:tăng|giảm)\s+từ\s+([\d.]+)\s+(?:lên|xuống|đến)\s+([\d.]+)',  # tăng từ X lên Y
            r'đóng cửa\s+(?:ở\s+(?:mức\s+)?)?([\d.]+)',  # đóng cửa ở X
            r'mở cửa\s+(?:ở\s+(?:mức\s+)?)?([\d.]+)',  # mở cửa ở X
            r'(?:ở|tại)\s+(?:mức\s+)?([\d.]+)',  # ở mức X
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    # Multiple prices in one match (e.g., từ X lên Y)
                    for price_str in match:
                        try:
                            price = float(price_str.replace(',', ''))
                            if 1 <= price <= 100000:  # Reasonable price range
                                prices.append(price)
                        except ValueError:
                            continue
                else:
                    # Single price match
                    try:
                        price = float(match.replace(',', ''))
                        if 1 <= price <= 100000:
                            prices.append(price)
                    except ValueError:
                        continue
        
        return list(set(prices))  # Remove duplicates
    
    def get_csv_prices(self, dates: List[str]) -> Dict[str, Dict[str, float]]:
        """Get CSV price data for specific dates."""
        # Find CSV file for this ticker
        csv_files = [f for f in os.listdir(self.market_data_dir) 
                    if f.startswith(f"{self.ticker}_") and f.endswith('.csv')]
        
        if not csv_files:
            return {}
        
        csv_path = os.path.join(self.market_data_dir, csv_files[0])
        
        try:
            df = pd.read_csv(csv_path)
            df['time'] = pd.to_datetime(df['time']).dt.strftime('%Y-%m-%d')
            
            csv_data = {}
            for date in dates:
                if date in df['time'].values:
                    row = df[df['time'] == date].iloc[0]
                    csv_data[date] = {
                        'open': float(row['open']),
                        'high': float(row['high']),
                        'low': float(row['low']),
                        'close': float(row['close'])
                    }
            
            return csv_data
            
        except Exception as e:
            print(f"   Agent {self.ticker}: Error reading CSV: {e}")
            return {}
    
    def analyze_dividend_probability(self) -> Dict:
        """Analyze if this ticker likely has dividend adjustment issues."""
        print(f"   Agent {self.ticker}: Starting analysis...")
        
        # Extract VPA prices from first 10 entries
        vpa_data = self.extract_vpa_prices(limit_entries=10)
        
        if not vpa_data:
            return {
                'ticker': self.ticker,
                'needs_dividend_check': False,
                'reason': 'No VPA price data found',
                'confidence': 0.0
            }
        
        # Get dates and extract all VPA prices
        dates = [item[0] for item in vpa_data]
        all_vpa_prices = []
        for _, prices in vpa_data:
            all_vpa_prices.extend(prices)
        
        if not all_vpa_prices:
            return {
                'ticker': self.ticker,
                'needs_dividend_check': False,
                'reason': 'No numerical prices extracted from VPA',
                'confidence': 0.0
            }
        
        # Get corresponding CSV data
        csv_data = self.get_csv_prices(dates)
        
        if not csv_data:
            return {
                'ticker': self.ticker,
                'needs_dividend_check': False,
                'reason': 'No matching CSV data found',
                'confidence': 0.0
            }
        
        # Compare VPA prices with CSV prices
        discrepancies = []
        for date in dates:
            if date in csv_data:
                csv_prices = [
                    csv_data[date]['open'],
                    csv_data[date]['high'], 
                    csv_data[date]['low'],
                    csv_data[date]['close']
                ]
                
                # Find VPA prices for this date
                date_vpa_prices = None
                for vpa_date, vpa_prices in vpa_data:
                    if vpa_date == date:
                        date_vpa_prices = vpa_prices
                        break
                
                if date_vpa_prices:
                    # Compare each VPA price with CSV price range
                    csv_min = min(csv_prices)
                    csv_max = max(csv_prices)
                    
                    for vpa_price in date_vpa_prices:
                        # Check if VPA price is significantly outside CSV range
                        if vpa_price > csv_max * 1.1:  # VPA price 10% higher than CSV max
                            ratio = vpa_price / csv_max
                            discrepancies.append(ratio)
                        elif vpa_price < csv_min * 0.9:  # VPA price 10% lower than CSV min
                            ratio = csv_min / vpa_price
                            discrepancies.append(ratio)
        
        # Analyze discrepancies
        if len(discrepancies) >= 3:  # Need multiple discrepancies
            avg_ratio = sum(discrepancies) / len(discrepancies)
            consistency = len([r for r in discrepancies if abs(r - avg_ratio) < avg_ratio * 0.2])
            confidence = min(0.95, consistency / len(discrepancies) * (len(discrepancies) / 10))
            
            if avg_ratio > 1.15 and confidence > 0.6:  # High confidence dividend detected
                return {
                    'ticker': self.ticker,
                    'needs_dividend_check': True,
                    'reason': f'Significant price discrepancies detected (avg ratio: {avg_ratio:.3f})',
                    'confidence': confidence,
                    'discrepancy_count': len(discrepancies),
                    'avg_ratio': avg_ratio,
                    'sample_vpa_prices': all_vpa_prices[:5],
                    'sample_csv_dates': list(csv_data.keys())[:3]
                }
        
        return {
            'ticker': self.ticker,
            'needs_dividend_check': False,
            'reason': f'No significant discrepancies found ({len(discrepancies)} discrepancies)',
            'confidence': 0.0,
            'discrepancy_count': len(discrepancies)
        }

class VPADividendScanner:
    """Main orchestrator for multi-agent VPA dividend scanning."""
    
    def __init__(self, is_week: bool = False, max_workers: int = 8):
        self.is_week = is_week
        self.max_workers = max_workers
        
        # Setup directories based on mode
        if is_week:
            self.vpa_dir = "vpa_data"
            self.market_data_dir = "market_data_week"
            self.check_dividends_dir = "market_data_week_check_dividends"
            self.vpa_main_file = "VPA_week.md"
        else:
            self.vpa_dir = "vpa_data"
            self.market_data_dir = "market_data"
            self.check_dividends_dir = "market_data_check_dividends"
            self.vpa_main_file = "VPA.md"
    
    def get_all_tickers(self) -> List[str]:
        """Get list of all tickers to check."""
        tickers = set()
        
        # Get tickers from individual VPA files
        if os.path.exists(self.vpa_dir):
            for file in os.listdir(self.vpa_dir):
                if file.endswith('.md'):
                    ticker = file.replace('.md', '')
                    tickers.add(ticker)
        
        # Get tickers from main VPA file
        if os.path.exists(self.vpa_main_file):
            try:
                with open(self.vpa_main_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Find all ticker headers
                ticker_headers = re.findall(r'^# ([A-Z0-9]+)$', content, re.MULTILINE)
                tickers.update(ticker_headers)
                
            except Exception as e:
                print(f"Error reading {self.vpa_main_file}: {e}")
        
        # Get tickers from CSV files
        if os.path.exists(self.market_data_dir):
            for file in os.listdir(self.market_data_dir):
                if file.endswith('.csv') and '_' in file:
                    ticker = file.split('_')[0]
                    tickers.add(ticker)
        
        return sorted(list(tickers))
    
    def create_agent(self, ticker: str) -> VPADividendAgent:
        """Create a dividend checking agent for a specific ticker."""
        # Determine VPA file path
        individual_vpa_file = os.path.join(self.vpa_dir, f"{ticker}.md")
        if os.path.exists(individual_vpa_file):
            vpa_file = individual_vpa_file
        else:
            vpa_file = self.vpa_main_file
        
        return VPADividendAgent(ticker, vpa_file, self.market_data_dir, self.is_week)
    
    def copy_to_check_dividends(self, ticker: str, analysis_result: Dict):
        """Copy ticker's files to check_dividends directory."""
        # Create check_dividends directory
        os.makedirs(self.check_dividends_dir, exist_ok=True)
        
        # Find and copy CSV file
        csv_files = [f for f in os.listdir(self.market_data_dir) 
                    if f.startswith(f"{ticker}_") and f.endswith('.csv')]
        
        if csv_files:
            src_csv = os.path.join(self.market_data_dir, csv_files[0])
            dst_csv = os.path.join(self.check_dividends_dir, csv_files[0])
            shutil.copy2(src_csv, dst_csv)
            
            # Create metadata file
            metadata_path = os.path.join(self.check_dividends_dir, f"{ticker}_dividend_info.txt")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                f.write(f"Ticker: {ticker}\n")
                f.write(f"Suspected Dividend Ratio: {analysis_result.get('avg_ratio', 'Unknown'):.6f}\n")
                f.write(f"Confidence: {analysis_result.get('confidence', 0):.3f}\n")
                f.write(f"Detected: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"CSV File: {csv_files[0]}\n")
                f.write(f"Reason: {analysis_result.get('reason', 'Unknown')}\n")
                f.write(f"Discrepancy Count: {analysis_result.get('discrepancy_count', 0)}\n")
                if 'sample_vpa_prices' in analysis_result:
                    f.write(f"Sample VPA Prices: {analysis_result['sample_vpa_prices']}\n")
                if 'sample_csv_dates' in analysis_result:
                    f.write(f"Sample CSV Dates: {analysis_result['sample_csv_dates']}\n")
            
            print(f"   ✅ Copied {ticker} to {self.check_dividends_dir}")
        else:
            print(f"   ⚠️  No CSV file found for {ticker}")
    
    def run_scan(self):
        """Execute multi-agent dividend scanning."""
        print("🔍 VPA Dividend Scanner - Multi-Agent System")
        print("=" * 60)
        
        mode = "Weekly" if self.is_week else "Daily"
        print(f"Mode: {mode}")
        print(f"VPA Directory: {self.vpa_dir}")
        print(f"Market Data Directory: {self.market_data_dir}")
        print(f"Check Dividends Directory: {self.check_dividends_dir}")
        print()
        
        # Get all tickers
        tickers = self.get_all_tickers()
        print(f"Found {len(tickers)} tickers to analyze")
        print(f"Deploying {min(self.max_workers, len(tickers))} agents...")
        print()
        
        # Deploy agents in parallel
        results = []
        dividend_tickers = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all agent tasks
            future_to_ticker = {}
            for ticker in tickers:
                agent = self.create_agent(ticker)
                future = executor.submit(agent.analyze_dividend_probability)
                future_to_ticker[future] = ticker
            
            # Collect results as they complete
            for future in as_completed(future_to_ticker):
                ticker = future_to_ticker[future]
                try:
                    result = future.result(timeout=30)  # 30 second timeout per agent
                    results.append(result)
                    
                    if result['needs_dividend_check']:
                        dividend_tickers.append(ticker)
                        print(f"   🚨 {ticker}: {result['reason']} (confidence: {result['confidence']:.1%})")
                        self.copy_to_check_dividends(ticker, result)
                    else:
                        print(f"   ✅ {ticker}: {result['reason']}")
                        
                except Exception as e:
                    print(f"   ❌ {ticker}: Agent failed - {e}")
        
        # Summary
        print()
        print("=" * 60)
        print("📊 DIVIDEND SCANNING SUMMARY")
        print("=" * 60)
        print(f"Total tickers analyzed: {len(results)}")
        print(f"Tickers needing dividend check: {len(dividend_tickers)}")
        print(f"Tickers with clean data: {len(results) - len(dividend_tickers)}")
        
        if dividend_tickers:
            print(f"\n🔧 Tickers flagged for dividend processing:")
            for ticker in sorted(dividend_tickers):
                print(f"   • {ticker}")
            print(f"\n📁 Files copied to: {self.check_dividends_dir}")
            print("👤 AI Agent should now process these dividend adjustments")
        else:
            print("\n✨ No dividend adjustments needed - all tickers have consistent data!")
        
        # Save detailed results
        results_file = f"dividend_scan_results_{'week' if self.is_week else 'daily'}.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'scan_time': datetime.now().isoformat(),
                'mode': mode,
                'total_tickers': len(results),
                'dividend_tickers': dividend_tickers,
                'results': results
            }, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Detailed results saved to: {results_file}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="VPA Dividend Scanner - Multi-Agent System")
    parser.add_argument('--week', action='store_true', help="Scan weekly data instead of daily")
    parser.add_argument('--workers', type=int, default=8, help="Number of parallel agents (default: 8)")
    args = parser.parse_args()
    
    scanner = VPADividendScanner(is_week=args.week, max_workers=args.workers)
    scanner.run_scan()

if __name__ == "__main__":
    main()