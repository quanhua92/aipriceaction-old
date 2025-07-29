#!/usr/bin/env python3

import pandas as pd

def verify_weekly_claims():
    """Verify specific weekly performance claims"""
    
    print("=== WEEKLY CLAIMS VERIFICATION ===\n")
    
    # VND weekly performance claim: +13.4% with +29.7% volume (line 210)
    print("1. VND Weekly Performance (Line 210):")
    print("   Claimed: +13.4% with +29.7% volume")
    
    try:
        df = pd.read_csv("market_data_week/VND_2025-01-02_to_2025-07-25.csv")
        week_jul21 = df[df['time'] == '2025-07-21'].iloc[0]
        week_jul14 = df[df['time'] == '2025-07-14'].iloc[0]
        
        price_change = ((week_jul21['close'] - week_jul14['close']) / week_jul14['close']) * 100
        volume_change = ((week_jul21['volume'] - week_jul14['volume']) / week_jul14['volume']) * 100
        
        print(f"   Actual: {price_change:+.1f}% with {volume_change:+.1f}% volume")
        print(f"   Jul 14: {week_jul14['close']} (Volume: {week_jul14['volume']:,})")
        print(f"   Jul 21: {week_jul21['close']} (Volume: {week_jul21['volume']:,})")
        
        if abs(price_change - 13.4) > 1.0:
            print(f"   ❌ WEEKLY PRICE ERROR: Claimed +13.4%, Actual {price_change:+.1f}%")
        else:
            print("   ✅ Weekly price change verified")
            
        if abs(volume_change - 29.7) > 5.0:
            print(f"   ❌ WEEKLY VOLUME ERROR: Claimed +29.7%, Actual {volume_change:+.1f}%")
        else:
            print("   ✅ Weekly volume change verified")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # VPB weekly performance claim: +11.3% with +20.3% volume (line 232)
    print("2. VPB Weekly Performance (Line 232):")
    print("   Claimed: +11.3% with +20.3% volume")
    
    try:
        df = pd.read_csv("market_data_week/VPB_2025-01-02_to_2025-07-25.csv")
        week_jul21 = df[df['time'] == '2025-07-21'].iloc[0]
        week_jul14 = df[df['time'] == '2025-07-14'].iloc[0]
        
        price_change = ((week_jul21['close'] - week_jul14['close']) / week_jul14['close']) * 100
        volume_change = ((week_jul21['volume'] - week_jul14['volume']) / week_jul14['volume']) * 100
        
        print(f"   Actual: {price_change:+.1f}% with {volume_change:+.1f}% volume")
        print(f"   Jul 14: {week_jul14['close']} (Volume: {week_jul14['volume']:,})")
        print(f"   Jul 21: {week_jul21['close']} (Volume: {week_jul21['volume']:,})")
        
        if abs(price_change - 11.3) > 1.0:
            print(f"   ❌ WEEKLY PRICE ERROR: Claimed +11.3%, Actual {price_change:+.1f}%")
        else:
            print("   ✅ Weekly price change verified")
            
        if abs(volume_change - 20.3) > 5.0:
            print(f"   ❌ WEEKLY VOLUME ERROR: Claimed +20.3%, Actual {volume_change:+.1f}%")
        else:
            print("   ✅ Weekly volume change verified")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print()
    
    # HDC weekly performance claim: +27% with +24.5% volume (line 100)
    print("3. HDC Weekly Performance (Line 100):")
    print("   Claimed: +27% with +24.5% volume")
    
    try:
        df = pd.read_csv("market_data_week/HDC_2025-01-02_to_2025-07-25.csv")
        week_jul21 = df[df['time'] == '2025-07-21'].iloc[0]  
        week_jul14 = df[df['time'] == '2025-07-14'].iloc[0]
        
        price_change = ((week_jul21['close'] - week_jul14['close']) / week_jul14['close']) * 100
        volume_change = ((week_jul21['volume'] - week_jul14['volume']) / week_jul14['volume']) * 100
        
        print(f"   Actual: {price_change:+.1f}% with {volume_change:+.1f}% volume")
        print(f"   Jul 14: {week_jul14['close']} (Volume: {week_jul14['volume']:,})")
        print(f"   Jul 21: {week_jul21['close']} (Volume: {week_jul21['volume']:,})")
        
        if abs(price_change - 27.0) > 2.0:
            print(f"   ❌ WEEKLY PRICE ERROR: Claimed +27%, Actual {price_change:+.1f}%")
        else:
            print("   ✅ Weekly price change verified")
            
        if abs(volume_change - 24.5) > 5.0:  # Looser tolerance for volume
            print(f"   ❌ WEEKLY VOLUME ERROR: Claimed +24.5%, Actual {volume_change:+.1f}%")
        else:
            print("   ✅ Weekly volume change verified")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

    print()
    
    # Check TCH daily change claim: -6.82% (line 167)
    print("4. TCH Daily Change (Line 167):")
    print("   Claimed: -6.82%")
    
    try:
        df = pd.read_csv("market_data/TCH_2025-01-02_to_2025-07-29.csv")
        jul29 = df[df['time'] == '2025-07-29'].iloc[0]
        jul28 = df[df['time'] == '2025-07-28'].iloc[0]
        
        daily_change = ((jul29['close'] - jul28['close']) / jul28['close']) * 100
        
        print(f"   Actual: {daily_change:+.2f}%")
        print(f"   Jul 28: {jul28['close']}")
        print(f"   Jul 29: {jul29['close']}")
        
        if abs(daily_change - (-6.82)) > 0.5:
            print(f"   ❌ DAILY CHANGE ERROR: Claimed -6.82%, Actual {daily_change:+.2f}%")
        else:
            print("   ✅ Daily change verified")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    verify_weekly_claims()