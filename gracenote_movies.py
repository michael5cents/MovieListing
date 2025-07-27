#!/usr/bin/env python3
"""
Gracenote Movie Listings
Using your working Video + Sports API plan
"""

import requests
from datetime import datetime, timedelta
import json

class GracenoteMovieAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://data.tmsapi.com/v1.1"
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MovieListingApp/1.0',
            'Accept': 'application/json'
        })
    
    def get_movie_showings(self, zip_code="90210", date_str=None, radius=50):
        """
        Get movie theater showings in an area
        This endpoint works with your Video + Sports plan
        """
        if not date_str:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        try:
            url = f"{self.base_url}/movies/showings"
            params = {
                'api_key': self.api_key,
                'startDate': date_str,
                'zip': zip_code,
                'radius': radius
            }
            
            print(f"🎬 Getting movie showings for {zip_code} on {date_str}...")
            response = self.session.get(url, params=params, timeout=15)
            
            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}: {response.text[:200]}"}
            
            movies = response.json()
            print(f"Found {len(movies)} movies")
            
            # Parse and organize movie data
            movie_list = []
            for movie in movies:
                title = movie.get('title', 'Unknown Movie')
                year = movie.get('releaseYear', '')
                rating = movie.get('ratings', [{}])[0].get('code', 'NR') if movie.get('ratings') else 'NR'
                runtime = movie.get('runTime', '')
                genres = movie.get('genres', [])
                
                # Get showtimes
                showtimes = []
                for showing in movie.get('showtimes', []):
                    theatre = showing.get('theatre', {}).get('name', 'Unknown Theatre')
                    times = showing.get('dateTime', [])
                    if times:
                        showtimes.append({
                            'theatre': theatre,
                            'times': times
                        })
                
                movie_list.append({
                    'title': title,
                    'year': year,
                    'rating': rating,
                    'runtime': runtime,
                    'genres': genres,
                    'tms_id': movie.get('tmsId', ''),
                    'showtimes': showtimes
                })
            
            return {
                'date': date_str,
                'zip_code': zip_code,
                'total_movies': len(movie_list),
                'movies': movie_list,
                'source': 'Gracenote TMS API'
            }
            
        except Exception as e:
            return {"error": f"Request failed: {str(e)}"}
    
    def display_movie_listings(self, zip_code="90210", max_movies=20):
        """
        Display formatted movie listings
        """
        result = self.get_movie_showings(zip_code)
        
        if result.get('error'):
            print(f"❌ Error: {result['error']}")
            return
        
        print(f"\n🎬 MOVIE LISTINGS FOR {zip_code}")
        print("=" * 60)
        print(f"Date: {result['date']}")
        print(f"Source: {result['source']}")
        print(f"Total Movies: {result['total_movies']}")
        print()
        
        movies = result['movies'][:max_movies]
        
        for i, movie in enumerate(movies, 1):
            print(f"{i:2d}. {movie['title']}")
            
            # Movie details
            details = []
            if movie['year']:
                details.append(f"({movie['year']})")
            if movie['rating']:
                details.append(f"Rated {movie['rating']}")
            if movie['runtime']:
                details.append(f"{movie['runtime']} min")
            if movie['genres']:
                details.append(f"Genres: {', '.join(movie['genres'][:3])}")
            
            if details:
                print(f"    {' | '.join(details)}")
            
            # Show theaters and times
            if movie['showtimes']:
                print(f"    Showtimes:")
                for showing in movie['showtimes'][:3]:  # Show first 3 theaters
                    theatre = showing['theatre']
                    times = showing['times'][:5]  # Show first 5 times
                    if times:
                        times_str = ', '.join(times)
                        print(f"      {theatre}: {times_str}")
            else:
                print(f"    No showtimes available")
            
            print()

def main():
    print("🎬 GRACENOTE MOVIE LISTINGS")
    print("=" * 40)
    
    api_key = 'uk2dqjggp2qr9vzgce4a8dq7'
    movie_api = GracenoteMovieAPI(api_key)
    
    # Get movie listings for your area
    zip_codes = ['36330']  # Your zip code
    
    for zip_code in zip_codes:
        movie_api.display_movie_listings(zip_code, max_movies=10)
        print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()