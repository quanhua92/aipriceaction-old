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
        
        # Handle both "Date" and "time" column names for logging
        date_column = "Date" if "Date" in df.columns else "time"
        open_column = "Open" if "Open" in df.columns else "open"
        high_column = "High" if "High" in df.columns else "high"
        low_column = "Low" if "Low" in df.columns else "low"
        close_column = "Close" if "Close" in df.columns else "close"
        volume_column = "Volume" if "Volume" in df.columns else "volume"
        
        logging.debug(f"Market data for {ticker}: {len(df)} rows, range {df.iloc[0][date_column]} to {df.iloc[-1][date_column]}")
        logging.debug(f"Latest price data: Open={latest[open_column]}, Close={latest[close_column]}, Volume={latest[volume_column]}")
        
        # Get existing VPA analysis
        vpa_file = Path(f"{vpa_folder}/{ticker}.md")
        previous_vpa = ""
        if vpa_file.exists():
            with open(vpa_file, 'r', encoding='utf-8') as f:
                previous_vpa = f.read()
            logging.debug(f"Loaded existing VPA analysis for {ticker}: {len(previous_vpa)} characters")
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


def call_ai_agent_for_vpa_analysis(ticker, context, week_mode=False, agent='claude'):
    """
    Call AI agent (claude or gemini) to process VPA analysis for a single ticker
    Returns True if successful, False otherwise
    """
    logging.debug(f"Preparing {agent.upper()} analysis for {ticker}...")
    
    # Create a temporary file with the context
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        json.dump(context, tmp, indent=2, ensure_ascii=False, default=str)
        context_file = tmp.name
    
    logging.debug(f"Context file created for {ticker}: {context_file}")
    
    try:
        # Prepare the AI agent prompt
        timeframe = "weekly" if week_mode else "daily"
        
        if agent == 'gemini':
            # Gemini prompt format
            prompt = f"""
Analyze ticker {ticker} for {timeframe} VPA using the context in {context_file}.

Context includes:
- Latest market data: {context['latest_date']}
- OHLCV data for latest and previous periods
- Existing VPA analysis history
- CSV file path and data range

Tasks:
1. Read the context file to understand the current market data
2. Analyze the price/volume relationship using Wyckoff methodology
3. Generate Vietnamese VPA analysis following the format in tasks/{'WEEKLY' if week_mode else 'DAILY'}_VPA.md
4. Append new analysis to the existing VPA file: {context['vpa_file']}

Requirements:
- Use Vietnamese financial terminology only
- Use DOT (.) as decimal separator, never comma (,)
- Follow the exact format: **Ngày YYYY-MM-DD:** [analysis] **Phân tích VPA/Wyckoff:** [signal]
- Only append if the date doesn't already exist in the file
- Apply proper Wyckoff VPA signals manually

The analysis should be contextual, building on previous VPA entries and comparing current price/volume action to previous periods.
"""
            # Call gemini -p
            cmd = ['gemini', '-p', prompt]
        else:
            # Claude prompt format (default)
            prompt = f"""
Analyze ticker {ticker} for {timeframe} VPA using the context in {context_file}.

Context includes:
- Latest market data: {context['latest_date']}
- OHLCV data for latest and previous periods
- Existing VPA analysis history
- CSV file path and data range

Tasks:
1. Read the context file to understand the current market data
2. Analyze the price/volume relationship using Wyckoff methodology
3. Generate Vietnamese VPA analysis following the format in tasks/{'WEEKLY' if week_mode else 'DAILY'}_VPA.md
4. Append new analysis to the existing VPA file: {context['vpa_file']}

Requirements:
- Use Vietnamese financial terminology only
- Use DOT (.) as decimal separator, never comma (,)
- Follow the exact format: **Ngày YYYY-MM-DD:** [analysis] **Phân tích VPA/Wyckoff:** [signal]
- Only append if the date doesn't already exist in the file
- Apply proper Wyckoff VPA signals manually

The analysis should be contextual, building on previous VPA entries and comparing current price/volume action to previous periods.
"""
            # Call claude -p
            cmd = ['claude', '-p', prompt]

        logging.info(f"🤖 Calling {agent.upper()} for {ticker} analysis...")
        
        # Call the AI agent
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logging.info(f"✓ {ticker}: {agent.upper()} analysis completed successfully")
            if result.stdout.strip():
                logging.debug(f"{agent.upper()} output for {ticker}: {result.stdout[:200]}...")
            return True
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
    finally:
        # Clean up temporary file
        try:
            os.unlink(context_file)
            logging.debug(f"Cleaned up context file for {ticker}: {context_file}")
        except Exception as e:
            logging.warning(f"Could not clean up context file {context_file}: {e}")


def call_ai_agent_for_dividend_processing(ticker, dividend_info, week_mode=False, agent='claude'):
    """
    Call AI agent to process dividend adjustments for a single ticker
    Returns True if successful, False otherwise
    """
    logging.debug(f"Preparing {agent.upper()} dividend processing for {ticker}...")
    
    # Create context for dividend processing
    vpa_folder = "vpa_data_week" if week_mode else "vpa_data"
    vpa_file = Path(f"{vpa_folder}/{ticker}.md")
    
    # Also check main VPA files
    main_vpa_file = Path("VPA_week.md" if week_mode else "VPA.md")
    
    dividend_context = {
        "ticker": ticker,
        "dividend_ratio": dividend_info['ratio'],
        "csv_file": str(dividend_info['csv_file']),
        "info_file": str(dividend_info['info_file']),
        "vpa_file": str(vpa_file),
        "main_vpa_file": str(main_vpa_file),
        "timeframe": "weekly" if week_mode else "daily"
    }
    
    # Create temporary context file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        json.dump(dividend_context, tmp, indent=2, ensure_ascii=False, default=str)
        context_file = tmp.name
    
    logging.debug(f"Dividend context file created for {ticker}: {context_file}")
    
    try:
        # Prepare dividend processing prompt
        timeframe = "weekly" if week_mode else "daily"
        prompt = f"""
Process dividend adjustments for ticker {ticker} using the context in {context_file}.

Context includes:
- Ticker: {ticker}
- Dividend ratio: {dividend_info['ratio']}
- VPA files to update: {vpa_file} and {main_vpa_file}
- Processing mode: {timeframe}

Tasks:
1. Read the dividend context from {context_file}
2. Load VPA files for {ticker} (both individual and main VPA files)
3. Update all Vietnamese price references using the dividend ratio
4. Preserve Vietnamese grammar and sentence structure
5. Save updated VPA files using Write tool

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

Requirements:
- Use Read tool to get existing VPA content
- Update price references while preserving Vietnamese context
- Use Write tool to save updated content
- Round prices to appropriate decimal places
- Maintain natural Vietnamese sentence structure
- DO NOT delete dividend files - that will be handled separately

Process both:
- Individual file: {vpa_file}
- Main VPA file: {main_vpa_file} (if {ticker} section exists)
"""

        logging.info(f"🔄 Calling {agent.upper()} for {ticker} dividend processing...")
        
        # Prepare command based on agent
        if agent == 'gemini':
            cmd = ['gemini', '-p', prompt]
        else:
            cmd = ['claude', '-p', prompt]
        
        # Call the AI agent
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logging.info(f"✅ {ticker}: {agent.upper()} dividend processing completed successfully")
            if result.stdout.strip():
                logging.debug(f"{agent.upper()} dividend output for {ticker}: {result.stdout[:200]}...")
            return True
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
    finally:
        # Clean up temporary file
        try:
            os.unlink(context_file)
            logging.debug(f"Cleaned up dividend context file for {ticker}: {context_file}")
        except Exception as e:
            logging.warning(f"Could not clean up dividend context file {context_file}: {e}")


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


def process_dividends(dividend_info, week_mode=False, agent='claude'):
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
        if call_ai_agent_for_dividend_processing(ticker, info, week_mode, agent):
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


def process_tickers(week_mode=False, agent='claude'):
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
    
    # Process each ticker
    successful = 0
    failed = []
    
    logging.info(f"🚀 Starting analysis of {len(tickers_to_process)} tickers...")
    
    for i, ticker in enumerate(tickers_to_process, 1):
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
        if call_ai_agent_for_vpa_analysis(ticker, context, week_mode, agent):
            successful += 1
            logging.info(f"✅ {ticker}: Analysis completed successfully")
        else:
            failed.append(ticker)
            logging.error(f"❌ {ticker}: Analysis failed")
    
    # Summary
    logging.info(f"\n📊 VPA Analysis Summary:")
    logging.info(f"   ✓ Successful: {successful}")
    logging.info(f"   ❌ Failed: {len(failed)}")
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
    parser.add_argument('--agent', choices=['claude', 'gemini'], default='claude',
                       help='AI agent to use for analysis (default: claude)')
    
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
            
            if not process_dividends(dividend_info, args.week, args.agent):
                logging.error("❌ Some dividend adjustments failed")
                logging.warning("⚠️  Continuing with VPA analysis using existing data")
            else:
                logging.info("✅ All dividend adjustments completed successfully")
            
            dividend_duration = datetime.now() - dividend_start
            logging.info(f"⏱️  Dividend processing took: {dividend_duration}")
        
        # Step 2: Process tickers
        logging.info("\n📋 Step 2: Processing ticker VPA analysis...")
        process_start = datetime.now()
        success = process_tickers(args.week, args.agent)
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