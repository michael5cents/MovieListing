#!/usr/bin/env python3
"""
Debug Gracenote API key and endpoints
"""

import requests
import os

def debug_gracenote_api():
    api_key = 'uk2dqjggp2qr9vzgce4a8dq7'
    
    print("🔍 GRACENOTE API DEBUG")
    print("=" * 40)
    print(f"API Key: {api_key}")
    print()
    
    # Test different endpoints to see what works
    endpoints_to_test = [
        ("Basic Station Info", "http://data.tmsapi.com/v1.1/stations/10161", {}),
        ("Station Airings", "http://data.tmsapi.com/v1.1/stations/10161/airings", {
            'startDateTime': '2025-07-27T00:00Z'
        }),
        ("Movies Endpoint", "http://data.tmsapi.com/v1.1/movies/showings", {
            'startDate': '2025-07-27'
        }),
        ("Programs Endpoint", "http://data.tmsapi.com/v1.1/programs/newShowAirings", {
            'startDateTime': '2025-07-27T00:00Z',
            'stationId': '10161'
        })
    ]
    
    for name, url, extra_params in endpoints_to_test:
        print(f"Testing {name}:")
        print(f"URL: {url}")
        
        params = {'api_key': api_key}
        params.update(extra_params)
        print(f"Params: {params}")
        
        try:
            response = requests.get(url, params=params, timeout=10)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS!")
                try:
                    data = response.json()
                    if isinstance(data, list):
                        print(f"Response: Array with {len(data)} items")
                        if data and len(data) > 0:
                            print(f"First item keys: {list(data[0].keys())}")
                    else:
                        print(f"Response keys: {list(data.keys())}")
                except:
                    print(f"Response text: {response.text[:200]}...")
            elif response.status_code == 403:
                print("❌ 403 Forbidden - API key may need activation")
            elif response.status_code == 401:
                print("❌ 401 Unauthorized - Invalid API key")
            elif response.status_code == 404:
                print("❌ 404 Not Found - Endpoint doesn't exist")
            else:
                print(f"❌ {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        print("-" * 40)
    
    print("\n🔑 NEXT STEPS:")
    print("1. Check your Gracenote developer dashboard")
    print("2. Verify API key is activated for TMS Data APIs")
    print("3. Check if you need to accept Terms of Service")
    print("4. Make sure you selected the correct API plan")

if __name__ == "__main__":
    debug_gracenote_api()