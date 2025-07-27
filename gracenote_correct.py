#!/usr/bin/env python3
"""
Correct Gracenote TMS API Implementation
Based on the official documentation provided
"""

import requests
from datetime import datetime, timedelta
import json
import os

class GracenoteCorrectAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GRACENOTE_API_KEY')
        self.base_url = "http://data.tmsapi.com/v1.1"
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'TVScheduleViewer/1.0',
            'Accept': 'application/xml',  # API only supports XML
            'Accept-encoding': 'gzip'  # Performance improvement per docs
        })
    
    def get_lineups(self, postal_code="90210"):
        """
        First step: Get available lineups for a postal code
        This tells us what stations are available
        """
        if not self.api_key:
            return {"error": "API key required"}
        
        try:
            url = f"{self.base_url}/lineups.xml"
            params = {
                'country': 'USA',
                'postalCode': postal_code,
                'api_key': self.api_key
            }
            
            print(f"Getting lineups for {postal_code}...")
            response = self.session.get(url, params=params, timeout=15)
            
            print(f"Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text}")
                return {"error": f"HTTP {response.status_code}: {response.text}"}
            
            # Parse XML response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            lineups = []
            for lineup in root.findall('.//lineup'):
                lineups.append({
                    'lineupId': lineup.get('lineupId', ''),
                    'name': lineup.get('name', ''),
                    'location': lineup.get('location', '')
                })
            
            print(f"Found {len(lineups)} lineups")
            return lineups
            
        except Exception as e:
            return {"error": f"Lineups request failed: {str(e)}"}
    
    def get_stations_from_lineup(self, lineup_id):
        """
        Get all stations in a specific lineup
        """
        if not self.api_key:
            return {"error": "API key required"}
        
        try:
            url = f"{self.base_url}/lineups/{lineup_id}.xml"
            params = {'api_key': self.api_key}
            
            print(f"Getting stations for lineup {lineup_id}...")
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
            
            # Parse XML response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            stations = []
            major_networks = {}
            
            for station in root.findall('.//station'):
                station_id = station.get('stationId', '')
                name = station.get('name', '')
                
                stations.append({
                    'stationId': station_id,
                    'name': name,
                    'callSign': station.get('callSign', '')
                })
                
                # Find major networks
                name_upper = name.upper()
                if 'NBC' in name_upper and 'nbc' not in major_networks:
                    major_networks['nbc'] = station_id
                elif 'ABC' in name_upper and 'abc' not in major_networks:
                    major_networks['abc'] = station_id
                elif 'CBS' in name_upper and 'cbs' not in major_networks:
                    major_networks['cbs'] = station_id
                elif 'FOX' in name_upper and 'fox' not in major_networks:
                    major_networks['fox'] = station_id
            
            print(f"Found {len(stations)} stations")
            print(f"Major networks found: {major_networks}")
            
            return {
                "lineup_id": lineup_id,
                "total_stations": len(stations),
                "major_networks": major_networks,
                "all_stations": stations
            }
            
        except Exception as e:
            return {"error": f"Stations request failed: {str(e)}"}
    
    def get_station_schedule(self, station_id, date_str):
        """
        Get schedule for a specific station
        This is the main TV schedule function
        """
        if not self.api_key:
            return {"error": "API key required"}
        
        try:
            url = f"{self.base_url}/stations/{station_id}/airings.xml"
            params = {
                'api_key': self.api_key,
                'startDateTime': f"{date_str}T00:00Z",
                'endDateTime': f"{date_str}T23:59Z"
            }
            
            print(f"Getting schedule for station {station_id} on {date_str}...")
            response = self.session.get(url, params=params, timeout=20)
            
            print(f"Status: {response.status_code}")
            if response.status_code != 200:
                print(f"Error: {response.text[:200]}")
                return {"error": f"HTTP {response.status_code}: {response.text[:200]}"}
            
            # Parse XML response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            airings = root.findall('.//airing')
            print(f"Found {len(airings)} programs")
            
            # Parse schedule
            schedule = []
            for airing in airings:
                start_time = airing.get('startTime', '')
                
                # Convert to readable time
                if 'T' in start_time:
                    dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
                    time_str = dt.strftime('%I:%M %p')
                else:
                    time_str = start_time
                
                # Get program element
                program = airing.find('program')
                if program is not None:
                    title = program.get('title', 'Unknown')
                    tms_id = program.get('tmsId', '')
                    
                    # Get description
                    desc_elem = program.find('shortDescription')
                    description = desc_elem.text if desc_elem is not None else ''
                    
                    if not description:
                        long_desc_elem = program.find('longDescription') 
                        description = long_desc_elem.text if long_desc_elem is not None else ''
                    
                    # Get episode info
                    episode_elem = program.find('episodeTitle')
                    episode_title = episode_elem.text if episode_elem is not None else ''
                    
                else:
                    title = 'Unknown Program'
                    description = ''
                    episode_title = ''
                    tms_id = ''
                
                schedule.append({
                    "time": time_str,
                    "title": title,
                    "description": description,
                    "episode": episode_title,
                    "season": airing.get('seasonNum', ''),
                    "episode_num": airing.get('episodeNum', ''),
                    "duration": airing.get('duration', ''),
                    "tms_id": tms_id
                })
            
            return {
                "station_id": station_id,
                "date": date_str,
                "source": "Gracenote TMS API",
                "status": "verified",
                "total_programs": len(schedule),
                "schedule": schedule
            }
            
        except Exception as e:
            print(f"Schedule request failed: {e}")
            return {"error": f"Schedule request failed: {str(e)}"}
    
    def get_network_schedule(self, network, date_str, postal_code="90210"):
        """
        Complete workflow: Get schedule for a major network
        """
        print(f"\n🏢 GETTING {network.upper()} SCHEDULE")
        print("=" * 50)
        
        # Step 1: Get lineups
        lineups = self.get_lineups(postal_code)
        if lineups.get('error'):
            return lineups
        
        # Step 2: Find a lineup with the network
        station_id = None
        for lineup in lineups:
            lineup_id = lineup.get('lineupId')
            if not lineup_id:
                continue
                
            stations_info = self.get_stations_from_lineup(lineup_id)
            if stations_info.get('error'):
                continue
                
            major_networks = stations_info.get('major_networks', {})
            if network.lower() in major_networks:
                station_id = major_networks[network.lower()]
                print(f"Found {network.upper()} station: {station_id}")
                break
        
        if not station_id:
            return {"error": f"Could not find {network.upper()} station in any lineup"}
        
        # Step 3: Get the schedule
        return self.get_station_schedule(station_id, date_str)

def test_gracenote_correct():
    """
    Test the correct implementation
    """
    print("🏢 CORRECT GRACENOTE TMS API TEST")
    print("=" * 50)
    
    api = GracenoteCorrectAPI()
    api.api_key = 'uk2dqjggp2qr9vzgce4a8dq7'  # Your active key
    
    if not api.api_key:
        print("❌ No API key provided")
        return
    
    print(f"Using API key: {api.api_key}")
    print()
    
    # Test lineups first
    print("Testing lineups...")
    lineups = api.get_lineups()
    if lineups.get('error'):
        print(f"❌ Lineups failed: {lineups['error']}")
        return
    else:
        print(f"✅ Lineups successful: {len(lineups)} found")
    
    # Test getting NBC schedule
    date_str = datetime.now().strftime('%Y-%m-%d')
    result = api.get_network_schedule('nbc', date_str)
    
    if result.get('error'):
        print(f"❌ NBC schedule failed: {result['error']}")
    else:
        print(f"✅ NBC schedule successful: {len(result.get('schedule', []))} programs")
        
        # Show sample programs
        schedule = result.get('schedule', [])
        if schedule:
            print("\nSample programs:")
            for prog in schedule[:5]:
                print(f"  {prog.get('time', 'N/A')} - {prog.get('title', 'N/A')}")

if __name__ == "__main__":
    test_gracenote_correct()