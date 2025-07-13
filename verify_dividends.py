#!/usr/bin/env python3
"""
Dividend Verification and VPA Price Update Script

This script detects dividend events by comparing VPA analysis prices with current CSV data.
When dividends occur, the CSV data gets adjusted retroactively, so if VPA shows higher
historical prices than current CSV, it indicates a dividend happened and we need to update
all VPA price references to match the dividend-adjusted CSV data.

Usage: python verify_dividends.py
"""

import os
import csv
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional

def parse_csv_data(csv_file: str) -> Dict[str, Dict]:
    """Parse CSV market data into a dictionary indexed by date."""
    data = {}
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = row['time']
                data[date] = {
                    'open': float(row['open']),
                    'high': float(row['high']),
                    'low': float(row['low']),
                    'close': float(row['close']),
                    'volume': int(row['volume'])
                }
    except Exception as e:
        print(f"Error reading {csv_file}: {e}")
    return data

def extract_prices_from_vpa_text(text: str) -> List[Tuple[str, float, float]]:
    """
    Extract all price references from VPA analysis text.
    Returns list of (date, from_price, to_price) tuples.
    """
    prices = []
    
    # Pattern to match date entries with price movements
    date_pattern = r'-\s+\*\*Ngày (\d{4}-\d{2}-\d{2}):\*\* (.+?)(?=-\s+\*\*Ngày|\Z)'
    date_matches = re.findall(date_pattern, text, re.DOTALL)
    
    for date, analysis_text in date_matches:
        # Clean up the analysis text
        analysis_text = analysis_text.strip()
        
        # Extract price movements - multiple patterns to catch different formats
        price_patterns = [
            # "từ 61.27 lên 61.87" or "từ 100.5 xuống 95.2"
            r'từ\s+([\d.]+)\s+(?:lên|xuống|đến)\s+([\d.]+)(?=\.|,|\s|$)',
            # "tăng từ 61.27 lên 61.87"
            r'(?:tăng|giảm)\s+từ\s+([\d.]+)\s+(?:lên|xuống|đến)\s+([\d.]+)(?=\.|,|\s|$)',
            # "ticker từ price lên price" format
            r'\w+\s+từ\s+([\d.]+)\s+(?:lên|xuống|đến)\s+([\d.]+)(?=\.|,|\s|$)',
        ]
        
        # Single price patterns - use positive lookahead to avoid capturing trailing punctuation
        single_price_patterns = [
            r'đóng cửa\s+(?:ở\s+(?:mức\s+)?)?(\d+(?:\.\d+)?)(?=\.|,|\s|$)',  # Closing price
            r'ở\s+(?:mức\s+)?(\d+(?:\.\d+)?)(?=\.|,|\s|$)',  # At level
            r'lên\s+(\d+(?:\.\d+)?)(?=\.|,|\s|$)',  # Up to
            r'xuống\s+(\d+(?:\.\d+)?)(?=\.|,|\s|$)',  # Down to
            r'mở cửa\s+(?:ở\s+(?:mức\s+)?)?(\d+(?:\.\d+)?)(?=\.|,|\s|$)',  # Opening price
        ]
        
        # First try to find from/to price patterns
        found_range = False
        for pattern in price_patterns:
            matches = re.findall(pattern, analysis_text)
            for match in matches:
                try:
                    from_price = float(match[0])
                    to_price = float(match[1])
                    prices.append((date, from_price, to_price))
                    found_range = True
                except (ValueError, IndexError):
                    continue
        
        # If no range found, look for single prices
        if not found_range:
            for pattern in single_price_patterns:
                matches = re.findall(pattern, analysis_text)
                for match in matches:
                    try:
                        # Clean the match - remove any trailing periods or commas
                        clean_match = match.rstrip('.,')
                        price = float(clean_match)
                        # For single prices, use same price for both from and to
                        prices.append((date, price, price))
                        break  # Only take first single price found
                    except ValueError as e:
                        print(f"Warning: Could not parse price '{match}' for date {date}: {e}")
                        continue
                if matches:  # Break outer loop if we found matches
                    break
    
    return prices

def detect_dividend_adjustment(vpa_prices: List[Tuple[str, float, float]], 
                             csv_data: Dict[str, Dict]) -> Optional[float]:
    """
    Detect if a dividend adjustment occurred by comparing VPA prices with CSV data.
    Returns the dividend adjustment ratio if detected, None otherwise.
    """
    valid_comparisons = []
    
    for date, vpa_from, vpa_to in vpa_prices:
        if date in csv_data:
            csv_open = csv_data[date]['open']
            csv_close = csv_data[date]['close']
            csv_high = csv_data[date]['high']
            csv_low = csv_data[date]['low']
            
            # Check if VPA prices are significantly higher than CSV prices
            try:
                # Compare VPA prices with the entire CSV price range for that day
                csv_min = min(csv_open, csv_close, csv_low)
                csv_max = max(csv_open, csv_close, csv_high)
                
                # Calculate ratios for VPA prices vs CSV range
                vpa_min = min(vpa_from, vpa_to)
                vpa_max = max(vpa_from, vpa_to)
                
                # Check if VPA prices are systematically higher than CSV prices
                min_ratio = vpa_min / csv_max if csv_max > 0 else 1  # Most conservative ratio
                max_ratio = vpa_max / csv_min if csv_min > 0 else 1  # Most aggressive ratio
                
                valid_comparisons.append((date, min_ratio, max_ratio, vpa_min, vpa_max, csv_min, csv_max))
                
            except (ValueError, TypeError, ZeroDivisionError):
                continue  # Skip invalid price data
    
    if len(valid_comparisons) < 5:  # Need at least 5 valid comparisons
        return None
    
    # Check for consistent dividend pattern
    # For a real dividend, we should see:
    # 1. Most dates showing VPA prices > CSV prices
    # 2. Ratios should be relatively consistent
    # 3. Minimum threshold should be 20% (not 10%) to avoid false positives
    
    significant_discrepancies = []
    for date, min_ratio, max_ratio, vpa_min, vpa_max, csv_min, csv_max in valid_comparisons:
        # Even the most conservative ratio should be > 1.2 for dividend
        if min_ratio > 1.2:
            significant_discrepancies.append((date, min_ratio, max_ratio))
    
    # Require at least 80% of comparisons to show significant discrepancy
    if len(significant_discrepancies) < len(valid_comparisons) * 0.8:
        return None
    
    # Calculate adjustment ratio using conservative estimates
    ratios = [min_ratio for _, min_ratio, _ in significant_discrepancies]
    avg_ratio = sum(ratios) / len(ratios)
    
    # Final validation: ratio should be significant and consistent
    ratio_std = (sum((r - avg_ratio)**2 for r in ratios) / len(ratios))**0.5
    ratio_cv = ratio_std / avg_ratio  # Coefficient of variation
    
    # Require: significant ratio (>1.2), low variability (<0.1), enough evidence
    if avg_ratio > 1.2 and ratio_cv < 0.1 and len(significant_discrepancies) >= 5:
        print(f"  Debug: Found {len(significant_discrepancies)} consistent discrepancies")
        print(f"  Debug: Average ratio: {avg_ratio:.4f}, CV: {ratio_cv:.4f}")
        return avg_ratio
    
    return None

def update_vpa_prices(vpa_content: str, adjustment_ratio: float) -> str:
    """
    Update all price references in VPA content by dividing by the adjustment ratio.
    Preserves all text, only changes the numerical price values.
    """
    def replace_price_range(match):
        try:
            price1 = float(match.group(1).rstrip('.,'))
            connector = match.group(2)  # lên, xuống, đến
            price2 = float(match.group(3).rstrip('.,'))
            new_price1 = round(price1 / adjustment_ratio, 2)
            new_price2 = round(price2 / adjustment_ratio, 2)
            return f"từ {new_price1} {connector} {new_price2}"
        except (ValueError, IndexError):
            return match.group(0)  # Return original if conversion fails
    
    def replace_single_price(match):
        try:
            prefix = match.group(1)
            price = float(match.group(2).rstrip('.,'))
            new_price = round(price / adjustment_ratio, 2)
            return f"{prefix}{new_price}"
        except (ValueError, IndexError):
            return match.group(0)  # Return original if conversion fails
    
    # Update "từ X lên/xuống/đến Y" patterns
    updated_content = re.sub(
        r'từ\s+([\d.]+)\s+(lên|xuống|đến)\s+([\d.]+)(?=\.|,|\s|$)',
        replace_price_range,
        vpa_content
    )
    
    # Update "tăng/giảm từ X lên/xuống Y" patterns  
    def replace_action_price_range(match):
        try:
            prefix = match.group(1)
            price1 = float(match.group(2).rstrip('.,'))
            connector = match.group(3)
            price2 = float(match.group(4).rstrip('.,'))
            new_price1 = round(price1 / adjustment_ratio, 2)
            new_price2 = round(price2 / adjustment_ratio, 2)
            return f"{prefix}{new_price1}{connector}{new_price2}"
        except (ValueError, IndexError):
            return match.group(0)
    
    updated_content = re.sub(
        r'((?:tăng|giảm)\s+từ\s+)([\d.]+)(\s+(?:lên|xuống|đến)\s+)([\d.]+)',
        replace_action_price_range,
        updated_content
    )
    
    # Update "ticker từ X lên/xuống Y" patterns
    def replace_ticker_price_range(match):
        try:
            prefix = match.group(1)
            price1 = float(match.group(2).rstrip('.,'))
            connector = match.group(3)
            price2 = float(match.group(4).rstrip('.,'))
            new_price1 = round(price1 / adjustment_ratio, 2)
            new_price2 = round(price2 / adjustment_ratio, 2)
            return f"{prefix}{new_price1}{connector}{new_price2}"
        except (ValueError, IndexError):
            return match.group(0)
    
    updated_content = re.sub(
        r'(\w+\s+từ\s+)([\d.]+)(\s+(?:lên|xuống|đến)\s+)([\d.]+)',
        replace_ticker_price_range,
        updated_content
    )
    
    # Update single price references
    single_price_patterns = [
        r'(đóng cửa\s+(?:ở\s+(?:mức\s+)?)?)(\d+(?:\.\d+)?)(?=\.|,|\s|$)',
        r'(ở\s+(?:mức\s+)?)(\d+(?:\.\d+)?)(?=\.|,|\s|$)',
        r'(lên\s+)(\d+(?:\.\d+)?)(?=\.|,|\s|$)',
        r'(xuống\s+)(\d+(?:\.\d+)?)(?=\.|,|\s|$)',
        r'(mở cửa\s+(?:ở\s+(?:mức\s+)?)?)(\d+(?:\.\d+)?)(?=\.|,|\s|$)',
    ]
    
    for pattern in single_price_patterns:
        updated_content = re.sub(pattern, replace_single_price, updated_content)
    
    return updated_content

def verify_and_update_ticker(ticker: str, dry_run: bool = False) -> Dict:
    """Verify dividend adjustment for a single ticker and update VPA if needed."""
    vpa_file = f"vpa_data/{ticker}.md"
    csv_file = f"market_data/{ticker}_2025-01-02_to_2025-07-13.csv"
    
    if not os.path.exists(vpa_file):
        return {'error': f'VPA file not found: {vpa_file}'}
    
    if not os.path.exists(csv_file):
        return {'error': f'CSV file not found: {csv_file}'}
    
    try:
        # Read VPA content
        with open(vpa_file, 'r', encoding='utf-8') as f:
            vpa_content = f.read()
        
        # Parse CSV data
        csv_data = parse_csv_data(csv_file)
        
        # Extract prices from VPA
        vpa_prices = extract_prices_from_vpa_text(vpa_content)
        
        if not vpa_prices:
            return {'status': 'no_prices', 'message': 'No price data found in VPA'}
        
        # Detect dividend adjustment
        adjustment_ratio = detect_dividend_adjustment(vpa_prices, csv_data)
        
        if adjustment_ratio is None:
            return {'status': 'no_dividend', 'message': 'No dividend adjustment detected'}
        
        if dry_run:
            return {
                'status': 'dividend_detected',
                'ticker': ticker,
                'adjustment_ratio': round(adjustment_ratio, 4),
                'prices_to_update': len(vpa_prices),
                'message': f'DIVIDEND DETECTED: Would update {len(vpa_prices)} price references with ratio {adjustment_ratio:.4f}'
            }
        
        # Update VPA prices
        try:
            updated_content = update_vpa_prices(vpa_content, adjustment_ratio)
            
            # Write updated content back to file
            with open(vpa_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
        except Exception as update_error:
            return {'error': f'Error updating prices for {ticker}: {str(update_error)}'}
        
        return {
            'status': 'updated',
            'ticker': ticker,
            'adjustment_ratio': round(adjustment_ratio, 4),
            'prices_updated': len(vpa_prices),
            'message': f'Updated {len(vpa_prices)} price references with ratio {adjustment_ratio:.4f}'
        }
        
    except Exception as e:
        return {'error': f'Error processing {ticker}: {str(e)}'}

def main():
    """Main function to check all tickers for dividend adjustments."""
    print("Dividend Verification and VPA Price Update")
    print("=" * 50)
    
    # Get list of tickers from vpa_data directory
    if not os.path.exists('vpa_data'):
        print("Error: vpa_data directory not found")
        return
    
    vpa_files = [f for f in os.listdir('vpa_data') if f.endswith('.md')]
    tickers = [f.replace('.md', '') for f in vpa_files]
    
    updated_tickers = []
    no_dividend_tickers = []
    error_tickers = []
    
    for ticker in sorted(tickers):
        print(f"\\nChecking {ticker}...")
        result = verify_and_update_ticker(ticker)
        
        if 'error' in result:
            print(f"  ERROR: {result['error']}")
            error_tickers.append(ticker)
        elif result['status'] == 'updated':
            print(f"  DIVIDEND DETECTED: {result['message']}")
            updated_tickers.append((ticker, result['adjustment_ratio']))
        elif result['status'] == 'dividend_detected':
            print(f"  DIVIDEND DETECTED: {result['message']}")
            updated_tickers.append((ticker, result['adjustment_ratio']))
        elif result['status'] == 'no_dividend':
            print(f"  OK: {result['message']}")
            no_dividend_tickers.append(ticker)
        else:
            print(f"  INFO: {result['message']}")
    
    # Summary
    print(f"\\n{'='*50}")
    print("DIVIDEND VERIFICATION SUMMARY")
    print(f"{'='*50}")
    print(f"Total tickers checked: {len(tickers)}")
    print(f"Tickers with dividend adjustments: {len(updated_tickers)}")
    print(f"Tickers with no dividends: {len(no_dividend_tickers)}")
    print(f"Tickers with errors: {len(error_tickers)}")
    
    if updated_tickers:
        print(f"\\nTickers updated for dividend adjustments:")
        for ticker, ratio in updated_tickers:
            print(f"  {ticker}: adjustment ratio {ratio:.4f}")
    
    if error_tickers:
        print(f"\\nTickers with errors:")
        for ticker in error_tickers:
            print(f"  {ticker}")

if __name__ == "__main__":
    main()