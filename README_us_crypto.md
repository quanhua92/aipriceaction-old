# AIPriceAction US & Cryptocurrency Analysis Pipeline

This is a complete data pipeline for analyzing US stock market indices and cryptocurrencies using Vietnamese VPA (Volume Price Analysis) methodology. The pipeline downloads global market data, generates professional candlestick charts, and produces comprehensive Vietnamese analysis reports.

## Overview

The US & Crypto pipeline is adapted from the original Vietnamese stock market analyzer to work with:
- **US Stock Market Indices**: DJI, S&P 500 (INX), NASDAQ (COMP), Russell 2000 (RUT), etc.
- **Major Cryptocurrencies**: Bitcoin (BTC), Ethereum (ETH), and other major crypto assets
- **Global Market Data**: Using vnstock's `world_index()` and `crypto()` methods with MSN source
- **Vietnamese VPA Analysis**: Professional VPA methodology applied to global markets

## Core Files & Usage

### 📊 Main Data Pipeline

#### `main_us_crypto.py`
**Purpose**: Primary data pipeline that downloads US index and crypto data, generates charts, and creates reports.

**Key Features**:
- Downloads US indices using `vnstock.world_index()` with MSN source
- Downloads crypto data using `vnstock.crypto()` with MSN source  
- Generates professional candlestick charts with volume and moving averages
- Creates comprehensive markdown reports with asset performance analysis
- Supports both daily (`1D`) and weekly (`1W`) intervals
- Smart caching prevents redundant API calls

**Usage**:
```bash
# Daily analysis (default)
uv run main_us_crypto.py

# Weekly analysis  
uv run main_us_crypto.py --week

# Custom date range
uv run main_us_crypto.py --start-date 2025-01-01 --end-date 2025-12-31

# Weekly analysis with custom dates
uv run main_us_crypto.py --week --start-date 2025-01-01 --end-date 2025-12-31
```

**Outputs**:
- `REPORT_us_crypto.md` or `REPORT_us_crypto_week.md`: Comprehensive market reports
- `market_data_us_crypto/` or `market_data_us_crypto_week/`: Raw CSV data files  
- `reports_us_crypto/` or `reports_us_crypto_week/`: Professional candlestick charts

---

### 🤖 AI-Powered VPA Analysis

#### `main_process_vpa_us_crypto.py`
**Purpose**: AI-powered VPA analysis coordinator with parallel processing for US indices and cryptocurrencies.

**Key Features**:
- Automatically generates Vietnamese VPA analysis using Claude/Gemini
- Parallel processing with configurable workers (default: 4)
- Smart analysis detection - only processes new data  
- Thread-safe logging with debug capabilities
- Performance metrics and speedup reporting
- Handles both US indices and crypto asset analysis

**Usage**:
```bash
# Daily VPA analysis with Claude (4 workers default)
uv run main_process_vpa_us_crypto.py

# Weekly VPA analysis with Gemini and 8 workers
uv run main_process_vpa_us_crypto.py --week --agent gemini --workers 8

# High-performance mode with 12 workers
uv run main_process_vpa_us_crypto.py --workers 12 --agent gemini

# Debug mode with verbose logging
uv run main_process_vpa_us_crypto.py --debug --verbose

# Sequential processing (1 worker)
uv run main_process_vpa_us_crypto.py --workers 1
```

**Outputs**:
- Individual VPA files in `vpa_data_us_crypto/` or `vpa_data_us_crypto_week/`
- Detailed logs in `/tmp/vpa_processing_us_crypto_*.log`
- Performance metrics and progress tracking

---

#### `merge_vpa_us_crypto.py`
**Purpose**: Merges new VPA analysis into master VPA files with asset class organization.

**Usage**:
```bash
# Merge daily VPA analysis
uv run merge_vpa_us_crypto.py

# Merge weekly VPA analysis  
uv run merge_vpa_us_crypto.py --week
```

**Outputs**:
- `VPA_us_crypto.md`: Master daily VPA analysis file
- `VPA_us_crypto_week.md`: Master weekly VPA analysis file
- Organized by asset classes (US_INDICES, MAJOR_CRYPTO, etc.)

---

### 📋 Configuration Files

#### `TICKERS_US.csv` 
List of US stock market indices to analyze:
```csv
ticker
DJI
INX
COMP
RUT
NYA
RUI
RUA
```

#### `TICKERS_CRYPTO.csv`
List of cryptocurrencies to analyze:
```csv
ticker
BTC
ETH
```

#### `ticker_group_us_crypto.json`
Asset class groupings for organizational purposes:
```json
{
    "US_INDICES": ["DJI", "INX", "COMP", "RUT", "NYA", "RUI", "RUA"],
    "MAJOR_CRYPTO": ["BTC", "ETH"],
    "ALTCOINS": ["USDT", "USDC", "BNB", "XRP", "ADA", "SOL", "DOGE"]
}
```

#### `GROUP_us_crypto.md`
Asset class reference table showing which assets belong to which categories.

---

### 📈 AI Task Protocols

#### `tasks/DAILY_PLAN_us_crypto.md`
**Purpose**: Daily market analysis and trading plan generation protocol for US/crypto markets.

**Features**:
- Comprehensive daily market analysis workflow
- US indices and cryptocurrency context analysis  
- Vietnamese VPA methodology adapted for global markets
- Trading opportunity identification and risk assessment

#### `tasks/WEEKLY_LEADER_us_crypto.md`  
**Purpose**: Weekly asset leadership analysis protocol using VPA-AssetLead methodology.

**Features**:
- Asset class strength assessment (US_INDICES, MAJOR_CRYPTO)
- Individual asset leader identification within each class
- Comprehensive weekly trend analysis
- Manual natural language analysis requirements

#### `tasks/DAILY_HOLD_us_crypto.md`
**Purpose**: Daily US/crypto portfolio management protocol with Portfolio-Strategist methodology.

**Features**:
- US indices and cryptocurrency portfolio analysis
- USD-based P&L calculations and risk management
- Asset class diversification strategies  
- Vietnamese VPA analysis adapted for global markets
- Action recommendation state transitions

#### `tasks/CHECK_HOLD_us_crypto.md`
**Purpose**: Portfolio holdings verification protocol to ensure data accuracy.

**Features**:
- USD price and P&L calculation verification
- VPA signal accuracy checking against source files
- Asset class classification verification
- Error prevention and quality control procedures

---

## Complete Workflow Examples

### Daily US & Crypto Analysis Workflow
```bash
# 1. Download market data and generate reports
uv run main_us_crypto.py

# 2. Generate VPA analysis with AI (parallel processing)
uv run main_process_vpa_us_crypto.py --workers 8

# 3. Merge VPA analysis into master files
uv run merge_vpa_us_crypto.py

# 4. Generate final reports with integrated VPA
uv run main_us_crypto.py
```

### Weekly US & Crypto Analysis Workflow  
```bash
# 1. Download weekly market data
uv run main_us_crypto.py --week

# 2. Generate weekly VPA analysis
uv run main_process_vpa_us_crypto.py --week --agent gemini --workers 6

# 3. Merge weekly VPA analysis
uv run merge_vpa_us_crypto.py --week

# 4. Generate weekly reports
uv run main_us_crypto.py --week
```

### High-Performance Analysis
```bash
# Maximum speed processing with 12 workers and Gemini
uv run main_process_vpa_us_crypto.py --workers 12 --agent gemini --debug

# Conservative sequential processing
uv run main_process_vpa_us_crypto.py --workers 1 --verbose
```

---

## Data Structure & Outputs

### Directory Structure
```
├── main_us_crypto.py                    # Main pipeline
├── main_process_vpa_us_crypto.py       # AI VPA coordinator  
├── merge_vpa_us_crypto.py              # VPA merger
├── TICKERS_US.csv                      # US indices list
├── TICKERS_CRYPTO.csv                  # Crypto assets list
├── ticker_group_us_crypto.json         # Asset groupings
├── GROUP_us_crypto.md                  # Asset class reference
├── VPA_us_crypto.md                    # Daily VPA analysis
├── VPA_us_crypto_week.md               # Weekly VPA analysis  
├── REPORT_us_crypto.md                 # Daily report
├── REPORT_us_crypto_week.md            # Weekly report
├── market_data_us_crypto/              # Daily CSV data
├── market_data_us_crypto_week/         # Weekly CSV data
├── vpa_data_us_crypto/                 # Daily VPA files
├── vpa_data_us_crypto_week/            # Weekly VPA files
├── reports_us_crypto/                  # Daily charts
├── reports_us_crypto_week/             # Weekly charts
└── tasks/                              # AI task protocols
    ├── DAILY_PLAN_us_crypto.md
    ├── WEEKLY_LEADER_us_crypto.md
    ├── DAILY_HOLD_us_crypto.md
    └── CHECK_HOLD_us_crypto.md
```

### Key Output Files

#### `REPORT_us_crypto.md` / `REPORT_us_crypto_week.md`
- **Asset Categories**: US Indices and Cryptocurrencies with navigation links
- **VPA Signal Summary**: Latest VPA signals organized by signal type
- **Performance Summary**: Asset performance with USD pricing
- **Individual Analysis**: Detailed analysis for each asset with:
  - Professional candlestick charts with volume and moving averages
  - Latest VPA analysis excerpts (last 5 daily entries)
  - Key statistics including USD price movements
  - Direct links to raw CSV data files

#### `VPA_us_crypto.md` / `VPA_us_crypto_week.md`  
- **Asset Class Organization**: Grouped by US_INDICES, MAJOR_CRYPTO, etc.
- **Vietnamese VPA Analysis**: Professional VPA methodology in Vietnamese
- **Signal Analysis**: Comprehensive Wyckoff methodology application
- **Volume Pattern Analysis**: Detailed volume-price relationship analysis
- **Trend Context**: Multi-timeframe trend analysis

---

## Asset Types & Data Sources

### US Stock Market Indices
- **Data Source**: `vnstock.world_index()` with MSN source
- **Supported Indices**: DJI, S&P 500 (INX), NASDAQ (COMP), Russell 2000 (RUT), NYSE Composite (NYA), Russell 1000 (RUI), Russell 3000 (RUA)
- **Price Format**: USD with appropriate precision for index values
- **Volume**: Daily/weekly trading volumes
- **Technical Analysis**: Moving averages (20, 50, 100), support/resistance levels

### Cryptocurrencies
- **Data Source**: `vnstock.crypto()` with MSN source  
- **Supported Assets**: Bitcoin (BTC), Ethereum (ETH), and major altcoins
- **Price Format**: USD with crypto-appropriate precision
- **Volume**: 24-hour trading volumes
- **Technical Analysis**: Crypto-specific volatility considerations

---

## Performance & Optimization

### Parallel Processing Performance
- **Default (4 workers)**: Balanced performance for most systems
- **High performance (8-12 workers)**: For powerful systems with fast internet
- **Sequential (1 worker)**: Conservative approach for limited resources
- **Typical speedup**: 3-8x faster than sequential processing depending on worker count

### Smart Caching
- **Data Caching**: Automatically caches downloaded CSV data to avoid redundant API calls
- **Analysis Detection**: Only processes tickers with new data since last VPA analysis
- **Resume Capability**: Can resume interrupted VPA processing sessions

### Resource Management
- **Memory Efficient**: Processes tickers individually to minimize RAM usage
- **Network Throttling**: Built-in delays to respect API rate limits
- **Error Recovery**: Graceful handling of network issues and API errors

---

## Vietnamese VPA Methodology for Global Markets

### Core VPA Concepts Applied to US/Crypto
- **Volume Price Analysis**: Wyckoff methodology adapted for global markets
- **Vietnamese Terminology**: Professional financial Vietnamese adapted for international assets
- **Signal Classification**: Same VPA signals (SOS, SOW, No Supply, etc.) applied to USD-denominated assets
- **Market Context**: Global market context integrated with individual asset analysis

### Key VPA Signals for Global Markets
- **Sign of Strength (SOS)**: Bullish breakout with volume confirmation
- **Sign of Weakness (SOW)**: Bearish breakdown with volume
- **No Supply**: Low volume pullback indicating strength
- **Effort to Rise**: High volume advance with good price progress
- **Effort to Fall**: High volume decline for assessment

---

## Error Handling & Troubleshooting

### Common Issues
1. **Missing API Data**: Some tickers may not be available on MSN source
2. **Network Timeouts**: Built-in retry logic handles temporary network issues
3. **CSV File Conflicts**: Smart caching prevents data corruption
4. **VPA Processing Errors**: Detailed logs in `/tmp/vpa_processing_us_crypto_*.log`

### Debug Mode
```bash
# Enable detailed logging for troubleshooting
uv run main_process_vpa_us_crypto.py --debug --verbose
```

### Log Files
- **VPA Processing**: `/tmp/vpa_processing_us_crypto_*.log`
- **Performance Metrics**: Real-time speedup and progress reporting
- **Error Detection**: Automatic detection and reporting of failed analyses

---

## Environment Setup

### Required Environment Variable
```bash
export ACCEPT_TC="tôi đồng ý"
```

### Dependencies
All dependencies are managed through the main `requirements.txt` file. The US/crypto pipeline uses the same core libraries as the Vietnamese pipeline:
- `vnstock`: For global market data access
- `pandas`: Data processing and analysis
- `mplfinance`: Professional candlestick chart generation
- `matplotlib`: Chart customization and saving

---

## Integration with Main Pipeline

The US & Crypto pipeline is designed to work alongside the original Vietnamese pipeline:

### Separate Data Paths
- **US/Crypto**: `market_data_us_crypto/`, `reports_us_crypto/`, `vpa_data_us_crypto/`  
- **Vietnamese**: `market_data/`, `reports/`, `vpa_data/`
- **No conflicts**: Both pipelines can run simultaneously

### Shared AI Resources
- Both pipelines can use the same Claude/Gemini AI agents
- Task protocols are adapted but use similar methodologies
- VPA analysis quality standards are consistent

### Combined Analysis
- Run both pipelines for comprehensive global + Vietnamese market coverage
- Compare VPA signals across different market regions
- Identify global market correlation patterns

---

## Best Practices

### Performance Optimization
1. **Start with 4 workers** and adjust based on system performance
2. **Use Gemini for large batches** (better parallel processing)
3. **Monitor system resources** when using high worker counts
4. **Use weekly analysis** for longer-term trend identification

### Data Quality
1. **Always run VPA verification** using task protocols
2. **Cross-reference USD pricing** between different data sources
3. **Monitor API rate limits** to avoid service interruptions
4. **Regular cache cleanup** to prevent disk space issues

### Analysis Workflow
1. **Daily routine**: `main_us_crypto.py` → `main_process_vpa_us_crypto.py` → `merge_vpa_us_crypto.py`
2. **Weekly deep dive**: Add `--week` flag to all commands
3. **Quality control**: Use `tasks/CHECK_HOLD_us_crypto.md` protocol for verification
4. **Portfolio management**: Follow `tasks/DAILY_HOLD_us_crypto.md` protocol

---

## Advanced Usage

### Custom Asset Lists
Modify `TICKERS_US.csv` and `TICKERS_CRYPTO.csv` to analyze different assets:
```csv
ticker
DJI
INX
BTC
ETH
COMP
```

### Asset Class Customization
Update `ticker_group_us_crypto.json` to create custom asset groupings:
```json
{
    "MAJOR_INDICES": ["DJI", "INX"],
    "GROWTH_INDICES": ["COMP", "RUT"], 
    "MAJOR_CRYPTO": ["BTC", "ETH"]
}
```

### Portfolio Analysis Integration
Use the portfolio management protocols to:
1. Track US index and crypto positions
2. Calculate USD-denominated P&L
3. Apply VPA methodology to position management
4. Generate diversification recommendations across asset classes

---

This README provides comprehensive guidance for using the AIPriceAction US & Cryptocurrency pipeline. The system brings professional Vietnamese VPA methodology to global markets, providing institutional-quality analysis with Vietnamese financial terminology adapted for international assets.