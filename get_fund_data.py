import os
import time
import matplotlib.pyplot as plt
import pandas as pd
from vnstock import *
from vnstock.explorer.fmarket.fund import Fund
import mplfinance as mpf
import re
import json
import argparse
from collections import defaultdict
from datetime import datetime, timedelta

def save_fund_data():
    """
    Saves various open-end fund data reports to the 'funds_data' directory.
    - Creates the 'funds_data' directory if it does not exist.
    - Downloads the complete fund listing.
    - For each fund in 'FUNDS.csv', it downloads:
        - NAV (Net Asset Value) report
        - Top holdings
        - Asset holdings
        - Industry holdings
    - A 1-second delay is added after each API call to avoid rate limiting.
    """
    # 1. Instantiate the Fund class
    fund_explorer = Fund()
    
    # 2. Create the funds_data directory
    output_dir = 'funds_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # 3. Download and save the complete fund listing
    try:
        print("Downloading fund listing...")
        all_funds_df = fund_explorer.listing()
        listing_path = os.path.join(output_dir, 'listing.csv')
        all_funds_df.to_csv(listing_path, index=False)
        print(f"Saved fund listing to: {listing_path}")
    except Exception as e:
        print(f"An error occurred while downloading the fund list: {e}")
        return
    finally:
        # Sleep after the API call, regardless of success or failure
        print("Waiting 1 second...")
        time.sleep(1)

    # 4. Read FUNDS.csv to get the list of tickers to process
    funds_csv_path = 'FUNDS.csv'
    if not os.path.exists(funds_csv_path):
        print(f"Error: Could not find {funds_csv_path}. Please create this file.")
        return

    try:
        tickers_df = pd.read_csv(funds_csv_path)
        fund_tickers = tickers_df['ticker'].tolist()
        print(f"\nFound {len(fund_tickers)} funds to process: {fund_tickers}")

        # Define the reports to fetch for each fund
        reports_to_fetch = {
            "nav_report": fund_explorer.details.nav_report,
            "top_holding": fund_explorer.details.top_holding,
            "asset_holding": fund_explorer.details.asset_holding,
            "industry_holding": fund_explorer.details.industry_holding,
        }

        # Loop through each fund ticker
        for ticker in fund_tickers:
            print(f"\n--- Processing fund: {ticker} ---")
            # Loop through each type of report
            for report_name, api_function in reports_to_fetch.items():
                try:
                    # Define the output path for the CSV file
                    file_path = os.path.join(output_dir, f'{ticker}_{report_name}.csv')
                    if os.path.exists(file_path):
                        print(f"File already exists: {file_path}. Skipping download.")
                        continue
                    print(f"Downloading {report_name} for '{ticker}'...")
                    # Call the appropriate API function (e.g., fund_explorer.details.nav_report)
                    details_df = api_function(symbol=ticker)
                    time.sleep(3)  # Sleep to avoid rate limiting
                    
                    # Save the data to a CSV file
                    details_df.to_csv(file_path, index=False)
                    print(f"Successfully saved to: {file_path}")

                except Exception as e:
                    print(f"An error occurred while fetching {report_name} for '{ticker}': {e}")

    except Exception as e:
        print(f"A critical error occurred while reading or processing {funds_csv_path}: {e}")


def main():
      save_fund_data()

if __name__ == "__main__":
    os.environ["ACCEPT_TC"] = "tôi đồng ý"
    main()
