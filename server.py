#!/usr/bin/env python3
"""
Official Network TV Schedule Server
Fetches accurate, date-driven schedules from official network sources
NO FAKE DATA - Only verified official programming
"""

from flask import Flask, jsonify, send_from_directory
from datetime import datetime, timedelta
import requests
import re
from urllib.parse import urljoin
from comprehensive_api import ComprehensiveTVAPI

app = Flask(__name__)

# Initialize comprehensive API
tv_api = ComprehensiveTVAPI()

def get_official_nbc_schedule(date_str):
    """
    Fetch official NBC schedule using comprehensive API
    ZERO FAKE DATA - Only verified sources
    """
    return tv_api.get_guaranteed_schedule('nbc', date_str)

def get_official_abc_schedule(date_str):
    """
    Fetch official ABC schedule using comprehensive API
    ZERO FAKE DATA - Only verified sources
    """
    return tv_api.get_guaranteed_schedule('abc', date_str)

def get_official_cbs_schedule(date_str):
    """
    Fetch official CBS schedule using comprehensive API
    ZERO FAKE DATA - Only verified sources
    """
    return tv_api.get_guaranteed_schedule('cbs', date_str)

def get_official_fox_schedule(date_str):
    """
    Fetch official FOX schedule using comprehensive API
    ZERO FAKE DATA - Only verified sources
    """
    return tv_api.get_guaranteed_schedule('fox', date_str)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/schedule/<network>/<date>')
def get_schedule(network, date):
    """
    API endpoint to get official network schedule for specific date
    Only returns verified data from official sources
    """
    try:
        # Validate date format
        datetime.strptime(date, '%Y-%m-%d')
        
        # Route to appropriate network function
        if network.lower() == 'nbc':
            result = get_official_nbc_schedule(date)
        elif network.lower() == 'abc':
            result = get_official_abc_schedule(date)
        elif network.lower() == 'cbs':
            result = get_official_cbs_schedule(date)
        elif network.lower() == 'fox':
            result = get_official_fox_schedule(date)
        else:
            return jsonify({
                "error": f"Unsupported network: {network}",
                "supported_networks": ["nbc", "abc", "cbs", "fox"]
            }), 400
        
        return jsonify(result)
        
    except ValueError:
        return jsonify({
            "error": "Invalid date format. Use YYYY-MM-DD"
        }), 400
    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/api/current-time')
def get_current_time():
    """Get current Eastern Time (network standard)"""
    from datetime import timezone, timedelta
    
    eastern_tz = timezone(timedelta(hours=-5))  # EST
    current = datetime.now(eastern_tz)
    
    return jsonify({
        'time': current.strftime('%I:%M %p'),
        'date': current.strftime('%B %d, %Y'),
        'timezone': 'Eastern Time'
    })

if __name__ == '__main__':
    print("="*50)
    print("OFFICIAL NETWORK TV SCHEDULE SERVER")
    print("="*50)
    print("✓ No fake data - only verified official sources")
    print("✓ Date-driven schedules from network websites")
    print("✓ NBC, ABC, CBS, FOX national programming")
    print()
    print("Server starting at: http://localhost:8000")
    print("Press Ctrl+C to stop")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=8000)