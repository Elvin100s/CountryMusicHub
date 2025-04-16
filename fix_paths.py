#!/usr/bin/env python
"""
Fix Song File Paths

This script fixes the file paths in the database after restoring a backup
to a new server. It ensures that all songs in the database point to the
correct location in the static/music directory.

Usage:
  python fix_paths.py

If song paths were stored with absolute paths, this script will convert them
to relative paths within the static/music directory.
"""

import os
import logging
from app import app, db
from models import Song

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_song_paths():
    """Update song file paths to ensure they point to the correct location."""
    with app.app_context():
        # Get all songs from the database
        songs = Song.query.all()
        logger.info(f"Found {len(songs)} songs in the database")
        
        fixed_count = 0
        music_folder = app.config.get('MUSIC_FOLDER', 'static/music')
        
        # Make sure the music folder exists
        os.makedirs(music_folder, exist_ok=True)
        
        for song in songs:
            old_path = song.file_path
            
            # Get just the filename from the path
            filename = os.path.basename(old_path)
            
            # Create the new correct path
            new_path = os.path.join(music_folder, filename)
            
            # Check if the path needs to be updated
            if old_path != new_path:
                logger.info(f"Updating path for '{song.name}' by '{song.artist.name}'")
                logger.info(f"  Old path: {old_path}")
                logger.info(f"  New path: {new_path}")
                
                # Update the path in the database
                song.file_path = new_path
                fixed_count += 1
        
        # Commit the changes if any paths were fixed
        if fixed_count > 0:
            db.session.commit()
            logger.info(f"Fixed {fixed_count} song paths")
        else:
            logger.info("All song paths are already correct")
        
        return fixed_count

if __name__ == "__main__":
    print("Starting path correction...")
    count = fix_song_paths()
    print(f"Path correction complete. Fixed {count} song paths.")
    print("Your database now has the correct paths for all songs.")