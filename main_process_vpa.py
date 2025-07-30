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


def needs_vpa_analysis(ticker, week_mode=False):
    """
    Determine if a ticker needs new VPA analysis
    Returns True if analysis is needed, False otherwise
    """
    logging.debug(f"Checking if {ticker} needs VPA analysis...")
    
    latest_data_date, csv_file = get_latest_csv_date(ticker, week_mode)
    if not latest_data_date:
        logging.warning(f"⚠️  No market data found for {ticker}")
        return False
    
    # Check if this specific date has already been analyzed
    if is_date_already_analyzed(ticker, latest_data_date, week_mode):
        logging.info(f"✓ {ticker}: Already analyzed (latest data: {latest_data_date})")
        return False
    
    last_vpa_date = get_vpa_last_date(ticker, week_mode)
    
    if not last_vpa_date:
        logging.info(f"📊 {ticker}: New VPA file needed (latest data: {latest_data_date})")
        return True
    
    logging.info(f"📊 {ticker}: Update needed (data: {latest_data_date}, last VPA: {last_vpa_date})")
    return True


def get_ticker_context(ticker, week_mode=False):
    """
    Gather context for a ticker using reliable Python operations
    Returns context dictionary or None if data unavailable
    """
    logging.debug(f"Gathering context for {ticker}...")
    
    market_folder = "market_data_week" if week_mode else "market_data"
    vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
    
    # Get latest market data
    latest_date, csv_file = get_latest_csv_date(ticker, week_mode)
    if not latest_date:
        logging.error(f"Cannot gather context for {ticker}: no market data available")
        return None
    
    try:
        df = pd.read_csv(csv_file)
        latest = df.iloc[-1]
        previous = df.iloc[-2] if len(df) > 1 else df.iloc[-1]
        
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
        
        context = {
            "ticker": ticker,
            "latest_date": latest[date_column],
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
        # Format last 10 OHLCV data points
        last_10_ohlcv_str = "\n".join([
            f"- {item['date']}: O={item['open']}, H={item['high']}, L={item['low']}, C={item['close']}, V={item['volume']}"
            for item in context['last_10_ohlcv']
        ])
        
        # Format last 10 VPA entries
        last_10_vpa_str = "\n---\n".join(context['last_10_vpa_entries']) if context['last_10_vpa_entries'] else 'No previous VPA entries found.'
        
        prompt = f"""
Analyze ticker {ticker} for {timeframe} VPA using the provided context data.

=== MARKET DATA CONTEXT ===
Ticker: {context['ticker']}
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
1. Analyze the price/volume relationship using Wyckoff methodology
2. Compare current data with previous periods
3. Generate Vietnamese VPA analysis following the standard format
4. OUTPUT the analysis entry in the exact format below (do NOT edit files)

Required Output Format:
**Ngày {context['latest_date']}:**
[Your detailed Vietnamese analysis of price/volume action, trends, support/resistance levels, and market context]

**Phân tích VPA/Wyckoff:** [Your Wyckoff signal assessment]

Requirements:
- Use Vietnamese financial terminology only  
- Use DOT (.) as decimal separator, never comma (,)
- Follow the exact format above with **Ngày** and **Phân tích VPA/Wyckoff:** sections
- Build on previous VPA entries if they exist
- Compare current price/volume action to previous periods
- Apply proper Wyckoff VPA methodology
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
        
        # Call the AI agent
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
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


def call_ai_agent_for_dividend_processing(ticker, dividend_info, week_mode=False, agent='claude', verbose=False):
    """
    Call AI agent to process dividend adjustments for a single ticker
    Returns True if successful, False otherwise
    """
    logging.debug(f"Preparing {agent.upper()} dividend processing for {ticker}...")
    
    # Get VPA file paths
    vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
    vpa_file = Path(f"{vpa_folder}/{ticker}.md")
    main_vpa_file = Path("VPA_week.md" if week_mode else "VPA.md")
    
    # Read existing VPA content
    individual_vpa_content = ""
    main_vpa_content = ""
    
    if vpa_file.exists():
        with open(vpa_file, 'r', encoding='utf-8') as f:
            individual_vpa_content = f.read()
    
    if main_vpa_file.exists():
        with open(main_vpa_file, 'r', encoding='utf-8') as f:
            main_vpa_content = f.read()
    
    try:
        # Prepare dividend processing prompt
        timeframe = "weekly" if week_mode else "daily"
        prompt = f"""
Process dividend adjustments for ticker {ticker} using the provided context data.

=== DIVIDEND ADJUSTMENT CONTEXT ===
Ticker: {ticker}
Dividend Ratio: {dividend_info['ratio']}
Processing Mode: {timeframe}

=== INDIVIDUAL VPA FILE CONTENT ===
File: {vpa_file}
Content:
{individual_vpa_content if individual_vpa_content else 'No individual VPA file found.'}

=== MAIN VPA FILE CONTENT ===
File: {main_vpa_file}
Content:
{main_vpa_content if main_vpa_content else 'No main VPA file found.'}

=== DIVIDEND PROCESSING TASK ===
Update all Vietnamese price references using the dividend ratio.

Dividend Ratio Logic:
- When ratio is {dividend_info['ratio']}, divide all price values by {dividend_info['ratio']}
- Example: "từ 64.4 lên 64.9" → "từ {64.4/dividend_info['ratio']:.1f} lên {64.9/dividend_info['ratio']:.1f}"

Vietnamese Price Patterns to Update:
- "từ X lên Y" (from X to Y)
- "từ X xuống Y" (from X down to Y)  
- "tăng từ X lên Y" (increased from X to Y)
- "giảm từ X xuống Y" (decreased from X to Y)
- "đóng cửa ở mức X" (closed at level X)
- "mở cửa ở X" (opened at X)
- "giá X" (price X)
- "mức X" (level X)

OUTPUT REQUIREMENTS:
Please output the updated content in the following format:

=== UPDATED INDIVIDUAL VPA ===
[Updated content for individual VPA file, or "NO_CHANGES" if no updates needed]

=== UPDATED MAIN VPA ===
[Updated content for main VPA file, or "NO_CHANGES" if no updates needed]

Requirements:
- Update price references while preserving Vietnamese context
- Round prices to appropriate decimal places (1-2 decimal places)
- Maintain natural Vietnamese sentence structure
- Only update numeric price values, not percentages or ratios
- Output ONLY the updated file contents - no additional text
- Use "NO_CHANGES" if a file doesn't need updates

IMPORTANT: Output only the updated file contents in the specified format. Do not use any file editing tools.
"""

        logging.info(f"🔄 Calling {agent.upper()} for {ticker} dividend processing...")
        
        # Show verbose output if requested
        if verbose:
            logging.info(f"📝 DIVIDEND PROMPT FOR {ticker}:")
            logging.info("-" * 80)
            logging.info(prompt)
            logging.info("-" * 80)
            logging.info(f"📊 DIVIDEND CONTEXT:")
            logging.info(f"   - Ticker: {ticker}")
            logging.info(f"   - Dividend ratio: {dividend_info['ratio']}")
            logging.info(f"   - Individual VPA exists: {vpa_file.exists()}")
            logging.info(f"   - Main VPA exists: {main_vpa_file.exists()}")
        
        # Prepare command based on agent
        if agent == 'gemini':
            cmd = ['gemini', '-p', prompt]
        elif agent == 'gemini-2.5-flash':
            cmd = ['gemini', '-m', 'gemini-2.5-flash', '-p', prompt]
        else:
            cmd = ['claude', '-p', prompt]
        
        # Call the AI agent
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            if result.stdout.strip():
                logging.info(f"🎯 {agent.upper()} generated dividend updates for {ticker}: {len(result.stdout)} chars")
                
                # Parse and apply the updates
                if parse_and_apply_dividend_updates(ticker, result.stdout, vpa_file, main_vpa_file):
                    logging.info(f"✅ {ticker}: {agent.upper()} dividend processing completed successfully")
                    return True
                else:
                    logging.error(f"❌ {ticker}: Failed to parse/apply dividend updates")
                    return False
            else:
                logging.error(f"❌ {ticker}: {agent.upper()} returned empty output")
                return False
        else:
            logging.error(f"❌ {ticker}: {agent.upper()} dividend processing failed (return code: {result.returncode})")
            if result.stderr:
                logging.error(f"{agent.upper()} dividend stderr for {ticker}: {result.stderr}")
            if result.stdout:
                logging.debug(f"{agent.upper()} dividend stdout for {ticker}: {result.stdout}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.error(f"❌ {ticker}: {agent.upper()} dividend processing timed out after 300 seconds")
        return False
    except Exception as e:
        logging.error(f"❌ {ticker}: Error calling {agent.upper()} for dividend processing - {e}")
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
    
    # Clean up files (even if some failed to prevent infinite loops)
    cleanup_dividend_files(dividend_info)
    
    return len(failed) == 0


def process_tickers(week_mode=False, agent='claude', verbose=False):
    """
    Process all tickers for VPA analysis using specified AI agent
    """
    logging.info(f"📊 Starting ticker processing phase using {agent.upper()}...")
    
    # Read tickers from CSV
    tickers = []
    try:
        logging.debug("Reading TICKERS.csv...")
        with open('TICKERS.csv', 'r') as f:
            reader = csv.DictReader(f)
            tickers = [row['ticker'] for row in reader]
        logging.info(f"Loaded {len(tickers)} tickers from TICKERS.csv")
    except Exception as e:
        logging.error(f"❌ Error reading TICKERS.csv: {e}")
        return False
    
    logging.info(f"📊 Processing {len(tickers)} tickers for {'weekly' if week_mode else 'daily'} VPA analysis using {agent.upper()}")
    
    # Filter tickers that need analysis
    logging.info("🔍 Checking which tickers need analysis...")
    tickers_to_process = []
    for ticker in tickers:
        if needs_vpa_analysis(ticker, week_mode):
            tickers_to_process.append(ticker)
    
    if not tickers_to_process:
        logging.info("✓ All tickers are up to date - no analysis needed")
        return True
    
    logging.info(f"📊 {len(tickers_to_process)} out of {len(tickers)} tickers need analysis:")
    for ticker in tickers_to_process:
        logging.info(f"   - {ticker}")
    
    # Process each ticker with timing
    successful = 0
    failed = []
    ticker_times = []
    
    logging.info(f"🚀 Starting analysis of {len(tickers_to_process)} tickers...")
    process_start_time = datetime.now()
    
    for i, ticker in enumerate(tickers_to_process, 1):
        ticker_start = datetime.now()
        logging.info(f"\n[{i}/{len(tickers_to_process)}] 📈 Processing {ticker}...")
        
        # Get context
        logging.debug(f"Gathering context for {ticker}...")
        context = get_ticker_context(ticker, week_mode)
        if not context:
            logging.error(f"❌ {ticker}: Could not gather context")
            failed.append(ticker)
            continue
        
        # Call AI agent for analysis
        logging.debug(f"Starting {agent.upper()} analysis for {ticker}...")
        if call_ai_agent_for_vpa_analysis(ticker, context, week_mode, agent, verbose):
            successful += 1
            ticker_duration = datetime.now() - ticker_start
            ticker_times.append(ticker_duration.total_seconds())
            
            # Calculate and display timing information
            avg_time = sum(ticker_times) / len(ticker_times)
            remaining_tickers = len(tickers_to_process) - i
            estimated_remaining = remaining_tickers * avg_time
            
            logging.info(f"✅ {ticker}: Analysis completed in {ticker_duration.total_seconds():.1f}s")
            if remaining_tickers > 0:
                logging.info(f"⏱️  Average: {avg_time:.1f}s/ticker, Est. remaining: {estimated_remaining/60:.1f}min ({remaining_tickers} left)")
        else:
            failed.append(ticker)
            ticker_duration = datetime.now() - ticker_start
            logging.error(f"❌ {ticker}: Analysis failed after {ticker_duration.total_seconds():.1f}s")
    
    total_processing_time = datetime.now() - process_start_time
    
    # Summary
    logging.info(f"\n📊 VPA Analysis Summary:")
    logging.info(f"   ✓ Successful: {successful}")
    logging.info(f"   ❌ Failed: {len(failed)}")
    logging.info(f"   ⏱️  Total processing time: {total_processing_time}")
    if ticker_times:
        logging.info(f"   📊 Average time per ticker: {sum(ticker_times)/len(ticker_times):.1f}s")
    logging.info(f"   📈 Success rate: {successful/(successful+len(failed))*100:.1f}%")
    
    if failed:
        logging.warning(f"   Failed tickers: {', '.join(failed)}")
        for ticker in failed:
            logging.debug(f"   - {ticker}: Check logs for details")
    
    return len(failed) == 0


def main():
    parser = argparse.ArgumentParser(description='Process VPA analysis using AI agent coordination')
    parser.add_argument('--week', action='store_true', 
                       help='Process weekly VPA analysis instead of daily')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug logging')
    parser.add_argument('--agent', choices=['claude', 'gemini', 'gemini-2.5-flash'], default='claude',
                       help='AI agent to use for analysis (default: claude)')
    parser.add_argument('--verbose', action='store_true',
                       help='Show detailed prompts and context sent to AI agents')
    
    args = parser.parse_args()
    
    # Setup logging first
    log_file = setup_logging(debug=args.debug)
    
    logging.info("🚀 Starting VPA Processing Coordinator")
    logging.info(f"📅 Mode: {'Weekly' if args.week else 'Daily'}")
    logging.info(f"🤖 AI Agent: {args.agent.upper()}")
    logging.info(f"📁 Data folders: {'market_data_week, vpa_data_week' if args.week else 'market_data, vpa_data'}")
    logging.info(f"📄 Log file: {log_file}")
    
    start_time = datetime.now()
    logging.info(f"⏰ Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Step 1: Check and process dividends
        logging.info("\n📋 Step 1: Checking dividend adjustments...")
        dividend_info = check_dividends_folder(args.week)
        
        if dividend_info is None:
            # No dividends found, continue to VPA analysis
            pass
        elif len(dividend_info) == 0:
            # Error in dividend detection
            logging.error("❌ Error in dividend detection - check dividend files manually")
            return 1
        else:
            # Process dividends with AI agent
            logging.info(f"🔄 Processing {len(dividend_info)} dividend adjustments...")
            dividend_start = datetime.now()
            
            if not process_dividends(dividend_info, args.week, args.agent, args.verbose):
                logging.error("❌ Some dividend adjustments failed")
                logging.warning("⚠️  Continuing with VPA analysis using existing data")
            else:
                logging.info("✅ All dividend adjustments completed successfully")
            
            dividend_duration = datetime.now() - dividend_start
            logging.info(f"⏱️  Dividend processing took: {dividend_duration}")
        
        # Step 2: Process tickers
        logging.info("\n📋 Step 2: Processing ticker VPA analysis...")
        process_start = datetime.now()
        success = process_tickers(args.week, args.agent, args.verbose)
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