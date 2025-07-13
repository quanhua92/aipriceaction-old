#!/usr/bin/env python3
"""
Test script for VPA Dividend Scanner

This script tests the multi-agent dividend scanning system with current data.
"""

import os
import sys
from vpa_dividend_scanner import VPADividendScanner

def test_scanner():
    """Test the VPA dividend scanner with current data."""
    print("🧪 Testing VPA Dividend Scanner")
    print("=" * 50)
    
    # Check if required directories exist
    required_dirs = ["vpa_data", "market_data"]
    missing_dirs = [d for d in required_dirs if not os.path.exists(d)]
    
    if missing_dirs:
        print(f"❌ Missing required directories: {missing_dirs}")
        print("Please ensure you have VPA data and market data available.")
        return False
    
    print("✅ Required directories found")
    
    # Test daily mode
    print("\n📊 Testing Daily Mode...")
    scanner_daily = VPADividendScanner(is_week=False, max_workers=4)
    
    # Get a few sample tickers for quick test
    all_tickers = scanner_daily.get_all_tickers()
    if not all_tickers:
        print("❌ No tickers found in VPA or market data")
        return False
    
    print(f"✅ Found {len(all_tickers)} tickers")
    
    # Test with first 3 tickers for quick validation
    test_tickers = all_tickers[:3]
    print(f"🔍 Testing with sample tickers: {test_tickers}")
    
    for ticker in test_tickers:
        print(f"\n🤖 Creating agent for {ticker}...")
        agent = scanner_daily.create_agent(ticker)
        
        # Test VPA price extraction
        vpa_prices = agent.extract_vpa_prices(limit_entries=3)
        print(f"   📈 VPA data: {len(vpa_prices)} entries found")
        
        if vpa_prices:
            for date, prices in vpa_prices[:2]:  # Show first 2
                print(f"      {date}: {len(prices)} prices: {prices[:3]}...")
        
        # Test CSV data access
        if vpa_prices:
            dates = [item[0] for item in vpa_prices[:2]]
            csv_data = agent.get_csv_prices(dates)
            print(f"   💾 CSV data: {len(csv_data)} matching dates")
            
            for date, data in list(csv_data.items())[:1]:  # Show first date
                print(f"      {date}: OHLC = {data['open']:.1f}, {data['high']:.1f}, {data['low']:.1f}, {data['close']:.1f}")
    
    print("\n✅ VPA Dividend Scanner test completed successfully!")
    print("\n🚀 To run full scan, use:")
    print("   python vpa_dividend_scanner.py")
    print("   python vpa_dividend_scanner.py --week")
    
    return True

if __name__ == "__main__":
    success = test_scanner()
    sys.exit(0 if success else 1)