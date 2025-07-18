#!/usr/bin/env python3
"""
Utility to validate ticker group classifications in PLAN.md against GROUP.md
"""

import os
import re

def load_group_mappings(base_dir):
    """Load ticker-to-group mappings from GROUP.md"""
    group_file = os.path.join(base_dir, 'GROUP.md')
    mappings = {}
    
    if not os.path.exists(group_file):
        return mappings
    
    with open(group_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the markdown table
    lines = content.strip().split('\n')
    for line in lines:
        if '|' in line and 'Ngành' not in line and ':--' not in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3 and parts[1] and parts[2]:
                sector = parts[1]
                tickers_str = parts[2]
                
                # Parse tickers
                tickers = [ticker.strip() for ticker in tickers_str.split(',')]
                for ticker in tickers:
                    if ticker:
                        mappings[ticker] = sector
    
    return mappings

def extract_ticker_classifications_from_plan(plan_file):
    """Extract ticker classifications from PLAN.md"""
    if not os.path.exists(plan_file):
        return {}
    
    with open(plan_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match ticker classifications like [**VHM**](#VHM) (Bất Động Sản)
    pattern = r'\[?\*\*([A-Z]+)\*\*\]?[^(]*\(([^)]+)\)'
    matches = re.findall(pattern, content)
    
    classifications = {}
    for ticker, sector in matches:
        # Clean up the sector name
        sector = sector.strip()
        if sector and not sector.startswith('#'):
            classifications[ticker] = sector
    
    return classifications

def vietnamese_sector_mappings():
    """Mapping from GROUP.md English names to Vietnamese names"""
    return {
        'BAN_LE': 'Bán Lẻ',
        'BAO_HIEM': 'Bảo Hiểm',
        'BAT_DONG_SAN': 'Bất Động Sản',
        'BAT_DONG_SAN_KCN': 'BĐS KCN',
        'CAO_SU': 'Cao Su',
        'CHUNG_KHOAN': 'Chứng Khoán',
        'CONG_NGHE': 'Công Nghệ',
        'DAU_KHI': 'Dầu Khí',
        'DAU_TU_CONG': 'Đầu Tư Công',
        'DET_MAY': 'Dệt May',
        'HANG_KHONG': 'Hàng Không',
        'HOA_CHAT': 'Hóa Chất',
        'KHAI_KHOANG': 'Khai Khoáng',
        'NANG_LUONG': 'Năng Lượng',
        'NGAN_HANG': 'Ngân Hàng',
        'NHUA': 'Nhựa',
        'NONG_NGHIEP': 'Nông Nghiệp',
        'OTHERS': 'Khác',
        'PENNY': 'Penny',
        'SUC_KHOE': 'Sức Khỏe',
        'THEP': 'Thép',
        'THUC_PHAM': 'Thực Phẩm',
        'THUY_SAN': 'Thuỷ Sản',
        'VAN_TAI': 'Vận Tải',
        'VLXD': 'VLXD',
        'XAY_DUNG': 'Xây Dựng',
        'XAY_LAP_DIEN': 'Xây Lắp Điện'
    }

def main():
    base_dir = '/Volumes/data/workspace/aipriceaction'
    plan_file = os.path.join(base_dir, 'PLAN.md')
    
    # Load mappings
    group_mappings = load_group_mappings(base_dir)
    plan_classifications = extract_ticker_classifications_from_plan(plan_file)
    vietnamese_mappings = vietnamese_sector_mappings()
    
    print("=== GROUP CLASSIFICATION VALIDATION ===")
    print(f"Total tickers in GROUP.md: {len(group_mappings)}")
    print(f"Total tickers in PLAN.md: {len(plan_classifications)}")
    
    # Debug: Show some GROUP.md entries
    if len(group_mappings) == 0:
        print("DEBUG: No mappings found in GROUP.md")
        group_file = os.path.join(base_dir, 'GROUP.md')
        with open(group_file, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"First 500 chars of GROUP.md:\n{content[:500]}")
    
    print()
    
    # Check for mismatches
    mismatches = []
    missing_from_group = []
    
    for ticker, plan_sector in plan_classifications.items():
        if ticker not in group_mappings:
            missing_from_group.append(ticker)
        else:
            group_sector_code = group_mappings[ticker]
            expected_vietnamese = vietnamese_mappings.get(group_sector_code, group_sector_code)
            
            if plan_sector != expected_vietnamese:
                mismatches.append({
                    'ticker': ticker,
                    'plan_sector': plan_sector,
                    'correct_sector': expected_vietnamese,
                    'group_code': group_sector_code
                })
    
    # Report results
    if mismatches:
        print("SECTOR MISMATCHES FOUND:")
        for mismatch in mismatches:
            print(f"  {mismatch['ticker']}: '{mismatch['plan_sector']}' → '{mismatch['correct_sector']}'")
        print()
    else:
        print("✓ No sector mismatches found!")
        print()
    
    if missing_from_group:
        print("TICKERS NOT FOUND IN GROUP.md:")
        for ticker in missing_from_group:
            print(f"  {ticker} (classified as '{plan_classifications[ticker]}' in PLAN.md)")
        print()
    else:
        print("✓ All PLAN.md tickers found in GROUP.md!")
        print()
    
    # Summary
    print("SUMMARY:")
    print(f"- Sector mismatches: {len(mismatches)}")
    print(f"- Missing from GROUP.md: {len(missing_from_group)}")
    
    if len(mismatches) == 0 and len(missing_from_group) == 0:
        print("✓ All ticker classifications are correct!")
    else:
        print("⚠ Action required: Fix the identified issues")
    
    return len(mismatches) + len(missing_from_group) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)