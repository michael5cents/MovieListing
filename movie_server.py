#!/usr/bin/env python3
"""
Movie Listings Server
Gracenote API + Clark Cinema Web Scraping
"""

from flask import Flask, jsonify, render_template_string
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

class MovieAPI:
    def __init__(self):
        self.gracenote_key = 'uk2dqjggp2qr9vzgce4a8dq7'
        self.base_url = "http://data.tmsapi.com/v1.1"
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MovieListingApp/1.0',
            'Accept': 'application/json'
        })
    
    def get_gracenote_movies(self, zip_code="36330"):
        """Get movies from Gracenote API"""
        try:
            url = f"{self.base_url}/movies/showings"
            params = {
                'api_key': self.gracenote_key,
                'startDate': datetime.now().strftime('%Y-%m-%d'),
                'zip': zip_code,
                'radius': 50
            }
            
            response = self.session.get(url, params=params, timeout=15)
            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}"}
            
            movies = response.json()
            
            # Format movie data
            movie_list = []
            for movie in movies:
                # Group showtimes by theater
                theater_times = {}
                for showing in movie.get('showtimes', []):
                    theatre = showing.get('theatre', {}).get('name', 'Unknown Theatre')
                    times = showing.get('dateTime', [])
                    # Ensure times is always an array
                    if isinstance(times, str):
                        times = [times]
                    elif not isinstance(times, list):
                        times = ['Check website for times']
                    
                    # Convert ISO times to 12-hour format
                    for time_str in times:
                        if 'T' in time_str:
                            try:
                                dt = datetime.fromisoformat(time_str)
                                formatted_time = dt.strftime('%I:%M %p').lstrip('0')
                                if theatre not in theater_times:
                                    theater_times[theatre] = []
                                theater_times[theatre].append(formatted_time)
                            except:
                                if theatre not in theater_times:
                                    theater_times[theatre] = []
                                theater_times[theatre].append(time_str)
                        else:
                            if theatre not in theater_times:
                                theater_times[theatre] = []
                            theater_times[theatre].append(time_str)
                
                # Convert to showtimes format
                showtimes = []
                for theatre, times in theater_times.items():
                    # Remove duplicates and sort times properly
                    unique_times = list(set(times))
                    
                    # Sort times by converting back to 24-hour for sorting
                    def sort_key(time_str):
                        try:
                            if 'AM' in time_str or 'PM' in time_str:
                                time_obj = datetime.strptime(time_str, '%I:%M %p')
                                return time_obj.strftime('%H:%M')
                            return time_str
                        except:
                            return time_str
                    
                    sorted_times = sorted(unique_times, key=sort_key)
                    
                    if sorted_times:
                        showtimes.append({
                            'theatre': theatre,
                            'times': sorted_times[:10]  # Limit times
                        })
                
                movie_list.append({
                    'title': movie.get('title', 'Unknown'),
                    'year': movie.get('releaseYear', ''),
                    'rating': movie.get('ratings', [{}])[0].get('code', 'NR') if movie.get('ratings') else 'NR',
                    'runtime': movie.get('runTime', ''),
                    'genres': movie.get('genres', []),
                    'showtimes': showtimes
                })
            
            return {
                'source': 'Gracenote TMS API',
                'total': len(movie_list),
                'movies': movie_list
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def scrape_clark_cinema(self):
        """Scrape Clark Cinemas Enterprise website"""
        try:
            # Clark Cinemas Enterprise website URL
            url = "https://enterprise.clarkcinemas.com/home"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
            }
            
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_text = soup.get_text()
            
            movies = []
            
            # Enhanced parsing to extract movie details and potentially showtimes
            movie_data = {
                "3D Fantastic Four: First Steps": {"rating": "PG-13", "runtime": "1 hr 55 min", "genre": "Science Fiction"},
                "Fantastic Four: First Steps": {"rating": "PG-13", "runtime": "1 hr 55 min", "genre": "Science Fiction"},
                "Smurfs": {"rating": "PG", "runtime": "1 hr 32 min", "genre": "Animation"},
                "I Know What You Did Last Summer": {"rating": "R", "runtime": "1 hr 51 min", "genre": "Horror"},
                "Superman": {"rating": "PG-13", "runtime": "2 hr 10 min", "genre": "Action"},
                "Jurassic World Rebirth": {"rating": "PG-13", "runtime": "2 hr 14 min", "genre": "Science Fiction"},
                "F1": {"rating": "PG-13", "runtime": "2 hr 36 min", "genre": "Action"},
                "How to Train Your Dragon": {"rating": "PG", "runtime": "2 hr 5 min", "genre": "Action"}
            }
            
            # Look for showtimes patterns in the HTML/text
            import re
            
            # Try to find time patterns (like 7:30 PM, 2:15 PM, etc.)
            time_patterns = re.findall(r'\b(?:1[0-2]|[1-9]):[0-5][0-9]\s*(?:AM|PM|am|pm)\b', page_text)
            
            # Also try to find movie sections that might contain showtimes
            # Look for script tags or data attributes that might contain showtime data
            scripts = soup.find_all('script')
            showtime_data = {}
            
            for script in scripts:
                if script.string:
                    script_content = script.string
                    # Look for JSON data or showtime patterns in scripts
                    if 'showtime' in script_content.lower() or 'movie' in script_content.lower():
                        # Try to extract time patterns from scripts
                        script_times = re.findall(r'\b(?:1[0-2]|[1-9]):[0-5][0-9]\s*(?:AM|PM|am|pm)\b', script_content)
                        if script_times:
                            time_patterns.extend(script_times)
            
            # Process each known movie
            for title, details in movie_data.items():
                if title.lower() in page_text.lower():
                    # Extract any showtimes that might be associated with this movie
                    showtimes = []
                    
                    if time_patterns:
                        # Clean up and format the times properly
                        formatted_times = []
                        for time_str in time_patterns[:5]:  # Limit to 5 times
                            # Ensure proper AM/PM formatting with space
                            if 'AM' in time_str.upper() or 'PM' in time_str.upper():
                                time_clean = time_str.upper().replace('AM', ' AM').replace('PM', ' PM')
                                time_clean = ' '.join(time_clean.split())  # Clean extra spaces
                                if time_clean not in formatted_times:
                                    formatted_times.append(time_clean)
                        
                        if formatted_times:
                            showtimes = [{
                                'theatre': 'Clark Cinemas - Enterprise',
                                'times': formatted_times
                            }]
                    
                    # Fallback if no specific times found
                    if not showtimes:
                        showtimes = [{
                            'theatre': 'Clark Cinemas - Enterprise',
                            'times': ['Call (334) 347-3811 for showtimes']
                        }]
                    
                    movies.append({
                        'title': title,
                        'year': 2025,
                        'rating': details['rating'],
                        'runtime': details['runtime'],
                        'genres': [details['genre']],
                        'showtimes': showtimes
                    })
            
            # Try alternative approach: look for structured data or API endpoints
            if not any('AM' in str(movie.get('showtimes', [])) or 'PM' in str(movie.get('showtimes', [])) for movie in movies):
                # Check if there are any data attributes or hidden elements with showtime info
                showtime_elements = soup.find_all(attrs={'data-showtime': True}) or soup.find_all(class_=lambda x: x and 'time' in x.lower())
                
                if showtime_elements:
                    extracted_times = []
                    for elem in showtime_elements:
                        elem_text = elem.get_text() or elem.get('data-showtime', '')
                        times = re.findall(r'\b(?:1[0-2]|[1-9]):[0-5][0-9]\s*(?:AM|PM|am|pm)\b', elem_text)
                        extracted_times.extend(times)
                    
                    if extracted_times:
                        # Update movies with extracted times
                        for movie in movies:
                            movie['showtimes'] = [{
                                'theatre': 'Clark Cinemas - Enterprise',
                                'times': extracted_times[:5]  # Limit to 5 times per movie
                            }]
            
            return {
                'source': 'Clark Cinemas - Enterprise Website',
                'total': len(movies),
                'movies': movies,
                'note': 'For exact showtimes visit https://enterprise.clarkcinemas.com or call (334) 347-3811'
            }
            
        except Exception as e:
            return {
                'error': f"Could not scrape Clark Cinemas: {str(e)}",
                'source': 'Clark Cinemas - Enterprise',
                'movies': []
            }

movie_api = MovieAPI()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Movie Listings - Dothan Area</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header { 
            background: linear-gradient(135deg, #2C3E50 0%, #3498DB 100%); 
            color: white; 
            padding: 40px 30px; 
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
            opacity: 0.1;
        }
        
        .header h1 { 
            font-size: 3em; 
            margin-bottom: 10px; 
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            position: relative;
            z-index: 1;
        }
        
        .header p { 
            font-size: 1.2em; 
            opacity: 0.9;
            position: relative;
            z-index: 1;
        }
        
        .refresh-btn { 
            background: rgba(255,255,255,0.2); 
            color: white; 
            padding: 12px 25px; 
            border: 2px solid rgba(255,255,255,0.3);
            border-radius: 25px; 
            cursor: pointer; 
            font-size: 16px;
            margin-top: 20px;
            transition: all 0.3s ease;
            position: relative;
            z-index: 1;
        }
        
        .refresh-btn:hover { 
            background: rgba(255,255,255,0.3);
            border-color: rgba(255,255,255,0.5);
            transform: translateY(-2px);
        }
        
        .content { padding: 40px 30px; }
        
        .theater-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 30px;
        }
        
        .theater-section { 
            background: white;
            border-radius: 15px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .theater-section:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.12);
        }
        
        .theater-header { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 25px;
            font-size: 1.5em; 
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .gracenote .theater-header { 
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
        }
        
        .clark-cinema .theater-header { 
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%); 
        }
        
        .theater-content { padding: 25px; }
        
        .source-info {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #007bff;
        }
        
        .movie-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .movie { 
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-radius: 12px; 
            padding: 20px;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .movie:hover {
            border-color: #007bff;
            box-shadow: 0 8px 20px rgba(0,123,255,0.1);
            transform: translateY(-2px);
        }
        
        .movie-title { 
            font-size: 1.4em; 
            font-weight: 700; 
            color: #2c3e50;
            margin-bottom: 8px;
            line-height: 1.3;
        }
        
        .movie-details {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .detail-badge {
            background: #e9ecef;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            color: #495057;
            font-weight: 500;
        }
        
        .rating-badge {
            background: #28a745;
            color: white;
        }
        
        .year-badge {
            background: #17a2b8;
            color: white;
        }
        
        .runtime-badge {
            background: #6f42c1;
            color: white;
        }
        
        .genres {
            margin-bottom: 15px;
        }
        
        .genre-tag {
            display: inline-block;
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin: 2px;
            color: #495057;
        }
        
        .showtimes-section {
            border-top: 1px solid #e9ecef;
            padding-top: 15px;
        }
        
        .showtime-group {
            margin-bottom: 12px;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .theater-name { 
            font-weight: 600; 
            color: #2c3e50;
            margin-bottom: 5px;
            font-size: 0.95em;
        }
        
        .times { 
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }
        
        .time-slot {
            background: #007bff;
            color: white;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 500;
        }
        
        .error { 
            color: #721c24; 
            background: #f8d7da; 
            padding: 15px; 
            border-radius: 8px;
            border: 1px solid #f5c6cb;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-size: 1.1em;
        }
        
        .loading::after {
            content: '';
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #007bff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-left: 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2em; }
            .content { padding: 20px; }
            .movie-grid { grid-template-columns: 1fr; }
            .movie-details { flex-direction: column; gap: 8px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Movie Listings</h1>
            <p>Current movies showing in Dothan area theaters</p>
            <button class="refresh-btn" onclick="location.reload()">🔄 Refresh Listings</button>
        </div>
        
        <div class="content">
            <div class="theater-grid">
                <div class="theater-section gracenote">
                    <div class="theater-header">
                        🎭 AMC Theaters (Gracenote API)
                    </div>
                    <div class="theater-content">
                        <div id="gracenote-movies" class="loading">Loading movie data...</div>
                    </div>
                </div>
                
                <div class="theater-section clark-cinema">
                    <div class="theater-header">
                        🎪 Clark Cinemas - Enterprise
                    </div>
                    <div class="theater-content">
                        <div id="clark-movies" class="loading">Loading Clark Cinemas data...</div>
                    </div>
                </div>
                
            </div>
        </div>
    </div>

    <script>
        async function loadMovies() {
            try {
                // Load Gracenote movies (AMC theaters)
                const gracenoteResponse = await fetch('/api/gracenote-movies');
                const gracenoteData = await gracenoteResponse.json();
                displayGracenoteMovies(gracenoteData);
                
                // Load Clark Cinemas movies
                const clarkResponse = await fetch('/api/clark-movies');
                const clarkData = await clarkResponse.json();
                displayClarkMovies(clarkData);
                
            } catch (error) {
                console.error('Error loading movies:', error);
                document.getElementById('gracenote-movies').innerHTML = 
                    '<div class="error">❌ Error loading movie data. Please refresh the page.</div>';
            }
        }
        
        function displayGracenoteMovies(data) {
            const container = document.getElementById('gracenote-movies');
            container.className = '';  // Remove loading class
            
            if (data.error) {
                container.innerHTML = `<div class="error">❌ Error loading data: ${data.error}</div>`;
                return;
            }
            
            let html = `
                <div class="source-info">
                    <strong>📡 Source:</strong> ${data.source} | 
                    <strong>🎬 Total Movies:</strong> ${data.total}
                </div>
                <div class="movie-grid">
            `;
            
            data.movies.forEach(movie => {
                html += `
                    <div class="movie">
                        <div class="movie-title">${movie.title}</div>
                        
                        <div class="movie-details">
                            ${movie.year ? `<span class="detail-badge year-badge">${movie.year}</span>` : ''}
                            ${movie.rating ? `<span class="detail-badge rating-badge">${movie.rating}</span>` : ''}
                            ${movie.runtime ? `<span class="detail-badge runtime-badge">${formatRuntime(movie.runtime)}</span>` : ''}
                        </div>
                        
                        ${movie.genres && movie.genres.length ? `
                            <div class="genres">
                                ${movie.genres.map(genre => `<span class="genre-tag">${genre}</span>`).join('')}
                            </div>
                        ` : ''}
                        
                        <div class="showtimes-section">
                `;
                
                movie.showtimes.forEach(showing => {
                    const times = Array.isArray(showing.times) ? showing.times : [showing.times || 'Check website for times'];
                    html += `
                        <div class="showtime-group">
                            <div class="theater-name">🎭 ${showing.theatre}</div>
                            <div class="times">
                                ${times.map(time => `<span class="time-slot">${time}</span>`).join('')}
                            </div>
                        </div>
                    `;
                });
                
                html += `</div></div>`;
            });
            
            html += `</div>`;
            container.innerHTML = html;
        }
        
        function displayClarkMovies(data) {
            const container = document.getElementById('clark-movies');
            container.className = '';  // Remove loading class
            
            if (data.error) {
                container.innerHTML = `<div class="error">❌ Error loading data: ${data.error}</div>`;
                return;
            }
            
            let html = `
                <div class="source-info">
                    <strong>📡 Source:</strong> ${data.source} | 
                    <strong>🎬 Total Movies:</strong> ${data.total}
                </div>
            `;
            
            if (data.note) {
                html += `<div class="source-info" style="border-left-color: #FF9800;"><em>ℹ️ ${data.note}</em></div>`;
            }
            
            html += `<div class="movie-grid">`;
            
            data.movies.forEach(movie => {
                html += `
                    <div class="movie">
                        <div class="movie-title">${movie.title}</div>
                        
                        <div class="showtimes-section">
                `;
                
                movie.showtimes.forEach(showing => {
                    const times = Array.isArray(showing.times) ? showing.times : [showing.times || 'Check website for times'];
                    html += `
                        <div class="showtime-group">
                            <div class="theater-name">🎪 ${showing.theatre}</div>
                            <div class="times">
                                ${times.map(time => `<span class="time-slot" style="background: #FF9800;">${time}</span>`).join('')}
                            </div>
                        </div>
                    `;
                });
                
                html += `</div></div>`;
            });
            
            html += `</div>`;
            container.innerHTML = html;
        }
        
        function formatRuntime(runtime) {
            if (!runtime) return '';
            
            // Handle PT format (e.g., "PT02H14M")
            if (runtime.startsWith('PT')) {
                const match = runtime.match(/PT(?:(\\d+)H)?(?:(\\d+)M)?/);
                if (match) {
                    const hours = match[1] ? parseInt(match[1]) : 0;
                    const minutes = match[2] ? parseInt(match[2]) : 0;
                    if (hours && minutes) {
                        return `${hours}h ${minutes}m`;
                    } else if (hours) {
                        return `${hours}h`;
                    } else if (minutes) {
                        return `${minutes}m`;
                    }
                }
            }
            
            // Return as-is if not PT format
            return runtime;
        }
        
        // Load movies when page loads
        loadMovies();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return HTML_TEMPLATE

@app.route('/api/gracenote-movies')
def gracenote_movies():
    return jsonify(movie_api.get_gracenote_movies())

@app.route('/api/clark-movies')
def clark_movies():
    return jsonify(movie_api.scrape_clark_cinema())

if __name__ == '__main__':
    print("🎬 MOVIE LISTINGS SERVER")
    print("=" * 40)
    print("✅ Gracenote API integration")
    print("✅ Clark Cinema web scraping")
    print("✅ Combined movie listings")
    print()
    print("Server starting at: http://localhost:8001")
    print("Press Ctrl+C to stop")
    
    app.run(debug=True, host='0.0.0.0', port=8001)