#!/usr/bin/env python3
"""
VPA Analysis Verification Script

This script verifies VPA (Volume Price Analysis) assessments against actual market data
by comparing the analysis statements with the corresponding price and volume data.
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

def parse_vpa_analysis(vpa_file: str) -> List[Dict]:
    """Parse VPA analysis file and extract date-specific analyses."""
    analyses = []
    try:
        with open(vpa_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find all date entries
        date_pattern = r'- \*\*Ngày (\d{4}-\d{2}-\d{2}):\*\* (.+?)(?=- \*\*Ngày|\Z)'
        matches = re.findall(date_pattern, content, re.DOTALL)
        
        for date, analysis_text in matches:
            # Extract price movement information
            price_info = extract_price_movement(analysis_text)
            volume_info = extract_volume_info(analysis_text)
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

def extract_price_movement(text: str) -> Optional[Dict]:
    """Extract price movement information from analysis text."""
    # Pattern 1: Ticker name followed by specific price movement with from/to prices
    # Examples: "AAA tăng từ 7,16 lên 7,17", "VCB giảm từ 57,2 xuống 56,7"
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
    
    # Pattern 2: General price movement with from/to prices (fallback)
    # Examples: "tăng từ 7,16 lên 7,17", "giảm từ 7,25 xuống 7,15"
    general_price_pattern = r'(tăng|giảm|đi ngang).*?từ\s+([\d.,]+)\.?\s+(?:lên|xuống|đến|về)\s+([\d.,]+)'
    match = re.search(general_price_pattern, text)
    
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
    
    # Pattern 3: Ticker name followed by direction with specific price levels
    # Examples: "AAA tăng nhẹ lên 56,6", "VCB đóng cửa ở 56,2"
    ticker_direction_pattern = r'[A-Z]{3,4}\s+(tăng|giảm|đi ngang)(?:\s+(?:nhẹ|mạnh|vọt))?(?:\s+(?:lên|xuống|về|ở))?\s+([\d.,]+)'
    match = re.search(ticker_direction_pattern, text)
    
    if match:
        direction = match.group(1)
        try:
            price = float(normalize_vietnamese_number(match.group(2)))
            return {
                'direction': direction,
                'price': price
            }
        except ValueError:
            pass
    
    # Pattern 4: Look for ticker followed by direction (simpler approach)
    ticker_simple_pattern = r'[A-Z]{3,4}\s+(tăng|giảm|đi ngang)'
    match = re.search(ticker_simple_pattern, text)
    if match:
        # Check if this is not a contextual reference
        start_pos = match.start()
        # Look for contextual words in the 20 characters before the match
        preceding_text = text[max(0, start_pos-20):start_pos].lower()
        contextual_words = ['sau phiên', 'tiếp nối', 'phiên trước']
        
        # If no contextual words found in preceding text, it's likely the actual movement
        if not any(word in preceding_text for word in contextual_words):
            return {'direction': match.group(1)}
    
    # Pattern 5: Simple fallback - just look for direction words
    # This will catch cases where previous patterns failed
    simple_direction_pattern = r'(tăng|giảm|đi ngang)'
    matches = list(re.finditer(simple_direction_pattern, text))
    
    if matches:
        # Prefer matches that are NOT preceded by contextual phrases
        for match in matches:
            start_pos = match.start()
            preceding_text = text[max(0, start_pos-15):start_pos].lower()
            contextual_phrases = ['sau phiên', 'tiếp nối', 'chuỗi', 'các phiên']
            
            # If this match is not in a contextual phrase, use it
            if not any(phrase in preceding_text for phrase in contextual_phrases):
                return {'direction': match.group(1)}
        
        # If all matches seem contextual, use the last one (often the actual movement)
        return {'direction': matches[-1].group(1)}
    
    return None

def extract_volume_info(text: str) -> Optional[Dict]:
    """Extract volume information from analysis text."""
    # Pattern 1: X.XX triệu đơn vị or X,XX triệu đơn vị
    volume_pattern1 = r'[Kk]hối lượng.*?(tăng|giảm|ổn định).*?\(([\d.,]+)\s*triệu'
    match1 = re.search(volume_pattern1, text)
    
    if match1:
        volume_direction = match1.group(1)
        # Remove commas before converting to float
        volume_amount = float(match1.group(2).replace(',', '.'))
        return {
            'direction': volume_direction,
            'amount_millions': volume_amount
        }
    
    # Pattern 2: X,XXX,XXX cổ phiếu or X,XXX,XXX đơn vị
    volume_pattern2 = r'[Kk]hối lượng.*?(tăng|giảm|ổn định).*?\(([\d,]+)\s*(?:cổ phiếu|đơn vị)\)'
    match2 = re.search(volume_pattern2, text)
    
    if match2:
        volume_direction = match2.group(1)
        # Convert from actual units to millions
        volume_actual = int(match2.group(2).replace(',', ''))
        volume_amount = volume_actual / 1_000_000
        return {
            'direction': volume_direction,
            'amount_millions': volume_amount
        }
    
    return None

def extract_vpa_signal(text: str) -> Optional[str]:
    """Extract VPA signal from analysis text."""
    # Common VPA signals
    signals = [
        'No Demand', 'Sign of Weakness', 'SOW', 'Effort to Rise',
        'Test for Supply', 'Sign of Strength', 'SOS'
    ]
    
    for signal in signals:
        if signal in text:
            return signal
    
    return None

def verify_price_movement(analysis: Dict, market_data: Dict) -> Dict:
    """Verify if the price movement analysis matches market data."""
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
        'actual_low': data['low']
    }
    
    if 'from_price' in price_info and 'to_price' in price_info:
        # Verify specific price levels (allowing small tolerance)
        tolerance = 0.02  # 2 cent tolerance
        from_price_ok = abs(price_info['from_price'] - data['open']) <= tolerance
        to_price_ok = abs(price_info['to_price'] - data['close']) <= tolerance
        
        verification['price_accuracy'] = 'accurate' if from_price_ok and to_price_ok else 'inaccurate'
        verification['analyzed_from'] = price_info['from_price']
        verification['analyzed_to'] = price_info['to_price']
    
    return verification

def verify_volume_analysis(analysis: Dict, market_data: Dict, previous_data: Dict = None) -> Dict:
    """Verify volume analysis against market data."""
    date = analysis['date']
    if date not in market_data:
        return {'status': 'error', 'message': f'No market data for {date}'}
    
    data = market_data[date]
    volume_info = analysis.get('volume_info')
    
    if not volume_info:
        return {'status': 'warning', 'message': 'No volume info in analysis'}
    
    actual_volume_millions = data['volume'] / 1_000_000
    analyzed_volume_millions = volume_info.get('amount_millions', 0)
    
    # Volume direction verification requires previous day's data
    volume_direction_correct = None
    if previous_data:
        prev_volume = previous_data['volume']
        actual_volume_direction = 'tăng' if data['volume'] > prev_volume else 'giảm'
        analyzed_volume_direction = volume_info.get('direction')
        volume_direction_correct = actual_volume_direction == analyzed_volume_direction
    
    # Check volume amount accuracy (allowing 10% tolerance)
    volume_amount_tolerance = 0.1 * analyzed_volume_millions
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
    """Verify VPA analysis for a single ticker."""
    vpa_file = f"vpa_data/{ticker}.md"
    csv_file = f"market_data/{ticker}_2025-01-02_to_2025-07-13.csv"
    
    if not os.path.exists(vpa_file):
        return {'error': f'VPA file not found: {vpa_file}'}
    
    if not os.path.exists(csv_file):
        return {'error': f'Market data file not found: {csv_file}'}
    
    market_data = parse_csv_data(csv_file)
    vpa_analyses = parse_vpa_analysis(vpa_file)
    
    results = {
        'ticker': ticker,
        'total_analyses': len(vpa_analyses),
        'verifications': [],
        'summary': {'correct': 0, 'incorrect': 0, 'warnings': 0, 'errors': 0}
    }
    
    # Sort market data by date for previous day lookups
    sorted_dates = sorted(market_data.keys())
    date_to_prev = {}
    for i, date in enumerate(sorted_dates):
        if i > 0:
            date_to_prev[date] = market_data[sorted_dates[i-1]]
    
    for analysis in vpa_analyses:
        date = analysis['date']
        
        price_verification = verify_price_movement(analysis, market_data)
        volume_verification = verify_volume_analysis(analysis, market_data, date_to_prev.get(date))
        
        verification_result = {
            'date': date,
            'analysis_text': analysis['analysis_text'][:100] + '...' if len(analysis['analysis_text']) > 100 else analysis['analysis_text'],
            'vpa_signal': analysis['vpa_signal'],
            'price_verification': price_verification,
            'volume_verification': volume_verification
        }
        
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
    print("VPA Analysis Verification Report")
    print("=" * 50)
    
    # Get list of tickers from vpa_data directory
    vpa_files = [f for f in os.listdir('vpa_data') if f.endswith('.md')]
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
        
        print(f"  Total analyses: {total}")
        if total > 0:
            print(f"  Correct: {summary['correct']} ({summary['correct']/total*100:.1f}%)")
            print(f"  Incorrect: {summary['incorrect']} ({summary['incorrect']/total*100:.1f}%)")
            print(f"  Warnings: {summary['warnings']} ({summary['warnings']/total*100:.1f}%)")
            print(f"  Errors: {summary['errors']} ({summary['errors']/total*100:.1f}%)")
        else:
            print("  No analyses found or parsed")
        
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
                if verification['price_verification']['status'] == 'incorrect':
                    pv = verification['price_verification']
                    print(f"      Price: Analyzed '{pv['analyzed_direction']}' but actual was '{pv['actual_direction']}'")
                if verification['volume_verification']['status'] == 'incorrect':
                    vv = verification['volume_verification']
                    print(f"      Volume: Analysis issues detected")
    
    # Overall summary
    print(f"\n{'='*50}")
    print("OVERALL SUMMARY")
    print(f"{'='*50}")
    
    total_analyses = sum(overall_summary.values())
    if total_analyses > 0:
        print(f"Total analyses verified: {total_analyses}")
        print(f"Correct: {overall_summary['correct']} ({overall_summary['correct']/total_analyses*100:.1f}%)")
        print(f"Incorrect: {overall_summary['incorrect']} ({overall_summary['incorrect']/total_analyses*100:.1f}%)")
        print(f"Warnings: {overall_summary['warnings']} ({overall_summary['warnings']/total_analyses*100:.1f}%)")
        print(f"Errors: {overall_summary['errors']} ({overall_summary['errors']/total_analyses*100:.1f}%)")
        
        if problematic_tickers:
            print(f"\nProblematic tickers (more incorrect than correct): {', '.join(problematic_tickers)}")

if __name__ == "__main__":
    main()