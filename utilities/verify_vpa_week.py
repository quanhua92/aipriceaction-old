#!/usr/bin/env python3
"""
Weekly VPA Analysis Verification Script

This script verifies weekly VPA (Volume Price Analysis) assessments against actual weekly market data
by comparing the analysis statements with the corresponding price and volume data.
"""

import os
import csv
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

def parse_csv_data(csv_file: str) -> Dict[str, Dict]:
    """Parse CSV weekly market data into a dictionary indexed by date."""
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

def parse_vpa_analysis(vpa_file: str) -> List[Dict]:
    """Parse weekly VPA analysis file and extract date-specific analyses."""
    analyses = []
    try:
        with open(vpa_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all date entries
        date_pattern = r'- \*\*Ngày (\d{4}-\d{2}-\d{2}):\*\* (.+?)(?=- \*\*Ngày|\Z)'
        matches = re.findall(date_pattern, content, re.DOTALL)
        
        for date, analysis_text in matches:
            # Validate that this is a Monday date for weekly analysis
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            if date_obj.weekday() != 0:  # 0 = Monday
                print(f"WARNING: Non-Monday date found in weekly analysis: {date}")
            
            # Extract price movement information
            price_info = extract_weekly_price_movement(analysis_text)
            volume_info = extract_weekly_volume_info(analysis_text)
            vpa_signal = extract_vpa_signal(analysis_text)
            
            analyses.append({
                'date': date,
                'analysis_text': analysis_text.strip(),
                'price_movement': price_info,
                'volume_info': volume_info,
                'vpa_signal': vpa_signal
            })
    except Exception as e:
        print(f"Error reading {vpa_file}: {e}")
    
    return analyses

def normalize_vietnamese_number(number_str: str) -> str:
    """Convert Vietnamese number format (7,57) to English format (7.57)."""
    # Remove any trailing dots that aren't decimal separators
    number_str = number_str.rstrip('.')
    # Replace comma with dot for decimal separator
    return number_str.replace(',', '.')

def extract_weekly_price_movement(text: str) -> Optional[Dict]:
    """Extract weekly price movement information from analysis text."""
    # Pattern 1: Ticker name followed by weekly price movement with from/to prices
    # Examples: "AAA tăng từ 7.16 lên 7.17", "VCB giảm từ 57.2 xuống 56.7"
    ticker_price_pattern = r'[A-Z]{3,4}\s+(tăng|giảm|đi ngang).*?từ\s+([\d.,]+)\.?\s+(?:lên|xuống|đến|về)\s+([\d.,]+)'
    match = re.search(ticker_price_pattern, text)
    
    if match:
        direction = match.group(1)
        try:
            from_price = float(normalize_vietnamese_number(match.group(2)))
            to_price = float(normalize_vietnamese_number(match.group(3)))
            return {
                'direction': direction,
                'from_price': from_price,
                'to_price': to_price
            }
        except ValueError:
            pass
    
    # Pattern 2: Weekly trend analysis with specific price levels
    # Examples: "tuần này tăng từ 64.4 lên 64.7"
    weekly_price_pattern = r'tuần\s+này\s+(tăng|giảm|đi ngang).*?từ\s+([\d.,]+)\.?\s+(?:lên|xuống|đến|về)\s+([\d.,]+)'
    match = re.search(weekly_price_pattern, text)
    
    if match:
        direction = match.group(1)
        try:
            from_price = float(normalize_vietnamese_number(match.group(2)))
            to_price = float(normalize_vietnamese_number(match.group(3)))
            return {
                'direction': direction,
                'from_price': from_price,
                'to_price': to_price
            }
        except ValueError:
            pass
    
    # Pattern 3: Simple weekly direction
    weekly_direction_pattern = r'tuần\s+này\s+(tăng|giảm|đi ngang)'
    match = re.search(weekly_direction_pattern, text)
    if match:
        return {'direction': match.group(1)}
    
    # Pattern 4: Look for ticker followed by direction (for weekly context)
    ticker_simple_pattern = r'[A-Z]{3,4}\s+(tăng|giảm|đi ngang)'
    match = re.search(ticker_simple_pattern, text)
    if match:
        # Check if this is not a contextual reference
        start_pos = match.start()
        # Look for contextual words in the 20 characters before the match
        preceding_text = text[max(0, start_pos-20):start_pos].lower()
        contextual_words = ['tuần trước', 'tiếp nối', 'sau tuần']
        
        # If no contextual words found in preceding text, it's likely the actual movement
        if not any(word in preceding_text for word in contextual_words):
            return {'direction': match.group(1)}
    
    return None

def extract_weekly_volume_info(text: str) -> Optional[Dict]:
    """Extract weekly volume information from analysis text."""
    # Pattern 1: Weekly volume with millions
    # Examples: "khối lượng 12.5 triệu đơn vị", "khối lượng tăng (15.2 triệu)"
    volume_pattern1 = r'khối\s+lượng.*?(tăng|giảm|ổn định).*?\(([\d.,]+)\s*triệu'
    match1 = re.search(volume_pattern1, text, re.IGNORECASE)
    
    if match1:
        volume_direction = match1.group(1)
        try:
            volume_amount = float(normalize_vietnamese_number(match1.group(2)))
            return {
                'direction': volume_direction,
                'amount_millions': volume_amount
            }
        except ValueError:
            pass
    
    # Pattern 2: Direct volume amount without direction
    volume_pattern2 = r'khối\s+lượng\s+([\d.,]+)\s*triệu'
    match2 = re.search(volume_pattern2, text, re.IGNORECASE)
    
    if match2:
        try:
            volume_amount = float(normalize_vietnamese_number(match2.group(1)))
            return {
                'amount_millions': volume_amount
            }
        except ValueError:
            pass
    
    # Pattern 3: Volume comparison to previous week
    volume_comparison_pattern = r'khối\s+lượng.*?(tăng|giảm).*?so\s+với\s+tuần\s+trước'
    match3 = re.search(volume_comparison_pattern, text, re.IGNORECASE)
    
    if match3:
        return {
            'direction': match3.group(1),
            'comparison': 'previous_week'
        }
    
    return None

def extract_vpa_signal(text: str) -> Optional[str]:
    """Extract VPA signal from analysis text."""
    # Common VPA signals with priority order
    signals = [
        'Sign of Strength', 'SOS', 'Sign of Weakness', 'SOW',
        'Test for Supply', 'Test for Demand', 'Effort to Rise',
        'Effort to Fall', 'No Demand', 'No Supply', 'Stopping Volume',
        'Secondary Test', 'ST'
    ]
    
    for signal in signals:
        if signal in text:
            return signal
    
    return None

def verify_weekly_price_movement(analysis: Dict, market_data: Dict) -> Dict:
    """Verify if the weekly price movement analysis matches market data."""
    date = analysis['date']
    if date not in market_data:
        return {'status': 'error', 'message': f'No market data for {date}'}
    
    data = market_data[date]
    actual_direction = 'tăng' if data['close'] > data['open'] else 'giảm' if data['close'] < data['open'] else 'đi ngang'
    
    price_info = analysis.get('price_movement')
    if not price_info:
        return {'status': 'warning', 'message': 'No price movement info in analysis'}
    
    analyzed_direction = price_info.get('direction')
    
    verification = {
        'status': 'correct' if actual_direction == analyzed_direction else 'incorrect',
        'actual_direction': actual_direction,
        'analyzed_direction': analyzed_direction,
        'actual_open': data['open'],
        'actual_close': data['close'],
        'actual_high': data['high'],
        'actual_low': data['low'],
        'weekly_spread': data['high'] - data['low']
    }
    
    if 'from_price' in price_info and 'to_price' in price_info:
        # Verify specific price levels (allowing small tolerance for weekly data)
        tolerance = 0.05  # 5 cent tolerance for weekly data
        from_price_ok = abs(price_info['from_price'] - data['open']) <= tolerance
        to_price_ok = abs(price_info['to_price'] - data['close']) <= tolerance
        
        verification['price_accuracy'] = 'accurate' if from_price_ok and to_price_ok else 'inaccurate'
        verification['analyzed_from'] = price_info['from_price']
        verification['analyzed_to'] = price_info['to_price']
    
    return verification

def verify_weekly_volume_analysis(analysis: Dict, market_data: Dict, previous_data: Dict = None) -> Dict:
    """Verify weekly volume analysis against market data."""
    date = analysis['date']
    if date not in market_data:
        return {'status': 'error', 'message': f'No market data for {date}'}
    
    data = market_data[date]
    volume_info = analysis.get('volume_info')
    
    if not volume_info:
        return {'status': 'warning', 'message': 'No volume info in analysis'}
    
    actual_volume_millions = data['volume'] / 1_000_000
    analyzed_volume_millions = volume_info.get('amount_millions', 0)
    
    # Weekly volume direction verification requires previous week's data
    volume_direction_correct = None
    if previous_data and 'direction' in volume_info:
        prev_volume = previous_data['volume']
        actual_volume_direction = 'tăng' if data['volume'] > prev_volume else 'giảm'
        analyzed_volume_direction = volume_info.get('direction')
        volume_direction_correct = actual_volume_direction == analyzed_volume_direction
    
    # Check volume amount accuracy (allowing 15% tolerance for weekly data)
    volume_amount_correct = False
    if analyzed_volume_millions > 0:
        volume_amount_tolerance = 0.15 * analyzed_volume_millions
        volume_amount_correct = abs(actual_volume_millions - analyzed_volume_millions) <= volume_amount_tolerance
    
    return {
        'status': 'correct' if volume_direction_correct and volume_amount_correct else 'partial' if volume_direction_correct or volume_amount_correct else 'incorrect',
        'actual_volume_millions': round(actual_volume_millions, 2),
        'analyzed_volume_millions': analyzed_volume_millions,
        'volume_direction_correct': volume_direction_correct,
        'volume_amount_correct': volume_amount_correct,
        'analyzed_direction': volume_info.get('direction')
    }

def verify_ticker(ticker: str) -> Dict:
    """Verify weekly VPA analysis for a single ticker."""
    vpa_file = f"vpa_data_week/{ticker}.md"
    # Use dynamic date detection for CSV files
    csv_files = [f for f in os.listdir('market_data_week') if f.startswith(f"{ticker}_") and f.endswith('.csv')]
    
    if not csv_files:
        return {'error': f'No weekly market data file found for {ticker}'}
    
    # Use the most recent CSV file
    csv_file = f"market_data_week/{sorted(csv_files)[-1]}"
    
    if not os.path.exists(vpa_file):
        return {'error': f'Weekly VPA file not found: {vpa_file}'}
    
    if not os.path.exists(csv_file):
        return {'error': f'Weekly market data file not found: {csv_file}'}
    
    market_data = parse_csv_data(csv_file)
    vpa_analyses = parse_vpa_analysis(vpa_file)
    
    results = {
        'ticker': ticker,
        'total_analyses': len(vpa_analyses),
        'verifications': [],
        'summary': {'correct': 0, 'incorrect': 0, 'warnings': 0, 'errors': 0}
    }
    
    # Sort market data by date for previous week lookups
    sorted_dates = sorted(market_data.keys())
    date_to_prev = {}
    for i, date in enumerate(sorted_dates):
        if i > 0:
            date_to_prev[date] = market_data[sorted_dates[i-1]]
    
    for analysis in vpa_analyses:
        date = analysis['date']
        
        # Verify this is a Monday date
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            if date_obj.weekday() != 0:
                analysis['date_warning'] = f"Non-Monday date: {date}"
        except ValueError:
            analysis['date_warning'] = f"Invalid date format: {date}"
        
        price_verification = verify_weekly_price_movement(analysis, market_data)
        volume_verification = verify_weekly_volume_analysis(analysis, market_data, date_to_prev.get(date))
        
        verification_result = {
            'date': date,
            'analysis_text': analysis['analysis_text'][:150] + '...' if len(analysis['analysis_text']) > 150 else analysis['analysis_text'],
            'vpa_signal': analysis['vpa_signal'],
            'price_verification': price_verification,
            'volume_verification': volume_verification
        }
        
        if 'date_warning' in analysis:
            verification_result['date_warning'] = analysis['date_warning']
        
        # Determine overall status
        if price_verification['status'] == 'error' or volume_verification['status'] == 'error':
            verification_result['overall_status'] = 'error'
            results['summary']['errors'] += 1
        elif price_verification['status'] == 'warning' or volume_verification['status'] == 'warning':
            verification_result['overall_status'] = 'warning'
            results['summary']['warnings'] += 1
        elif price_verification['status'] == 'correct' and volume_verification['status'] in ['correct', 'partial']:
            verification_result['overall_status'] = 'correct'
            results['summary']['correct'] += 1
        else:
            verification_result['overall_status'] = 'incorrect'
            results['summary']['incorrect'] += 1
        
        results['verifications'].append(verification_result)
    
    return results

def main():
    """Main verification function."""
    print("Weekly VPA Analysis Verification Report")
    print("=" * 50)
    
    # Get list of tickers from vpa_data_week directory
    if not os.path.exists('vpa_data_week'):
        print("ERROR: vpa_data_week directory not found")
        return
    
    vpa_files = [f for f in os.listdir('vpa_data_week') if f.endswith('.md')]
    tickers = [f.replace('.md', '') for f in vpa_files]
    
    overall_summary = {'correct': 0, 'incorrect': 0, 'warnings': 0, 'errors': 0}
    problematic_tickers = []
    
    for ticker in sorted(tickers):
        print(f"\nVerifying {ticker}...")
        results = verify_ticker(ticker)
        
        if 'error' in results:
            print(f"  ERROR: {results['error']}")
            continue
        
        summary = results['summary']
        total = sum(summary.values())
        
        print(f"  Total weekly analyses: {total}")
        if total > 0:
            print(f"  Correct: {summary['correct']} ({summary['correct']/total*100:.1f}%)")
            print(f"  Incorrect: {summary['incorrect']} ({summary['incorrect']/total*100:.1f}%)")
            print(f"  Warnings: {summary['warnings']} ({summary['warnings']/total*100:.1f}%)")
            print(f"  Errors: {summary['errors']} ({summary['errors']/total*100:.1f}%)")
        else:
            print("  No weekly analyses found or parsed")
        
        # Update overall summary
        for key in overall_summary:
            overall_summary[key] += summary[key]
        
        # Flag problematic tickers
        if summary['incorrect'] > summary['correct']:
            problematic_tickers.append(ticker)
        
        # Show detailed issues for problematic analyses
        for verification in results['verifications']:
            if verification['overall_status'] in ['incorrect', 'error']:
                print(f"    ISSUE on {verification['date']}: {verification['analysis_text']}")
                if 'date_warning' in verification:
                    print(f"      DATE WARNING: {verification['date_warning']}")
                if verification['price_verification']['status'] == 'incorrect':
                    pv = verification['price_verification']
                    print(f"      Price: Analyzed '{pv['analyzed_direction']}' but actual was '{pv['actual_direction']}'")
                if verification['volume_verification']['status'] == 'incorrect':
                    print(f"      Volume: Analysis issues detected")
    
    # Overall summary
    print(f"\n{'='*50}")
    print("OVERALL WEEKLY VPA SUMMARY")
    print(f"{'='*50}")
    
    total_analyses = sum(overall_summary.values())
    if total_analyses > 0:
        print(f"Total weekly analyses verified: {total_analyses}")
        print(f"Correct: {overall_summary['correct']} ({overall_summary['correct']/total_analyses*100:.1f}%)")
        print(f"Incorrect: {overall_summary['incorrect']} ({overall_summary['incorrect']/total_analyses*100:.1f}%)")
        print(f"Warnings: {overall_summary['warnings']} ({overall_summary['warnings']/total_analyses*100:.1f}%)")
        print(f"Errors: {overall_summary['errors']} ({overall_summary['errors']/total_analyses*100:.1f}%)")
        
        if problematic_tickers:
            print(f"\nProblematic tickers (more incorrect than correct): {', '.join(problematic_tickers)}")
    else:
        print("No weekly analyses found to verify")

if __name__ == "__main__":
    main()