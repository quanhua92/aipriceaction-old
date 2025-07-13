#!/usr/bin/env python3
"""
VPA Data Merger - Combines individual ticker VPA files into main VPA.md

This script reads all individual VPA analysis files from vpa_data/ directory
and combines them into a single VPA.md or VPA_week.md file, maintaining
proper structure and formatting.

Usage: python merge_vpa.py [--week]
"""

import os
import re
import shutil
import argparse
from datetime import datetime

# --- Argument Parsing ---
parser = argparse.ArgumentParser(
    description='Merge VPA data from vpa_data/ folder into main VPA file.'
)
parser.add_argument(
    '--week',
    action='store_true',
    help='If specified, writes to VPA_week.md instead of VPA.md.'
)
args = parser.parse_args()

# --- File Configuration ---
if args.week:
    main_vpa_filename = 'VPA_week.md'
    source_dir = "market_data_week"
    dest_dir = "market_data_week_processed"
    vpa_data_dir = 'vpa_data_week'
else:
    main_vpa_filename = 'VPA.md'
    source_dir = "market_data"
    dest_dir = "market_data_processed"
    vpa_data_dir = 'vpa_data'

print(f"Merging VPA data into: {main_vpa_filename}")
print(f"Reading from: {vpa_data_dir}/")

def backup_market_data():
    """Backup current market_data to market_data_processed before processing VPA."""
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
    """Get all ticker VPA files from vpa_data directory."""
    if not os.path.exists(vpa_data_dir):
        print(f"   - VPA data directory {vpa_data_dir} not found.")
        return []
    
    ticker_files = []
    for filename in os.listdir(vpa_data_dir):
        if filename.endswith('.md'):
            ticker = filename.replace('.md', '')
            file_path = os.path.join(vpa_data_dir, filename)
            ticker_files.append((ticker, file_path))
    
    # Sort by ticker name
    ticker_files.sort(key=lambda x: x[0])
    return ticker_files

def merge_vpa_data():
    """Main function to merge all VPA data into single file."""
    print("Starting VPA data merge...")
    
    # Get all ticker files
    ticker_files = get_all_ticker_files()
    
    if not ticker_files:
        print("   - No ticker files found in vpa_data directory.")
        return
    
    print(f"   - Found {len(ticker_files)} ticker files to merge")
    
    # Read and merge all ticker data
    merged_content = []
    processed_tickers = []
    skipped_tickers = []
    
    for ticker, file_path in ticker_files:
        content = read_ticker_vpa_file(file_path)
        
        if content:
            # Add ticker header and content
            merged_content.append(f"# {ticker}")
            merged_content.append("")  # Blank line after header
            merged_content.append(content)
            merged_content.append("")  # Blank line after content
            merged_content.append("---")  # Separator
            merged_content.append("")  # Blank line after separator
            
            processed_tickers.append(ticker)
        else:
            skipped_tickers.append(ticker)
    
    if not merged_content:
        print("   - No valid VPA data found to merge.")
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
        
        print(f"   - Successfully merged VPA data into {main_vpa_filename}")
        print(f"   - Processed tickers: {len(processed_tickers)}")
        
        if processed_tickers:
            print(f"   - Included: {', '.join(processed_tickers[:10])}")
            if len(processed_tickers) > 10:
                print(f"     ... and {len(processed_tickers) - 10} more")
        
        if skipped_tickers:
            print(f"   - Skipped empty files: {len(skipped_tickers)}")
            if len(skipped_tickers) <= 5:
                print(f"     {', '.join(skipped_tickers)}")
    
    except Exception as e:
        print(f"   - Error writing to {main_vpa_filename}: {e}")

def main():
    """Main execution function."""
    print("=" * 60)
    print("VPA Data Merger")
    print("=" * 60)
    
    # Backup market data before processing VPA
    backup_market_data()
    
    # Merge VPA data
    merge_vpa_data()
    
    print()
    print("=" * 60)
    print("VPA merge completed successfully!")
    print(f"Check {main_vpa_filename} for the merged results.")
    print("=" * 60)

if __name__ == "__main__":
    main()