# AIPriceAction Data Pipeline

This project is a flexible and efficient data pipeline designed to download, analyze, and visualize stock data from the Vietnamese market.

It automatically fetches daily price data for a configurable list of tickers, generates detailed candlestick charts, caches data locally to avoid redundant downloads, and integrates qualitative analysis into a single, comprehensive markdown report.

---

## 🚀 View the Latest Analysis

The primary output of this project is the **`REPORT.md`** file. This file is automatically regenerated with the latest data and analysis every time the script runs.

**➡️ [Click here to view the Daily Market Report](REPORT.md)**

**➡️ [Click here to view the Weekly Market Report](REPORT_week.md)**

**🎢 [Click here to view the latest Market Leaders](LEADER.md)**

**🐎 [Click here to view the Market Impact Contributors](IMPACT.md)**

**🏦 [Click here to view the Fund Performance Deep-Dive](FUNDS.md)**

---

## 🎯 View the Trading Plan

Based on the latest analysis, the **`PLAN.md`** file outlines potential trading strategies and top opportunities. This plan synthesizes VPA signals for a mid-term perspective.

**➡️ [Click here to view the trading plan](PLAN.md)**

---
## Analysis Sources

1. **Daily Analysis Sources:**

* **`REPORT.md`**: For the most recent daily signals and price/volume activity (last 10 days).
* **`VPA.md`**: For the detailed, multi-session daily VPA narrative of each ticker. 
* **`market_data.txt`**: For the raw daily price, volume, and OHLC data (last 40 days) used to verify daily signals. 

2. **Weekly Analysis Sources:**

* **`REPORT_week.md`**: For the most recent weekly signals, providing a strategic, big-picture view.
* **`VPA_week.md`**: For the broader historical context and the multi-week VPA narrative.
* **`market_data_week.txt`**: For the raw weekly OHLC data (last 40 weeks) to verify long-term signals. 


3. **Contextual & Grouping Sources:**

* **`LEADER.md`**: For assessing the **industry context** based on weekly analysis. You must use this to determine if a ticker is in a strong (`Dẫn dắt Đồng Thuận`), weakening, or weak (`Yếu/Phân Phối`) industry group.
* **`GROUP.md`**: The definitive source for mapping individual tickers to their respective industry groups.
* **`IMPACT.md`**: Identifies the top stocks and sectors driving or holding back the VN-Index, providing insight into market-wide momentum.

### 4. Fund Universe Analysis

*   **`FUNDS.md`**: A comprehensive deep-dive into the performance, risk profiles, and portfolio compositions of major Vietnamese investment funds. Use this to compare professional money managers against the market and each other.

---

## 📚 VPA & Wyckoff Method Tutorial System

This project includes a comprehensive Vietnamese-language tutorial system covering Volume Price Analysis (VPA) and Wyckoff Method principles with real market data examples.

### 📖 Tutorial Chapters

**Fundamental Concepts:**
- [Chapter 1.1: VPA Basics (Vietnamese)](docs/tutorials/vpa-basics-vi.md)
- [Chapter 1.2: Wyckoff Laws (Vietnamese)](docs/tutorials/wyckoff-laws-vi.md)
- [Chapter 1.3: Composite Man (Vietnamese)](docs/tutorials/composite-man-vi.md)

**Market Phases:**
- [Chapter 2.1: Accumulation Phases (Vietnamese)](docs/tutorials/accumulation-phases-vi.md)
- [Chapter 2.2: Distribution Phases (Vietnamese)](docs/tutorials/distribution-phases-vi.md)

**Signal Recognition:**
- [Chapter 3.1: Bullish VPA Signals (Vietnamese)](docs/tutorials/bullish-vpa-signals-vi.md)
- [Chapter 3.2: Bearish VPA Signals (Vietnamese)](docs/tutorials/bearish-vpa-signals-vi.md)

**Trading Systems:**
- [Chapter 4.1: Trading Systems (Vietnamese)](docs/tutorials/trading-systems-vi.md)

**Advanced Concepts:**
- [Chapter 5.1: Advanced Pattern Recognition](docs/tutorials/advanced-pattern-recognition.md)
- [Chapter 5.2: Institutional Backtesting Engine](docs/tutorials/institutional-backtesting.md)
- [Chapter 5.3: Smart Money Flow Analysis](docs/tutorials/smart-money-flow.md)
- [Chapter 5.4: Machine Learning Pattern Recognition](docs/tutorials/ml-pattern-recognition.md)

### 🎯 Case Studies: Chiến Dịch Tích Lũy 2025

Detailed case studies analyzing institutional accumulation campaigns in Vietnamese stocks during 2025:

**➡️ [Nghiên Cứu Tình Huống: VIC - Chiến Dịch Tích Lũy Bất Động Sản 2025](docs/tutorials/case-studies/vic-accumulation-2025.md)**
- Phân tích pattern tích lũy VIC Vingroup với chuỗi VPA hoàn hảo
- Thể hiện sức mạnh leader bất động sản trong phục hồi thị trường

**➡️ [Nghiên Cứu Tình Huống: VHM - Chiến Dịch Tích Lũy Biến Động 2025](docs/tutorials/case-studies/vhm-accumulation-2025.md)**
- Pattern tích lũy với biến động cao của VHM Vinhomes
- Minh họa đặc tính beta cao trong ngành bất động sản

**➡️ [Nghiên Cứu Tình Huống: SSI - Chiến Dịch Tích Lũy Nhà Vô Địch Ngành Chứng Khoán 2025](docs/tutorials/case-studies/ssi-accumulation-2025.md)**
- Phân tích Shakeout pattern và luân chuyển ngành chứng khoán
- Thể hiện đặc tính dịch vụ tài chính trong chu kỳ phục hồi

**➡️ [Nghiên Cứu Tình Huống: VIX - Chiến Dịch Tích Lũy Gã Khổng Lồ Cơ Sở Hạ Tầng 2025](docs/tutorials/case-studies/vix-accumulation-2025.md)**
- Pattern đảo chiều từ phân phối sang tích lũy
- Minh họa đặc tính chu kỳ cơ sở hạ tầng

**➡️ [Nghiên Cứu Tình Huống: LPB - Chiến Dịch Tích Lũy Chuyển Đổi Ngân Hàng 2025](docs/tutorials/case-studies/lpb-accumulation-2025.md)**
- Chuỗi VPA kinh điển: No Supply → Test for Supply → Sign of Strength
- Thể hiện câu chuyện chuyển đổi ngân hàng khu vực

### 🗺️ Navigation

**➡️ [Tutorial Map & Content Overview](docs/MAP_OF_CONTENT.md)**
**➡️ [VPA Methods & Methodology](docs/methods/README.md)**

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
