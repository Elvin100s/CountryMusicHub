#!/usr/bin/env python
"""
Bulk Song Upload Script for Country Music Paradise

This script allows for offline bulk upload of music files to the database.
It walks through a directory structure and adds songs to matching artists.

Usage:
  python bulk_upload.py /path/to/music_directory

Directory structure should be:
  /music_directory
    /Artist Name 1
      - Song Name 1.mp3
      - Song Name 2.mp3
    /Artist Name 2
      - Song Name 3.mp3
"""

import os
import sys
import logging
import shutil
from app import app, db
from models import Artist, Song

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_filename(filename):
    """Extract song name from filename by removing extension and cleaning it up."""
    # Remove extension
    song_name = os.path.splitext(filename)[0]
    # Remove track numbers if present (like "01 - " or "01.")
    if song_name[0:2].isdigit() and (song_name[2:4] == " -" or song_name[2] == "."):
        song_name = song_name[4:].strip() if song_name[2:4] == " -" else song_name[3:].strip()
    return song_name

def process_directory(music_dir):
    """Process the music directory and add songs to the database."""
    if not os.path.isdir(music_dir):
        logger.error(f"Directory not found: {music_dir}")
        return False
    
    # Get all artists from the database
    artists = {artist.name.lower(): artist for artist in Artist.query.all()}
    
    # Ensure music folder exists
    music_folder = app.config.get('MUSIC_FOLDER', 'static/music')
    os.makedirs(music_folder, exist_ok=True)
    
    success_count = 0
    error_count = 0
    
    # Walk through the directory
    for root, dirs, files in os.walk(music_dir):
        # Get the artist name from the directory name
        artist_name = os.path.basename(root)
        
        # Skip the root directory itself
        if artist_name == os.path.basename(music_dir):
            continue
        
        # Check if the artist exists
        artist = artists.get(artist_name.lower())
        if not artist:
            logger.warning(f"Artist not found: {artist_name}. Skipping songs.")
            continue
        
        logger.info(f"Processing songs for artist: {artist_name}")
        
        # Process each music file
        for filename in files:
            if not filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
                continue  # Skip non-music files
            
            song_name = clean_filename(filename)
            file_path = os.path.join(root, filename)
            
            # Check if song already exists
            existing_song = Song.query.filter_by(name=song_name, artist_id=artist.id).first()
            if existing_song:
                logger.warning(f"Song already exists: {song_name} for {artist_name}. Skipping.")
                continue
            
            try:
                # Copy file to music folder
                destination = os.path.join(music_folder, f"{artist_name}_{filename}")
                shutil.copy2(file_path, destination)
                
                # Create song record
                new_song = Song(
                    name=song_name,
                    artist_id=artist.id,
                    file_path=destination,
                    source='bulk_upload'
                )
                
                db.session.add(new_song)
                success_count += 1
                logger.info(f"Added song: {song_name} for {artist_name}")
            except Exception as e:
                logger.error(f"Error processing {file_path}: {str(e)}")
                error_count += 1
    
    # Commit all changes
    if success_count > 0:
        db.session.commit()
    
    logger.info(f"Bulk upload complete. Added {success_count} songs. Errors: {error_count}")
    return True

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/music_directory")
        sys.exit(1)
    
    music_dir = sys.argv[1]
    
    with app.app_context():
        if process_directory(music_dir):
            print(f"Successfully processed directory: {music_dir}")
        else:
            print(f"Failed to process directory: {music_dir}")
            sys.exit(1)