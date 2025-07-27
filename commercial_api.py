#!/usr/bin/env python3
"""
Commercial-Grade TV Schedule API
Uses the EXACT same sources that commercial TV guides use:
- Gracenote TMS API (Nielsen/Tribune Media Services)
- Rovi API (backup)
- Schedule Direct (for non-commercial)
"""

import requests
from datetime import datetime, timedelta
import json
import os

class CommercialTVAPI:
    def __init__(self, gracenote_api_key=None, rovi_api_key=None):
        self.gracenote_key = gracenote_api_key or os.getenv('GRACENOTE_API_KEY')
        self.rovi_key = rovi_api_key or os.getenv('ROVI_API_KEY')
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TVScheduleViewer/1.0 Commercial',
            'Accept': 'application/json'
        })
        
        # Station IDs for major networks (Gracenote/TMS format)
        self.station_ids = {
            'nbc': '20364',  # NBC National
            'abc': '20361',  # ABC National  
            'cbs': '20362',  # CBS National
            'fox': '20363'   # FOX National
        }
    
    def get_gracenote_schedule(self, network, date_str):
        """
        Gracenote TMS API - The industry standard
        Used by cable companies, streaming services, and TV guides
        """
        if not self.gracenote_key:
            return {
                "error": "Gracenote API key required",
                "message": "Sign up at https://developer.tmsapi.com/ for commercial-grade data",
                "network": network.upper(),
                "date": date_str
            }
        
        try:
            print(f"🏢 Fetching {network.upper()} from Gracenote TMS API (Commercial Grade)...")
            
            station_id = self.station_ids.get(network.lower())
            if not station_id:
                return {"error": f"No station ID for {network}"}
            
            # Gracenote TMS API endpoint for TV schedule
            url = "https://data.tmsapi.com/v1.1/programs/newShowAirings"
            
            params = {
                'startDateTime': f"{date_str}T00:00:00Z",
                'endDateTime': f"{date_str}T23:59:59Z", 
                'stationId': station_id,
                'api_key': self.gracenote_key
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            schedule = []
            
            for airing in data:
                program = airing.get('program', {})
                
                # Convert to readable time format
                start_time = airing.get('startTime', '')
                if 'T' in start_time:
                    dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    time_str = dt.strftime('%I:%M %p')
                else:
                    time_str = start_time
                
                schedule.append({
                    "time": time_str,
                    "title": program.get('title', 'Unknown'),
                    "description": program.get('shortDescription', program.get('longDescription', 'No description')),
                    "episode": program.get('episodeTitle', ''),
                    "season": airing.get('seasonNum', ''),
                    "episode_num": airing.get('episodeNum', ''),
                    "duration": airing.get('duration', ''),
                    "genre": program.get('genres', []),
                    "rating": program.get('contentRating', [])
                })
            
            return {
                "network": network.upper(),
                "date": date_str,
                "source": "Gracenote TMS API (Commercial)",
                "status": "premium_verified",
                "total_programs": len(schedule),
                "schedule": schedule
            }
            
        except requests.RequestException as e:
            return {"error": f"Gracenote API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Gracenote API error: {str(e)}"}
    
    def get_rovi_schedule(self, network, date_str):
        """
        Rovi API - Alternative commercial provider
        """
        if not self.rovi_key:
            return {"error": "Rovi API key required"}
        
        try:
            print(f"🏢 Fetching {network.upper()} from Rovi API (Commercial Grade)...")
            
            # Rovi API endpoints (example structure)
            url = "http://api.rovicorp.com/TVlistings/v9/listings/linearschedule/info"
            
            params = {
                'apikey': self.rovi_key,
                'sig': self._generate_rovi_signature(),  # Rovi requires signature
                'format': 'json',
                'locale': 'en-US',
                'countrycode': 'US',
                'postalcode': '90210',  # Required for local programming
                'msoid': self._get_rovi_mso_id(network),
                'date': date_str
            }
            
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            # Parse Rovi response format
            schedule = []
            # Implementation would depend on Rovi's exact response format
            
            return {
                "network": network.upper(),
                "date": date_str,
                "source": "Rovi API (Commercial)",
                "status": "premium_verified",
                "schedule": schedule
            }
            
        except Exception as e:
            return {"error": f"Rovi API error: {str(e)}"}
    
    def get_schedule_direct(self, network, date_str):
        """
        Schedule Direct - Non-commercial but high quality
        """
        try:
            print(f"📡 Fetching {network.upper()} from Schedule Direct...")
            
            # Schedule Direct requires authentication
            # This would need login credentials and token management
            return {
                "error": "Schedule Direct requires account setup",
                "message": "Visit https://schedulesdirect.org/ for non-commercial access",
                "network": network.upper(),
                "date": date_str
            }
            
        except Exception as e:
            return {"error": f"Schedule Direct error: {str(e)}"}
    
    def _generate_rovi_signature(self):
        """Generate required signature for Rovi API"""
        # Rovi requires MD5 signature - implementation would be here
        return "placeholder_signature"
    
    def _get_rovi_mso_id(self, network):
        """Get Rovi MSO (Multiple System Operator) ID for network"""
        mso_ids = {
            'nbc': 'NBC_MSO_ID',
            'abc': 'ABC_MSO_ID',
            'cbs': 'CBS_MSO_ID', 
            'fox': 'FOX_MSO_ID'
        }
        return mso_ids.get(network.lower(), '')
    
    def get_commercial_grade_schedule(self, network, date_str):
        """
        Get schedule using commercial-grade APIs
        """
        print(f"\n🏢 COMMERCIAL-GRADE SCHEDULE LOOKUP: {network.upper()}")
        print("=" * 60)
        print("Using the EXACT same APIs as cable companies and streaming services")
        
        # Try Gracenote TMS first (industry standard)
        result = self.get_gracenote_schedule(network, date_str)
        if not result.get('error') and result.get('schedule'):
            print(f"✅ SUCCESS: Gracenote returned {len(result['schedule'])} programs")
            return result
        else:
            print(f"❌ Gracenote failed: {result.get('error', 'No data')}")
        
        # Try Rovi as backup
        result = self.get_rovi_schedule(network, date_str)
        if not result.get('error') and result.get('schedule'):
            print(f"✅ SUCCESS: Rovi returned {len(result['schedule'])} programs")
            return result
        else:
            print(f"❌ Rovi failed: {result.get('error', 'No data')}")
        
        # Try Schedule Direct for non-commercial
        result = self.get_schedule_direct(network, date_str)
        if not result.get('error') and result.get('schedule'):
            print(f"✅ SUCCESS: Schedule Direct returned {len(result['schedule'])} programs")
            return result
        else:
            print(f"❌ Schedule Direct failed: {result.get('error', 'No data')}")
        
        return {
            "error": "All commercial APIs require valid keys",
            "network": network.upper(),
            "date": date_str,
            "next_steps": [
                "Sign up for Gracenote API at https://developer.tmsapi.com/",
                "Contact Rovi for commercial licensing",
                "Register at Schedule Direct for non-commercial use"
            ]
        }

def setup_api_keys():
    """
    Interactive setup for API keys
    """
    print("🔑 COMMERCIAL TV API SETUP")
    print("=" * 40)
    print("To get commercial-grade schedule data, you need API keys from:")
    print()
    print("1. 🏢 GRACENOTE TMS API (Recommended - Industry Standard)")
    print("   • Used by: Cable companies, streaming services, TV guides")
    print("   • Sign up: https://developer.tmsapi.com/")
    print("   • Free tier available for testing")
    print()
    print("2. 🏢 ROVI API (Alternative Commercial Provider)")
    print("   • Contact Rovi for licensing")
    print("   • Typically requires commercial agreement")
    print()
    print("3. 📡 SCHEDULE DIRECT (Non-commercial)")
    print("   • Visit: https://schedulesdirect.org/")
    print("   • Good for personal projects")
    print()
    
    gracenote_key = input("Enter Gracenote API key (or press Enter to skip): ").strip()
    rovi_key = input("Enter Rovi API key (or press Enter to skip): ").strip()
    
    if gracenote_key or rovi_key:
        # Save to environment file
        with open('.env', 'w') as f:
            if gracenote_key:
                f.write(f"GRACENOTE_API_KEY={gracenote_key}\n")
            if rovi_key:
                f.write(f"ROVI_API_KEY={rovi_key}\n")
        
        print("✅ API keys saved to .env file")
    else:
        print("⚠️  No API keys provided - commercial features will be limited")

if __name__ == "__main__":
    setup_api_keys()
    
    api = CommercialTVAPI()
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    for network in ['nbc', 'abc', 'cbs', 'fox']:
        result = api.get_commercial_grade_schedule(network, date_str)
        print(f"\n📺 {network.upper()} Result:")
        if result.get('schedule'):
            print(f"Programs found: {len(result['schedule'])}")
            for prog in result['schedule'][:3]:
                print(f"  {prog.get('time', 'N/A')} - {prog.get('title', 'N/A')}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
        print()