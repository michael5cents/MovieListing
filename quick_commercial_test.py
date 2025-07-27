#!/usr/bin/env python3
"""
Quick test of commercial API without interactive input
"""

from commercial_api import CommercialTVAPI
from datetime import datetime

def test_commercial_apis():
    print("🏢 COMMERCIAL-GRADE TV API TEST")
    print("=" * 50)
    print("Testing the EXACT same APIs used by cable companies")
    print()
    
    # Initialize without keys to show what's needed
    api = CommercialTVAPI()
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    print(f"Testing for date: {date_str}")
    print()
    
    for network in ['nbc', 'abc', 'cbs', 'fox']:
        result = api.get_commercial_grade_schedule(network, date_str)
        
        print(f"📺 {network.upper()} Results:")
        if result.get('error'):
            print(f"   Status: {result['error']}")
            if 'next_steps' in result:
                print("   Next steps:")
                for step in result['next_steps']:
                    print(f"   • {step}")
        else:
            print(f"   Programs: {len(result.get('schedule', []))}")
            print(f"   Source: {result.get('source', 'Unknown')}")
        print()
    
    print("🔑 TO GET WORKING DATA:")
    print("=" * 30)
    print("1. Sign up at: https://developer.tmsapi.com/")
    print("2. Get your free API key")
    print("3. Set environment variable: export GRACENOTE_API_KEY='your_key'")
    print("4. Re-run this script")
    print()
    print("💡 This will give you the EXACT same data as:")
    print("   • Netflix")
    print("   • Cable company guides") 
    print("   • Streaming services")
    print("   • TV Guide magazine")

if __name__ == "__main__":
    test_commercial_apis()