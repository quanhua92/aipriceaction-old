#!/usr/bin/env python3
"""
Main US & Crypto VPA Processing Coordinator
Follows the protocol for US indices and cryptocurrency VPA analysis
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
    log_file = f"/tmp/vpa_us_crypto_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        handlers=[console_handler, file_handler]
    )
    
    logging.info(f"US & Crypto VPA logging initialized - Log file: {log_file}")
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
    Note: US indices and crypto typically don't have dividends, but keeping for compatibility
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


def check_dividends_folder(week_mode=False):
    """
    Step 1: Check dividend adjustment folder
    Returns dividend_info dict if dividends need processing, None if no dividends
    Note: US indices and crypto typically don't have dividends
    """
    dividend_folder = "market_data_us_crypto_check_dividends_week" if week_mode else "market_data_us_crypto_check_dividends"
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
    market_folder = "market_data_us_crypto_week" if week_mode else "market_data_us_crypto"
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
    vpa_folder = "vpa_data_us_crypto_week" if week_mode else "vpa_data_us_crypto"
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
    vpa_folder = "vpa_data_us_crypto_week" if week_mode else "vpa_data_us_crypto"
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
    Special case: If VPA file doesn't exist, only return last 10 dates.
    Returns list of dates that need analysis, empty list if none needed
    """
    logging.debug(f"Checking which dates need VPA analysis for {ticker}...")
    
    # Get all available dates from CSV
    market_folder = "market_data_us_crypto_week" if week_mode else "market_data_us_crypto"
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
        vpa_folder = "vpa_data_us_crypto_week" if week_mode else "vpa_data_us_crypto"
        vpa_file = Path(f"{vpa_folder}/{ticker}.md")
        
        if not vpa_file.exists():
            # VPA file doesn't exist - return only last 10 dates
            last_10_dates = all_dates[-10:] if len(all_dates) >= 10 else all_dates
            logging.info(f"📊 {ticker}: VPA file doesn't exist, processing last {len(last_10_dates)} dates: {last_10_dates}")
            return last_10_dates
        
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
    
    market_folder = "market_data_us_crypto_week" if week_mode else "market_data_us_crypto"
    vpa_folder = "vpa_data_us_crypto_week" if week_mode else "vpa_data_us_crypto"
    
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
        
        # Get existing VPA analysis and extract last 10 VPA entries
        vpa_file = Path(f"{vpa_folder}/{ticker}.md")
        previous_vpa = ""
        last_10_vpa_entries = []
        if vpa_file.exists():
            with open(vpa_file, 'r', encoding='utf-8') as f:
                previous_vpa = f.read()
            logging.debug(f"Loaded existing VPA analysis for {ticker}: {len(previous_vpa)} characters")
            
            # Extract last 10 VPA entries
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
            
            # Get the last 10 entries (or all if less than 10)
            last_10_vpa_entries = entries_with_headers[-10:] if entries_with_headers else []
        else:
            logging.debug(f"No existing VPA file for {ticker}")
        
        # Determine asset type for context
        asset_type = "US_INDEX"  # Default
        try:
            us_tickers = pd.read_csv('TICKERS_US.csv')['ticker'].tolist()
            crypto_tickers = pd.read_csv('TICKERS_CRYPTO.csv')['ticker'].tolist()
            
            if ticker in us_tickers:
                asset_type = "US_INDEX"
            elif ticker in crypto_tickers:
                asset_type = "CRYPTO"
        except:
            # Fallback logic
            if ticker in ['BTC', 'ETH', 'USDT', 'USDC', 'BNB', 'BUSD', 'XRP', 'ADA', 'SOL', 'DOGE']:
                asset_type = "CRYPTO"
        
        context = {
            "ticker": ticker,
            "asset_type": asset_type,
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
            "last_10_vpa_entries": last_10_vpa_entries,
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
    vpa_folder = "vpa_data_us_crypto_week" if week_mode else "vpa_data_us_crypto"
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
        vpa_folder = "vpa_data_us_crypto_week" if week_mode else "vpa_data_us_crypto"
        
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


def parse_and_append_vpa_analysis(ticker, ai_output, week_mode=False):
    """
    Parse AI agent output and append VPA analysis to appropriate file
    Returns True if successful, False otherwise
    """
    vpa_folder = "vpa_data_us_crypto_week" if week_mode else "vpa_data_us_crypto"
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
    Enhanced for US indices and cryptocurrencies
    Returns True if successful, False otherwise
    """
    logging.debug(f"Preparing {agent.upper()} analysis for {ticker}...")
    
    try:
        # Prepare the AI agent prompt
        timeframe = "weekly" if week_mode else "daily"
        asset_type = context.get('asset_type', 'UNKNOWN')
        
        # Include all context directly in the prompt
        # Format last 10 OHLCV data points
        last_10_ohlcv_str = "\n".join([
            f"- {item['date']}: O={item['open']}, H={item['high']}, L={item['low']}, C={item['close']}, V={item['volume']}"
            for item in context['last_10_ohlcv']
        ])
        
        # Format last 10 VPA entries
        last_10_vpa_str = "\n---\n".join(context['last_10_vpa_entries']) if context['last_10_vpa_entries'] else 'No previous VPA entries found.'
        
        # Asset-specific context
        asset_description = ""
        currency = "USD"
        if asset_type == "US_INDEX":
            asset_description = f"{ticker} is a US stock market index."
        elif asset_type == "CRYPTO":
            asset_description = f"{ticker} is a cryptocurrency."
        
        prompt = f"""
Analyze {asset_type.lower()} ticker {ticker} for {timeframe} VPA using the provided context data.

=== MARKET DATA CONTEXT ===
Ticker: {context['ticker']}
Asset Type: {asset_type} ({asset_description})
Latest Date: {context['latest_date']}
Timeframe: {context['timeframe']}
Total Data Rows: {context['data_rows']}
Date Range: {context['date_range']}

Latest OHLCV:
- Open: {context['latest_ohlcv']['open']}
- High: {context['latest_ohlcv']['high']}
- Low: {context['latest_ohlcv']['low']}
- Close: {context['latest_ohlcv']['close']}
- Volume: {context['latest_ohlcv']['volume']}

Previous OHLCV:
- Open: {context['previous_ohlcv']['open']}
- High: {context['previous_ohlcv']['high']}
- Low: {context['previous_ohlcv']['low']}
- Close: {context['previous_ohlcv']['close']}
- Volume: {context['previous_ohlcv']['volume']}

Last 10 OHLCV Data Points:
{last_10_ohlcv_str}

Last 10 VPA Entries:
{last_10_vpa_str}

=== ANALYSIS TASK ===
1. Analyze the price/volume relationship using Wyckoff methodology adapted for {asset_type.lower()}
2. Compare current data with previous periods
3. Generate Vietnamese VPA analysis following the standard format
4. Consider {asset_type}-specific factors (market hours, volatility patterns, etc.)
5. OUTPUT the analysis entry in the exact format below (do NOT edit files)

Required Output Format:
**Ngày {context['latest_date']}:**
[Your detailed Vietnamese analysis of price/volume action, trends, support/resistance levels, and market context for this {asset_type.lower()}]

**Phân tích VPA/Wyckoff:** [Your Wyckoff signal assessment]

Requirements:
- Use Vietnamese financial terminology only  
- Use DOT (.) as decimal separator, never comma (,)
- Reference prices in {currency}
- Follow the exact format above with **Ngày** and **Phân tích VPA/Wyckoff:** sections
- Build on previous VPA entries if they exist
- Compare current price/volume action to previous periods
- Apply proper Wyckoff VPA methodology adapted for {asset_type.lower()} markets
- Consider global market context for {asset_type.lower()} assets
- Output ONLY the formatted analysis entry - no additional text

IMPORTANT: Output only the VPA analysis entry in the specified format. Do not use any file editing tools.
"""
        
        # Prepare command based on agent
        if agent == 'gemini':
            cmd = ['gemini', '-p', prompt]
        elif agent == 'gemini-2.5-flash':
            cmd = ['gemini', '-m', 'gemini-2.5-flash', '-p', prompt]
        else:
            cmd = ['claude', '-p', prompt]

        logging.info(f"🤖 Calling {agent.upper()} for {ticker} ({asset_type}) analysis...")
        
        # Show verbose output if requested
        if verbose:
            logging.info(f"📝 PROMPT FOR {ticker}:")
            logging.info("-" * 80)
            logging.info(prompt)
            logging.info("-" * 80)
            logging.info(f"📊 CONTEXT SUMMARY:")
            logging.info(f"   - Asset type: {asset_type}")
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
    Process all US & Crypto tickers for VPA analysis with sequential date processing per ticker
    Each ticker processes its dates sequentially, but tickers are processed in parallel
    """
    logging.info(f"📊 Starting sequential-by-date US & Crypto ticker processing using {agent.upper()} with {workers} workers...")
    
    # Read tickers from both CSV files
    tickers = []
    try:
        logging.debug("Reading TICKERS_US.csv...")
        with open('TICKERS_US.csv', 'r') as f:
            reader = csv.DictReader(f)
            us_tickers = [row['ticker'] for row in reader]
        logging.info(f"Loaded {len(us_tickers)} US tickers from TICKERS_US.csv")
        tickers.extend(us_tickers)
    except Exception as e:
        logging.warning(f"⚠️  Error reading TICKERS_US.csv: {e}")
    
    try:
        logging.debug("Reading TICKERS_CRYPTO.csv...")
        with open('TICKERS_CRYPTO.csv', 'r') as f:
            reader = csv.DictReader(f)
            crypto_tickers = [row['ticker'] for row in reader]
        logging.info(f"Loaded {len(crypto_tickers)} crypto tickers from TICKERS_CRYPTO.csv")
        tickers.extend(crypto_tickers)
    except Exception as e:
        logging.warning(f"⚠️  Error reading TICKERS_CRYPTO.csv: {e}")
    
    if not tickers:
        logging.error("❌ No tickers found in US or Crypto CSV files")
        return False
    
    logging.info(f"📊 Processing {len(tickers)} total tickers for {'weekly' if week_mode else 'daily'} VPA analysis using {agent.upper()}")
    
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
    logging.info(f"\n📊 Sequential-by-Date US & Crypto VPA Analysis Summary:")
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
    parser = argparse.ArgumentParser(description='Process US & Crypto VPA analysis using AI agent coordination')
    parser.add_argument('--week', action='store_true', 
                       help='Process weekly VPA analysis instead of daily')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug logging')
    parser.add_argument('--agent', choices=['claude', 'gemini', 'gemini-2.5-flash'], default='claude',
                       help='AI agent to use for analysis (default: claude)')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed prompts and context sent to AI agents')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers for VPA processing (default: 4)')
    
    args = parser.parse_args()
    
    # Setup logging first
    log_file = setup_logging(debug=args.debug)
    
    logging.info("🚀 Starting US & Crypto VPA Processing Coordinator")
    logging.info(f"📅 Mode: {'Weekly' if args.week else 'Daily'}")
    logging.info(f"🤖 AI Agent: {args.agent.upper()}")
    logging.info(f"👥 Parallel Workers: {args.workers}")
    logging.info(f"📁 Data folders: {'market_data_us_crypto_week, vpa_data_us_crypto_week' if args.week else 'market_data_us_crypto, vpa_data_us_crypto'}")
    logging.info(f"📄 Log file: {log_file}")
    
    start_time = datetime.now()
    logging.info(f"⏰ Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Step 1: Check and process dividends (unlikely for US indices and crypto)
        logging.info("\n📋 Step 1: Checking dividend adjustments...")
        dividend_info = check_dividends_folder(args.week)
        
        if dividend_info is None:
            # No dividends found, continue to VPA analysis
            logging.info("✓ No dividends found (expected for US indices and crypto)")
            pass
        elif len(dividend_info) == 0:
            # Error in dividend detection
            logging.error("❌ Error in dividend detection - check dividend files manually")
            return 1
        else:
            # Process dividends with AI agent (unlikely scenario)
            logging.info(f"🔄 Processing {len(dividend_info)} dividend adjustments...")
            logging.warning("⚠️  Dividends found for US indices/crypto - unusual, please verify")
        
        # Step 2: Process tickers
        logging.info("\n📋 Step 2: Processing US & Crypto ticker VPA analysis...")
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
            merge_cmd = ['uv', 'run', 'merge_vpa_us_crypto.py']
            if args.week:
                merge_cmd.append('--week')
            
            logging.debug(f"Running merge command: {' '.join(merge_cmd)}")
            logging.info("Note: If merge_vpa_us_crypto.py doesn't exist, you may need to create it or merge manually")
            
            # Try to run merge command, but don't fail if it doesn't exist
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
        except FileNotFoundError:
            logging.warning("⚠️  merge_vpa_us_crypto.py not found")
            logging.warning("Please create this utility or merge individual VPA files manually")
        except Exception as e:
            logging.error(f"⚠️  Could not run merge_vpa_us_crypto.py: {e}")
            logging.error("Please merge individual VPA files manually")
        
        # Final summary
        total_duration = datetime.now() - start_time
        logging.info(f"\n🎉 US & Crypto VPA Processing Complete!")
        logging.info(f"⏱️  Total time: {total_duration}")
        logging.info(f"📁 Check {'VPA_us_crypto_week.md' if args.week else 'VPA_us_crypto.md'} for final results")
        logging.info(f"📄 Full log saved to: {log_file}")
        
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