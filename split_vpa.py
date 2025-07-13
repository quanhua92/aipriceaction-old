#!/usr/bin/env python3
"""
Script to split VPA.md into individual ticker files
"""

import re
import os
import argparse

def split_vpa_file(week=False):
    """Split VPA.md into individual ticker files in vpa_data/ directory"""
    
    if week:
        vpa_file = "/Volumes/data/workspace/aipriceaction/VPA_week.md"
        output_dir = "/Volumes/data/workspace/aipriceaction/vpa_data_week"
    else:
        vpa_file = "/Volumes/data/workspace/aipriceaction/VPA.md"
        output_dir = "/Volumes/data/workspace/aipriceaction/vpa_data"
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Read the entire VPA.md file
    with open(vpa_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content by ticker headers (# TICKER_NAME)
    sections = re.split(r'\n(?=# [A-Z]+\n)', content)
    
    # Remove empty first section if it exists
    if sections and not sections[0].strip():
        sections = sections[1:]
    
    ticker_count = 0
    
    for section in sections:
        if not section.strip():
            continue
            
        # Extract ticker name from header
        lines = section.strip().split('\n')
        if not lines:
            continue
            
        header_line = lines[0]
        if not header_line.startswith('# '):
            continue
            
        ticker = header_line[2:].strip()
        
        # Skip if ticker is empty
        if not ticker:
            continue
            
        # Write ticker content to individual file
        output_file = os.path.join(output_dir, f"{ticker}.md")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(section.strip())
        
        ticker_count += 1
        print(f"Created: {output_file}")
    
    print(f"\nTotal tickers split: {ticker_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split VPA files into individual ticker files')
    parser.add_argument('--week', action='store_true', help='Process VPA_week.md instead of VPA.md')
    
    args = parser.parse_args()
    split_vpa_file(week=args.week)