#!/usr/bin/env python3
"""
Comprehensive Leadership Score Calculator for Vietnamese Stock Market Sectors

This script calculates leadership scores for all eligible sectors using the methodology:
- Base Period Analysis (Common consolidation phases)
- Leadership Score = (VPA Story Score × 0.6) + (Relative Performance Score × 0.4)
- VPA Story Score (0-100 points) based on Wyckoff narrative quality
- Relative Performance Score: Percentage price change from base period start
- Confidence Score (0-100%) based on signal clarity and risk assessment

Date: 2025-07-18
"""

import json
import pandas as pd
import os
from datetime import datetime
import numpy as np
from typing import Dict, List, Tuple, Optional
import re

class LeadershipScoreCalculator:
    def __init__(self, base_dir: str = "/Volumes/data/workspace/aipriceaction"):
        self.base_dir = base_dir
        self.market_data_dir = os.path.join(base_dir, "market_data")
        self.vpa_data_dir = os.path.join(base_dir, "vpa_data")
        
        # Load sector groupings
        with open(os.path.join(base_dir, "ticker_group.json"), 'r', encoding='utf-8') as f:
            self.ticker_groups = json.load(f)
        
        # Base period definitions
        self.base_periods = {
            "early_2025": ("2025-01-02", "2025-03-31"),
            "mid_2025": ("2025-04-01", "2025-05-31"),
            "recent_breakout": ("2025-06-01", "2025-07-18")
        }
        
        # Priority sectors as specified
        self.priority_sectors = [
            "NGAN_HANG",
            "BAT_DONG_SAN", 
            "CHUNG_KHOAN",
            "THUC_PHAM",
            "BAN_LE"
        ]
        
        # VPA signal scoring
        self.vpa_signal_scores = {
            # Bullish signals
            "SOS": 90,
            "SIGN OF STRENGTH": 90,
            "EFFORT TO RISE": 75,
            "NO SUPPLY": 80,
            "TEST FOR SUPPLY": 70,
            "TEST FOR DEMAND": 65,
            "SUCCESSFUL TEST": 75,
            
            # Bearish signals  
            "SOW": 20,
            "SIGN OF WEAKNESS": 20,
            "EFFORT TO FALL": 25,
            "NO DEMAND": 30,
            "UP-THRUST": 15,
            "UPTHRUST": 15,
            "SELLING CLIMAX": 10,
            
            # Neutral/Accumulation
            "ACCUMULATION": 60,
            "DISTRIBUTION": 25,
            "GIẰNG CO": 50,
            "SIDEWAYS": 50,
            "TÍCH LŨY": 60
        }
    
    def load_price_data(self, ticker: str) -> Optional[pd.DataFrame]:
        """Load price data for a ticker"""
        try:
            file_path = os.path.join(self.market_data_dir, f"{ticker}_2025-01-02_to_2025-07-18.csv")
            if not os.path.exists(file_path):
                return None
                
            df = pd.read_csv(file_path)
            df['time'] = pd.to_datetime(df['time'])
            df = df.set_index('time').sort_index()
            return df
        except Exception as e:
            print(f"Error loading data for {ticker}: {e}")
            return None
    
    def load_vpa_analysis(self, ticker: str) -> str:
        """Load VPA analysis for a ticker"""
        try:
            file_path = os.path.join(self.vpa_data_dir, f"{ticker}.md")
            if not os.path.exists(file_path):
                return ""
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            print(f"Error loading VPA analysis for {ticker}: {e}")
            return ""
    
    def calculate_performance_score(self, ticker: str, start_date: str = "2025-01-02", 
                                   end_date: str = "2025-07-18") -> float:
        """Calculate relative performance score (percentage change)"""
        df = self.load_price_data(ticker)
        if df is None or len(df) == 0:
            return 0.0
            
        try:
            start_price = df.loc[df.index >= start_date, 'close'].iloc[0]
            end_price = df.loc[df.index <= end_date, 'close'].iloc[-1]
            
            performance = ((end_price - start_price) / start_price) * 100
            return round(performance, 2)
        except Exception as e:
            print(f"Error calculating performance for {ticker}: {e}")
            return 0.0
    
    def extract_vpa_signals(self, vpa_content: str) -> List[str]:
        """Extract VPA signals from analysis content"""
        signals = []
        
        # Pattern to find VPA signals in analysis
        patterns = [
            r'\*\*([^*]+)\*\*',  # **Signal Name**
            r'tín hiệu\s+([^.]+)',  # Vietnamese signal descriptions
            r'signal\s+([^.]+)',   # English signal descriptions
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, vpa_content, re.IGNORECASE)
            for match in matches:
                signal = match.strip().upper()
                if any(key in signal for key in self.vpa_signal_scores.keys()):
                    signals.append(signal)
        
        return signals
    
    def calculate_vpa_story_score(self, ticker: str) -> Tuple[float, str]:
        """Calculate VPA story score based on signal quality and narrative"""
        vpa_content = self.load_vpa_analysis(ticker)
        if not vpa_content:
            return 30.0, "No VPA analysis available"
        
        signals = self.extract_vpa_signals(vpa_content)
        if not signals:
            return 40.0, "No clear VPA signals detected"
        
        # Score based on signal quality
        total_score = 0
        signal_count = 0
        narrative_quality = 0
        
        for signal in signals[-5:]:  # Focus on last 5 signals
            for key, score in self.vpa_signal_scores.items():
                if key in signal:
                    total_score += score
                    signal_count += 1
                    break
        
        if signal_count == 0:
            return 40.0, "No recognizable VPA signals"
        
        base_score = total_score / signal_count
        
        # Narrative quality bonuses
        content_lower = vpa_content.lower()
        
        # Perfect Wyckoff story elements
        if "accumulation" in content_lower and "shakeout" in content_lower:
            narrative_quality += 10
        if "sos" in content_lower and "test" in content_lower:
            narrative_quality += 10
        if "sign of strength" in content_lower:
            narrative_quality += 10
        if "no supply" in content_lower:
            narrative_quality += 5
        
        # Penalties for negative signals
        if "sow" in content_lower or "sign of weakness" in content_lower:
            narrative_quality -= 15
        if "up-thrust" in content_lower or "upthrust" in content_lower:
            narrative_quality -= 10
        if "no demand" in content_lower:
            narrative_quality -= 5
        
        final_score = min(100, max(0, base_score + narrative_quality))
        
        # Generate narrative description
        if final_score >= 90:
            narrative = "Perfect multi-stage Wyckoff story"
        elif final_score >= 70:
            narrative = "Strong story with minor imperfections"
        elif final_score >= 50:
            narrative = "Developing story with mixed signals"
        else:
            narrative = "Weak or unclear VPA narrative"
        
        return final_score, narrative
    
    def calculate_confidence_score(self, ticker: str, vpa_score: float, 
                                  performance_score: float) -> float:
        """Calculate confidence score based on signal clarity and risk"""
        vpa_content = self.load_vpa_analysis(ticker)
        confidence = 50.0  # Base confidence
        
        # VPA quality impact
        if vpa_score >= 90:
            confidence += 30
        elif vpa_score >= 70:
            confidence += 20
        elif vpa_score >= 50:
            confidence += 10
        else:
            confidence -= 10
        
        # Performance consistency
        if performance_score > 20:
            confidence += 15
        elif performance_score > 10:
            confidence += 10
        elif performance_score > 0:
            confidence += 5
        else:
            confidence -= 15
        
        # Recent signal clarity
        if vpa_content:
            recent_content = vpa_content[-1000:]  # Last 1000 characters
            if any(signal in recent_content.lower() for signal in ["sos", "sign of strength", "effort to rise"]):
                confidence += 15
            elif any(signal in recent_content.lower() for signal in ["sow", "sign of weakness", "no demand"]):
                confidence -= 15
        
        return min(100, max(0, confidence))
    
    def calculate_ticker_leadership_score(self, ticker: str) -> Dict:
        """Calculate complete leadership score for a ticker"""
        # Get VPA story score
        vpa_score, vpa_narrative = self.calculate_vpa_story_score(ticker)
        
        # Get relative performance score
        performance_score = self.calculate_performance_score(ticker)
        
        # Calculate leadership score
        leadership_score = (vpa_score * 0.6) + (performance_score * 0.4)
        
        # Calculate confidence score
        confidence_score = self.calculate_confidence_score(ticker, vpa_score, performance_score)
        
        return {
            "ticker": ticker,
            "leadership_score": round(leadership_score, 2),
            "vpa_score": round(vpa_score, 2),
            "performance_score": performance_score,
            "confidence_score": round(confidence_score, 2),
            "vpa_narrative": vpa_narrative
        }
    
    def calculate_sector_leadership(self, sector_name: str, tickers: List[str]) -> Dict:
        """Calculate leadership scores for an entire sector"""
        sector_results = []
        valid_tickers = 0
        
        print(f"\nProcessing sector: {sector_name} ({len(tickers)} tickers)")
        
        for ticker in tickers:
            result = self.calculate_ticker_leadership_score(ticker)
            if result["performance_score"] != 0:  # Valid data
                sector_results.append(result)
                valid_tickers += 1
                print(f"  {ticker}: Leadership={result['leadership_score']:.1f}, VPA={result['vpa_score']:.1f}, Performance={result['performance_score']:.1f}%")
        
        if not sector_results:
            return {
                "sector": sector_name,
                "status": "No valid data",
                "top_3": [],
                "breadth": 0,
                "classification": "Cannot analyze"
            }
        
        # Sort by leadership score
        sector_results.sort(key=lambda x: x["leadership_score"], reverse=True)
        
        # Calculate trend breadth
        positive_performers = len([r for r in sector_results if r["performance_score"] > 0])
        breadth = (positive_performers / len(sector_results)) * 100
        
        # Classify sector health
        avg_performance = np.mean([r["performance_score"] for r in sector_results])
        
        if breadth > 70 and avg_performance > 5:
            classification = "Dẫn Dắt Đồng Thuận"
        elif breadth < 70 and avg_performance > 5:
            classification = "Dẫn Dắt Phân Hóa"
        elif abs(avg_performance) < 5:
            classification = "Đang Tích Lũy"
        else:
            classification = "Yếu/Phân Phối"
        
        return {
            "sector": sector_name,
            "ticker_count": len(tickers),
            "valid_tickers": valid_tickers,
            "top_3": sector_results[:3],
            "all_tickers": sector_results,
            "breadth": round(breadth, 1),
            "avg_performance": round(avg_performance, 2),
            "classification": classification
        }
    
    def generate_comprehensive_report(self) -> Dict:
        """Generate comprehensive leadership analysis for all sectors"""
        print("Starting Comprehensive Leadership Score Calculation...")
        print(f"Base Period: 2025-01-02 to 2025-07-18")
        print(f"Total Sectors: {len(self.ticker_groups)}")
        
        all_results = {}
        
        # Process priority sectors first
        priority_results = {}
        for sector in self.priority_sectors:
            if sector in self.ticker_groups:
                result = self.calculate_sector_leadership(sector, self.ticker_groups[sector])
                priority_results[sector] = result
                all_results[sector] = result
        
        # Process remaining sectors
        for sector, tickers in self.ticker_groups.items():
            if sector not in self.priority_sectors:
                result = self.calculate_sector_leadership(sector, tickers)
                all_results[sector] = result
        
        # Rank sectors by average leadership score of top 3
        sector_rankings = []
        for sector, data in all_results.items():
            if data["top_3"]:
                avg_top3_score = np.mean([t["leadership_score"] for t in data["top_3"]])
                sector_rankings.append({
                    "sector": sector,
                    "avg_leadership_score": round(avg_top3_score, 2),
                    "classification": data["classification"],
                    "breadth": data["breadth"]
                })
        
        sector_rankings.sort(key=lambda x: x["avg_leadership_score"], reverse=True)
        
        return {
            "calculation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "methodology": {
                "base_period": "2025-01-02 to 2025-07-18",
                "leadership_formula": "VPA Story Score (60%) + Relative Performance Score (40%)",
                "vpa_scoring": "0-100 points based on Wyckoff narrative quality",
                "performance_scoring": "Percentage price change from base period start",
                "confidence_scoring": "0-100% based on signal clarity and risk assessment"
            },
            "sector_rankings": sector_rankings,
            "priority_sectors": priority_results,
            "all_sectors": all_results,
            "summary": {
                "total_sectors_analyzed": len(all_results),
                "sectors_with_data": len([s for s in all_results.values() if s.get("valid_tickers", 0) > 0]),
                "top_sector": sector_rankings[0]["sector"] if sector_rankings else "None"
            }
        }
    
    def save_results(self, results: Dict, filename: str = "leadership_analysis_results.json"):
        """Save results to JSON file"""
        filepath = os.path.join(self.base_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {filepath}")
    
    def generate_markdown_report(self, results: Dict) -> str:
        """Generate markdown report of leadership analysis"""
        report = f"""# Comprehensive Leadership Score Analysis
Generated: {results['calculation_date']}

## Executive Summary
- **Total Sectors Analyzed**: {results['summary']['total_sectors_analyzed']}
- **Sectors with Valid Data**: {results['summary']['sectors_with_data']}
- **Top Performing Sector**: {results['summary']['top_sector']}

## Methodology
- **Base Period**: {results['methodology']['base_period']}
- **Leadership Formula**: {results['methodology']['leadership_formula']}
- **VPA Scoring**: {results['methodology']['vpa_scoring']}
- **Performance Scoring**: {results['methodology']['performance_scoring']}
- **Confidence Scoring**: {results['methodology']['confidence_scoring']}

## Sector Rankings (by Average Top 3 Leadership Score)

| Rank | Sector | Avg Leadership Score | Classification | Breadth |
|------|--------|---------------------|----------------|---------|
"""
        
        for i, sector in enumerate(results['sector_rankings'], 1):
            report += f"| {i} | {sector['sector']} | {sector['avg_leadership_score']} | {sector['classification']} | {sector['breadth']}% |\n"
        
        report += "\n## Priority Sectors Detailed Analysis\n\n"
        
        for sector_name, data in results['priority_sectors'].items():
            report += f"### {sector_name}\n"
            report += f"- **Classification**: {data['classification']}\n"
            report += f"- **Breadth**: {data['breadth']}% ({data['valid_tickers']}/{data['ticker_count']} tickers)\n"
            report += f"- **Average Performance**: {data['avg_performance']}%\n\n"
            
            if data['top_3']:
                report += "**Top 3 Leaders:**\n\n"
                for i, ticker in enumerate(data['top_3'], 1):
                    report += f"{i}. **{ticker['ticker']}**\n"
                    report += f"   - Leadership Score: {ticker['leadership_score']}\n"
                    report += f"   - VPA Score: {ticker['vpa_score']}/100\n"
                    report += f"   - Performance: {ticker['performance_score']}%\n"
                    report += f"   - Confidence: {ticker['confidence_score']}%\n"
                    report += f"   - VPA Narrative: {ticker['vpa_narrative']}\n\n"
            
            report += "---\n\n"
        
        return report

def main():
    """Main execution function"""
    calculator = LeadershipScoreCalculator()
    
    # Generate comprehensive analysis
    results = calculator.generate_comprehensive_report()
    
    # Save JSON results
    calculator.save_results(results)
    
    # Generate and save markdown report
    markdown_report = calculator.generate_markdown_report(results)
    
    report_path = os.path.join(calculator.base_dir, "leadership_analysis_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(markdown_report)
    
    print(f"\nMarkdown report saved to: {report_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("LEADERSHIP ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"Total Sectors Analyzed: {results['summary']['total_sectors_analyzed']}")
    print(f"Top Performing Sector: {results['summary']['top_sector']}")
    
    print("\nTop 5 Sectors by Leadership Score:")
    for i, sector in enumerate(results['sector_rankings'][:5], 1):
        print(f"{i}. {sector['sector']}: {sector['avg_leadership_score']} ({sector['classification']})")

if __name__ == "__main__":
    main()