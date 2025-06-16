import os
import time
import matplotlib.pyplot as plt
import pandas as pd
import mplfinance as mpf
from datetime import datetime
from vnstock import Vnstock

# --- Configuration ---
# The list of tickers is now read from TICKERS.csv
try:
    TICKERS_TO_DOWNLOAD = pd.read_csv('TICKERS.csv')['ticker'].tolist()
    print(f"Loaded {len(TICKERS_TO_DOWNLOAD)} tickers from TICKERS.csv")
except FileNotFoundError:
    print("TICKERS.csv not found. Using default list.")
    TICKERS_TO_DOWNLOAD = ["VNINDEX", "TCB", "FPT"]


# Define the start and end dates for the data you want to download.
START_DATE = "2025-01-02"
END_DATE = datetime.now().strftime('%Y-%m-%d')

# Define the names for your data and report directories.
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
    """
    print("Setting up base directories...")
    for directory in [DATA_DIR, REPORTS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"  - Created directory: {directory}")

def download_stock_data(ticker, start_date, end_date):
    """
    Checks for local data first. If not found, downloads historical stock data.
    
    Args:
        ticker (str): The stock symbol or index name.
        start_date (str): The start date in 'YYYY-MM-DD' format.
        end_date (str): The end date in 'YYYY-MM-DD' format.

    Returns:
        pandas.DataFrame: A DataFrame containing the historical data, or None if fails.
    """
    print(f"\n-> Processing ticker: {ticker}")
    
    # --- SMART CACHING ---
    # Construct filename based on ticker and date range
    file_name = f"{ticker}_{start_date}_to_{end_date}.csv"
    file_path = os.path.join(DATA_DIR, file_name)

    # Check if the data file already exists
    if os.path.exists(file_path):
        print(f"   - Found local data. Loading from: {file_path}")
        # Load from CSV, ensuring the 'time' column is parsed as dates
        df = pd.read_csv(file_path, parse_dates=['time'])
        return df
    # --- END SMART CACHING ---

    print(f"   - No local data found. Downloading from {start_date} to {end_date}...")
    try:
        df = stock_reader.quote.history(
            symbol=ticker,
            start=start_date,
            end=end_date,
            interval='1D'
        )
        time.sleep(2)

        if not df.empty:
            print(f"   - Success! Downloaded {len(df)} raw records for {ticker}.")
            df['time'] = pd.to_datetime(df['time'])

            # Filter the DataFrame to the exact date range
            mask = (df['time'] >= pd.to_datetime(start_date)) & (df['time'] <= pd.to_datetime(end_date))
            df_filtered = df.loc[mask].copy()

            # Add the 'ticker' column to each row
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

def save_data_to_csv(df, ticker, start_date, end_date):
    """
    Saves the DataFrame to a CSV file in the main data directory.
    """
    # Construct filename with date range
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
        print("   - VPA.md not found. Skipping analysis section.")
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

def generate_candlestick_report(df, ticker):
    """
    Generates and saves a candlestick chart with volume.
    Returns the path to the saved image.
    """
    print(f"   - Generating candlestick report for {ticker}...")
    
    ticker_report_path = os.path.join(REPORTS_DIR, ticker)
    os.makedirs(ticker_report_path, exist_ok=True)
    output_file = os.path.join(ticker_report_path, f"{ticker}_candlestick_chart.png")

    # mplfinance requires specific column names and a DatetimeIndex.
    # We'll create a copy to avoid changing the original DataFrame.
    plot_df = df.copy()
    plot_df.rename(columns={
        'time': 'Date',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }, inplace=True)
    plot_df.set_index('Date', inplace=True)

    # Define a custom style for the chart
    # style = 'charles'
    # style = 'classic'
    style = 'yahoo'

    # Create and save the plot
    mpf.plot(
        plot_df,
        type='candle',
        style=style,
        title=f"{ticker} from {START_DATE} to {END_DATE}",
        ylabel='Price (VND)',
        volume=True,
        ylabel_lower='Volume',
        mav=(20, 50, 100),
        figratio=(20, 10),
        savefig=dict(fname=output_file, dpi=150, bbox_inches='tight')
    )
    
    print(f"   - Report saved to: {output_file}")
    return output_file

def generate_master_report(report_data, vpa_analyses):
    """
    Generates an improved master REPORT.md file with a Table of Contents and deep links.
    This file is overwritten on each run.
    """
    print(f"\n-> Generating master report: {MASTER_REPORT_FILENAME}")
    
    with open(MASTER_REPORT_FILENAME, 'w', encoding='utf-8') as f:
        # --- Main Header ---
        f.write("# AIPriceAction Market Report\n")
        f.write(f"*Report generated for data from **{START_DATE}** to **{END_DATE}**.*\n")
        f.write(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
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
            
            # --- VPA Analysis Section with Deep Link and Blockquote Rendering ---
            if data['ticker'] in vpa_analyses:
                f.write(f"#### [VPA Analysis](./{VPA_ANALYSIS_FILENAME}#{ticker_id})\n")
                # Format the analysis text as a blockquote for better rendering
                analysis_text = vpa_analyses[data['ticker']]
                blockquote_analysis = '> ' + analysis_text.replace('\n', '\n> ')
                f.write(blockquote_analysis + "\n\n")
            
            f.write(f"![Price Chart for {data['ticker']}]({data['chart_path']})\n\n")
            
            # Add a formatted "Back to Top" link, aligned to the right.
            up_link_html = '<p align="right"><a href="#table-of-contents">↑ Back to Top</a></p>\n\n'
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
            f.write(f"| 52-Week High | {data['high52w']:,} |\n")
            f.write(f"| 52-Week Low | {data['low52w']:,} |\n")

            f.write(f"\n**[Download {data['ticker']} Data (.csv)]({data['csv_path']})**\n\n")
            f.write("---\n\n")
            
    print("   - Master report generated successfully.")


def main():
    """Main function to orchestrate the data download and report generation."""
    print("--- AIPriceAction Data Pipeline: START ---")
    
    setup_directories()
    vpa_analyses = parse_vpa_analysis(VPA_ANALYSIS_FILENAME)
    
    master_report_data = []

    # Sort the list, keeping 'VNINDEX' at the top and sorting the rest alphabetically
    TICKERS_TO_DOWNLOAD.sort(key=lambda t: (0, t) if t == 'VNINDEX' else (1, t))

    for ticker in TICKERS_TO_DOWNLOAD:
        stock_df = download_stock_data(ticker, START_DATE, END_DATE)
        
        if stock_df is not None and not stock_df.empty:
            csv_path = save_data_to_csv(stock_df, ticker, START_DATE, END_DATE)
            chart_path = generate_candlestick_report(stock_df, ticker)
            
            # Calculate additional stats for the report
            period_open = stock_df['open'].iloc[0]
            latest_close = stock_df['close'].iloc[-1]
            change_pct = ((latest_close - period_open) / period_open) * 100 if period_open != 0 else 0

            # Get 52-week high/low from the full (unfiltered) dataset if possible
            # This is a simplification; a more robust solution would download a year of data.
            full_year_df = stock_reader.quote.history(symbol=ticker, start=(datetime.now() - pd.DateOffset(years=1)).strftime('%Y-%m-%d'), end=END_DATE)
            high_52w = full_year_df['high'].max() if not full_year_df.empty else stock_df['high'].max()
            low_52w = full_year_df['low'].min() if not full_year_df.empty else stock_df['low'].min()
            
            # Gather all information for the master report
            report_entry = {
                'ticker': ticker,
                'records': len(stock_df),
                'start_date': stock_df['time'].min().strftime('%Y-%m-%d'),
                'end_date': stock_df['time'].max().strftime('%Y-%m-%d'),
                'period_open': period_open,
                'latest_close': latest_close,
                'period_high': stock_df['high'].max(),
                'period_low': stock_df['low'].min(),
                'change_pct': change_pct,
                'total_volume': stock_df['volume'].sum(),
                'high52w': high_52w,
                'low52w': low_52w,
                'csv_path': csv_path,
                'chart_path': chart_path,
            }
            master_report_data.append(report_entry)
            
    # Generate the final master markdown report if any data was processed
    if master_report_data:
        generate_master_report(master_report_data, vpa_analyses)
            
    print("\n--- AIPriceAction Data Pipeline: FINISHED ---")


if __name__ == "__main__":
    # This environment variable is required by vnstock to accept the terms and conditions.
    os.environ["ACCEPT_TC"] = "tôi đồng ý"
    main()

