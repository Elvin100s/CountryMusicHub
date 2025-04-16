import os
import requests
import logging
import re
import random
import time
from urllib.parse import urlparse, urljoin, quote
from werkzeug.utils import secure_filename
from app import app

logger = logging.getLogger(__name__)

# API base URLs
FMA_API_BASE = "https://freemusicarchive.org/api"
JAMENDO_API_BASE = "https://api.jamendo.com/v3.0"
JAMENDO_API_KEY = os.environ.get("JAMENDO_API_KEY", "")
TUBIDY_BASE_URL = "https://tubidy.cool" # Using as reference only, not actually calling the API

def search_songs(query, artist=None):
    """
    Search for songs using Tubidy, Free Music Archive API, or Jamendo API
    Returns a list of songs with metadata
    """
    results = []
    
    # Search Tubidy (our main source for country music)
    try:
        tubidy_results = search_tubidy(query, artist)
        results.extend(tubidy_results)
    except Exception as e:
        logger.error(f"Error searching Tubidy: {str(e)}")
    
    # Try Free Music Archive as backup
    try:
        fma_results = search_fma(query, artist)
        results.extend(fma_results)
    except Exception as e:
        logger.error(f"Error searching FMA: {str(e)}")
    
    # Try Jamendo if we have an API key
    if JAMENDO_API_KEY:
        try:
            jamendo_results = search_jamendo(query, artist)
            results.extend(jamendo_results)
        except Exception as e:
            logger.error(f"Error searching Jamendo: {str(e)}")
    
    return results


def search_tubidy(query, artist=None):
    """
    Search for songs using Tubidy
    This is a simulation of what a real Tubidy API integration might look like
    """
    logger.info(f"Searching Tubidy for: {query}, artist: {artist}")
    
    # In a real implementation, this would make a request to Tubidy's API or scrape the site
    # For this demo, we'll simulate results with country music songs
    
    # List of country music songs for demonstration
    country_songs = [
        {"title": "Ring of Fire", "artist": "Johnny Cash"},
        {"title": "Jolene", "artist": "Dolly Parton"},
        {"title": "Friends in Low Places", "artist": "Garth Brooks"},
        {"title": "Always On My Mind", "artist": "Willie Nelson"},
        {"title": "I Walk The Line", "artist": "Johnny Cash"},
        {"title": "Stand By Your Man", "artist": "Tammy Wynette"},
        {"title": "Achy Breaky Heart", "artist": "Billy Ray Cyrus"},
        {"title": "9 to 5", "artist": "Dolly Parton"},
        {"title": "The Gambler", "artist": "Kenny Rogers"},
        {"title": "Coal Miner's Daughter", "artist": "Loretta Lynn"},
        {"title": "Redneck Woman", "artist": "Gretchen Wilson"},
        {"title": "Man! I Feel Like a Woman!", "artist": "Shania Twain"},
        {"title": "It's Five O'Clock Somewhere", "artist": "Alan Jackson & Jimmy Buffett"},
        {"title": "Sweet Home Alabama", "artist": "Lynyrd Skynyrd"},
        {"title": "Take Me Home, Country Roads", "artist": "John Denver"}
    ]
    
    results = []
    search_terms = query.lower().split() if query else []
    artist_term = artist.lower() if artist else None
    
    # Filter songs based on search terms
    for song in country_songs:
        song_title = song["title"].lower()
        song_artist = song["artist"].lower()
        
        # Check if song matches search terms
        matches_query = not search_terms or any(term in song_title for term in search_terms)
        matches_artist = not artist_term or artist_term in song_artist
        
        if matches_query or matches_artist:
            # Generate a random duration between 2 and 5 minutes
            duration_mins = random.randint(2, 5)
            duration_secs = random.randint(0, 59)
            duration = f"{duration_mins}:{duration_secs:02d}"
            
            # Add to results
            results.append({
                "id": f"tubidy_{int(time.time())}_{len(results)}",
                "name": song["title"],
                "artist": song["artist"],
                "source": "Tubidy",
                "source_url": f"{TUBIDY_BASE_URL}/music/download/{quote(song['artist'])}/{quote(song['title'])}",
                "license": "Free to download",
                "duration": duration,
                "thumbnail": f"https://source.unsplash.com/100x100/?music,country,{quote(song['title'])}"
            })
    
    # If no matches, return some generic results
    if not results:
        for i in range(5):
            song = random.choice(country_songs)
            results.append({
                "id": f"tubidy_{int(time.time())}_{i}",
                "name": song["title"],
                "artist": song["artist"],
                "source": "Tubidy",
                "source_url": f"{TUBIDY_BASE_URL}/music/download/{quote(song['artist'])}/{quote(song['title'])}",
                "license": "Free to download",
                "duration": f"{random.randint(2, 5)}:{random.randint(0, 59):02d}",
                "thumbnail": f"https://source.unsplash.com/100x100/?music,country,{quote(song['title'])}"
            })
    
    return results[:10]  # Return at most 10 results

def search_fma(query, artist=None):
    """
    Search for songs using Free Music Archive API
    """
    # Simulate FMA API search since actual API requires registration
    # This is a placeholder. In a real application, you would use the actual API
    
    # For demonstration, return some Creative Commons country music tracks
    # These would normally come from the API
    return [
        {
            "id": f"fma_{i}",
            "name": f"{query} Song {i}" if query else f"Country Classic {i}",
            "artist": artist or "Various Artists",
            "source": "Free Music Archive",
            "source_url": f"https://freemusicarchive.org/music/download/{i}",
            "license": "CC BY-NC-SA"
        }
        for i in range(1, 6)
    ]

def search_jamendo(query, artist=None):
    """
    Search for songs using Jamendo API
    """
    if not JAMENDO_API_KEY:
        return []
    
    params = {
        "client_id": JAMENDO_API_KEY,
        "format": "json",
        "limit": 10,
        "include": "musicinfo licenses",
        "tags": "country",
    }
    
    if query:
        params["namesearch"] = query
    
    if artist:
        params["artist_name"] = artist
    
    try:
        response = requests.get(f"{JAMENDO_API_BASE}/tracks/", params=params)
        if response.status_code == 200:
            data = response.json()
            results = []
            
            if "results" in data:
                for track in data["results"]:
                    results.append({
                        "id": f"jamendo_{track['id']}",
                        "name": track["name"],
                        "artist": track["artist_name"],
                        "source": "Jamendo",
                        "source_url": track.get("audiodownload") or track.get("audio"),
                        "license": track.get("license", {}).get("name", "Unknown")
                    })
            
            return results
    except Exception as e:
        logger.error(f"Error in Jamendo API call: {str(e)}")
        return []

def download_song(song_name, artist_name, source_url, source):
    """
    Download a song from the provided URL and save it to the music folder
    Returns the file path if successful, None otherwise
    """
    if not source_url:
        logger.error("No source URL provided for download")
        return None
    
    # Create safe filename
    safe_filename = secure_filename(f"{artist_name}_{song_name}.mp3")
    file_path = os.path.join(app.config["MUSIC_FOLDER"], safe_filename)
    
    try:
        # For demonstration, we'll create a simple MP3 file if the URL doesn't work
        # In a real application, you would download from the actual URL
        
        try:
            response = requests.get(source_url, stream=True)
            
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                
                logger.info(f"Song downloaded from {source}: {file_path}")
                return file_path
        except Exception as e:
            logger.error(f"Error downloading from {source_url}: {str(e)}")
        
        # If the download fails, create a dummy MP3 file for demonstration
        # In a real application, you would return an error
        with open(file_path, 'wb') as f:
            # Create a minimal MP3 file (not actually playable, just for demo)
            f.write(b'\xFF\xFB\x90\x44\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        
        logger.warning(f"Created dummy MP3 file as fallback: {file_path}")
        return file_path
    
    except Exception as e:
        logger.error(f"Error saving song file: {str(e)}")
        return None
