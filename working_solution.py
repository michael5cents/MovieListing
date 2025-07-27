#!/usr/bin/env python3
"""
WORKING TV Schedule Solution
Uses reliable APIs that work immediately without approval delays
"""

import requests
from datetime import datetime, timedelta
import json

class WorkingTVAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TVScheduleViewer/1.0'
        })
    
    def get_tvmaze_schedule(self, network, date_str):
        """
        TVmaze API - Works immediately, no key required
        """
        try:
            print(f"📺 Fetching {network.upper()} from TVmaze (free, unlimited)...")
            
            # Get US schedule for the date
            url = "https://api.tvmaze.com/schedule"
            params = {
                'country': 'US',
                'date': date_str
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            all_shows = response.json()
            
            # Filter for the specific network
            network_map = {
                'nbc': 'NBC',
                'abc': 'ABC', 
                'cbs': 'CBS',
                'fox': 'FOX'
            }
            
            target_network = network_map.get(network.lower())
            if not target_network:
                return {"error": f"Network {network} not supported"}
            
            network_shows = []
            for show in all_shows:
                show_network = show.get('show', {}).get('network')
                if show_network and show_network.get('name') == target_network:
                    
                    airtime = show.get('airtime', 'TBA')
                    title = show.get('show', {}).get('name', 'Unknown Show')
                    summary = show.get('show', {}).get('summary', 'No description available')
                    
                    # Clean HTML tags
                    if summary:
                        import re
                        summary = re.sub('<[^<]+?>', '', summary)
                    
                    network_shows.append({
                        "time": airtime,
                        "title": title,
                        "description": summary[:200] + "..." if len(summary) > 200 else summary,
                        "runtime": show.get('runtime', ''),
                        "season": show.get('season', ''),
                        "episode": show.get('number', '')
                    })
            
            # Sort by time
            network_shows.sort(key=lambda x: x['time'])
            
            return {
                "network": network.upper(),
                "date": date_str,
                "source": "TVmaze API (Free)",
                "status": "verified",
                "total_programs": len(network_shows),
                "schedule": network_shows
            }
            
        except Exception as e:
            return {"error": f"TVmaze failed: {str(e)}"}
    
    def get_comprehensive_schedule(self, network, date_str):
        """
        Get schedule using all available working sources
        """
        print(f"\n📺 GETTING {network.upper()} SCHEDULE FOR {date_str}")
        print("=" * 50)
        
        # Try TVmaze first (most reliable free option)
        result = self.get_tvmaze_schedule(network, date_str)
        
        if not result.get('error') and result.get('schedule'):
            print(f"✅ SUCCESS: {len(result['schedule'])} programs from TVmaze")
            return result
        else:
            print(f"❌ TVmaze failed: {result.get('error', 'No data')}")
            
        # If TVmaze fails, return empty schedule (no fake data)
        return {
            "network": network.upper(),
            "date": date_str,
            "source": "No working sources",
            "status": "no_data",
            "schedule": [],
            "error": "All data sources failed"
        }

def test_working_solution():
    """
    Test the working TV schedule solution
    """
    print("📺 WORKING TV SCHEDULE TEST")
    print("=" * 40)
    print("Using reliable APIs that work immediately")
    print()
    
    api = WorkingTVAPI()
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    for network in ['nbc', 'abc', 'cbs', 'fox']:
        result = api.get_comprehensive_schedule(network, date_str)
        
        print(f"\n📺 {network.upper()} Results:")
        print(f"   Status: {result.get('status', 'unknown')}")
        print(f"   Source: {result.get('source', 'unknown')}")
        print(f"   Programs: {len(result.get('schedule', []))}")
        
        if result.get('schedule'):
            print("   Sample programs:")
            for prog in result['schedule'][:3]:
                print(f"     {prog.get('time', 'TBA')} - {prog.get('title', 'Unknown')}")
        elif result.get('error'):
            print(f"   Error: {result['error']}")

if __name__ == "__main__":
    test_working_solution()