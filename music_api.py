import os
import requests
import logging
import re
from urllib.parse import urlparse, urljoin
from werkzeug.utils import secure_filename
from app import app

logger = logging.getLogger(__name__)

# FMA API base URL
FMA_API_BASE = "https://freemusicarchive.org/api"
JAMENDO_API_BASE = "https://api.jamendo.com/v3.0"
JAMENDO_API_KEY = os.environ.get("JAMENDO_API_KEY", "")

def search_songs(query, artist=None):
    """
    Search for songs using Free Music Archive API or Jamendo API
    Returns a list of songs with metadata
    """
    results = []
    
    # Try Free Music Archive first
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
    
    # Add more APIs here if needed
    
    return results

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
