# Movie Listings - Dothan Area

A professional movie listings website that displays current movies and showtimes for theaters in the Dothan, Alabama area.

## Features

- 🎬 **Real-time Movie Data**: Uses Gracenote TMS API for accurate AMC theater listings
- 🎪 **Clark Cinemas Integration**: Scrapes Clark Cinemas - Enterprise website for current movies
- 📱 **Responsive Design**: Professional, mobile-friendly interface
- ⏰ **Formatted Showtimes**: Clean 12-hour time format with organized theater groupings
- 🔄 **Live Updates**: Refresh button to get latest movie data

## Theaters Included

- **AMC Dothan Pavilion 12** - Full showtimes via Gracenote API
- **AMC Dothan 6** - Full showtimes via Gracenote API  
- **Clark Cinemas - Enterprise** - Full movie listings with actual showtimes via web scraping

## Installation

1. Clone the repository:
```bash
git clone https://github.com/michael5cents/MovieListing.git
cd MovieListing
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Gracenote API key:
   - Sign up at [Gracenote Developer Portal](https://developer.gracenote.com/)
   - Update the API key in `movie_server.py`

## Usage

1. Start the server:
```bash
source venv/bin/activate
python3 movie_server.py
```

2. Open your browser to:
   - `http://localhost:8001` or
   - `http://[your-ip]:8001`

## API Endpoints

- `GET /` - Main movie listings page
- `GET /api/gracenote-movies` - JSON data for AMC theaters
- `GET /api/clark-movies` - JSON data for Clark Cinemas

## Technologies Used

- **Backend**: Python Flask
- **Data Sources**: Gracenote TMS API, Web Scraping
- **Frontend**: HTML5, CSS3, JavaScript
- **Libraries**: BeautifulSoup, Requests

## Configuration

The app is configured for zip code 36330 (Dothan, AL area). To change location:
1. Update the zip code in the `get_gracenote_movies()` method
2. Modify the Clark Cinemas URL if needed

## Data Sources

- **AMC Theaters**: Real-time data via Gracenote TMS API
- **Clark Cinemas**: Live showtimes scraped from https://enterprise.clarkcinemas.com

## License

This project is for educational and personal use.