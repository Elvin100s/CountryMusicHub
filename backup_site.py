#!/usr/bin/env python
"""
Country Music Paradise - Backup Script

This script creates a complete backup of your Country Music Paradise site.
It backs up both the database and song files into a single ZIP archive
that can be easily transferred to a new server.

Usage:
  python backup_site.py

The backup will be created in the 'backups' directory.
"""

import os
import shutil
import datetime
import logging
import zipfile
import subprocess
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_backup():
    """Create a complete backup of the site including database and song files."""
    # Create a timestamp for the backup filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = "backups"
    backup_filename = f"country_music_backup_{timestamp}"
    
    # Make sure the backup directory exists
    os.makedirs(backup_dir, exist_ok=True)
    
    # Full paths
    db_backup_path = os.path.join(backup_dir, f"{backup_filename}.dump")
    zip_backup_path = os.path.join(backup_dir, f"{backup_filename}.zip")
    
    try:
        # Step 1: Backup the database
        logger.info("Backing up database...")
        
        # Get database connection info from environment
        db_url = os.environ.get("DATABASE_URL", "")
        
        if "postgresql" in db_url:
            # Extract connection details (rough parsing, adjust as needed)
            db_parts = db_url.replace("postgresql://", "").replace("postgres://", "").split("@")
            if len(db_parts) == 2:
                user_pass = db_parts[0].split(":")
                host_db = db_parts[1].split("/")
                
                if len(user_pass) == 2 and len(host_db) >= 2:
                    db_user = user_pass[0]
                    # db_pass = user_pass[1]  # We don't need to use this directly
                    db_host = host_db[0].split(":")[0]
                    db_name = host_db[1].split("?")[0]
                    
                    # Create PostgreSQL dump
                    # Note: We use environment variables for password to avoid it in the command
                    cmd = ["pg_dump", "-h", db_host, "-U", db_user, "-F", "c", "-b", "-v", "-f", db_backup_path, db_name]
                    result = subprocess.run(cmd, env=os.environ, capture_output=True, text=True)
                    
                    if result.returncode != 0:
                        logger.error(f"Database backup failed: {result.stderr}")
                        return False
                    else:
                        logger.info(f"Database backup created at {db_backup_path}")
                else:
                    logger.error("Could not parse DATABASE_URL properly")
                    return False
            else:
                logger.error("Could not parse DATABASE_URL properly")
                return False
        else:
            logger.error("Only PostgreSQL databases are supported for now")
            return False
        
        # Step 2: Create a ZIP archive with everything
        logger.info("Creating complete backup archive...")
        
        with zipfile.ZipFile(zip_backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add the database dump
            zipf.write(db_backup_path, os.path.basename(db_backup_path))
            
            # Add all the song files
            music_dir = os.path.join("static", "music")
            if os.path.exists(music_dir):
                for root, _, files in os.walk(music_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Store with the relative path structure
                        zipf.write(file_path, file_path)
                        logger.debug(f"Added {file_path} to backup")
        
        logger.info(f"Backup completed successfully: {zip_backup_path}")
        logger.info(f"Total size: {os.path.getsize(zip_backup_path) / (1024*1024):.2f} MB")
        
        # Remove the temporary database dump
        os.remove(db_backup_path)
        
        return zip_backup_path
        
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Country Music Paradise backup...")
    result = create_backup()
    
    if result:
        print(f"Backup completed successfully: {result}")
        print("\nTo restore this backup on a new server:")
        print("1. Install Country Music Paradise following the README instructions")
        print("2. Extract the ZIP backup file")
        print("3. Restore the database using: pg_restore -U username -d database_name backup_file.dump")
        print("4. Copy the song files to the static/music directory")
        print("5. Run fix_paths.py to ensure all file paths are correct")
        sys.exit(0)
    else:
        print("Backup failed. Check the log for details.")
        sys.exit(1)