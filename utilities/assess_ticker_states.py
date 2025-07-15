#!/usr/bin/env python3
"""
Ticker State Assessment Utility for Daily Planning Protocol

This utility processes fact sheets and applies the VPA-Strategist state transition rules
to determine the new state for each ticker according to tasks/DAILY_PLAN.md protocol.

Usage:
    python assess_ticker_states.py
    
Input:
    utilities/fact_sheets.json - Generated fact sheets from generate_fact_sheets.py
    
Output:
    utilities/ticker_states.json - Final state assessments with reasoning
"""

import json
import re
from datetime import datetime, timedelta

def load_fact_sheets():
    """Load fact sheets from JSON file"""
    try:
        with open('utilities/fact_sheets.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("ERROR: utilities/fact_sheets.json not found. Run generate_fact_sheets.py first.")
        return {}

def is_bullish_signal(signal):
    """Check if signal is bullish"""
    bullish_signals = ["SOS", "Sign of Strength", "Effort to Rise", "SOS Bar"]
    return any(bs in signal for bs in bullish_signals)

def is_bearish_signal(signal):
    """Check if signal is bearish"""
    bearish_signals = ["Sign of Weakness", "SOW", "No Demand", "Upthrust"]
    return any(bs in signal for bs in bearish_signals)

def is_neutral_signal(signal):
    """Check if signal is neutral"""
    neutral_signals = ["Test for Supply", "No Supply", "No Signal"]
    return any(ns in signal for ns in neutral_signals)

def get_signal_strength(signal):
    """Get signal strength: 1=bullish, 0=neutral, -1=bearish"""
    if is_bullish_signal(signal):
        return 1
    elif is_bearish_signal(signal):
        return -1
    else:
        return 0

def is_recent_signal(date_str, days_threshold=5):
    """Check if signal date is recent (within threshold days)"""
    try:
        if date_str == "N/A":
            return False
        signal_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()
        return (today - signal_date).days <= days_threshold
    except:
        return False

def assess_top_list_ticker(ticker_data):
    """Assess tickers currently in Top List - WEEKLY PRIORITY + STABILITY"""
    ticker = ticker_data['ticker']
    daily_signal = ticker_data['most_recent_daily_signal']['signal']
    daily_date = ticker_data['most_recent_daily_signal']['date']
    weekly_signal = ticker_data['weekly_context']['signal']
    weekly_date = ticker_data['weekly_context']['week_ending_date']
    industry_status = ticker_data['industry_status']
    
    # Primary Assessment: Weekly Context
    weekly_strength = get_signal_strength(weekly_signal)
    daily_strength = get_signal_strength(daily_signal)
    
    # Initial confidence based on weekly signal
    if weekly_strength == 1:  # Weekly bullish
        confidence = 95
        foundation = "Strong weekly foundation"
    elif weekly_strength == 0:  # Weekly neutral
        confidence = 85
        foundation = "Neutral weekly context"
    else:  # Weekly bearish
        confidence = 75
        foundation = "Weak weekly context"
    
    # Adjust confidence based on daily signals
    if daily_strength == -1:  # Daily bearish
        confidence = max(75, confidence - 10)
        daily_adjustment = f"reduced by daily {daily_signal}"
    elif daily_strength == 1:  # Daily bullish
        confidence = min(95, confidence + 5)
        daily_adjustment = f"supported by daily {daily_signal}"
    else:
        daily_adjustment = "neutral daily action"
    
    # Check for removal conditions (VERY HIGH THRESHOLD)
    should_remove = False
    removal_reason = ""
    
    if (weekly_strength == -1 and daily_strength == -1 and 
        is_recent_signal(daily_date, 3) and 
        "Yếu" in industry_status):
        should_remove = True
        removal_reason = f"Weekly bearish + recent daily {daily_signal} + weak industry"
    
    if should_remove:
        new_state = "Downgraded"
        reasoning = f"Moved to Downgraded: {removal_reason}"
    else:
        new_state = "Top List"
        reasoning = f"Maintained in Top List: {foundation}, {daily_adjustment}"
    
    return {
        "ticker": ticker,
        "previous_state": "Top List",
        "new_state": new_state,
        "confidence": confidence,
        "reasoning": reasoning,
        "weekly_signal": weekly_signal,
        "daily_signal": daily_signal,
        "weekly_date": weekly_date,
        "daily_date": daily_date
    }

def assess_potential_list_ticker(ticker_data):
    """Assess tickers currently in Potential List - WEEKLY PRIORITY + RESPONSIVE TO DAILY SOS"""
    ticker = ticker_data['ticker']
    daily_signal = ticker_data['most_recent_daily_signal']['signal']
    daily_date = ticker_data['most_recent_daily_signal']['date']
    weekly_signal = ticker_data['weekly_context']['signal']
    weekly_date = ticker_data['weekly_context']['week_ending_date']
    industry_status = ticker_data['industry_status']
    
    weekly_strength = get_signal_strength(weekly_signal)
    daily_strength = get_signal_strength(daily_signal)
    
    # Promotion Assessment
    if weekly_strength == 1 and daily_strength == 1:
        # Weekly Strong + Daily Strong
        new_state = "Top List"
        confidence = 95
        reasoning = f"Promoted to Top List: Strong weekly {weekly_signal} + strong daily {daily_signal}"
    elif (weekly_strength <= 0 and daily_strength == 1 and 
          is_recent_signal(daily_date, 2)):
        # Weekly Neutral/Weak + Recent Daily SOS
        new_state = "Top List"
        confidence = 80
        reasoning = f"Promoted to Top List: Recent daily {daily_signal} ({daily_date}) - don't miss breakout"
    elif (weekly_strength == 1 and daily_strength >= 0 and 
          "Dẫn dắt" in industry_status):
        # Weekly Strong + Daily Neutral + Leading Industry
        new_state = "Top List"
        confidence = 85
        reasoning = f"Promoted to Top List: Strong weekly {weekly_signal} + leading industry"
    elif (weekly_strength == -1 and daily_strength == -1 and 
          is_recent_signal(daily_date, 2)):
        # Demotion Assessment
        new_state = "Downgraded"
        confidence = 70
        reasoning = f"Moved to Downgraded: Weekly {weekly_signal} + recent daily {daily_signal}"
    elif (weekly_strength == 0 and daily_strength == 0 and 
          "Yếu" in industry_status):
        # Unlisted conditions
        new_state = "Unlisted"
        confidence = 60
        reasoning = f"Moved to Unlisted: Neutral signals + weak industry"
    else:
        # Stay in Potential List
        new_state = "Potential List"
        confidence = 75
        reasoning = f"Maintained in Potential List: Monitoring weekly {weekly_signal} + daily {daily_signal}"
    
    return {
        "ticker": ticker,
        "previous_state": "Potential List",
        "new_state": new_state,
        "confidence": confidence,
        "reasoning": reasoning,
        "weekly_signal": weekly_signal,
        "daily_signal": daily_signal,
        "weekly_date": weekly_date,
        "daily_date": daily_date
    }

def assess_downgraded_ticker(ticker_data):
    """Assess tickers currently in Downgraded - RESPONSIVE TO RECOVERY"""
    ticker = ticker_data['ticker']
    daily_signal = ticker_data['most_recent_daily_signal']['signal']
    daily_date = ticker_data['most_recent_daily_signal']['date']
    weekly_signal = ticker_data['weekly_context']['signal']
    weekly_date = ticker_data['weekly_context']['week_ending_date']
    industry_status = ticker_data['industry_status']
    
    weekly_strength = get_signal_strength(weekly_signal)
    daily_strength = get_signal_strength(daily_signal)
    
    # Fast Recovery Assessment
    if (daily_strength == 1 and weekly_strength >= 0 and 
        is_recent_signal(daily_date, 2)):
        # Daily SOS + Weekly supportive/neutral
        new_state = "Potential List"
        confidence = 80
        reasoning = f"Fast tracked to Potential List: Daily {daily_signal} + supportive weekly context"
    elif (daily_strength == 1 and weekly_strength == -1 and 
          is_recent_signal(daily_date, 1)):
        # Daily SOS + Weekly still bearish (need more confirmation)
        new_state = "Downgraded"
        confidence = 75
        reasoning = f"Monitoring recovery: Daily {daily_signal} but weekly still {weekly_signal}"
    elif weekly_strength == 1:
        # Weekly Recovery
        new_state = "Potential List"
        confidence = 85
        reasoning = f"Promoted to Potential List: Weekly recovery signal {weekly_signal}"
    elif (weekly_strength == -1 and daily_strength == -1 and 
          "Yếu" in industry_status):
        # Removal criteria
        new_state = "Unlisted"
        confidence = 65
        reasoning = f"Removed: Continued bearish signals + weak industry"
    else:
        # Stay in Downgraded
        new_state = "Downgraded"
        confidence = 70
        reasoning = f"Maintained in Downgraded: Monitoring for recovery signals"
    
    return {
        "ticker": ticker,
        "previous_state": "Downgraded",
        "new_state": new_state,
        "confidence": confidence,
        "reasoning": reasoning,
        "weekly_signal": weekly_signal,
        "daily_signal": daily_signal,
        "weekly_date": weekly_date,
        "daily_date": daily_date
    }

def assess_unlisted_ticker(ticker_data):
    """Assess tickers currently Unlisted - WEEKLY PRIORITY + DAILY SOS CAPTURE"""
    ticker = ticker_data['ticker']
    daily_signal = ticker_data['most_recent_daily_signal']['signal']
    daily_date = ticker_data['most_recent_daily_signal']['date']
    weekly_signal = ticker_data['weekly_context']['signal']
    weekly_date = ticker_data['weekly_context']['week_ending_date']
    industry_status = ticker_data['industry_status']
    
    weekly_strength = get_signal_strength(weekly_signal)
    daily_strength = get_signal_strength(daily_signal)
    
    # Entry Assessment - Responsive to Opportunities
    if (daily_strength == 1 and weekly_strength >= 0 and 
        is_recent_signal(daily_date, 2)):
        # Daily SOS + Weekly neutral/positive
        new_state = "Potential List"
        confidence = 80
        reasoning = f"Fast entry to Potential List: Daily {daily_signal} + supportive weekly context"
    elif (daily_strength == 1 and weekly_strength == -1 and 
          is_recent_signal(daily_date, 1)):
        # Daily SOS + Weekly negative (need confirmation)
        new_state = "Potential List"
        confidence = 75
        reasoning = f"Entry to Potential List: Strong daily {daily_signal} - monitor for confirmation"
    elif weekly_strength == 1:
        # Weekly SOS + Daily any
        new_state = "Potential List"
        confidence = 85
        reasoning = f"Immediate entry to Potential List: Weekly {weekly_signal}"
    else:
        # Stay Unlisted
        new_state = "Unlisted"
        confidence = 60
        reasoning = f"Remained Unlisted: Monitoring for entry signals"
    
    return {
        "ticker": ticker,
        "previous_state": "Unlisted",
        "new_state": new_state,
        "confidence": confidence,
        "reasoning": reasoning,
        "weekly_signal": weekly_signal,
        "daily_signal": daily_signal,
        "weekly_date": weekly_date,
        "daily_date": daily_date
    }

def assess_all_tickers(fact_sheets):
    """Assess all tickers according to their previous state"""
    assessments = {}
    
    for ticker, data in fact_sheets.items():
        previous_state = data['previous_state']
        
        if previous_state == "Top List":
            assessment = assess_top_list_ticker(data)
        elif previous_state == "Potential List":
            assessment = assess_potential_list_ticker(data)
        elif previous_state == "Downgraded":
            assessment = assess_downgraded_ticker(data)
        else:  # Unlisted
            assessment = assess_unlisted_ticker(data)
        
        assessments[ticker] = assessment
    
    return assessments

def generate_state_summary(assessments):
    """Generate summary of state changes"""
    summary = {
        "Top List": [],
        "Potential List": [],
        "Downgraded": [],
        "Unlisted": []
    }
    
    changes = {
        "promoted_to_top": [],
        "added_to_potential": [],
        "moved_to_downgraded": [],
        "removed_to_unlisted": [],
        "no_change": []
    }
    
    for ticker, assessment in assessments.items():
        new_state = assessment['new_state']
        previous_state = assessment['previous_state']
        
        # Add to summary by new state
        summary[new_state].append({
            "ticker": ticker,
            "confidence": assessment['confidence'],
            "reasoning": assessment['reasoning']
        })
        
        # Track changes
        if previous_state != new_state:
            if new_state == "Top List":
                changes["promoted_to_top"].append(assessment)
            elif new_state == "Potential List" and previous_state == "Unlisted":
                changes["added_to_potential"].append(assessment)
            elif new_state == "Downgraded":
                changes["moved_to_downgraded"].append(assessment)
            elif new_state == "Unlisted":
                changes["removed_to_unlisted"].append(assessment)
        else:
            changes["no_change"].append(assessment)
    
    return summary, changes

def main():
    """Main function to assess all ticker states"""
    print("Assessing ticker states according to VPA-Strategist protocol...")
    
    # Load fact sheets
    fact_sheets = load_fact_sheets()
    if not fact_sheets:
        return
    
    # Assess all tickers
    assessments = assess_all_tickers(fact_sheets)
    
    # Generate summary
    summary, changes = generate_state_summary(assessments)
    
    # Output results
    output_data = {
        "assessments": assessments,
        "summary": summary,
        "changes": changes,
        "metadata": {
            "total_tickers": len(assessments),
            "generation_time": datetime.now().isoformat()
        }
    }
    
    with open('utilities/ticker_states.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Ticker state assessment completed!")
    print(f"Total tickers processed: {len(assessments)}")
    print(f"Output file: utilities/ticker_states.json")
    
    # Print summary
    print("\nNew state distribution:")
    for state, tickers in summary.items():
        print(f"  {state}: {len(tickers)} tickers")
    
    print("\nState changes:")
    for change_type, ticker_list in changes.items():
        if ticker_list:
            print(f"  {change_type}: {len(ticker_list)} tickers")
            for assessment in ticker_list[:3]:  # Show first 3 examples
                print(f"    {assessment['ticker']}: {assessment['reasoning']}")
            if len(ticker_list) > 3:
                print(f"    ... and {len(ticker_list) - 3} more")

if __name__ == "__main__":
    main()