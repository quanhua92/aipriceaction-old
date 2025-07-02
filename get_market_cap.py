import os
import time
import random
import pandas as pd
from vnstock import Vnstock
import warnings
import argparse

# --- HIDE THE WARNING ---
warnings.simplefilter(action='ignore', category=FutureWarning)

# Set environment variable to accept vnstock's terms and conditions
if "ACCEPT_TC" not in os.environ:
    os.environ["ACCEPT_TC"] = "tôi đồng ý"

def get_market_cap_vnstock(symbol: str) -> int:
    """
    Fetches the market capitalization for a given stock symbol using vnstock.
    
    Args:
        symbol: The stock ticker symbol (e.g., 'FPT').

    Returns:
        The market capitalization in billions (Tỷ) of VND, or -1 if an error occurs.
    """
    try:
        stock = Vnstock().stock(symbol=symbol, source="VCI")
        data = stock.finance.ratio(period='year', lang='vi')
        time.sleep(random.uniform(1.5, 5.0))
        market_cap = data[('Chỉ tiêu định giá', 'Vốn hóa (Tỷ đồng)')].iloc[0]
        market_cap_int = int(market_cap)
        print(f"SUCCESS: Fetched new data for {symbol}: {market_cap_int} (Billion VND)")
        return market_cap_int
    except Exception as e:
        print(f"ERROR: Could not fetch market cap for {symbol}. Reason: {e}")
        return -1

def main():
    """
    Main function to read tickers, fetch market caps, and save to a sorted CSV file.
    Supports a resume mode to use existing data as a cache.
    """
    parser = argparse.ArgumentParser(
        description="Fetch market capitalization and save to a sorted CSV. The --resume flag uses the existing output file as a cache to avoid re-fetching data."
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Use existing data from the output file as a cache. The file will still be completely rewritten to ensure it is sorted."
    )
    args = parser.parse_args()

    input_file = "TICKERS.csv"
    output_file = "stock_market_cap.csv"
    
    # --- 1. Load and Sort Tickers (The "source of truth" for order) ---
    print(f"Reading tickers from {input_file}...")
    try:
        df = pd.read_csv(input_file)
        tickers = df['ticker'].dropna().unique().tolist()
    except FileNotFoundError:
        print(f"FATAL: Input file '{input_file}' not found. Please create it.")
        return
    except KeyError:
        print(f"FATAL: The file '{input_file}' must contain a column named 'ticker'.")
        return
    
    tickers.sort() # Sort tickers alphabetically
    print(f"Found {len(tickers)} unique tickers. The output will be in this sorted order.")

    # --- 2. Pre-load existing data if in resume mode (acts as a cache) ---
    existing_market_caps = {}
    if args.resume:
        print(f"--- Resume mode enabled: Reading '{output_file}' to build cache ---")
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        ticker_in_file, market_cap = line.strip().split(',')
                        if ticker_in_file and market_cap:
                            existing_market_caps[ticker_in_file] = int(market_cap)
                    except ValueError:
                        print(f"WARN: Skipping malformed line in cache file: {line.strip()}")
            print(f"Pre-loaded {len(existing_market_caps)} tickers from cache.")
        except FileNotFoundError:
            print(f"INFO: Cache file '{output_file}' not found. Will fetch all data.")
    else:
        print("--- Starting fresh (overwrite mode) ---")

    # --- 3. Process all tickers and write to a new file ---
    # The file is always opened in 'w' mode to guarantee a fresh, sorted output.
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for ticker in tickers:
                # Skip non-stock symbols like indices
                if ticker == "VNINDEX":
                    print(f"INFO: Skipping index '{ticker}'.")
                    continue
                
                market_cap = -1
                # Check if we have valid, cached data for this ticker
                if ticker in existing_market_caps:
                    market_cap = existing_market_caps[ticker]
                    print(f"INFO: Using cached data for {ticker}: {market_cap}")
                else:
                    # If not in cache, fetch from the API
                    market_cap = get_market_cap_vnstock(ticker)
                
                # Write to file if the data is valid (either from cache or new fetch)
                if market_cap != -1:
                    f.write(f"{ticker},{market_cap}\n")
                    f.flush() # Ensure data is written to disk immediately

    except IOError as e:
        print(f"FATAL: Could not write to output file {output_file}. Reason: {e}")
        return

    print("\n--- All tickers processed ---")
    print(f"SUCCESS: A new, sorted '{output_file}' has been created.")

if __name__ == "__main__":
    main()