# Utilities Directory

This directory contains supporting scripts that are not part of the core daily/weekly workflow but provide useful functionality for development and maintenance.

## Scripts

### `split_vpa.py`
- **Purpose**: Splits combined VPA.md files into individual ticker files
- **Usage**: `python split_vpa.py [--week]`
- **Note**: Originally used to create the vpa_data/ structure. Now mainly useful for converting existing VPA files to individual format.

### `verify_vpa.py` 
- **Purpose**: Verifies VPA analysis accuracy against actual market data
- **Usage**: `python verify_vpa.py`
- **Output**: Detailed accuracy report comparing VPA predictions with CSV data
- **Use case**: Quality assurance and improving VPA analysis accuracy

### `test_vpa_scanner.py`
- **Purpose**: Tests the VPA dividend scanner functionality
- **Usage**: `python test_vpa_scanner.py`
- **Use case**: Development and debugging of dividend detection system

### `verify_dividends.py` (Legacy)
- **Purpose**: Original dividend verification script
- **Status**: Superseded by `vpa_dividend_scanner.py`
- **Note**: Kept for reference and fallback if needed

### `get_fund_data.py`
- **Purpose**: Downloads Vietnamese fund data and reports
- **Usage**: `python get_fund_data.py`
- **Output**: Fund performance data in funds_data/ directory
- **Note**: Separate from main stock analysis workflow

## Usage Notes

- These scripts are not part of the automated GitHub Actions workflows
- They can be run manually for development, testing, or one-time tasks
- Some may require additional dependencies beyond the main requirements.txt