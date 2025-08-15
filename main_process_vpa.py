#!/usr/bin/env python3
"""
Main VPA Processing Coordinator
Follows the protocol from tasks/DAILY_VPA.md and tasks/WEEKLY_VPA.md
Uses Python as coordinator and claude -p for complex analysis tasks
"""

import argparse
import csv
import glob
import json
import logging
import os
import pandas as pd
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path


def setup_logging(debug=False):
    """Setup logging configuration"""
    level = logging.DEBUG if debug else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Setup file handler in /tmp
    log_file = f"/tmp/vpa_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        handlers=[console_handler, file_handler]
    )
    
    logging.info(f"Logging initialized - Log file: {log_file}")
    return log_file


# Thread-safe logging lock
_log_lock = threading.Lock()


def thread_safe_log(level, message):
    """Thread-safe logging function"""
    with _log_lock:
        if level == 'info':
            logging.info(message)
        elif level == 'debug':
            logging.debug(message)
        elif level == 'warning':
            logging.warning(message)
        elif level == 'error':
            logging.error(message)


def get_dividend_info(dividend_folder):
    """
    Gather dividend information from dividend_info.txt files
    Returns dict of {ticker: {ratio, csv_file, info_file}}
    """
    dividend_path = Path(dividend_folder)
    dividend_info = {}
    
    logging.debug(f"Scanning for dividend info files in {dividend_folder}")
    
    # Look for *_dividend_info.txt files
    info_files = list(dividend_path.glob("*_dividend_info.txt"))
    
    for info_file in info_files:
        try:
            logging.debug(f"Reading dividend info from {info_file}")
            with open(info_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse dividend info
            ticker = None
            ratio = None
            csv_file = None
            
            for line in content.strip().split('\n'):
                if line.startswith('Ticker: '):
                    ticker = line.replace('Ticker: ', '').strip()
                elif line.startswith('Dividend Ratio: '):
                    ratio = float(line.replace('Dividend Ratio: ', '').strip())
                elif line.startswith('CSV File: '):
                    csv_file = line.replace('CSV File: ', '').strip()
            
            if ticker and ratio and csv_file:
                dividend_info[ticker] = {
                    'ratio': ratio,
                    'csv_file': dividend_path / csv_file,
                    'info_file': info_file
                }
                logging.info(f"📋 Found dividend info for {ticker}: ratio={ratio}")
            else:
                logging.warning(f"⚠️  Incomplete dividend info in {info_file}")
                
        except Exception as e:
            logging.error(f"❌ Error reading dividend info from {info_file}: {e}")
    
    return dividend_info


def get_dividend_tickers(week_mode=False):
    """
    Get list of tickers that have dividends available for optional adjustment
    Returns set of ticker symbols (empty set if no dividends or folder doesn't exist)
    """
    dividend_folder = "market_data_check_dividends_week" if week_mode else "market_data_check_dividends"
    dividend_path = Path(dividend_folder)
    dividend_tickers = set()
    
    logging.debug(f"Scanning for optional dividend tickers in {dividend_folder}")
    
    if not dividend_path.exists():
        logging.debug(f"No dividend folder found at {dividend_folder}")
        return dividend_tickers
    
    # Look for *_dividend_info.txt files to get ticker names
    info_files = list(dividend_path.glob("*_dividend_info.txt"))
    
    for info_file in info_files:
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract ticker name from file content
            for line in content.strip().split('\n'):
                if line.startswith('Ticker: '):
                    ticker = line.replace('Ticker: ', '').strip()
                    if ticker:
                        dividend_tickers.add(ticker)
                        logging.debug(f"Found optional dividend ticker: {ticker}")
                    break
                
        except Exception as e:
            logging.error(f"❌ Error reading dividend ticker from {info_file}: {e}")
    
    if dividend_tickers:
        logging.info(f"📋 Found {len(dividend_tickers)} tickers with optional dividend adjustments: {sorted(dividend_tickers)}")
    
    return dividend_tickers


def check_dividends_folder(week_mode=False):
    """
    Step 1: Check dividend adjustment folder
    Returns dividend_info dict if dividends need processing, None if no dividends
    """
    dividend_folder = "market_data_check_dividends_week" if week_mode else "market_data_check_dividends"
    dividend_path = Path(dividend_folder)
    
    logging.debug(f"Checking dividend folder: {dividend_folder}")
    
    if not dividend_path.exists():
        logging.info(f"✓ No dividend folder found at {dividend_folder}")
        return None
    
    dividend_files = list(dividend_path.glob("*.csv"))
    dividend_info_files = list(dividend_path.glob("*_dividend_info.txt"))
    
    if not dividend_files and not dividend_info_files:
        logging.info(f"✓ Dividend folder exists but is empty: {dividend_folder}")
        return None
    
    if not dividend_info_files:
        logging.warning(f"⚠️  Found {len(dividend_files)} CSV files but no dividend info files in {dividend_folder}")
        logging.error("❌ MANUAL DIVIDEND PROCESSING REQUIRED - Missing dividend info files")
        return {}
    
    logging.info(f"📊 Found {len(dividend_info_files)} dividend info files in {dividend_folder}")
    dividend_info = get_dividend_info(dividend_folder)
    
    if dividend_info:
        logging.info(f"✅ Ready to process dividends for {len(dividend_info)} tickers")
        return dividend_info
    else:
        logging.error("❌ Could not parse dividend information")
        return {}


def get_latest_csv_date(ticker, week_mode=False):
    """
    Get the latest date from the most recent CSV file for a ticker
    Returns (date_string, csv_file_path) or (None, None) if not found
    """
    market_folder = "market_data_week" if week_mode else "market_data"
    csv_pattern = f"{market_folder}/{ticker}_*.csv"
    
    logging.debug(f"Looking for CSV files: {csv_pattern}")
    csv_files = glob.glob(csv_pattern)
    
    if not csv_files:
        logging.debug(f"No CSV files found for {ticker} in {market_folder}")
        return None, None
    
    # Get the most recent file (by filename which includes date range)
    latest_file = max(csv_files)
    logging.debug(f"Using latest CSV file for {ticker}: {latest_file}")
    
    try:
        df = pd.read_csv(latest_file)
        if len(df) == 0:
            logging.warning(f"CSV file is empty for {ticker}: {latest_file}")
            return None, latest_file
        
        # Handle both "Date" and "time" column names
        date_column = "Date" if "Date" in df.columns else "time"
        latest_date = df.iloc[-1][date_column]
        logging.debug(f"Latest data date for {ticker}: {latest_date} ({len(df)} total rows)")
        return latest_date, latest_file
    except Exception as e:
        logging.error(f"Error reading CSV for {ticker}: {e}")
        return None, latest_file


def get_vpa_last_date(ticker, week_mode=False):
    """
    Get the last analysis date from VPA file
    Returns date_string or None if not found or file doesn't exist
    """
    vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
    vpa_file = Path(f"{vpa_folder}/{ticker}.md")
    
    logging.debug(f"Checking VPA file: {vpa_file}")
    
    if not vpa_file.exists():
        logging.debug(f"VPA file does not exist for {ticker}: {vpa_file}")
        return None
    
    try:
        with open(vpa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find all date entries (format: **Ngày YYYY-MM-DD:**)
        import re
        date_pattern = r'\*\*Ngày (\d{4}-\d{2}-\d{2}):\*\*'
        dates = re.findall(date_pattern, content)
        
        if dates:
            last_date = dates[-1]
            logging.debug(f"Found {len(dates)} VPA entries for {ticker}, last date: {last_date}")
            return last_date
        
        logging.debug(f"No VPA date entries found for {ticker}")
        return None
    except Exception as e:
        logging.error(f"Error reading VPA file for {ticker}: {e}")
        return None


def is_date_already_analyzed(ticker, target_date, week_mode=False):
    """
    Check if a specific date has already been analyzed in VPA file
    Returns True if date already exists, False otherwise
    """
    vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
    vpa_file = Path(f"{vpa_folder}/{ticker}.md")
    
    if not vpa_file.exists():
        logging.debug(f"VPA file does not exist for {ticker}, date {target_date} not analyzed")
        return False
    
    try:
        with open(vpa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if the specific date exists
        import re
        date_pattern = rf'\*\*Ngày {re.escape(target_date)}:\*\*'
        match = re.search(date_pattern, content)
        
        if match:
            logging.debug(f"Date {target_date} already analyzed for {ticker}")
            return True
        
        logging.debug(f"Date {target_date} not yet analyzed for {ticker}")
        return False
    except Exception as e:
        logging.error(f"Error checking VPA file for {ticker}, date {target_date}: {e}")
        return False


def get_dates_needing_analysis(ticker, week_mode=False):
    """
    Simple flow: loop from last row of CSV and check VPA. 
    If date not in VPA, add to list. If date exists in VPA, stop checking.
    Special case: If VPA file doesn't exist, only return last 2 dates.
    Returns list of dates that need analysis, empty list if none needed
    """
    logging.debug(f"Checking which dates need VPA analysis for {ticker}...")
    
    # Get all available dates from CSV
    market_folder = "market_data_week" if week_mode else "market_data"
    csv_pattern = f"{market_folder}/{ticker}_*.csv"
    
    csv_files = glob.glob(csv_pattern)
    if not csv_files:
        logging.warning(f"⚠️  No market data found for {ticker}")
        return []
    
    # Get the most recent CSV file
    latest_csv_file = max(csv_files)
    
    try:
        df = pd.read_csv(latest_csv_file)
        if len(df) == 0:
            logging.warning(f"CSV file is empty for {ticker}: {latest_csv_file}")
            return []
        
        # Handle both "Date" and "time" column names
        date_column = "Date" if "Date" in df.columns else "time"
        all_dates = df[date_column].tolist()
        
        logging.debug(f"Found {len(all_dates)} dates in CSV for {ticker}: {all_dates[0]} to {all_dates[-1]}")
        
        # Check if VPA file exists
        vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
        vpa_file = Path(f"{vpa_folder}/{ticker}.md")
        
        if not vpa_file.exists():
            # VPA file doesn't exist - return only last 2 dates
            last_2_dates = all_dates[-2:] if len(all_dates) >= 2 else all_dates
            logging.info(f"📊 {ticker}: VPA file doesn't exist, processing last {len(last_2_dates)} dates: {last_2_dates}")
            return last_2_dates
        
        # VPA file exists - use original logic
        dates_needing_analysis = []
        
        # Loop from last row backwards
        for i in range(len(all_dates) - 1, -1, -1):
            date_str = all_dates[i]
            
            # Check if this date is already analyzed
            if is_date_already_analyzed(ticker, date_str, week_mode):
                # Found an analyzed date - stop here since all previous dates should be analyzed
                break
            else:
                # Date is missing - add to beginning of list (to maintain chronological order)
                dates_needing_analysis.insert(0, date_str)
        
        if dates_needing_analysis:
            logging.info(f"📊 {ticker}: Need to analyze {len(dates_needing_analysis)} dates: {dates_needing_analysis}")
        else:
            logging.info(f"✓ {ticker}: All dates already analyzed")
        
        return dates_needing_analysis
        
    except Exception as e:
        logging.error(f"Error reading CSV for {ticker}: {e}")
        return []


def needs_vpa_analysis(ticker, week_mode=False):
    """
    Determine if a ticker needs new VPA analysis
    Returns True if analysis is needed, False otherwise
    """
    dates_needed = get_dates_needing_analysis(ticker, week_mode)
    return len(dates_needed) > 0


def get_ticker_context(ticker, target_date=None, week_mode=False):
    """
    Gather context for a ticker using reliable Python operations
    Returns context dictionary or None if data unavailable
    If target_date is provided, get context for that specific date
    """
    logging.debug(f"Gathering context for {ticker} (target_date: {target_date})...")
    
    market_folder = "market_data_week" if week_mode else "market_data"
    vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
    
    # Get CSV file
    latest_date, csv_file = get_latest_csv_date(ticker, week_mode)
    if not latest_date or not csv_file:
        logging.error(f"Cannot gather context for {ticker}: no market data available")
        return None
    
    try:
        df = pd.read_csv(csv_file)
        
        # Handle both "Date" and "time" column names
        date_column = "Date" if "Date" in df.columns else "time"
        
        if target_date:
            # Find the specific target date
            target_row = df[df[date_column] == target_date]
            if target_row.empty:
                logging.error(f"Target date {target_date} not found in CSV for {ticker}")
                return None
            
            target_index = target_row.index[0]
            latest = df.iloc[target_index]
            previous = df.iloc[target_index - 1] if target_index > 0 else df.iloc[target_index]
            
            logging.debug(f"Using target date {target_date} for {ticker} (index: {target_index})")
        else:
            # Use latest data (original behavior)
            latest = df.iloc[-1]
            previous = df.iloc[-2] if len(df) > 1 else df.iloc[-1]
            target_date = latest[date_column]
        
        # Get last 10 OHLCV data points
        last_10_df = df.tail(10)
        last_10_ohlcv = []
        # Handle both "Date" and "time" column names for logging
        date_column = "Date" if "Date" in df.columns else "time"
        open_column = "Open" if "Open" in df.columns else "open"
        high_column = "High" if "High" in df.columns else "high"
        low_column = "Low" if "Low" in df.columns else "low"
        close_column = "Close" if "Close" in df.columns else "close"
        volume_column = "Volume" if "Volume" in df.columns else "volume"
        
        for _, row in last_10_df.iterrows():
            last_10_ohlcv.append({
                "date": row[date_column],
                "open": float(row[open_column]),
                "high": float(row[high_column]),
                "low": float(row[low_column]),
                "close": float(row[close_column]),
                "volume": int(row[volume_column])
            })
        
        logging.debug(f"Market data for {ticker}: {len(df)} rows, range {df.iloc[0][date_column]} to {df.iloc[-1][date_column]}")
        logging.debug(f"Latest price data: Open={latest[open_column]}, Close={latest[close_column]}, Volume={latest[volume_column]}")
        
        # Get existing VPA analysis and extract last 2 VPA entries
        vpa_file = Path(f"{vpa_folder}/{ticker}.md")
        previous_vpa = ""
        last_2_vpa_entries = []
        if vpa_file.exists():
            with open(vpa_file, 'r', encoding='utf-8') as f:
                previous_vpa = f.read()
            logging.debug(f"Loaded existing VPA analysis for {ticker}: {len(previous_vpa)} characters")
            
            # Extract last 2 VPA entries
            import re
            # Find all VPA entries (each entry starts with **Ngày and ends before the next **Ngày or EOF)
            vpa_entries = re.split(r'(\*\*Ngày \d{4}-\d{2}-\d{2}:\*\*)', previous_vpa)
            
            # Reconstruct entries with their date headers
            entries_with_headers = []
            for i in range(1, len(vpa_entries), 2):  # Start from 1 to skip the text before first date
                if i+1 < len(vpa_entries):
                    entry = vpa_entries[i] + vpa_entries[i+1]  # Date header + content
                    entries_with_headers.append(entry)
                elif i < len(vpa_entries):
                    entry = vpa_entries[i]  # Just the date header if no content follows
                    entries_with_headers.append(entry)
            
            # Get the last 2 entries (or all if less than 2)
            last_2_vpa_entries = entries_with_headers[-2:] if entries_with_headers else []
        else:
            logging.debug(f"No existing VPA file for {ticker}")
        
        context = {
            "ticker": ticker,
            "latest_date": target_date,  # Use the target date (or actual latest if not specified)
            "latest_ohlcv": {
                "open": float(latest[open_column]),
                "high": float(latest[high_column]),
                "low": float(latest[low_column]),
                "close": float(latest[close_column]),
                "volume": int(latest[volume_column])
            },
            "previous_ohlcv": {
                "open": float(previous[open_column]),
                "high": float(previous[high_column]),
                "low": float(previous[low_column]),
                "close": float(previous[close_column]),
                "volume": int(previous[volume_column])
            },
            "last_10_ohlcv": last_10_ohlcv,
            "last_2_vpa_entries": last_2_vpa_entries,
            "csv_file": csv_file,
            "data_rows": len(df),
            "date_range": f"{df.iloc[0][date_column]} to {df.iloc[-1][date_column]}",
            "previous_vpa": previous_vpa,
            "vpa_file": str(vpa_file),
            "timeframe": "weekly" if week_mode else "daily"
        }
        
        logging.debug(f"Context gathered successfully for {ticker}")
        return context
        
    except Exception as e:
        logging.error(f"Error gathering context for {ticker}: {e}")
        return None


def validate_vpa_file_format(ticker, week_mode=False):
    """
    Validate and fix VPA file formatting issues after AI processing
    Checks for proper line breaks between entries
    """
    vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
    vpa_file = Path(f"{vpa_folder}/{ticker}.md")
    
    if not vpa_file.exists():
        logging.warning(f"⚠️  VPA file doesn't exist for validation: {vpa_file}")
        return
    
    try:
        with open(vpa_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for missing line breaks between entries
        # Pattern: **Phân tích VPA/Wyckoff:** [text] **Ngày YYYY-MM-DD:**
        import re
        
        # Check if file has been completely overwritten (should have multiple entries)
        date_entries = re.findall(r'\*\*Ngày \d{4}-\d{2}-\d{2}:\*\*', content)
        
        # If we have existing VPA content in context but only 1 entry, file was overwritten
        vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
        
        if len(date_entries) == 1:
            logging.warning(f"⚠️  {ticker} VPA file appears to have been overwritten (only 1 entry found)")
            logging.warning(f"   This suggests the AI agent replaced the entire file instead of appending")
            
        # Also check for missing line breaks between entries  
        problem_pattern = r'(\*\*Phân tích VPA/Wyckoff:\*\*[^*]+?)(\*\*Ngày \d{4}-\d{2}-\d{2}:\*\*)'
        matches = re.findall(problem_pattern, content)
        
        if matches:
            logging.warning(f"⚠️  Found {len(matches)} formatting issues in {ticker} VPA file")
            
            # Fix by adding double line breaks between VPA analysis and next date entry
            fixed_content = re.sub(problem_pattern, r'\1\n\n\2', content)
            
            # Also ensure proper spacing after header
            if not content.startswith('# ' + ticker + '\n\n'):
                fixed_content = re.sub(r'^(# ' + re.escape(ticker) + r')\n?', r'\1\n\n', fixed_content)
            
            # Write back the fixed content
            with open(vpa_file, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            
            logging.info(f"✅ Fixed formatting issues in {ticker} VPA file")
            
            # Show git diff for the fix
            try:
                result = subprocess.run(['git', 'diff', str(vpa_file)], 
                                      capture_output=True, text=True, timeout=10)
                if result.stdout.strip():
                    logging.info(f"📝 Formatting changes for {ticker}:")
                    logging.info("-" * 60)
                    for line in result.stdout.split('\n')[:20]:  # Show first 20 lines
                        if line.startswith(('+', '-', '@@')):
                            logging.info(line)
                    logging.info("-" * 60)
            except Exception as e:
                logging.debug(f"Could not show git diff: {e}")
        else:
            logging.debug(f"✓ VPA file format looks good for {ticker}")
            
    except Exception as e:
        logging.error(f"❌ Error validating VPA file format for {ticker}: {e}")


def validate_vpa_content(ticker, vpa_entry):
    """
    Validate VPA content for common errors before saving
    Returns True if valid, False if errors found
    """
    import re
    
    # Extract all numeric values that could be prices
    price_patterns = [
        r'từ\s+(\d+\.?\d*)\s+(?:lên|xuống)\s+(\d+\.?\d*)',  # "từ X lên Y" patterns
        r'tăng.*?từ\s+(\d+\.?\d*)\s+lên\s+(\d+\.?\d*)',
        r'giảm.*?từ\s+(\d+\.?\d*)\s+xuống\s+(\d+\.?\d*)',
        r'mở cửa.*?(\d+\.?\d*)',
        r'đóng cửa.*?(\d+\.?\d*)',
        r'cao nhất.*?(\d+\.?\d*)',
        r'thấp nhất.*?(\d+\.?\d*)'
    ]
    
    extracted_prices = []
    for pattern in price_patterns:
        matches = re.findall(pattern, vpa_entry)
        for match in matches:
            if isinstance(match, tuple):
                extracted_prices.extend([float(p) for p in match])
            else:
                extracted_prices.append(float(match))
    
    # Check for unreasonable price values
    errors = []
    for price in extracted_prices:
        if price < 1:  # Too low for Vietnamese stocks
            errors.append(f"Price {price} is too low (< 1 VND)")
        elif price > 500:  # Too high for most Vietnamese stocks
            errors.append(f"Price {price} is too high (> 500 VND)")
        elif 1 < price < 20 and price != int(price):  # Likely volume confusion
            # Volume numbers like 15.79 million often get confused as prices
            errors.append(f"Price {price} looks like volume data (millions of shares)")
    
    # Check for volume confusion patterns
    volume_confusion_patterns = [
        r'(\d+\.\d{1,2})\s*triệu.*?(?:lên|xuống|từ)',  # Volume numbers used in price contexts
        r'từ\s+(\d{1,2}\.\d{1,2})\s+lên',  # Small decimal numbers unlikely to be prices
    ]
    
    for pattern in volume_confusion_patterns:
        matches = re.findall(pattern, vpa_entry)
        for match in matches:
            value = float(match)
            if 1 < value < 50:  # Typical volume range
                errors.append(f"Value {value} in price context appears to be volume data")
    
    if errors:
        logging.warning(f"⚠️  {ticker}: VPA validation warnings:")
        for error in errors:
            logging.warning(f"   - {error}")
        # For now, return True but log warnings
        # In production, you might want to return False to reject bad content
        return True
    
    return True


def parse_and_append_vpa_analysis(ticker, ai_output, week_mode=False):
    """
    Parse AI agent output and append VPA analysis to appropriate file
    Returns True if successful, False otherwise
    """
    vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
    vpa_file = Path(f"{vpa_folder}/{ticker}.md")
    
    logging.debug(f"Parsing VPA output for {ticker}...")
    logging.debug(f"📄 Raw AI output length: {len(ai_output)} characters")
    logging.debug(f"📄 Raw AI output preview:\n{'-'*50}\n{ai_output[:800]}\n{'-'*50}")
    
    try:
        # Extract the VPA analysis from AI output
        # Look for the formatted VPA entry in the output
        lines = ai_output.strip().split('\n')
        vpa_entry_lines = []
        
        logging.debug(f"🔍 Splitting AI output into {len(lines)} lines")
        
        # Find VPA entry pattern: **Ngày YYYY-MM-DD:** followed by analysis
        in_vpa_entry = False
        for i, line in enumerate(lines):
            logging.debug(f"Line {i+1}: '{line}' (in_vpa_entry: {in_vpa_entry})")
            
            if '**Ngày ' in line and ':**' in line:
                logging.debug(f"✓ Found VPA date pattern in line {i+1}: '{line}'")
                in_vpa_entry = True
                vpa_entry_lines.append(line)
            elif in_vpa_entry:
                vpa_entry_lines.append(line)
                logging.debug(f"  Added line {i+1} to VPA entry: '{line}'")
                # Stop collecting if we hit another date entry or analysis summary
                if ('**Ngày ' in line and ':**' in line and len(vpa_entry_lines) > 1) or \
                   line.strip().startswith('---') or line.strip().startswith('###'):
                    vpa_entry_lines.pop()  # Remove the stopping line
                    logging.debug(f"  Stopped parsing at line {i+1} due to stop condition")
                    break
        
        logging.debug(f"🎯 Extracted {len(vpa_entry_lines)} lines for VPA entry")
        for i, line in enumerate(vpa_entry_lines):
            logging.debug(f"  VPA line {i+1}: '{line}'")
        
        if not vpa_entry_lines:
            logging.error(f"❌ {ticker}: Could not extract VPA entry from AI output")
            logging.error(f"❌ Lines that were checked:")
            for i, line in enumerate(lines[:10]):  # Show first 10 lines for debugging
                logging.error(f"   Line {i+1}: '{line}'")
            return False
        
        # Join the VPA entry and clean it up
        # Strip newlines from each part and join with single newline
        vpa_entry = '\n'.join([line.strip() for line in vpa_entry_lines]) + '\n'
        
        logging.debug(f"📝 Final VPA entry for {ticker} ({len(vpa_entry)} chars):")
        logging.debug(f"📝 VPA entry content:\n{'-'*40}\n{vpa_entry}\n{'-'*40}")
        
        # Validate VPA content before saving
        if not validate_vpa_content(ticker, vpa_entry):
            logging.error(f"❌ {ticker}: VPA content validation failed")
            return False
        
        # Create VPA directory if it doesn't exist
        vpa_folder_path = Path(vpa_folder)
        vpa_folder_path.mkdir(exist_ok=True)
        logging.debug(f"📁 VPA folder ensured: {vpa_folder_path}")
        
        # Append to existing file or create new one
        if vpa_file.exists():
            with open(vpa_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            logging.debug(f"📖 Existing VPA file found with {len(existing_content)} characters")
            
            # Append with proper spacing
            if not existing_content.endswith('\n'):
                vpa_entry = '\n' + vpa_entry
            
            new_content = existing_content + vpa_entry
            logging.debug(f"📝 Final content length: {len(new_content)} characters")
        else:
            # Create new file with header
            new_content = f"# {ticker}\n\n{vpa_entry}"
            logging.debug(f"📝 Creating new VPA file with header, total length: {len(new_content)} characters")
        
        # Write the updated content
        with open(vpa_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        logging.info(f"✅ {ticker}: VPA analysis appended to {vpa_file}")
        logging.debug(f"✅ File write successful: {vpa_file}")
        return True
        
    except Exception as e:
        logging.error(f"❌ {ticker}: Error parsing/appending VPA analysis: {e}")
        logging.error(f"❌ Exception details: {type(e).__name__}: {str(e)}")
        return False


def call_ai_agent_for_vpa_analysis(ticker, context, week_mode=False, agent='claude', verbose=False):
    """
    Call AI agent (claude or gemini) to generate VPA analysis output for a single ticker
    Returns True if successful, False otherwise
    """
    logging.debug(f"Preparing {agent.upper()} analysis for {ticker}...")
    
    try:
        # Prepare the AI agent prompt
        timeframe = "weekly" if week_mode else "daily"
        
        # Include all context directly in the prompt
        # Format last 10 OHLCV data points with clear labeling
        last_10_ohlcv_str = "\n".join([
            f"- {item['date']}: Open={item['open']}, High={item['high']}, Low={item['low']}, Close={item['close']}, Volume={item['volume']:,} shares"
            for item in context['last_10_ohlcv']
        ])
        
        # Format last 2 VPA entries
        last_2_vpa_str = "\n---\n".join(context['last_2_vpa_entries']) if context['last_2_vpa_entries'] else 'No previous VPA entries found.'
        
        prompt = f"""
Analyze ticker {ticker} for {timeframe} VPA using the provided context data.

=== MARKET DATA CONTEXT ===
Ticker: {context['ticker']}
Latest Date: {context['latest_date']}
Timeframe: {context['timeframe']}
Total Data Rows: {context['data_rows']}
Date Range: {context['date_range']}

Latest OHLCV ({context['latest_date']}):
- Open: {context['latest_ohlcv']['open']} VND
- High: {context['latest_ohlcv']['high']} VND  
- Low: {context['latest_ohlcv']['low']} VND
- Close: {context['latest_ohlcv']['close']} VND
- Volume: {context['latest_ohlcv']['volume']:,} shares

Previous OHLCV:
- Open: {context['previous_ohlcv']['open']} VND
- High: {context['previous_ohlcv']['high']} VND
- Low: {context['previous_ohlcv']['low']} VND  
- Close: {context['previous_ohlcv']['close']} VND
- Volume: {context['previous_ohlcv']['volume']:,} shares

Last 10 OHLCV Data Points:
{last_10_ohlcv_str}

Last 2 VPA Entries:
{last_2_vpa_str}

=== ANALYSIS TASK ===
1. Analyze the price/volume relationship using Wyckoff methodology
2. Compare current data with previous periods
3. Generate Vietnamese VPA analysis following the standard format
4. OUTPUT the analysis entry in the exact format below (do NOT edit files)

Required Output Format:
**Ngày {context['latest_date']}:** [Your detailed Vietnamese analysis of price/volume action, trends, support/resistance levels, and market context]. **Phân tích VPA/Wyckoff:** [Your Wyckoff signal assessment]

Example:
**Ngày 2025-08-01:** VCB tăng từ 61.5 lên 62.3 với khối lượng giao dịch đạt 15.2 triệu cổ phiếu. Cây nến tăng có biên độ rộng và đóng cửa gần mức cao nhất phiên. **Phân tích VPA/Wyckoff:** Sign of Strength (SOS) - Lực cầu mạnh mẽ với khối lượng gia tăng xác nhận xu hướng tăng.

Requirements:
- Use Vietnamese financial terminology only  
- Use DOT (.) as decimal separator, never comma (,)
- ALL PRICES must be in VND (Vietnamese Dong) - typical range 20-100 VND for stocks
- Volume is in SHARES (millions of shares) - never confuse volume numbers with prices
- When describing volume, always use "triệu cổ phiếu" (million shares) 
- SINGLE-LINE FORMAT: Start with **Ngày** followed by analysis, end with **Phân tích VPA/Wyckoff:**
- NO separate sections or line breaks between Ngày and Phân tích
- Build on previous VPA entries if they exist
- Compare current price/volume action to previous periods
- Apply proper Wyckoff VPA methodology
- Output ONLY the formatted analysis entry - no additional text

CRITICAL: 
- Stock prices are typically 20-100 VND per share
- Volume is typically 5-50 million shares per day
- NEVER mix these up - 42.32 million shares is VOLUME, not a price
- When writing "từ X lên Y", X and Y must be PRICES in VND, not volume

IMPORTANT: Output only the VPA analysis entry in the specified format. Do not use any file editing tools.
"""
        
        # Prepare command based on agent
        if agent == 'gemini':
            cmd = ['gemini', '-p', prompt]
        elif agent == 'gemini-2.5-flash':
            cmd = ['gemini', '-m', 'gemini-2.5-flash', '-p', prompt]
        else:
            cmd = ['claude', '-p', prompt]

        logging.info(f"🤖 Calling {agent.upper()} for {ticker} analysis...")
        
        # Show verbose output if requested
        if verbose:
            logging.info(f"📝 PROMPT FOR {ticker}:")
            logging.info("-" * 80)
            logging.info(prompt)
            logging.info("-" * 80)
            logging.info(f"📊 CONTEXT SUMMARY:")
            logging.info(f"   - Latest date: {context.get('latest_date', 'N/A')}")
            logging.info(f"   - Data rows: {context.get('data_rows', 'N/A')}")
            logging.info(f"   - Date range: {context.get('date_range', 'N/A')}")
            logging.info(f"   - VPA file exists: {bool(context.get('previous_vpa', ''))}")
            logging.info(f"   - Latest close: {context.get('latest_ohlcv', {}).get('close', 'N/A')}")
            logging.info(f"   - Latest volume: {context.get('latest_ohlcv', {}).get('volume', 'N/A')}")
        
        # Call the AI agent with enhanced monitoring
        logging.debug(f"🔍 {ticker}: Starting {agent.upper()} process...")
        
        import subprocess as sp
        import time
        import select
        import os
        
        process = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, text=True, preexec_fn=os.setsid)
        
        stdout_data = ""
        stderr_data = ""
        start_time = time.time()
        timeout_seconds = 300
        last_output_time = start_time
        
        logging.debug(f"🔍 {ticker}: Process started with PID {process.pid}")
        
        # Read output in real-time with timeout
        while True:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Check for timeout
            if elapsed > timeout_seconds:
                logging.error(f"⏰ {ticker}: Timeout after {timeout_seconds}s, killing process...")
                try:
                    os.killpg(os.getpgid(process.pid), 9)  # Kill process group
                except:
                    process.kill()
                process.wait()
                raise subprocess.TimeoutExpired(cmd, timeout_seconds)
            
            # Progress indicator every 60 seconds for regular VPA
            if int(elapsed) % 60 == 0 and int(elapsed) > 0:
                logging.info(f"⏳ {ticker}: Still processing VPA... ({elapsed:.0f}s elapsed)")
            
            # Check if there's data to read (non-blocking)
            ready, _, _ = select.select([process.stdout, process.stderr], [], [], 0.5)
            
            if process.stdout in ready:
                stdout_line = process.stdout.readline()
                if stdout_line:
                    stdout_data += stdout_line
                    last_output_time = current_time
                    if verbose:
                        logging.debug(f"🤖 {ticker} {agent.upper()}: {stdout_line.rstrip()}")
            
            if process.stderr in ready:
                stderr_line = process.stderr.readline()
                if stderr_line:
                    stderr_data += stderr_line
                    last_output_time = current_time
                    logging.warning(f"⚠️  {ticker} {agent.upper()} stderr: {stderr_line.rstrip()}")
            
            # Check if process is done
            if process.poll() is not None:
                logging.debug(f"🔍 {ticker}: Process finished, collecting remaining output...")
                # Get any remaining output
                remaining_stdout, remaining_stderr = process.communicate()
                if remaining_stdout:
                    stdout_data += remaining_stdout
                if remaining_stderr:
                    stderr_data += remaining_stderr
                break
            
            # Small sleep to prevent busy waiting
            time.sleep(0.1)
        
        # Create result object for compatibility
        class ProcessResult:
            def __init__(self, returncode, stdout, stderr):
                self.returncode = returncode
                self.stdout = stdout
                self.stderr = stderr
        
        result = ProcessResult(process.returncode, stdout_data, stderr_data)
        
        if result.returncode == 0:
            if result.stdout.strip():
                logging.info(f"🎯 {agent.upper()} generated analysis for {ticker}: {len(result.stdout)} chars")
                logging.debug(f"🎯 {agent.upper()} full output for {ticker}:")
                logging.debug(f"STDOUT:\n{'='*60}\n{result.stdout}\n{'='*60}")
                if result.stderr:
                    logging.debug(f"STDERR:\n{'='*60}\n{result.stderr}\n{'='*60}")
                
                # Parse and append the analysis output
                if parse_and_append_vpa_analysis(ticker, result.stdout, week_mode):
                    logging.info(f"✓ {ticker}: {agent.upper()} analysis completed and saved")
                    return True
                else:
                    logging.error(f"❌ {ticker}: Failed to parse/save {agent.upper()} analysis")
                    logging.error(f"❌ Raw output that failed to parse:")
                    logging.error(f"{'!'*60}\n{result.stdout}\n{'!'*60}")
                    return False
            else:
                logging.error(f"❌ {ticker}: {agent.upper()} returned empty output")
                if result.stderr:
                    logging.error(f"❌ {agent.upper()} stderr: {result.stderr}")
                return False
        else:
            logging.error(f"❌ {ticker}: {agent.upper()} analysis failed (return code: {result.returncode})")
            if result.stderr:
                logging.error(f"{agent.upper()} stderr for {ticker}: {result.stderr}")
            if result.stdout:
                logging.debug(f"{agent.upper()} stdout for {ticker}: {result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error(f"❌ {ticker}: {agent.upper()} analysis timed out after 300 seconds")
        return False
    except Exception as e:
        logging.error(f"❌ {ticker}: Error calling {agent.upper()} - {e}")
        return False


def split_content_by_lines(content, max_lines=10):
    """
    Split content into chunks by lines to avoid command line argument length issues
    Returns list of line chunks
    """
    if not content:
        return []
    
    lines = content.split('\n')
    chunks = []
    
    for i in range(0, len(lines), max_lines):
        chunk = '\n'.join(lines[i:i + max_lines])
        chunks.append(chunk)
    
    return chunks


def call_ai_agent_for_dividend_processing(ticker, dividend_info, week_mode=False, agent='claude', verbose=False):
    """
    Call AI agent to process dividend adjustments for a single ticker using line-based chunking
    Returns True if successful, False otherwise
    """
    logging.debug(f"Preparing {agent.upper()} dividend processing for {ticker}...")
    
    # Get VPA file paths
    vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
    vpa_file = Path(f"{vpa_folder}/{ticker}.md")
    main_vpa_file = Path("VPA_week.md" if week_mode else "VPA.md")
    
    # Read existing VPA content - ONLY individual ticker file for dividends
    individual_vpa_content = ""
    
    if vpa_file.exists():
        with open(vpa_file, 'r', encoding='utf-8') as f:
            individual_vpa_content = f.read()
    
    # SKIP reading main VPA.md for dividend processing - it's huge and contains all tickers
    main_vpa_content = ""
    
    try:
        # For dividend processing, only process individual VPA file (much smaller)
        individual_size = len(individual_vpa_content)
        
        logging.info(f"📊 {ticker}: Individual VPA file size: {individual_size} chars")
        
        # Individual VPA files are small (typically <30K chars), process directly
        if individual_size > 20000:  # Chunk if individual file is >20K to avoid timeouts
            logging.info(f"🔄 {ticker}: Individual VPA large, using chunking...")
            return process_dividend_with_chunking(ticker, dividend_info, individual_vpa_content, "", vpa_file, None, week_mode, agent, verbose)
        else:
            logging.info(f"🔄 {ticker}: Processing individual VPA directly...")
            return process_dividend_direct(ticker, dividend_info, individual_vpa_content, "", vpa_file, None, week_mode, agent, verbose)
        
    except Exception as e:
        logging.error(f"❌ {ticker}: Error in dividend processing - {e}")
        return False


def process_dividend_direct(ticker, dividend_info, individual_vpa_content, main_vpa_content, vpa_file, main_vpa_file, week_mode, agent, verbose, max_retries=2):
    """
    Process dividends directly - AI outputs adjusted content, Python handles file operations
    """
    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                logging.info(f"🔄 {ticker}: Retrying direct dividend processing (attempt {attempt + 1}/{max_retries + 1})")
            
            logging.debug(f"🔍 {ticker}: Starting direct dividend processing...")
            logging.debug(f"🔍 {ticker}: Dividend ratio: {dividend_info['ratio']:.6f}")
            logging.debug(f"🔍 {ticker}: Content length: {len(individual_vpa_content)} chars")
        
            # Simple prompt - just ask AI to adjust prices and output the content
            prompt = f"""Adjust Vietnamese stock prices in this VPA content for dividend ratio {dividend_info['ratio']}.

Divide ALL price numbers by {dividend_info['ratio']:.6f} and round to 1-2 decimals.
Attempt: {attempt + 1}

Content to adjust:
{individual_vpa_content}

Examples of what to change:
- "từ 66.5 lên 67.1" → "từ {66.5/dividend_info['ratio']:.1f} lên {67.1/dividend_info['ratio']:.1f}"  
- "tăng từ 68.1 lên 69.8" → "tăng từ {68.1/dividend_info['ratio']:.1f} lên {69.8/dividend_info['ratio']:.1f}"
- "giảm từ 69.7 xuống 69.0" → "giảm từ {69.7/dividend_info['ratio']:.1f} xuống {69.0/dividend_info['ratio']:.1f}"

IMPORTANT: Output ONLY the adjusted VPA content with updated prices. Keep all Vietnamese text and formatting exactly the same."""

            # Prepare command based on agent
            if agent == 'gemini':
                cmd = ['gemini', '-p', prompt]
            elif agent == 'gemini-2.5-flash':
                cmd = ['gemini', '-m', 'gemini-2.5-flash', '-p', prompt]
            else:
                cmd = ['claude', '-p', prompt]
            
            logging.info(f"🔄 Calling {agent.upper()} for {ticker} dividend processing (direct)...")
            logging.debug(f"🔍 {ticker}: Command: {' '.join(cmd[:3])}... (truncated)")
            logging.debug(f"🔍 {ticker}: Prompt length: {len(prompt)} chars")
            
            # Add progress indicator
            logging.info(f"⏳ {ticker}: Waiting for {agent.upper()} response...")
            
            # Increase timeout for retries
            timeout_seconds = 300 if attempt == 0 else 420  # 5 min first try, 7 min for retries
            
            # Use simple subprocess for now to avoid complexity
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_seconds)
            
            if result.returncode == 0 and result.stdout.strip():
                adjusted_content = result.stdout.strip()
                if attempt > 0:
                    logging.info(f"✅ {ticker}: Direct dividend processing succeeded on retry attempt {attempt + 1}")
                logging.info(f"🎯 {agent.upper()} adjusted {ticker} content: {len(adjusted_content)} chars")
                
                # Python handles file replacement - simple and direct
                if apply_simple_dividend_update(ticker, adjusted_content, vpa_file):
                    # Delete dividend files immediately after successful processing
                    cleanup_single_ticker_dividend_files(ticker, dividend_info)
                    logging.info(f"✅ {ticker}: Direct dividend processing completed successfully")
                    return True
            else:
                error_msg = f"Return code {result.returncode}"
                if result.stderr:
                    error_msg += f", stderr: {result.stderr[:200]}"
                logging.warning(f"⚠️  {ticker}: Direct dividend processing attempt {attempt + 1} failed: {error_msg}")
                
                # If this is the last attempt, fail
                if attempt == max_retries:
                    logging.error(f"❌ {ticker}: Direct dividend processing failed after {max_retries + 1} attempts")
                    return False
                    
        except subprocess.TimeoutExpired:
            logging.warning(f"⏰ {ticker}: Direct dividend processing timed out on attempt {attempt + 1}")
            if attempt == max_retries:
                logging.error(f"❌ {ticker}: Direct dividend processing timed out after {max_retries + 1} attempts")
                return False
        except Exception as e:
            logging.warning(f"⚠️  {ticker}: Error in direct dividend processing attempt {attempt + 1}: {e}")
            if attempt == max_retries:
                logging.error(f"❌ {ticker}: Direct dividend processing failed after {max_retries + 1} attempts")
                return False
    
    # Fallback (shouldn't reach here)
    logging.error(f"❌ {ticker}: Direct dividend processing failed unexpectedly")
    return False


def apply_simple_dividend_update(ticker, adjusted_content, vpa_file):
    """
    Simple file replacement - like VPA processing does
    """
    try:
        vpa_file.parent.mkdir(exist_ok=True)
        with open(vpa_file, 'w', encoding='utf-8') as f:
            f.write(adjusted_content)
        logging.info(f"✅ {ticker}: Updated VPA file with dividend-adjusted prices")
        return True
    except Exception as e:
        logging.error(f"❌ {ticker}: Error updating VPA file: {e}")
        return False


def cleanup_single_ticker_dividend_files(ticker, dividend_info):
    """
    Clean up dividend files for a single ticker immediately after processing
    dividend_info should be the individual ticker's info object, not the full dictionary
    """
    try:
        # dividend_info is the individual ticker's info object directly
        info = dividend_info
        
        # Remove CSV file if it exists
        if info['csv_file'].exists():
            info['csv_file'].unlink()
            logging.info(f"🗑️  Deleted dividend CSV: {info['csv_file'].name}")
        
        # Remove info file
        if info['info_file'].exists():
            info['info_file'].unlink()
            logging.info(f"🗑️  Deleted dividend info: {info['info_file'].name}")
            
        logging.info(f"🧹 {ticker}: Dividend files cleaned up immediately")
        
    except Exception as e:
        logging.warning(f"⚠️  {ticker}: Could not clean up dividend files: {e}")
        logging.debug(f"🔍 {ticker}: dividend_info type: {type(dividend_info)}")
        logging.debug(f"🔍 {ticker}: dividend_info content: {dividend_info}")


def process_dividend_with_chunking(ticker, dividend_info, individual_vpa_content, main_vpa_content, vpa_file, main_vpa_file, week_mode, agent, verbose):
    """
    Process dividends using line-based chunking for large files
    """
    try:
        # Split content into 10-line chunks
        individual_chunks = split_content_by_lines(individual_vpa_content, max_lines=10)
        main_chunks = split_content_by_lines(main_vpa_content, max_lines=10)
        
        logging.info(f"📊 {ticker}: Split into {len(individual_chunks)} individual chunks, {len(main_chunks)} main chunks")
        
        # Process individual VPA chunks
        processed_individual_chunks = []
        for i, chunk in enumerate(individual_chunks, 1):
            if not chunk.strip():
                processed_individual_chunks.append(chunk)
                continue
                
            logging.debug(f"Processing individual chunk {i}/{len(individual_chunks)} for {ticker}")
            processed_chunk = process_single_chunk(ticker, chunk, dividend_info, f"Individual-{i}", agent)
            if processed_chunk is not None:
                processed_individual_chunks.append(processed_chunk)
            else:
                logging.warning(f"⚠️  Failed to process individual chunk {i}, keeping original")
                processed_individual_chunks.append(chunk)
        
        # Process main VPA chunks
        processed_main_chunks = []
        for i, chunk in enumerate(main_chunks, 1):
            if not chunk.strip():
                processed_main_chunks.append(chunk)
                continue
                
            logging.debug(f"Processing main chunk {i}/{len(main_chunks)} for {ticker}")
            processed_chunk = process_single_chunk(ticker, chunk, dividend_info, f"Main-{i}", agent)
            if processed_chunk is not None:
                processed_main_chunks.append(processed_chunk)
            else:
                logging.warning(f"⚠️  Failed to process main chunk {i}, keeping original")
                processed_main_chunks.append(chunk)
        
        # Combine processed chunks
        updated_individual_content = '\n'.join(processed_individual_chunks)
        updated_main_content = '\n'.join(processed_main_chunks)
        
        # Apply updates to files
        if apply_chunked_dividend_updates(ticker, updated_individual_content, updated_main_content, vpa_file, main_vpa_file):
            logging.info(f"✅ {ticker}: Chunked dividend processing completed successfully")
            return True
        else:
            logging.error(f"❌ {ticker}: Failed to apply chunked dividend updates")
            return False
            
    except Exception as e:
        logging.error(f"❌ {ticker}: Error in chunked dividend processing - {e}")
        return False


def process_single_chunk(ticker, chunk_content, dividend_info, chunk_name, agent, max_retries=2):
    """
    Process a single chunk of VPA content for dividend adjustments with retry logic
    Returns processed content or None if failed
    """
    if not chunk_content or not chunk_content.strip():
        return ""
    
    for attempt in range(max_retries + 1):  # 0, 1, 2 (3 total attempts)
        try:
            if attempt > 0:
                logging.info(f"🔄 {ticker}: Retrying chunk {chunk_name} (attempt {attempt + 1}/{max_retries + 1})")
            
            prompt = f"""Update price references in this VPA text chunk for dividend adjustment.

Ticker: {ticker}
Dividend Ratio: {dividend_info['ratio']}
Chunk: {chunk_name}
Attempt: {attempt + 1}

Content to process:
{chunk_content}

Task: Divide all Vietnamese price values by {dividend_info['ratio']}.
- "từ 64.4 lên 64.9" → "từ {64.4/dividend_info['ratio']:.1f} lên {64.9/dividend_info['ratio']:.1f}"

Output: ONLY the updated chunk content with adjusted prices. If no prices found, output original text unchanged."""

            # Prepare command
            if agent == 'gemini':
                cmd = ['gemini', '-p', prompt]
            elif agent == 'gemini-2.5-flash':
                cmd = ['gemini', '-m', 'gemini-2.5-flash', '-p', prompt]
            else:
                cmd = ['claude', '-p', prompt]
            
            # Increase timeout for retries
            timeout = 120 if attempt == 0 else 180
            logging.debug(f"🔍 {ticker}: Processing chunk {chunk_name} with {timeout}s timeout (attempt {attempt + 1})")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            
            if result.returncode == 0 and result.stdout.strip():
                processed_content = result.stdout.strip()
                if attempt > 0:
                    logging.info(f"✅ {ticker}: Chunk {chunk_name} succeeded on retry attempt {attempt + 1}")
                logging.debug(f"✓ {ticker}: Processed chunk {chunk_name}: {len(processed_content)} chars")
                return processed_content
            else:
                error_msg = f"Return code {result.returncode}"
                if result.stderr:
                    error_msg += f", stderr: {result.stderr[:200]}"
                logging.warning(f"⚠️  {ticker}: Chunk {chunk_name} attempt {attempt + 1} failed: {error_msg}")
                
                # If this is the last attempt, return original content
                if attempt == max_retries:
                    logging.warning(f"❌ {ticker}: Chunk {chunk_name} failed after {max_retries + 1} attempts, using original")
                    return chunk_content
                    
        except subprocess.TimeoutExpired:
            logging.warning(f"⏰ {ticker}: Chunk {chunk_name} timed out on attempt {attempt + 1}")
            if attempt == max_retries:
                logging.warning(f"❌ {ticker}: Chunk {chunk_name} timed out after {max_retries + 1} attempts, using original")
                return chunk_content
        except Exception as e:
            logging.warning(f"⚠️  {ticker}: Error processing chunk {chunk_name} attempt {attempt + 1}: {e}")
            if attempt == max_retries:
                logging.warning(f"❌ {ticker}: Chunk {chunk_name} failed after {max_retries + 1} attempts, using original")
                return chunk_content
    
    # Fallback (shouldn't reach here)
    return chunk_content


def apply_chunked_dividend_updates(ticker, updated_individual_content, updated_main_content, vpa_file, main_vpa_file):
    """
    Apply chunked dividend updates to VPA files
    """
    try:
        # Apply individual VPA file update
        if updated_individual_content.strip():
            vpa_file.parent.mkdir(exist_ok=True)
            with open(vpa_file, 'w', encoding='utf-8') as f:
                f.write(updated_individual_content)
            logging.info(f"✅ {ticker}: Updated individual VPA file")
        
        # Apply main VPA file update  
        if updated_main_content.strip():
            with open(main_vpa_file, 'w', encoding='utf-8') as f:
                f.write(updated_main_content)
            logging.info(f"✅ {ticker}: Updated main VPA file")
        
        return True
        
    except Exception as e:
        logging.error(f"❌ {ticker}: Error applying chunked updates: {e}")
        return False


def parse_and_apply_dividend_updates(ticker, ai_output, vpa_file, main_vpa_file):
    """
    Parse AI agent output for dividend updates and apply them to files
    Returns True if successful, False otherwise
    """
    logging.debug(f"Parsing dividend updates for {ticker}...")
    logging.debug(f"📄 Raw AI output length: {len(ai_output)} characters")
    
    try:
        # Parse the output to extract individual and main VPA updates
        lines = ai_output.strip().split('\n')
        
        individual_vpa_section = False
        main_vpa_section = False
        individual_content = []
        main_content = []
        
        for line in lines:
            if '=== UPDATED INDIVIDUAL VPA ===' in line:
                individual_vpa_section = True
                main_vpa_section = False
                continue
            elif '=== UPDATED MAIN VPA ===' in line:
                individual_vpa_section = False
                main_vpa_section = True
                continue
            
            if individual_vpa_section:
                individual_content.append(line)
            elif main_vpa_section:
                main_content.append(line)
        
        # Clean up content
        individual_update = '\n'.join(individual_content).strip()
        main_update = '\n'.join(main_content).strip()
        
        logging.debug(f"📝 Individual VPA update length: {len(individual_update)} chars")
        logging.debug(f"📝 Main VPA update length: {len(main_update)} chars")
        
        # Apply individual VPA file update
        if individual_update and individual_update != "NO_CHANGES":
            if vpa_file.exists() or individual_update.strip():
                # Create VPA directory if it doesn't exist
                vpa_file.parent.mkdir(exist_ok=True)
                
                with open(vpa_file, 'w', encoding='utf-8') as f:
                    f.write(individual_update)
                logging.info(f"✅ {ticker}: Updated individual VPA file: {vpa_file}")
            else:
                logging.debug(f"📝 {ticker}: No individual VPA file to update")
        else:
            logging.debug(f"📝 {ticker}: No changes needed for individual VPA file")
        
        # Apply main VPA file update
        if main_update and main_update != "NO_CHANGES":
            if main_vpa_file.exists() or main_update.strip():
                with open(main_vpa_file, 'w', encoding='utf-8') as f:
                    f.write(main_update)
                logging.info(f"✅ {ticker}: Updated main VPA file: {main_vpa_file}")
            else:
                logging.debug(f"📝 {ticker}: No main VPA file to update")
        else:
            logging.debug(f"📝 {ticker}: No changes needed for main VPA file")
        
        logging.info(f"✅ {ticker}: Dividend updates applied successfully")
        return True
        
    except Exception as e:
        logging.error(f"❌ {ticker}: Error parsing/applying dividend updates: {e}")
        logging.error(f"❌ Exception details: {type(e).__name__}: {str(e)}")
        logging.error(f"❌ Raw output that failed to parse:")
        logging.error(f"{'!'*60}\n{ai_output}\n{'!'*60}")
        return False


def cleanup_dividend_files(dividend_info):
    """
    Clean up processed dividend files
    """
    logging.info("🧹 Cleaning up processed dividend files...")
    
    for ticker, info in dividend_info.items():
        try:
            # Remove CSV file if it exists
            if info['csv_file'].exists():
                info['csv_file'].unlink()
                logging.debug(f"Deleted dividend CSV: {info['csv_file']}")
            
            # Remove info file
            if info['info_file'].exists():
                info['info_file'].unlink()
                logging.debug(f"Deleted dividend info: {info['info_file']}")
                
            logging.info(f"✅ Cleaned up dividend files for {ticker}")
            
        except Exception as e:
            logging.error(f"❌ Error cleaning up dividend files for {ticker}: {e}")


def process_dividends(dividend_info, week_mode=False, agent='claude', verbose=False):
    """
    Process all dividend adjustments using AI agent
    Returns True if all successful, False if any failed
    """
    if not dividend_info:
        return True
    
    logging.info(f"🔄 Starting dividend processing for {len(dividend_info)} tickers using {agent.upper()}...")
    
    successful = 0
    failed = []
    
    for ticker, info in dividend_info.items():
        logging.info(f"📋 Processing dividend for {ticker} (ratio: {info['ratio']})...")
        
        # Validate dividend ratio
        if info['ratio'] <= 0 or info['ratio'] > 10:
            logging.error(f"❌ {ticker}: Invalid dividend ratio {info['ratio']}")
            failed.append(ticker)
            continue
        
        # Process dividend with AI agent
        if call_ai_agent_for_dividend_processing(ticker, info, week_mode, agent, verbose):
            successful += 1
            logging.info(f"✅ {ticker}: Dividend processing completed")
        else:
            failed.append(ticker)
            logging.error(f"❌ {ticker}: Dividend processing failed")
    
    # Summary
    logging.info(f"📊 Dividend Processing Summary:")
    logging.info(f"   ✅ Successful: {successful}")
    logging.info(f"   ❌ Failed: {len(failed)}")
    
    if failed:
        logging.warning(f"   Failed tickers: {', '.join(failed)}")
    
    # Files are cleaned up individually after each ticker processing
    # No bulk cleanup needed since files are deleted immediately after success
    
    return len(failed) == 0


def process_single_ticker_date(ticker, target_date, week_mode, agent, verbose, task_index, total_tasks):
    """
    Process a single ticker for a specific date VPA analysis
    Returns (ticker, target_date, success, duration, error_msg)
    """
    start_time = datetime.now()
    
    try:
        thread_safe_log('info', f"[{task_index}/{total_tasks}] 📈 Processing {ticker} for {target_date}...")
        
        # Check if this date is already analyzed
        if is_date_already_analyzed(ticker, target_date, week_mode):
            thread_safe_log('info', f"✓ {ticker} {target_date}: Already analyzed")
            duration = datetime.now() - start_time
            return ticker, target_date, True, duration.total_seconds(), None
        
        # Get context for specific date
        thread_safe_log('debug', f"Gathering context for {ticker} on {target_date}...")
        context = get_ticker_context(ticker, target_date, week_mode)
        if not context:
            error_msg = f"Could not gather context for {ticker} on {target_date}"
            thread_safe_log('error', f"❌ {ticker} {target_date}: {error_msg}")
            duration = datetime.now() - start_time
            return ticker, target_date, False, duration.total_seconds(), error_msg
        
        # Call AI agent for analysis
        thread_safe_log('debug', f"Starting {agent.upper()} analysis for {ticker} on {target_date}...")
        if call_ai_agent_for_vpa_analysis(ticker, context, week_mode, agent, verbose):
            duration = datetime.now() - start_time
            thread_safe_log('info', f"✅ {ticker} {target_date}: Analysis completed in {duration.total_seconds():.1f}s")
            return ticker, target_date, True, duration.total_seconds(), None
        else:
            error_msg = f"AI analysis failed for {ticker} on {target_date}"
            duration = datetime.now() - start_time
            thread_safe_log('error', f"❌ {ticker} {target_date}: {error_msg} after {duration.total_seconds():.1f}s")
            return ticker, target_date, False, duration.total_seconds(), error_msg
            
    except Exception as e:
        error_msg = f"Exception processing {ticker} on {target_date}: {e}"
        duration = datetime.now() - start_time
        thread_safe_log('error', f"❌ {ticker} {target_date}: {error_msg}")
        return ticker, target_date, False, duration.total_seconds(), error_msg


def process_single_ticker(ticker, week_mode, agent, verbose, ticker_index, total_tickers):
    """
    Process a single ticker for VPA analysis (legacy function for backward compatibility)
    Returns (ticker, success, duration, error_msg)
    """
    start_time = datetime.now()
    
    try:
        thread_safe_log('info', f"[{ticker_index}/{total_tickers}] 📈 Processing {ticker}...")
        
        # Check if ticker needs analysis
        if not needs_vpa_analysis(ticker, week_mode):
            thread_safe_log('info', f"✓ {ticker}: Already up to date")
            duration = datetime.now() - start_time
            return ticker, True, duration.total_seconds(), None
        
        # Get context
        thread_safe_log('debug', f"Gathering context for {ticker}...")
        context = get_ticker_context(ticker, None, week_mode)
        if not context:
            error_msg = f"Could not gather context for {ticker}"
            thread_safe_log('error', f"❌ {ticker}: {error_msg}")
            duration = datetime.now() - start_time
            return ticker, False, duration.total_seconds(), error_msg
        
        # Call AI agent for analysis
        thread_safe_log('debug', f"Starting {agent.upper()} analysis for {ticker}...")
        if call_ai_agent_for_vpa_analysis(ticker, context, week_mode, agent, verbose):
            duration = datetime.now() - start_time
            thread_safe_log('info', f"✅ {ticker}: Analysis completed in {duration.total_seconds():.1f}s")
            return ticker, True, duration.total_seconds(), None
        else:
            error_msg = f"AI analysis failed for {ticker}"
            duration = datetime.now() - start_time
            thread_safe_log('error', f"❌ {ticker}: {error_msg} after {duration.total_seconds():.1f}s")
            return ticker, False, duration.total_seconds(), error_msg
            
    except Exception as e:
        error_msg = f"Exception processing {ticker}: {e}"
        duration = datetime.now() - start_time
        thread_safe_log('error', f"❌ {ticker}: {error_msg}")
        return ticker, False, duration.total_seconds(), error_msg


def process_ticker_dates_sequentially(ticker, dates_needed, week_mode, agent, verbose):
    """
    Process all dates for a single ticker sequentially (chronologically)
    Returns (ticker, successful_count, failed_dates, total_duration)
    """
    logging.info(f"📈 Processing {ticker} with {len(dates_needed)} dates sequentially...")
    
    start_time = datetime.now()
    successful_count = 0
    failed_dates = []
    
    for i, target_date in enumerate(dates_needed, 1):
        logging.info(f"  📅 [{i}/{len(dates_needed)}] {ticker}: Processing {target_date}...")
        
        try:
            # Check if this date is already analyzed (in case of race conditions from previous runs)
            if is_date_already_analyzed(ticker, target_date, week_mode):
                logging.info(f"  ✓ {ticker} {target_date}: Already analyzed, skipping")
                successful_count += 1
                continue
            
            # Get context for specific date
            context = get_ticker_context(ticker, target_date, week_mode)
            if not context:
                error_msg = f"Could not gather context for {ticker} on {target_date}"
                logging.error(f"  ❌ {ticker} {target_date}: {error_msg}")
                failed_dates.append(target_date)
                continue
            
            # Call AI agent for analysis
            if call_ai_agent_for_vpa_analysis(ticker, context, week_mode, agent, verbose):
                logging.info(f"  ✅ {ticker} {target_date}: Analysis completed")
                successful_count += 1
            else:
                logging.error(f"  ❌ {ticker} {target_date}: AI analysis failed")
                failed_dates.append(target_date)
                
        except Exception as e:
            logging.error(f"  ❌ {ticker} {target_date}: Exception - {e}")
            failed_dates.append(target_date)
    
    total_duration = datetime.now() - start_time
    logging.info(f"✅ {ticker}: Completed {successful_count}/{len(dates_needed)} dates in {total_duration}")
    
    return ticker, successful_count, failed_dates, total_duration.total_seconds()


def process_tickers(week_mode=False, agent='claude', verbose=False, workers=4):
    """
    Process all tickers for VPA analysis with sequential date processing per ticker
    Each ticker processes its dates sequentially, but tickers are processed in parallel
    """
    logging.info(f"📊 Starting sequential-by-date ticker processing using {agent.upper()} with {workers} workers...")
    
    # Read tickers from ticker_group.json
    tickers = []
    try:
        logging.debug("Reading ticker_group.json...")
        with open('ticker_group.json', 'r', encoding='utf-8') as f:
            ticker_groups_config = json.load(f)
        
        # Join all tickers from all sectors into one list
        for sector, sector_tickers in ticker_groups_config.items():
            tickers.extend(sector_tickers)
        
        # Remove duplicates while preserving order
        seen = set()
        tickers = [ticker for ticker in tickers if not (ticker in seen or seen.add(ticker))]
        
        logging.info(f"Loaded {len(tickers)} tickers from ticker_group.json across {len(ticker_groups_config)} sectors")
    except Exception as e:
        logging.error(f"❌ Error reading ticker_group.json: {e}")
        return False
    
    # Check for dividend tickers (for informational purposes only - they will be processed normally)
    dividend_tickers = get_dividend_tickers(week_mode)
    if dividend_tickers:
        logging.info(f"📋 Found {len(dividend_tickers)} tickers with optional dividend adjustments: {sorted(dividend_tickers)}")
        logging.info(f"✓ These tickers will be processed normally (dividend adjustment is optional)")
    
    logging.info(f"📊 Processing {len(tickers)} tickers for {'weekly' if week_mode else 'daily'} VPA analysis using {agent.upper()}")
    
    # Build ticker-dates mapping for tickers that need processing
    logging.info("🔍 Checking which dates need analysis for each ticker...")
    ticker_dates_map = {}  # {ticker: [dates_list]}
    total_dates_count = 0
    
    for ticker in tickers:
        dates_needed = get_dates_needing_analysis(ticker, week_mode)
        if dates_needed:
            ticker_dates_map[ticker] = dates_needed
            total_dates_count += len(dates_needed)
    
    if not ticker_dates_map:
        logging.info("✓ All ticker dates are up to date - no analysis needed")
        return True
    
    logging.info(f"📊 Found {len(ticker_dates_map)} tickers with {total_dates_count} dates to process:")
    for ticker, dates in ticker_dates_map.items():
        logging.info(f"   - {ticker}: {len(dates)} dates ({dates[0]} to {dates[-1]})")
    
    # Process tickers in parallel (but dates sequential within each ticker)
    successful_tickers = 0
    failed_ticker_dates = {}  # {ticker: [failed_dates]}
    ticker_processing_times = []
    completed_tickers = 0
    
    logging.info(f"🚀 Starting parallel ticker processing with {workers} workers...")
    logging.info(f"   📅 Each ticker will process its dates SEQUENTIALLY to avoid race conditions")
    process_start_time = datetime.now()
    
    # Use ThreadPoolExecutor for parallel processing of tickers
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit ticker processing tasks
        future_to_ticker = {}
        for ticker, dates_needed in ticker_dates_map.items():
            future = executor.submit(process_ticker_dates_sequentially, ticker, dates_needed, week_mode, agent, verbose)
            future_to_ticker[future] = ticker
        
        # Process completed ticker tasks as they finish
        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            completed_tickers += 1
            
            try:
                result_ticker, successful_count, failed_dates, duration = future.result()
                ticker_processing_times.append(duration)
                
                if not failed_dates:
                    successful_tickers += 1
                    thread_safe_log('info', f"✅ {result_ticker}: All {successful_count} dates completed successfully")
                else:
                    failed_ticker_dates[result_ticker] = failed_dates
                    thread_safe_log('error', f"❌ {result_ticker}: {len(failed_dates)} dates failed out of {successful_count + len(failed_dates)}")
                
                # Progress reporting
                remaining_tickers = len(ticker_dates_map) - completed_tickers
                if remaining_tickers > 0:
                    avg_time = sum(ticker_processing_times) / len(ticker_processing_times)
                    estimated_remaining = remaining_tickers * avg_time
                    thread_safe_log('info', f"⏱️  Progress: {completed_tickers}/{len(ticker_dates_map)} tickers, Est. remaining: {estimated_remaining/60:.1f}min")
                        
            except Exception as e:
                failed_ticker_dates[ticker] = ["Exception occurred"]
                thread_safe_log('error', f"❌ {ticker}: Exception in ticker processing: {e}")
    
    total_processing_time = datetime.now() - process_start_time
    
    # Calculate summary statistics
    total_successful_dates = 0
    total_failed_dates = 0
    for ticker, dates in ticker_dates_map.items():
        if ticker in failed_ticker_dates:
            failed_count = len(failed_ticker_dates[ticker])
            total_failed_dates += failed_count
            total_successful_dates += len(dates) - failed_count
        else:
            total_successful_dates += len(dates)
    
    # Summary
    logging.info(f"\n📊 Sequential-by-Date VPA Analysis Summary:")
    logging.info(f"   👥 Workers used: {workers} (for parallel ticker processing)")
    logging.info(f"   🎯 Processing strategy: Sequential dates within ticker, parallel across tickers")
    logging.info(f"   📈 Tickers processed: {len(ticker_dates_map)}")
    logging.info(f"   📅 Total dates processed: {total_dates_count}")
    logging.info(f"   ✅ Successful tickers: {successful_tickers}")
    logging.info(f"   ✓ Successful dates: {total_successful_dates}")
    logging.info(f"   ❌ Failed dates: {total_failed_dates}")
    logging.info(f"   ⏱️  Total processing time: {total_processing_time}")
    if ticker_processing_times:
        logging.info(f"   📊 Average time per ticker: {sum(ticker_processing_times)/len(ticker_processing_times):.1f}s")
    if total_dates_count > 0:
        logging.info(f"   📈 Success rate: {total_successful_dates/total_dates_count*100:.1f}%")
    
    if failed_ticker_dates:
        logging.warning(f"   Failed ticker-date details:")
        for ticker, failed_dates in failed_ticker_dates.items():
            logging.warning(f"   - {ticker}: {len(failed_dates)} failed dates")
            for date in failed_dates[:5]:  # Show first 5 failed dates
                logging.warning(f"     • {date}")
            if len(failed_dates) > 5:
                logging.warning(f"     ... and {len(failed_dates) - 5} more")
    
    return total_failed_dates == 0


def main():
    parser = argparse.ArgumentParser(description='Process VPA analysis using AI agent coordination')
    parser.add_argument('--week', action='store_true', 
                       help='Process weekly VPA analysis instead of daily')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug logging')
    parser.add_argument('--agent', choices=['claude', 'gemini', 'gemini-2.5-flash'], default='gemini',
                       help='AI agent to use for analysis (default: gemini)')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed prompts and context sent to AI agents')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers for VPA processing (default: 4)')
    parser.add_argument('--fix-dividends', action='store_true',
                       help='Process dividend adjustments for tickers in market_data_check_dividends/')
    
    # Check if user explicitly specified agent before parsing
    import sys
    user_specified_agent = '--agent' in sys.argv
    
    args = parser.parse_args()
    
    # Determine dividend agent to use (without modifying args.agent)
    if args.fix_dividends and not user_specified_agent:
        dividend_agent = 'gemini-2.5-flash'
    else:
        dividend_agent = args.agent
    
    # Setup logging first
    log_file = setup_logging(debug=args.debug)
    
    # Show agent selection info for fix-dividends mode
    if args.fix_dividends and not user_specified_agent:
        logging.info(f"🔧 Fix-dividends mode: Using default agent {dividend_agent}")
    elif args.fix_dividends and user_specified_agent:
        logging.info(f"🔧 Fix-dividends mode: Using user-specified agent {dividend_agent}")
    
    logging.info("🚀 Starting VPA Processing Coordinator")
    logging.info(f"📅 Mode: {'Weekly' if args.week else 'Daily'}")
    logging.info(f"🤖 AI Agent: {dividend_agent.upper() if args.fix_dividends else args.agent.upper()}")
    logging.info(f"👥 Parallel Workers: {args.workers}")
    logging.info(f"📁 Data folders: {'market_data_week, vpa_data_week' if args.week else 'market_data, vpa_data'}")
    logging.info(f"📄 Log file: {log_file}")
    
    start_time = datetime.now()
    logging.info(f"⏰ Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Check if we're in fix-dividends mode
        if args.fix_dividends:
            logging.info("\n📋 Running in DIVIDEND FIX mode...")
            dividend_info = check_dividends_folder(args.week)
            
            if dividend_info is None:
                logging.info("✓ No dividends found - nothing to fix")
                return 0
            elif len(dividend_info) == 0:
                logging.error("❌ Error in dividend detection - check dividend files manually")
                return 1
            else:
                # Process dividends with AI agent
                logging.info(f"🔄 Processing {len(dividend_info)} dividend adjustments...")
                dividend_start = datetime.now()
                
                if not process_dividends(dividend_info, args.week, dividend_agent, args.verbose):
                    logging.error("❌ Some dividend adjustments failed")
                    return 1
                else:
                    logging.info("✅ All dividend adjustments completed successfully")
                
                dividend_duration = datetime.now() - dividend_start
                logging.info(f"⏱️  Dividend processing took: {dividend_duration}")
                
                total_duration = datetime.now() - start_time
                logging.info(f"\n🎉 Dividend Fix Complete!")
                logging.info(f"⏱️  Total time: {total_duration}")
                logging.info(f"📄 Full log saved to: {log_file}")
                return 0
        
        # Regular processing mode - detect dividends but don't process them
        # Step 1: Check for dividend tickers (detection only, no processing)
        logging.info("\n📋 Step 1: Checking for dividend adjustments...")
        dividend_tickers = get_dividend_tickers(args.week)
        
        # Step 2: Process all tickers (including dividend tickers with current prices)
        logging.info("\n📋 Step 2: Processing ticker VPA analysis...")
        process_start = datetime.now()
        success = process_tickers(args.week, args.agent, args.verbose, args.workers)
        process_duration = datetime.now() - process_start
        
        logging.info(f"⏱️  Ticker processing took: {process_duration}")
        
        if not success:
            logging.error("❌ Some tickers failed to process")
            return 1
        
        # Step 3: Merge results (call existing utility)
        logging.info("\n📋 Step 3: Merging VPA analysis...")
        try:
            merge_cmd = ['uv', 'run', 'merge_vpa.py']
            if args.week:
                merge_cmd.append('--week')
            
            logging.debug(f"Running merge command: {' '.join(merge_cmd)}")
            result = subprocess.run(merge_cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logging.info("✓ VPA analysis merged successfully")
                if result.stdout.strip():
                    logging.debug(f"Merge output: {result.stdout}")
            else:
                logging.warning(f"⚠️  Merge warning (return code: {result.returncode})")
                if result.stderr:
                    logging.warning(f"Merge stderr: {result.stderr}")
                logging.warning("You may need to merge manually using Read/Write tools")
                
        except subprocess.TimeoutExpired:
            logging.error("❌ Merge process timed out after 120 seconds")
            logging.error("Please merge individual VPA files manually")
        except Exception as e:
            logging.error(f"⚠️  Could not run merge_vpa.py: {e}")
            logging.error("Please merge individual VPA files manually")
        
        # Final summary
        total_duration = datetime.now() - start_time
        logging.info(f"\n🎉 VPA Processing Complete!")
        logging.info(f"⏱️  Total time: {total_duration}")
        logging.info(f"📁 Check {'VPA_week.md' if args.week else 'VPA.md'} for final results")
        logging.info(f"📄 Full log saved to: {log_file}")
        
        # Show dividend info if dividends are available (optional)
        if dividend_tickers:
            logging.info("")
            logging.info("=" * 80)
            logging.info("💡 OPTIONAL DIVIDEND ADJUSTMENTS AVAILABLE 💡")
            logging.info("=" * 80)
            logging.info("")
            logging.info(f"📋 The following {len(dividend_tickers)} tickers have optional dividend adjustments available:")
            for ticker in sorted(dividend_tickers):
                logging.info(f"   • {ticker}")
            logging.info("")
            logging.info("✓ These tickers were processed normally with current prices.")
            logging.info("🔧 If you want to apply dividend price adjustments, run:")
            logging.info("")
            fix_cmd = f"uv run main_process_vpa.py --agent gemini-2.5-flash --fix-dividends"
            if args.week:
                fix_cmd += " --week"
            if args.verbose:
                fix_cmd += " --verbose"
            if args.debug:
                fix_cmd += " --debug"
            logging.info(f"   {fix_cmd}")
            logging.info("")
            logging.info("=" * 80)
        
        return 0
        
    except KeyboardInterrupt:
        logging.warning("\n⚡ Process interrupted by user")
        return 130
    except Exception as e:
        logging.error(f"\n💥 Unexpected error: {e}")
        logging.error("Check the log file for full details")
        return 1


if __name__ == '__main__':
    sys.exit(main())
