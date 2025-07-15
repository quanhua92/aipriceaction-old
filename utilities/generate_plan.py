#!/usr/bin/env python3
"""
PLAN.md Generator for Daily Planning Protocol

This utility generates the complete PLAN.md file using verified ticker states and fact sheets
according to the VPA-Strategist methodology defined in tasks/DAILY_PLAN.md.

Usage:
    python generate_plan.py
    
Input:
    utilities/ticker_states.json - Final ticker state assessments
    utilities/fact_sheets.json - Verified fact sheets
    REPORT.md, REPORT_week.md - For VNINDEX analysis
    
Output:
    PLAN.md - Complete daily trading plan
"""

import json
import re
from datetime import datetime

def load_ticker_states():
    """Load ticker states from JSON file"""
    try:
        with open('utilities/ticker_states.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: utilities/ticker_states.json not found. Run assess_ticker_states.py first.")
        return {}

def load_fact_sheets():
    """Load fact sheets from JSON file"""
    try:
        with open('utilities/fact_sheets.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: utilities/fact_sheets.json not found. Run generate_fact_sheets.py first.")
        return {}

def generate_vnindex_analysis():
    """Generate VNINDEX analysis section"""
    try:
        # Read VNINDEX context from reports
        with open('REPORT.md', 'r', encoding='utf-8') as f:
            daily_report = f.read()
        
        with open('REPORT_week.md', 'r', encoding='utf-8') as f:
            weekly_report = f.read()
        
        # Extract VNINDEX sections
        vnindex_daily = re.search(r'### VNINDEX\n(.*?)(?=### [A-Z]|\Z)', daily_report, re.DOTALL)
        vnindex_weekly = re.search(r'### VNINDEX\n(.*?)(?=### [A-Z]|\Z)', weekly_report, re.DOTALL)
        
        daily_context = vnindex_daily.group(1).strip() if vnindex_daily else "Không có dữ liệu VNINDEX hàng ngày"
        weekly_context = vnindex_weekly.group(1).strip() if vnindex_weekly else "Không có dữ liệu VNINDEX hàng tuần"
        
        # Generate analysis
        analysis = f"""## 1. Phân Tích Trạng Thái VNINDEX & Chiến Lược

![Weekly Chart](reports_week/VNINDEX/VNINDEX_candlestick_chart.png) | ![Daily Chart](reports/VNINDEX/VNINDEX_candlestick_chart.png)

**Bối Cảnh Tuần**: {weekly_context[:300]}...

**Hành Động Gần Đây**: {daily_context[:300]}...

**Vùng Tốt Nhất Để Gia Tăng Tỷ Trọng**: Theo dõi mức hỗ trợ quan trọng và tín hiệu xác nhận từ phân tích VPA."""
        
        return analysis
    
    except Exception as e:
        return f"""## 1. Phân Tích Trạng Thái VNINDEX & Chiến Lược

![Weekly Chart](reports_week/VNINDEX/VNINDEX_candlestick_chart.png) | ![Daily Chart](reports/VNINDEX/VNINDEX_candlestick_chart.png)

**Bối Cảnh Tuần**: Đang cập nhật phân tích tuần.

**Hành Động Gần Đây**: Đang cập nhật phân tích hàng ngày.

**Vùng Tốt Nhất Để Gia Tăng Tỷ Trọng**: Theo dõi mức hỗ trợ quan trọng và tín hiệu xác nhận từ phân tích VPA."""

def generate_top_list(ticker_states, fact_sheets):
    """Generate Top List section"""
    top_tickers = []
    
    for data in ticker_states['summary']['Top List']:
        ticker = data['ticker']
        ticker_info = {
            'ticker': ticker,
            'confidence': data['confidence'],
            'reasoning': data['reasoning'],
            'fact_sheet': fact_sheets.get(ticker, {})
        }
        top_tickers.append(ticker_info)
    
    # Sort by confidence score (descending)
    top_tickers.sort(key=lambda x: x['confidence'], reverse=True)
    
    content = "## 2. Top 26 Cơ Hội Giao Dịch\n\n"
    
    for i, ticker_info in enumerate(top_tickers, 1):
        ticker = ticker_info['ticker']
        confidence = ticker_info['confidence']
        industry = ticker_info['fact_sheet'].get('industry_group', 'Unknown')
        industry_status = ticker_info['fact_sheet'].get('industry_status', 'Unknown')
        
        content += f"{i}. [**{ticker}**](#{ticker}) ({industry} - {industry_status}) - (Độ tin cậy: {confidence}%)\n"
    
    return content

def generate_potential_list(ticker_states, fact_sheets):
    """Generate Potential List section"""
    potential_tickers = []
    
    for data in ticker_states['summary']['Potential List']:
        ticker = data['ticker']
        ticker_info = {
            'ticker': ticker,
            'confidence': data['confidence'],
            'reasoning': data['reasoning'],
            'fact_sheet': fact_sheets.get(ticker, {})
        }
        potential_tickers.append(ticker_info)
    
    # Sort by confidence score (descending)
    potential_tickers.sort(key=lambda x: x['confidence'], reverse=True)
    
    content = "## 3. Danh Sách Cổ Phiếu Tiềm Năng\n\n"
    
    for i, ticker_info in enumerate(potential_tickers, 1):
        ticker = ticker_info['ticker']
        confidence = ticker_info['confidence']
        reasoning = ticker_info['reasoning']
        industry = ticker_info['fact_sheet'].get('industry_group', 'Unknown')
        daily_signal = ticker_info['fact_sheet'].get('most_recent_daily_signal', {}).get('signal', 'N/A')
        daily_date = ticker_info['fact_sheet'].get('most_recent_daily_signal', {}).get('date', 'N/A')
        
        content += f"{i}. [**{ticker}**](#{ticker}) ({industry}) - (Độ tin cậy: {confidence}%)\n"
        content += f"   - **Lý do**: {reasoning}\n"
        content += f"   - **Tín hiệu gần đây**: {daily_signal} ({daily_date})\n\n"
    
    return content

def generate_downgraded_list(ticker_states, fact_sheets):
    """Generate Downgraded List section"""
    downgraded_tickers = []
    
    for data in ticker_states['summary']['Downgraded']:
        ticker = data['ticker']
        ticker_info = {
            'ticker': ticker,
            'confidence': data['confidence'],
            'reasoning': data['reasoning'],
            'fact_sheet': fact_sheets.get(ticker, {})
        }
        downgraded_tickers.append(ticker_info)
    
    if not downgraded_tickers:
        return "## 4. Danh Sách Cổ Phiếu Bị Hạ Ưu Tiên\n\n*Không có cổ phiếu nào trong danh sách này.*\n\n"
    
    content = "## 4. Danh Sách Cổ Phiếu Bị Hạ Ưu Tiên\n\n"
    
    for i, ticker_info in enumerate(downgraded_tickers, 1):
        ticker = ticker_info['ticker']
        confidence = ticker_info['confidence']
        reasoning = ticker_info['reasoning']
        
        content += f"{i}. [**{ticker}**](#{ticker}) - (Độ tin cậy: {confidence}%)\n"
        content += f"   - **Lý do hạ ưu tiên**: {reasoning}\n\n"
    
    return content

def generate_detailed_analysis(ticker_states, fact_sheets):
    """Generate detailed analysis for Top List tickers"""
    top_tickers = [data['ticker'] for data in ticker_states['summary']['Top List']]
    
    if not top_tickers:
        return "## 5. Phân Tích Chi Tiết\n\n*Không có cổ phiếu nào trong Top List.*\n\n"
    
    content = "## 5. Phân Tích Chi Tiết\n\n"
    
    for ticker in sorted(top_tickers):
        fact_sheet = fact_sheets.get(ticker, {})
        assessment = ticker_states['assessments'].get(ticker, {})
        
        daily_signal = fact_sheet.get('most_recent_daily_signal', {}).get('signal', 'N/A')
        daily_date = fact_sheet.get('most_recent_daily_signal', {}).get('date', 'N/A')
        weekly_signal = fact_sheet.get('weekly_context', {}).get('signal', 'N/A')
        weekly_date = fact_sheet.get('weekly_context', {}).get('week_ending_date', 'N/A')
        industry = fact_sheet.get('industry_group', 'Unknown')
        industry_status = fact_sheet.get('industry_status', 'Unknown')
        confidence = assessment.get('confidence', 0)
        reasoning = assessment.get('reasoning', 'N/A')
        
        content += f"### {ticker}\n\n"
        content += f"- ![Weekly Chart](reports_week/{ticker}/{ticker}_candlestick_chart.png) | ![Daily Chart](reports/{ticker}/{ticker}_candlestick_chart.png) | [View Report](REPORT.md#{ticker})\n"
        content += f"- **Phân Tích Cốt Lõi:**\n"
        content += f"  - **Weekly VPA Narrative:** Tuần kết thúc {weekly_date} có tín hiệu {weekly_signal}\n"
        content += f"  - **Daily VPA Narrative:** Ngày {daily_date} có tín hiệu {daily_signal}\n"
        content += f"  - **Industry Context:** Ngành {industry} ở trạng thái {industry_status}\n"
        content += f"  - **Synthesis:** {reasoning}\n"
        content += f"- **Độ Tin Cậy:** {confidence}%\n"
        content += f"- **Vùng Tham Gia Tốt Nhất:** Theo dõi mức hỗ trợ kỹ thuật và xác nhận từ volume\n\n"
    
    return content

def generate_audit_log(ticker_states):
    """Generate audit log section"""
    changes = ticker_states['changes']
    
    content = "## 6. Nhật Ký Thay Đổi Kế Hoạch (AUDIT LOG)\n\n"
    
    # Promoted to Top List
    if changes['promoted_to_top']:
        content += "### Cổ Phiếu Được Nâng Lên \"Top 26\":\n"
        for change in changes['promoted_to_top']:
            ticker = change['ticker']
            prev_state = change['previous_state']
            reasoning = change['reasoning']
            daily_signal = change['daily_signal']
            daily_date = change['daily_date']
            weekly_signal = change['weekly_signal']
            weekly_date = change['weekly_date']
            
            content += f"- **{ticker}**: Từ `{prev_state}`. Lý do: {reasoning}. "
            content += f"Tín hiệu ngày {daily_date}: {daily_signal}, "
            content += f"tuần kết thúc {weekly_date}: {weekly_signal}.\n"
        content += "\n"
    
    # Added to Potential List
    if changes['added_to_potential']:
        content += "### Cổ Phiếu Được Thêm Vào \"Potential List\":\n"
        for change in changes['added_to_potential'][:10]:  # Show first 10
            ticker = change['ticker']
            reasoning = change['reasoning']
            daily_signal = change['daily_signal']
            daily_date = change['daily_date']
            
            content += f"- **{ticker}**: Từ `Unlisted`. Lý do: {reasoning}. "
            content += f"Tín hiệu ngày {daily_date}: {daily_signal}.\n"
        
        if len(changes['added_to_potential']) > 10:
            content += f"- *... và {len(changes['added_to_potential']) - 10} cổ phiếu khác*\n"
        content += "\n"
    
    # Moved to Downgraded
    if changes['moved_to_downgraded']:
        content += "### Cổ Phiếu Bị Giáng Xuống \"Hạ Ưu Tiên\":\n"
        for change in changes['moved_to_downgraded']:
            ticker = change['ticker']
            prev_state = change['previous_state']
            reasoning = change['reasoning']
            daily_signal = change['daily_signal']
            daily_date = change['daily_date']
            
            content += f"- **{ticker}**: Từ `{prev_state}`. Lý do: {reasoning}. "
            content += f"Tín hiệu ngày {daily_date}: {daily_signal}.\n"
        content += "\n"
    
    # Removed to Unlisted
    if changes['removed_to_unlisted']:
        content += "### Cổ Phiếu Bị Loại Bỏ Hoàn Toàn:\n"
        for change in changes['removed_to_unlisted']:
            ticker = change['ticker']
            prev_state = change['previous_state']
            reasoning = change['reasoning']
            daily_signal = change['daily_signal']
            daily_date = change['daily_date']
            
            content += f"- **{ticker}**: Từ `{prev_state}`. Lý do: {reasoning}. "
            content += f"Tín hiệu ngày {daily_date}: {daily_signal}.\n"
        content += "\n"
    
    if not any([changes['promoted_to_top'], changes['added_to_potential'], 
                changes['moved_to_downgraded'], changes['removed_to_unlisted']]):
        content += "*Không có thay đổi trạng thái nào.*\n\n"
    
    return content

def generate_summary_stats(ticker_states):
    """Generate summary statistics"""
    summary = ticker_states['summary']
    changes = ticker_states['changes']
    
    content = "## 7. Tổng Kết\n\n"
    content += f"**Tổng số cổ phiếu được phân tích:** {ticker_states['metadata']['total_tickers']}\n\n"
    content += f"**Phân bổ trạng thái:**\n"
    content += f"- Top List: {len(summary['Top List'])} cổ phiếu\n"
    content += f"- Potential List: {len(summary['Potential List'])} cổ phiếu\n"
    content += f"- Downgraded: {len(summary['Downgraded'])} cổ phiếu\n"
    content += f"- Unlisted: {len(summary['Unlisted'])} cổ phiếu\n\n"
    
    content += f"**Thay đổi từ phiên trước:**\n"
    content += f"- Được nâng lên Top List: {len(changes['promoted_to_top'])} cổ phiếu\n"
    content += f"- Thêm vào Potential List: {len(changes['added_to_potential'])} cổ phiếu\n"
    content += f"- Hạ xuống Downgraded: {len(changes['moved_to_downgraded'])} cổ phiếu\n"
    content += f"- Loại bỏ hoàn toàn: {len(changes['removed_to_unlisted'])} cổ phiếu\n\n"
    
    content += f"**Thời gian cập nhật:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return content

def main():
    """Main function to generate PLAN.md"""
    print("Generating PLAN.md according to VPA-Strategist protocol...")
    
    # Load data
    ticker_states = load_ticker_states()
    fact_sheets = load_fact_sheets()
    
    if not ticker_states or not fact_sheets:
        return
    
    # Generate sections
    print("Generating VNINDEX analysis...")
    vnindex_analysis = generate_vnindex_analysis()
    
    print("Generating Top List...")
    top_list = generate_top_list(ticker_states, fact_sheets)
    
    print("Generating Potential List...")
    potential_list = generate_potential_list(ticker_states, fact_sheets)
    
    print("Generating Downgraded List...")
    downgraded_list = generate_downgraded_list(ticker_states, fact_sheets)
    
    print("Generating detailed analysis...")
    detailed_analysis = generate_detailed_analysis(ticker_states, fact_sheets)
    
    print("Generating audit log...")
    audit_log = generate_audit_log(ticker_states)
    
    print("Generating summary statistics...")
    summary_stats = generate_summary_stats(ticker_states)
    
    # Combine all sections
    plan_content = f"""# PLAN.md - Kế Hoạch Giao Dịch Hàng Ngày

*Được tạo tự động bởi VPA-Strategist Protocol*

{vnindex_analysis}

{top_list}

{potential_list}

{downgraded_list}

{detailed_analysis}

{audit_log}

{summary_stats}

---

*Lưu ý: Đây là phân tích dựa trên phương pháp VPA (Volume Price Analysis) và chỉ mang tính chất tham khảo. Nhà đầu tư cần tự nghiên cứu và đánh giá rủi ro trước khi đưa ra quyết định đầu tư.*
"""
    
    # Write to file
    with open('PLAN.md', 'w', encoding='utf-8') as f:
        f.write(plan_content)
    
    print("PLAN.md generated successfully!")
    print(f"Total sections: 7")
    print(f"Top List: {len(ticker_states['summary']['Top List'])} tickers")
    print(f"Potential List: {len(ticker_states['summary']['Potential List'])} tickers")
    print(f"New opportunities identified: {len(ticker_states['changes']['added_to_potential'])}")

if __name__ == "__main__":
    main()