import os
import time
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
import re
import json
import argparse
from collections import defaultdict
from datetime import datetime, timedelta
from vnstock import Vnstock

# --- Configuration ---
# The list of tickers is now read from TICKERS.csv
try:
    TICKERS_TO_DOWNLOAD = pd.read_csv('TICKERS.csv')['ticker'].tolist()
    print(f"Loaded {len(TICKERS_TO_DOWNLOAD)} tickers from TICKERS.csv")
except FileNotFoundError:
    print("TICKERS.csv not found. Using default list.")
    TICKERS_TO_DOWNLOAD = ["VNINDEX", "TCB", "FPT"]


# Define the names for your data and report directories.
# These can be modified by the --week flag in main().
DATA_DIR = "market_data"
REPORTS_DIR = "reports"
MASTER_REPORT_FILENAME = "REPORT.md"
VPA_ANALYSIS_FILENAME = "VPA.md"

# Instantiate the vnstock object once
stock_reader = Vnstock().stock(symbol="SSI", source="TCBS")

# --- Core Functions ---

def setup_directories():
    """
    Creates the main data and reports directories if they don't already exist.
    Uses the global DATA_DIR and REPORTS_DIR variables.
    """
    print("Setting up base directories...")
    for directory in [DATA_DIR, REPORTS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  - Created directory: {directory}")

def download_stock_data(ticker, start_date, end_date, interval='1D'):
    """
    Checks for local data first. If not found, downloads historical stock data.
    """
    print(f"\n-> Processing ticker: {ticker} (Interval: {interval})")
    
    # --- SMART CACHING ---
    file_name = f"{ticker}_{start_date}_to_{end_date}.csv"
    file_path = os.path.join(DATA_DIR, file_name)

    if os.path.exists(file_path):
        print(f"   - Found local data. Loading from: {file_path}")
        df = pd.read_csv(file_path)
        if interval == '1D':
             df['time'] = pd.to_datetime(df['time'])
        return df
    # --- END SMART CACHING ---

    print(f"   - No local data found. Downloading from {start_date} to {end_date}...")
    try:
        df = stock_reader.quote.history(
            symbol=ticker,
            start=start_date,
            end=end_date,
            interval=interval
        )
        time.sleep(2)

        if not df.empty:
            print(f"   - Success! Downloaded {len(df)} raw records for {ticker}.")
            df['time'] = pd.to_datetime(df['time'])

            mask = (df['time'] >= pd.to_datetime(start_date)) & (df['time'] <= pd.to_datetime(end_date))
            df_filtered = df.loc[mask].copy()

            df_filtered.insert(0, 'ticker', ticker)

            if not df_filtered.empty:
                 df_filtered = df_filtered.sort_values(by='time')
                 return df_filtered
            else:
                print("   - No data available for the specified date range after filtering.")
                return None
        else:
            print(f"   - ERROR: Could not retrieve data for {ticker}. Skipping.")
            return None
            
    except Exception as e:
        print(f"   - ERROR: An exception occurred for {ticker}: {e}")
        return None

def reformat_time_column_for_weekly_data(df):
    """
    Converts the 'time' column from a single date to a 'Monday-Friday' string range.
    It correctly finds the Monday and Friday of the week for any given date.
    """
    print("   - Reformatting time column for weekly view (Mon-Fri)...")
    
    def get_week_range(any_date):
        """Calculates the Monday and Friday for the week of the given date."""
        # weekday() returns 0 for Monday and 6 for Sunday.
        days_to_monday = any_date.weekday()
        monday = any_date - timedelta(days=days_to_monday)
        friday = monday + timedelta(days=4)
        return f"{monday.strftime('%Y-%m-%d')}-{friday.strftime('%Y-%m-%d')}"

    # Ensure 'time' is a datetime object before applying transformations
    df['time'] = pd.to_datetime(df['time'])
    
    # Apply the robust function to calculate the week range for each row
    df['time'] = df['time'].apply(get_week_range)
    return df

def save_data_to_csv(df, ticker, start_date, end_date, interval):
    """
    Saves the DataFrame to a CSV file in the main data directory.
    """
    file_name = f"{ticker}_{start_date}_to_{end_date}.csv"
    output_file = os.path.join(DATA_DIR, file_name)
    
    df.to_csv(output_file, index=False)
    print(f"   - Data saved to: {output_file}")
    return output_file

def parse_vpa_analysis(file_path):
    """
    Parses the VPA.md file to extract analysis for each ticker, preserving indentation.
    
    Args:
        file_path (str): The path to the VPA.md file.

    Returns:
        dict: A dictionary with tickers as keys and analysis text as values.
    """
    print(f"\n-> Reading VPA analysis from: {file_path}")
    if not os.path.exists(file_path):
        print(f"   - {os.path.basename(file_path)} not found. Skipping analysis section.")
        return {}

    analyses = {}
    current_ticker = None
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped_line = line.strip()

            # Check for a ticker header (e.g., "# VNINDEX").
            # The header line should only contain the ticker and the leading '#'.
            if stripped_line.startswith('# ') and len(stripped_line.split()) == 2:
                current_ticker = stripped_line.split()[1]
                analyses[current_ticker] = []
                continue

            # Stop capturing content at a separator line
            if stripped_line == '---':
                current_ticker = None
                continue

            # If we are inside a ticker's section, append the line
            if current_ticker:
                # Use rstrip() to remove the trailing newline but preserve leading spaces
                analyses[current_ticker].append(line.rstrip('\n'))

    # Join the collected lines for each ticker into a single block of text
    for ticker, lines in analyses.items():
        analyses[ticker] = '\n'.join(lines).strip()
        
    print(f"   - Found analysis for {len(analyses)} tickers.")
    return analyses


def get_latest_vpa_signal(analysis_text: str) -> str | None:
    """
    Parses the VPA analysis text for a single ticker to find the signal
    from the most recent entry.

    Args:
        analysis_text: The full VPA analysis content for one ticker.

    Returns:
        The normalized signal string (e.g., "Sign of Strength") or None.
    """
    # CORRECTED: Use \s+ to match one or more spaces after the dash,
    # matching the format in VPA.md ("-   **Ngày...")
    entries = re.split(r'\n-\s+\*\*Ngày.*?\:\*\*', analysis_text)

    if len(entries) <= 1:
        return None  # No valid date entries found

    # The text of the last entry is the last element of the split list.
    latest_entry_text = entries[-1]

    # Less important signals are at the top, most important are at the bottom.
    # The last match found in this dictionary will be the one that is returned.
    signals_to_check = {
        # --- Minor Signals ---
        "Test for Supply": r"Test for Supply",
        "No Demand": r"No Demand",
        "No Supply": r"No Supply",
        # --- Effort Signals ---
        "Effort to Rise": r"Effort to Rise",
        "Effort to Fall": r"Effort to Fall",
        # --- Potential Turning Points ---
        "Stopping Volume": r"Stopping Volume",
        "Buying Climax": r"Buying Climax|Topping Out Volume",
        "Selling Climax": r"Selling Climax",
        "Anomaly": r"Anomaly|sự bất thường",
        # --- Major, More Definitive Signals ---
        "Shakeout": r"Shakeout",
        "Sign of Weakness": r"Sign of Weakness|SOW",
        "Sign of Strength": r"Sign of Strength|SOS",
    }

    found_signal = None  # Initialize variable to store the latest match
    for signal_name, signal_pattern in signals_to_check.items():
        if re.search(signal_pattern, latest_entry_text, re.IGNORECASE):
            # If a match is found, update the variable.
            # This will be overwritten by any subsequent matches.
            found_signal = signal_name
    # After checking all possible signals, return the last one that was found.
    return found_signal


def generate_candlestick_report(df, ticker, start_date, end_date, interval):
    """
    Generates and saves a candlestick chart with volume.
    """
    print(f"   - Generating candlestick report for {ticker}...")
    
    ticker_report_path = os.path.join(REPORTS_DIR, ticker)
    os.makedirs(ticker_report_path, exist_ok=True)
    output_file = os.path.join(ticker_report_path, f"{ticker}_candlestick_chart.png")

    plot_df = df.copy()
    plot_df['time'] = pd.to_datetime(plot_df['time'])
    plot_df.rename(columns={
        'time': 'Date', 'open': 'Open', 'high': 'High',
        'low': 'Low', 'close': 'Close', 'volume': 'Volume'
    }, inplace=True)
    plot_df.set_index('Date', inplace=True)

    style = 'yahoo'
    timeframe = "Weekly" if interval == '1W' else "Daily"

    mpf.plot(
        plot_df,
        type='candle', style=style,
        title=f"{ticker} ({timeframe}) from {start_date} to {end_date}",
        ylabel='Price (VND)', volume=True, ylabel_lower='Volume',
        mav=(20, 50, 100), figratio=(20, 10),
        savefig=dict(fname=output_file, dpi=150, bbox_inches='tight')
    )
    
    print(f"   - Report saved to: {output_file}")
    return output_file

def generate_master_report(report_data, vpa_analyses, ticker_groups, ticker_to_group_map, start_date, end_date):
    """
    Generates an improved master REPORT.md file with a Table of Contents and deep links.
    This file is overwritten on each run.
    """
    print(f"\n-> Generating master report: {MASTER_REPORT_FILENAME}")
    signal_groups = defaultdict(list)
    for ticker, analysis_text in vpa_analyses.items():
        # Skip any tickers that might have been parsed but have no actual analysis text
        if not analysis_text or not analysis_text.strip():
            continue

        latest_signal = get_latest_vpa_signal(analysis_text)

        if latest_signal:
            signal_groups[latest_signal].append(ticker)
        else:
            # If no specific signal is found in the latest entry, group it as "Others"
            signal_groups["Others"].append(ticker)

    with open(MASTER_REPORT_FILENAME, 'w', encoding='utf-8') as f:
        # --- Main Header ---
        f.write("# AIPriceAction Market Report\n")
        f.write(f"*Report generated for data from **{start_date}** to **{end_date}**.*\n")
        f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        # --- START: Add invitation to view Trading Plan ---
        f.write("---\n\n")
        f.write("## 🎯 View the Trading Plan\n\n")
        f.write("**➡️ [Click here to view the trading plan](PLAN.md)**\n\n")
        f.write("**🎢 [Click here to view the latest market leaders](LEADER.md)**\n\n")
        f.write("---\n\n")
        # --- END: Add invitation ---

        # --- Write the VPA Signal Summary Table ---
        if signal_groups:
            # Use an explicit ID for a stable anchor link
            f.write('<h3 id="vpa-signal-summary">VPA Signal Summary (from Latest Analysis)</h3>\n\n')
            f.write("| Signal | Tickers |\n")
            f.write("|:---|:---|\n")

            # Pop "Others" from the dictionary to handle it separately at the end
            other_tickers = sorted(signal_groups.pop("Others", []))

            # Sort and write the main, recognized signals
            sorted_signals = sorted(signal_groups.keys())
            for signal in sorted_signals:
                tickers = sorted(signal_groups[signal])
                ticker_links = [f"[{t}](#{t.lower()})" for t in tickers]
                f.write(f"| {signal} | {', '.join(ticker_links)} |\n")

            # Now, write the "Others" row at the end of the table if it's not empty
            if other_tickers:
                ticker_links = [f"[{t}](#{t.lower()})" for t in other_tickers]
                f.write(f"| Others | {', '.join(ticker_links)} |\n")

            f.write("\n---\n\n")

        # --- Write the Ticker Groups Section ---
        if ticker_groups:
            f.write("## Groups\n")
            # Create a set of tickers that are actually in the report for efficient lookup
            tickers_in_report = {rd['ticker'] for rd in report_data}
            sorted_groups = sorted(ticker_groups.keys())
            for group in sorted_groups:
                tickers_in_group = sorted(ticker_groups[group])
                # Create a list of markdown links ONLY for tickers that are both in the group and in the report
                ticker_links = [f"[{t}](#{t.lower()})" for t in tickers_in_group if t in tickers_in_report]
                if ticker_links:
                    group_anchor = group.lower().replace('_', '-')
                    f.write(f'<h3 id="{group_anchor}">{group}</h3>\n\n')
                    f.write(', '.join(ticker_links) + "\n\n")
            f.write("---\n\n")

        # --- Table of Contents ---
        f.write("## Table of Contents\n")
        f.write("| Ticker | Actions |\n")
        f.write("|:-------|:--------|\n")
        for data in report_data:
            ticker_id = data['ticker'].lower() # Markdown anchors are typically lowercase
            # Add a direct link to the CSV data file
            f.write(f"| **[{data['ticker']}](#{ticker_id})** | [[Download CSV]({data['csv_path']})] |\n")
        f.write("\n---\n\n")

        # --- Summary Table ---
        f.write("## Ticker Performance Summary\n")
        f.write("| Ticker | Period High | Period Low | Latest Close | Change % | Total Volume |\n")
        f.write("|:-------|------------:|-----------:|-------------:|---------:|-------------:|\n")
        for data in report_data:
            change_color = "green" if data['change_pct'] >= 0 else "red"
            change_symbol = "📈" if data['change_pct'] >= 0 else "📉"
            f.write(
                f"| **{data['ticker']}** | {data['period_high']:,} | {data['period_low']:,} | **{data['latest_close']:,}** | "
                f"<span style='color:{change_color};'>{data['change_pct']:.2f}% {change_symbol}</span> | "
                f"{data['total_volume']:,} |\n"
            )
        
        f.write("\n---\n\n")

        # --- Detailed Section for each Ticker ---
        f.write("## Individual Ticker Analysis\n")
        for data in report_data:
            ticker_id = data['ticker'].lower()
            f.write(f"### {data['ticker']}\n\n")
            
            # --- VPA Analysis Section with Deep Link and Limited Blockquote ---
            if data['ticker'] in vpa_analyses:
                full_analysis_text = vpa_analyses[data['ticker']]

                # Check if there is any analysis text to process
                if full_analysis_text and full_analysis_text.strip():
                    # 1. Extract all dates from the full analysis to create the date range for the link
                    dates = re.findall(r'\d{4}-\d{2}-\d{2}', full_analysis_text)
                    if dates:
                        # Sort unique dates to ensure correct start and end
                        sorted_dates = sorted(list(set(dates)))
                        start_date_str = sorted_dates[0]
                        end_date_str = sorted_dates[-1]
                        vpa_link_text = f"VPA Analysis ({start_date_str} - {end_date_str})"
                    else:
                        vpa_link_text = "VPA Analysis"  # Fallback if no dates are found

                    f.write(f"#### [{vpa_link_text}](./{VPA_ANALYSIS_FILENAME}#{ticker_id})\n")

                    # 2. Split the full analysis into daily entries using a positive lookahead.
                    # This splits before "-   **Ngày" without consuming the delimiter.
                    daily_entries = re.split(r'\n(?=-   \*\*Ngày)', full_analysis_text)

                    # 3. Get the last 10 daily entries for the summary
                    limited_entries = daily_entries[-10:]

                    # 4. Join the limited entries back into a single text block
                    limited_analysis_text = "\n".join(limited_entries)

                    # 5. Format the limited analysis as a blockquote for better rendering in Markdown
                    blockquote_analysis = '> ' + limited_analysis_text.replace('\n', '\n> ')
                    f.write(blockquote_analysis + "\n\n")

            f.write(f"![Price Chart for {data['ticker']}]({data['chart_path']})\n\n")
            
            # --- Build the Back to Top / Back to Group links ---
            # Start with the standard Back to Top link
            links = []

            # Check if the current ticker belongs to a group
            ticker_name = data['ticker']
            if ticker_name in ticker_to_group_map:
                group_name = ticker_to_group_map[ticker_name]
                group_anchor = group_name.lower().replace('_', '-')
                # Add the "Back to Group" link
                links.append(f'<a href="#{group_anchor}">↑ Back to group {group_name}</a>')

            links.append('<a href="#vpa-signal-summary">↑ Back to Top</a>')
            # Join the links with a separator and wrap them in the paragraph tag
            up_link_html = f'<p align="right">{" &nbsp;|&nbsp; ".join(links)}</p>\n\n'
            f.write(up_link_html)

            # --- Statistics Table ---
            f.write("#### Key Statistics\n")
            f.write("| Metric | Value |\n")
            f.write("|:---|---:|\n")
            f.write(f"| Date Range | {data['start_date']} to {data['end_date']} |\n")
            f.write(f"| **Latest Close** | **{data['latest_close']:,}** |\n")
            f.write(f"| Period Open | {data['period_open']:,} |\n")
            f.write(f"| Period High | {data['period_high']:,} |\n")
            f.write(f"| Period Low | {data['period_low']:,} |\n")
            f.write(f"| Period Change % | {data['change_pct']:.2f}% |\n")

            f.write(f"\n**[Download {data['ticker']} Data (.csv)]({data['csv_path']})**\n\n")
            f.write("---\n\n")
            
    print("   - Master report generated successfully.")


def main():
    """Main function to orchestrate the data download and report generation."""
    global DATA_DIR, REPORTS_DIR, MASTER_REPORT_FILENAME, VPA_ANALYSIS_FILENAME

    parser = argparse.ArgumentParser(description="AIPriceAction Data Pipeline")
    parser.add_argument('--start-date', default="2025-01-02", type=str, help="The start date for data download in 'YYYY-MM-DD' format.")
    parser.add_argument('--end-date', default=datetime.now().strftime('%Y-%m-%d'), type=str, help="The end date for data download in 'YYYY-MM-DD' format.")
    parser.add_argument('--week', action='store_true', help="Enable weekly data processing mode.")
    args = parser.parse_args()

    data_interval = '1D'
    if args.week:
        print("--- Weekly mode enabled. Changing directories and data interval. ---")
        DATA_DIR = "market_data_week"
        REPORTS_DIR = "reports_week"
        MASTER_REPORT_FILENAME = "REPORT_week.md"
        VPA_ANALYSIS_FILENAME = "VPA_week.md"
        data_interval = '1W'

    START_DATE = args.start_date
    END_DATE = args.end_date

    print("--- AIPriceAction Data Pipeline: START ---")
    print(f"--- Using data period: {START_DATE} to {END_DATE} ---")
    
    setup_directories()
    vpa_analyses = parse_vpa_analysis(VPA_ANALYSIS_FILENAME)

    try:
        with open('ticker_group.json', 'r', encoding='utf-8') as f:
            ticker_groups = json.load(f)
        print("Loaded ticker groups from ticker_group.json")
    except FileNotFoundError:
        print("ticker_group.json not found. Skipping group section.")
        ticker_groups = {}

    ticker_to_group_map = {}
    for group, tickers in ticker_groups.items():
        for ticker in tickers:
            ticker_to_group_map[ticker] = group
    
    master_report_data = []
    TICKERS_TO_DOWNLOAD.sort(key=lambda t: (0, t) if t == 'VNINDEX' else (1, t))

    for ticker in TICKERS_TO_DOWNLOAD:
        stock_df = download_stock_data(ticker, START_DATE, END_DATE, interval=data_interval)
        
        if stock_df is not None and not stock_df.empty:
            # Generate chart and stats with original datetime objects first
            chart_path = generate_candlestick_report(stock_df, ticker, START_DATE, END_DATE, data_interval)
            
            period_open = stock_df['open'].iloc[0]
            latest_close = stock_df['close'].iloc[-1]
            change_pct = ((latest_close - period_open) / period_open) * 100 if period_open != 0 else 0
            
            # Create a copy for CSV and reformat if needed
            df_for_csv = stock_df.copy()
            if args.week:
                df_for_csv = reformat_time_column_for_weekly_data(df_for_csv)
            
            csv_path = save_data_to_csv(df_for_csv, ticker, START_DATE, END_DATE, data_interval)

            report_entry = {
                'ticker': ticker, 'records': len(stock_df),
                'start_date': stock_df['time'].min().strftime('%Y-%m-%d'),
                'end_date': stock_df['time'].max().strftime('%Y-%m-%d'),
                'period_open': period_open, 'latest_close': latest_close,
                'period_high': stock_df['high'].max(), 'period_low': stock_df['low'].min(),
                'change_pct': change_pct, 'total_volume': stock_df['volume'].sum(),
                'csv_path': csv_path, 'chart_path': chart_path,
            }
            master_report_data.append(report_entry)
            
    if master_report_data:
        generate_master_report(master_report_data, vpa_analyses, ticker_groups, ticker_to_group_map, START_DATE, END_DATE)
            
    print("\n--- AIPriceAction Data Pipeline: FINISHED ---")


if __name__ == "__main__":
    os.environ["ACCEPT_TC"] = "tôi đồng ý"
    main()

