#!/usr/bin/env python3
"""
NBC Schedule Lookup Tool
Usage: python3 schedule_lookup.py "11:00 AM"
Returns only real verified programming for the specified time slot
"""

import sys
from datetime import datetime, timezone, timedelta

def get_current_date():
    """Get current date in Mountain Time"""
    mountain_tz = timezone(timedelta(hours=-7))  # MDT
    return datetime.now(mountain_tz)

def lookup_nbc_programming(time_slot):
    """
    Look up real NBC programming for a specific time slot
    Args:
        time_slot (str): Time in format like "11:00 AM" or "2:30 PM"
    Returns:
        dict: Program info or error if not found/verified
    """
    
    current_date = get_current_date()
    date_str = current_date.strftime('%Y-%m-%d')
    day_name = current_date.strftime('%A')
    
    print(f"Looking up NBC programming for {time_slot} on {day_name}, {date_str}")
    print("Attempting real-time verification...")
    
    # This would use MCP firecrawl to get real data from:
    # https://www.tvpassport.com/tv-listings/stations/nbc-wrgx-dothan-al-hd/19093/{date_str}
    
    # For now, return that verification is needed
    return {
        "time": time_slot,
        "date": date_str,
        "day": day_name,
        "status": "VERIFICATION_NEEDED",
        "message": f"Real-time lookup for {time_slot} requires live data verification",
        "source_needed": f"https://www.tvpassport.com/tv-listings/stations/nbc-wrgx-dothan-al-hd/19093/{date_str}"
    }

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 schedule_lookup.py \"11:00 AM\"")
        print("Example: python3 schedule_lookup.py \"2:30 PM\"")
        sys.exit(1)
    
    time_slot = sys.argv[1]
    result = lookup_nbc_programming(time_slot)
    
    print("\n" + "="*50)
    print(f"NBC SCHEDULE LOOKUP RESULT")
    print("="*50)
    
    if result["status"] == "VERIFICATION_NEEDED":
        print(f"Time Requested: {result['time']}")
        print(f"Date: {result['date']} ({result['day']})")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        print(f"Source URL: {result['source_needed']}")
    else:
        print(f"Time: {result['time']}")
        print(f"Program: {result.get('title', 'Unknown')}")
        print(f"Description: {result.get('description', 'N/A')}")
        print(f"Verified: {result.get('verified', False)}")

if __name__ == "__main__":
    main()