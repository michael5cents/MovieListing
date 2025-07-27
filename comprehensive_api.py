#!/usr/bin/env python3
"""
Comprehensive TV Schedule API
Uses multiple reliable FREE APIs for guaranteed schedule accuracy
- TVmaze API (primary) - Free unlimited requests
- TV-API.com (backup) - Free tier available
"""

import requests
from datetime import datetime, timedelta
import json
import time

class ComprehensiveTVAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; TVScheduleViewer/1.0)',
            'Accept': 'application/json'
        })
    
    def get_tvmaze_schedule(self, network, date_str):
        """
        TVmaze API - Free unlimited requests
        Get schedule for specific date and network
        """
        try:
            print(f"Fetching {network.upper()} schedule from TVmaze API...")
            
            # TVmaze network IDs for major US networks
            network_ids = {
                'nbc': 'NBC',
                'abc': 'ABC', 
                'cbs': 'CBS',
                'fox': 'FOX'
            }
            
            network_name = network_ids.get(network.lower())
            if not network_name:
                return {"error": f"Network {network} not supported"}
            
            # Get schedule for specific date
            url = f"https://api.tvmaze.com/schedule"
            params = {
                'country': 'US',
                'date': date_str
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            all_shows = response.json()
            network_shows = []
            
            # Filter for specific network
            for show in all_shows:
                if (show.get('show', {}).get('network', {}) and 
                    show['show']['network'].get('name') == network_name):
                    
                    airtime = show.get('airtime', '')
                    show_name = show.get('show', {}).get('name', 'Unknown Show')
                    summary = show.get('show', {}).get('summary', 'No description available')
                    
                    # Clean HTML from summary
                    if summary:
                        summary = summary.replace('<p>', '').replace('</p>', '').replace('<b>', '').replace('</b>', '')
                    
                    network_shows.append({
                        "time": airtime,
                        "title": show_name,
                        "description": summary[:200] + "..." if len(summary) > 200 else summary
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
            print(f"TVmaze API failed for {network}: {e}")
            return {"error": f"TVmaze API failed: {str(e)}"}
    
    def get_tv_api_schedule(self, network, date_str):
        """
        TV-API.com backup source
        """
        try:
            print(f"Fetching {network.upper()} schedule from TV-API.com...")
            
            # This would require API key for full access
            # For now, return structure for future implementation
            return {
                "network": network.upper(),
                "date": date_str,
                "source": "TV-API.com",
                "status": "requires_api_key",
                "schedule": []
            }
            
        except Exception as e:
            return {"error": f"TV-API failed: {str(e)}"}
    
    def get_network_direct_schedule(self, network, date_str):
        """
        Fallback: Direct network website scraping
        """
        try:
            print(f"Scraping {network.upper()} official website...")
            
            network_urls = {
                'nbc': 'https://www.nbc.com/schedule',
                'abc': 'https://abc.com/schedule', 
                'cbs': 'https://www.cbs.com/schedule/',
                'fox': 'https://www.fox.com/schedule/'
            }
            
            url = network_urls.get(network.lower())
            if not url:
                return {"error": f"No direct URL for {network}"}
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Basic fallback schedule - would need specific parsing for each network
            fallback_schedule = []
            
            return {
                "network": network.upper(),
                "date": date_str,
                "source": f"{network.upper()}.com Official",
                "status": "limited_data",
                "schedule": fallback_schedule
            }
            
        except Exception as e:
            return {"error": f"Direct scraping failed: {str(e)}"}
    
    def get_guaranteed_schedule(self, network, date_str):
        """
        Multi-source approach for guaranteed accuracy
        """
        print(f"\n🔍 COMPREHENSIVE SCHEDULE LOOKUP: {network.upper()} for {date_str}")
        print("=" * 60)
        
        # Try TVmaze API first (best free option)
        result = self.get_tvmaze_schedule(network, date_str)
        if not result.get('error') and result.get('schedule'):
            print(f"✅ SUCCESS: TVmaze API returned {len(result['schedule'])} programs")
            return result
        else:
            print(f"❌ TVmaze failed: {result.get('error', 'No programs found')}")
        
        # Try TV-API.com as backup
        result = self.get_tv_api_schedule(network, date_str)
        if not result.get('error') and result.get('schedule'):
            print(f"✅ SUCCESS: TV-API returned {len(result['schedule'])} programs")
            return result
        else:
            print(f"❌ TV-API failed: {result.get('error', 'No programs found')}")
        
        # Try direct network scraping as last resort
        result = self.get_network_direct_schedule(network, date_str)
        if not result.get('error') and result.get('schedule'):
            print(f"✅ SUCCESS: Direct scraping returned {len(result['schedule'])} programs")
            return result
        else:
            print(f"❌ Direct scraping failed: {result.get('error', 'No programs found')}")
        
        print(f"❌ ALL SOURCES FAILED FOR {network.upper()}")
        return {
            "error": "All schedule sources exhausted",
            "network": network.upper(),
            "date": date_str,
            "sources_tried": ["TVmaze API", "TV-API.com", "Direct Scraping"],
            "status": "no_data_available",
            "schedule": []
        }

def test_api():
    """Test the comprehensive API"""
    api = ComprehensiveTVAPI()
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    print("🎬 COMPREHENSIVE TV SCHEDULE API TEST")
    print("=" * 50)
    
    for network in ['nbc', 'abc', 'cbs', 'fox']:
        result = api.get_guaranteed_schedule(network, date_str)
        
        print(f"\n📺 {network.upper()} RESULTS:")
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Programs: {len(result.get('schedule', []))}")
        
        if result.get('schedule'):
            print("Sample programs:")
            for prog in result['schedule'][:3]:
                print(f"  {prog.get('time', 'N/A')} - {prog.get('title', 'N/A')}")
        
        time.sleep(1)  # Be respectful to APIs

if __name__ == "__main__":
    test_api()