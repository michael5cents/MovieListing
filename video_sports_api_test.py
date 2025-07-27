#!/usr/bin/env python3
"""
Test Video + Sports API endpoints that should work with your plan
"""

import requests

def test_video_sports_apis():
    api_key = 'uk2dqjggp2qr9vzgce4a8dq7'
    
    print("🎬 TESTING VIDEO + SPORTS API ENDPOINTS")
    print("=" * 50)
    print("Plan: Gracenote Developer Video + Sports APIs")
    print("Limits: 2 calls/second, 50 calls/day")
    print()
    
    # Test Video + Sports specific endpoints
    endpoints = [
        # Sports endpoints (these should work with your plan)
        ("Sports Events", "http://data.tmsapi.com/v1.1/sports/events", {}),
        ("Sports Teams", "http://data.tmsapi.com/v1.1/sports/teams", {}),
        
        # Video/Movie endpoints (these should work)
        ("Movies Showings", "http://data.tmsapi.com/v1.1/movies/showings", {
            'startDate': '2025-07-27',
            'zip': '90210'
        }),
        ("Movie Details", "http://data.tmsapi.com/v1.1/movies/MV000000060000", {}),
        
        # Program endpoints (might work for TV data)
        ("Programs Search", "http://data.tmsapi.com/v1.1/programs", {
            'q': 'NBC',
            'entityType': 'show'
        }),
        ("Program Airings", "http://data.tmsapi.com/v1.1/programs/newShowAirings", {
            'startDateTime': '2025-07-27T00:00Z',
            'stationId': '10161'
        }),
        
        # Try celebrity endpoint
        ("Celebrity Details", "http://data.tmsapi.com/v1.1/people/1", {}),
    ]
    
    working_endpoints = []
    call_count = 0
    
    for name, url, params in endpoints:
        if call_count >= 8:  # Save some calls for actual use
            print(f"Skipping {name} - preserving API calls")
            continue
            
        print(f"Testing {name}:")
        print(f"  URL: {url}")
        
        test_params = {'api_key': api_key}
        test_params.update(params)
        
        try:
            response = requests.get(url, params=test_params, timeout=10)
            call_count += 1
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ SUCCESS! Response size: {len(response.content)} bytes")
                working_endpoints.append((name, url))
                
                # Show content type
                content_type = response.headers.get('content-type', 'unknown')
                print(f"  Content-Type: {content_type}")
                
                # Show preview
                preview = response.text[:150].replace('\n', ' ')
                print(f"  Preview: {preview}...")
                
            elif response.status_code == 400:
                error_text = response.text[:200]
                print(f"  ❌ 400 Bad Request: {error_text}")
            elif response.status_code == 403:
                print(f"  ❌ 403 Forbidden - Not included in Video + Sports plan")
            elif response.status_code == 404:
                print(f"  ❌ 404 Not Found")
            else:
                print(f"  ❌ {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ Request failed: {e}")
        
        print()
    
    print(f"🔄 API Calls Used: {call_count}/50 today")
    print()
    
    print("✅ WORKING ENDPOINTS:")
    if working_endpoints:
        for name, url in working_endpoints:
            print(f"  • {name}: {url}")
    else:
        print("  None found - may need different plan for TV schedule data")
        
    print()
    print("📋 NEXT STEPS:")
    print("1. If no TV/lineup endpoints work, you need TMS Data API access")
    print("2. Contact Gracenote to add TV schedule data to your plan")
    print("3. Or upgrade to a plan that includes TV lineup data")

if __name__ == "__main__":
    test_video_sports_apis()