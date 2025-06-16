# AIPriceAction Data Pipeline

This project is a flexible and efficient data pipeline designed to download, analyze, and visualize stock data from the Vietnamese market.

It automatically fetches daily price data for a configurable list of tickers, generates detailed candlestick charts, caches data locally to avoid redundant downloads, and integrates qualitative analysis into a single, comprehensive markdown report.

---

## 🚀 View the Latest Analysis

The primary output of this project is the **`REPORT.md`** file. This file is automatically regenerated with the latest data and analysis every time the script runs.

**➡️ [Click here to view the latest market report](REPORT.md)**

---

## Key Features

-   **Configurable Ticker List**: Easily manage which stocks to analyze by editing a simple `TICKERS.csv` file.
-   **Smart Data Caching**: Automatically saves downloaded data and re-loads it from local files on subsequent runs, saving time and network requests.
-   **VPA Integration**: Reads your qualitative analysis from a `VPA.md` file and seamlessly integrates it into the final report.
-   **Detailed Reporting**: Generates a master `REPORT.md` with a summary table, a table of contents, and a detailed breakdown for each ticker.
-   **Advanced Charting**: Creates professional candlestick charts for each ticker, complete with volume and multiple moving averages.

## Setup and Usage

### 1. Configure Tickers

Create and edit the **`TICKERS.csv`** file in the main project directory. Add the ticker symbols you want to analyze, one per line, under the `ticker` header.

_Example `TICKERS.csv`:_

```csv
ticker
VNINDEX
TCB
FPT
```

### 2. (Optional) Add Your Analysis

You can add your own price action analysis to the **`VPA.md`** file. The script will parse this file and display your notes alongside the corresponding ticker in the final report. Use a markdown header for each ticker.

_Example `VPA.md`:_

```markdown
# FPT

-   Strong uptrend continues.
-   A pullback to the 20-day MA could be a buying opportunity.

# TCB

-   Showing signs of accumulation in the current range.
```

### 3. Install Dependencies

Before running the script for the first time, install the required Python libraries using the `requirements.txt` file.

Open your terminal and run:

```bash
pip install -r requirements.txt
```

### 4. Run the Pipeline

To execute the data pipeline, simply run the `main.py` script from your terminal:

```bash
python main.py
```
