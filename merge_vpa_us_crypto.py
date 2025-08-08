#!/usr/bin/env python3
"""
US & Crypto VPA Data Merger - Combines individual ticker VPA files into main VPA_us_crypto.md

This script reads all individual US & Crypto VPA analysis files from vpa_data_us_crypto/ directory
and combines them into a single VPA_us_crypto.md or VPA_us_crypto_week.md file, maintaining
proper structure and formatting.

Usage: python merge_vpa_us_crypto.py [--week]
"""

import os
import re
import shutil
import argparse
from datetime import datetime

# --- Argument Parsing ---
parser = argparse.ArgumentParser(
    description='Merge US & Crypto VPA data from vpa_data_us_crypto/ folder into main VPA_us_crypto file.'
)
parser.add_argument(
    '--week',
    action='store_true',
    help='If specified, writes to VPA_us_crypto_week.md instead of VPA_us_crypto.md.'
)
args = parser.parse_args()

# --- File Configuration ---
if args.week:
    main_vpa_filename = 'VPA_us_crypto_week.md'
    source_dir = "market_data_us_crypto_week"
    dest_dir = "market_data_us_crypto_week_processed"
    vpa_data_dir = 'vpa_data_us_crypto_week'
else:
    main_vpa_filename = 'VPA_us_crypto.md'
    source_dir = "market_data_us_crypto"
    dest_dir = "market_data_us_crypto_processed"
    vpa_data_dir = 'vpa_data_us_crypto'

print(f"Merging US & Crypto VPA data into: {main_vpa_filename}")
print(f"Reading from: {vpa_data_dir}/")

def backup_market_data():
    """Backup current market_data_us_crypto to market_data_us_crypto_processed before processing VPA."""
    if not os.path.exists(source_dir):
        print(f"   - Source directory {source_dir} not found. Skipping backup.")
        return
    
    print(f"   - Backing up {source_dir} to {dest_dir}...")
    
    # Remove existing processed directory if it exists to avoid duplicates
    # (since filenames contain dates and will accumulate over time)
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        print(f"   - Removed existing {dest_dir} to prevent duplicate files")
    
    # Copy entire directory
    shutil.copytree(source_dir, dest_dir)
    print(f"   - Successfully backed up {len(os.listdir(source_dir))} files from {source_dir} to {dest_dir}")

def read_ticker_vpa_file(ticker_file):
    """Read and parse a single ticker VPA file."""
    if not os.path.exists(ticker_file):
        return None
    
    try:
        with open(ticker_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        if not content:
            return None
        
        # Remove any existing header if present (in case file has # TICKER header)
        ticker_name = os.path.basename(ticker_file).replace('.md', '')
        
        # Remove header line if it exists
        lines = content.split('\n')
        if lines and lines[0].strip() == f"# {ticker_name}":
            content = '\n'.join(lines[1:]).strip()
        
        return content
    except Exception as e:
        print(f"   - Error reading {ticker_file}: {e}")
        return None

def get_all_ticker_files():
    """Get all ticker VPA files from vpa_data_us_crypto directory."""
    if not os.path.exists(vpa_data_dir):
        print(f"   - VPA data directory {vpa_data_dir} not found.")
        return []
    
    ticker_files = []
    for filename in os.listdir(vpa_data_dir):
        if filename.endswith('.md'):
            ticker = filename.replace('.md', '')
            file_path = os.path.join(vpa_data_dir, filename)
            ticker_files.append((ticker, file_path))
    
    # Sort by ticker name - prioritize US indices first, then crypto
    def sort_key(x):
        ticker = x[0]
        # US indices first (DJI, INX, etc.)
        if ticker in ['DJI', 'INX', 'COMP', 'RUT', 'NYA', 'RUI', 'RUA', 'UKX', 'DAX', 'PX1', 'N225', '000001', 'HSI', 'SENSEX', 'ME00000000']:
            return (0, ticker)  # US indices get priority 0
        # Crypto second (BTC, ETH, etc.)
        elif ticker in ['BTC', 'ETH', 'USDT', 'USDC', 'BNB', 'BUSD', 'XRP', 'ADA', 'SOL', 'DOGE']:
            return (1, ticker)  # Crypto gets priority 1
        else:
            return (2, ticker)  # Other assets get priority 2
    
    ticker_files.sort(key=sort_key)
    return ticker_files

def get_asset_type(ticker):
    """Determine if ticker is US index or crypto for section headers."""
    us_indices = ['DJI', 'INX', 'COMP', 'RUT', 'NYA', 'RUI', 'RUA', 'UKX', 'DAX', 'PX1', 'N225', '000001', 'HSI', 'SENSEX', 'ME00000000']
    crypto_assets = ['BTC', 'ETH', 'USDT', 'USDC', 'BNB', 'BUSD', 'XRP', 'ADA', 'SOL', 'DOGE']
    
    if ticker in us_indices:
        return "US_INDEX"
    elif ticker in crypto_assets:
        return "CRYPTO"
    else:
        return "OTHER"

def merge_vpa_data():
    """Main function to merge all US & Crypto VPA data into single file."""
    print("Starting US & Crypto VPA data merge...")
    
    # Get all ticker files
    ticker_files = get_all_ticker_files()
    
    if not ticker_files:
        print(f"   - No ticker files found in {vpa_data_dir} directory.")
        return
    
    print(f"   - Found {len(ticker_files)} ticker files to merge")
    
    # Group tickers by asset type for organized output
    us_tickers = []
    crypto_tickers = []
    other_tickers = []
    
    for ticker, file_path in ticker_files:
        asset_type = get_asset_type(ticker)
        content = read_ticker_vpa_file(file_path)
        
        if content:
            ticker_data = (ticker, content)
            if asset_type == "US_INDEX":
                us_tickers.append(ticker_data)
            elif asset_type == "CRYPTO":
                crypto_tickers.append(ticker_data)
            else:
                other_tickers.append(ticker_data)
    
    # Build merged content with sections
    merged_content = []
    processed_tickers = []
    
    # Add header comment
    timeframe = "Weekly" if args.week else "Daily"
    merged_content.append(f"<!-- US & Crypto {timeframe} VPA Analysis -->")
    merged_content.append(f"<!-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->")
    merged_content.append("")
    
    # Add US Indices section
    if us_tickers:
        merged_content.append("<!-- === US INDICES === -->")
        merged_content.append("")
        
        for ticker, content in us_tickers:
            merged_content.append(f"# {ticker}")
            merged_content.append("")  # Blank line after header
            merged_content.append(content)
            merged_content.append("")  # Blank line after content
            merged_content.append("---")  # Separator
            merged_content.append("")  # Blank line after separator
            processed_tickers.append(f"{ticker} (US Index)")
    
    # Add Cryptocurrencies section
    if crypto_tickers:
        merged_content.append("<!-- === CRYPTOCURRENCIES === -->")
        merged_content.append("")
        
        for ticker, content in crypto_tickers:
            merged_content.append(f"# {ticker}")
            merged_content.append("")  # Blank line after header
            merged_content.append(content)
            merged_content.append("")  # Blank line after content
            merged_content.append("---")  # Separator
            merged_content.append("")  # Blank line after separator
            processed_tickers.append(f"{ticker} (Crypto)")
    
    # Add Other Assets section (if any)
    if other_tickers:
        merged_content.append("<!-- === OTHER ASSETS === -->")
        merged_content.append("")
        
        for ticker, content in other_tickers:
            merged_content.append(f"# {ticker}")
            merged_content.append("")  # Blank line after header
            merged_content.append(content)
            merged_content.append("")  # Blank line after content
            merged_content.append("---")  # Separator
            merged_content.append("")  # Blank line after separator
            processed_tickers.append(f"{ticker} (Other)")
    
    if not merged_content or len(processed_tickers) == 0:
        print("   - No valid US & Crypto VPA data found to merge.")
        return
    
    # Remove the last separator and blank lines
    while merged_content and (merged_content[-1] == "" or merged_content[-1] == "---"):
        merged_content.pop()
    
    # Write to main VPA file
    final_content = '\n'.join(merged_content)
    
    try:
        with open(main_vpa_filename, 'w', encoding='utf-8') as f:
            f.write(final_content)
            f.write('\n')  # Final newline
        
        print(f"   - Successfully merged US & Crypto VPA data into {main_vpa_filename}")
        print(f"   - Processed assets: {len(processed_tickers)}")
        
        if processed_tickers:
            print(f"   - Included: {', '.join(processed_tickers[:10])}")
            if len(processed_tickers) > 10:
                print(f"     ... and {len(processed_tickers) - 10} more")
        
        # Show breakdown by asset type
        us_count = len(us_tickers)
        crypto_count = len(crypto_tickers)
        other_count = len(other_tickers)
        
        print(f"   - Asset breakdown:")
        if us_count > 0:
            print(f"     • US Indices: {us_count}")
        if crypto_count > 0:
            print(f"     • Cryptocurrencies: {crypto_count}")
        if other_count > 0:
            print(f"     • Other Assets: {other_count}")
    
    except Exception as e:
        print(f"   - Error writing to {main_vpa_filename}: {e}")

def main():
    """Main execution function."""
    print("=" * 60)
    print("US & Crypto VPA Data Merger")
    print("=" * 60)
    
    # Backup market data before processing VPA
    backup_market_data()
    
    # Merge VPA data
    merge_vpa_data()
    
    print()
    print("=" * 60)
    print("US & Crypto VPA merge completed successfully!")
    print(f"Check {main_vpa_filename} for the merged results.")
    print("=" * 60)

if __name__ == "__main__":
    main()