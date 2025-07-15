#!/usr/bin/env python3
"""
Script to split TICKERS.csv into 8 batch files for parallel processing
"""

import csv
import os
import math

def split_tickers():
    base_dir = '/Volumes/data/workspace/aipriceaction'
    tickers_file = os.path.join(base_dir, 'TICKERS.csv')
    data_dir = os.path.join(base_dir, 'utilities', 'data')
    
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)
    
    # Read tickers from CSV
    tickers = []
    with open(tickers_file, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if row:  # Skip empty rows
                tickers.append(row[0])
    
    print(f"Total tickers: {len(tickers)}")
    
    # Calculate batch size (divide into 8 groups)
    batch_size = math.ceil(len(tickers) / 8)
    print(f"Batch size: {batch_size}")
    
    # Split into 8 batches
    for i in range(8):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, len(tickers))
        batch_tickers = tickers[start_idx:end_idx]
        
        if not batch_tickers:  # Skip empty batches
            continue
            
        # Write batch file
        batch_file = os.path.join(data_dir, f'batch_{i+1}.csv')
        with open(batch_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ticker'])  # Header
            for ticker in batch_tickers:
                writer.writerow([ticker])
        
        print(f"Batch {i+1}: {len(batch_tickers)} tickers -> {batch_file}")
    
    print(f"\nSuccessfully split {len(tickers)} tickers into 8 batch files in {data_dir}")

if __name__ == "__main__":
    split_tickers()