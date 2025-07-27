#!/usr/bin/env python3
"""
Test what Gracenote API endpoints your key can access
"""

import requests

def test_api_permissions():
    api_key = 'uk2dqjggp2qr9vzgce4a8dq7'
    base_url = "http://data.tmsapi.com/v1.1"
    
    print("🔍 TESTING API PERMISSIONS")
    print("=" * 40)
    print(f"API Key: {api_key}")
    print()
    
    # Test different endpoints to see what works
    test_endpoints = [
        # Basic endpoints
        ("Root API", f"{base_url}/", {}),
        ("Lineups (no extension)", f"{base_url}/lineups", {'country': 'USA', 'postalCode': '90210'}),
        ("Lineups (.xml)", f"{base_url}/lineups.xml", {'country': 'USA', 'postalCode': '90210'}),
        
        # Try different regions
        ("Movies", f"{base_url}/movies.xml", {}),
        ("Programs", f"{base_url}/programs.xml", {}),
        ("Sports", f"{base_url}/sports.xml", {}),
        
        # Try with different parameters
        ("Lineups Canada", f"{base_url}/lineups.xml", {'country': 'CAN', 'postalCode': 'M5H'}),
        ("Lineups minimal", f"{base_url}/lineups", {'country': 'USA'}),
    ]
    
    working_endpoints = []
    
    for name, url, params in test_endpoints:
        print(f"Testing {name}:")
        print(f"  URL: {url}")
        
        test_params = {'api_key': api_key}
        test_params.update(params)
        
        try:
            response = requests.get(url, params=test_params, timeout=8)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ SUCCESS! Response length: {len(response.content)}")
                working_endpoints.append((name, url, params))
                
                # Show a sample of the response
                content_preview = response.text[:200].replace('\n', ' ')
                print(f"  Preview: {content_preview}...")
                
            elif response.status_code == 400:
                print(f"  ❌ 400 Bad Request - {response.text[:100]}")
            elif response.status_code == 401:
                print(f"  ❌ 401 Unauthorized - Invalid API key")
            elif response.status_code == 403:
                print(f"  ❌ 403 Forbidden - No permission for this endpoint")
            elif response.status_code == 404:
                print(f"  ❌ 404 Not Found - Endpoint doesn't exist")
            elif response.status_code == 500:
                print(f"  ❌ 500 Server Error - {response.text[:100]}")
            else:
                print(f"  ❌ {response.status_code} - {response.text[:100]}")
                
        except Exception as e:
            print(f"  ❌ Request failed: {e}")
        
        print()
    
    print("🎯 WORKING ENDPOINTS:")
    if working_endpoints:
        for name, url, params in working_endpoints:
            print(f"  ✅ {name}: {url}")
    else:
        print("  ❌ No working endpoints found")
        print()
        print("🔧 TROUBLESHOOTING:")
        print("  1. Check if your API key needs activation in Gracenote dashboard")
        print("  2. Verify you accepted Terms of Service for TMS Data APIs")
        print("  3. Confirm your plan includes TV lineup data")
        print("  4. Check if you need to verify your email address")

if __name__ == "__main__":
    test_api_permissions()