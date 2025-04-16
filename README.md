# Country Music Paradise

A beautiful website to browse, play, and download free, legal country music featuring legendary artists like Bryan Adams, Dolly Parton, and many more. No registration required!

![Country Music Paradise Screenshot](static/img/screenshot.png)

## Features

- **No Login Required**: Listen to and download music without creating an account
- **Country Music Legends**: Browse music from artists like Bryan Adams, Kenny Rogers, Dolly Parton, and more
- **Upload Music**: Upload your own MP3 files directly to any artist's collection (multiple files at once)
- **Smart Upload**: Song titles are automatically extracted from filenames
- **Tubidy Integration**: Search and add songs from Tubidy and other free music sources
- **Mobile-Friendly**: Works on all modern browsers including mobile devices
- **Backup & Restore**: Easily backup and restore your entire song collection when moving servers
- **Modern Design**: Beautiful interface with a focus on usability

## How to Run Locally

### Prerequisites

- Python 3.7+
- PostgreSQL database

### Installation Steps

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/country-music-paradise.git
   cd country-music-paradise
   ```

2. Set up a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install Flask==2.3.3 Flask-Login==0.6.2 Flask-SQLAlchemy==3.1.1 gunicorn==23.0.0 
   pip install psycopg2-binary==2.9.9 requests==2.31.0 SQLAlchemy==2.0.23 Werkzeug==2.3.7
   pip install email-validator==2.0.0 trafilatura==1.6.1
   ```
   
   Alternatively, create a requirements.txt file with the following content:
   ```
   email-validator==2.0.0
   Flask==2.3.3
   Flask-Login==0.6.2
   Flask-SQLAlchemy==3.1.1
   gunicorn==23.0.0
   psycopg2-binary==2.9.9
   requests==2.31.0
   SQLAlchemy==2.0.23
   trafilatura==1.6.1
   Werkzeug==2.3.7
   ```
   
   And install using:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a PostgreSQL database
   - Set the `DATABASE_URL` environment variable:
     ```
     export DATABASE_URL=postgresql://username:password@localhost/country_music
     ```

5. Initialize the database:
   ```
   python reset_db.py
   ```

6. Run the application:
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

7. Open a browser and go to `http://localhost:5000`

## Hosting on a Server

### Option 1: Hosting on a VPS or Dedicated Server

1. Deploy the code to your server
2. Install PostgreSQL and create a database
3. Install the application dependencies
4. Set up the `DATABASE_URL` environment variable
5. Run the database initialization script
6. Use Gunicorn behind Nginx for production:
   ```
   gunicorn --bind 0.0.0.0:5000 --workers=3 main:app
   ```

### Option 2: Hosting on PythonAnywhere

1. Upload the project files to PythonAnywhere
2. Create a PostgreSQL database
3. Set the `DATABASE_URL` environment variable
4. Create a web app with manual configuration pointing to `main.py`
5. Set the WSGI configuration file to use Flask with your `app` object

### Option 3: Hosting on Heroku

1. Create a `Procfile` with:
   ```
   web: gunicorn main:app
   ```
2. Commit the project to Git
3. Create a Heroku app
4. Set up a PostgreSQL add-on
5. Deploy your project to Heroku
6. Run initialization:
   ```
   heroku run python reset_db.py
   ```

## Adding Songs to the Collection

### Method 1: Web Interface Upload

1. Navigate to any artist's page
2. Click the "Upload From Computer" button
3. Select a file (or multiple files) from your device
4. The song title will be automatically extracted from the filename
5. Click "Upload" to add the song to the collection

### Method 2: Offline Bulk Upload

The site includes a powerful bulk upload script that can process entire directories of music files organized by artist:

1. Organize your MP3 files in a directory structure:
   ```
   /music_to_add
     /Bryan Adams
       - Summer of 69.mp3
       - Everything I Do.mp3
     /Kenny Rogers
       - The Gambler.mp3
   ```

2. Use the included bulk upload script:
   ```bash
   python bulk_upload.py /path/to/music_to_add
   ```

3. The script will:
   - Match directory names to artists in the database
   - Extract song titles from filenames automatically
   - Copy all files to the correct location
   - Add all songs to the database
   - Skip any duplicates automatically

## Backing Up and Restoring Your Music Collection

When you download the code as a ZIP file, it will NOT include your database or uploaded songs. Follow these steps to backup and restore your music collection:

### Backing Up Songs and Database

#### Method 1: Using the Automatic Backup Script (Recommended)

1. Simply run the backup script:
   ```bash
   python backup_site.py
   ```

2. The script will:
   - Create a backup of your PostgreSQL database
   - Archive all your song files
   - Package everything in a timestamped ZIP file in the `backups` directory
   - Provide instructions for restoring

#### Method 2: Manual Backup

1. **Back up your song files**:
   - All uploaded songs are stored in the `static/music` directory
   - Download or copy this entire directory to save your music files

2. **Back up your database**:
   ```bash
   # For PostgreSQL databases - run this in your terminal
   pg_dump -U username -F c -b -v -f country_music_backup.dump your_database_name
   ```

3. **Bundle everything together** (optional):
   ```bash
   # This creates a single archive with code, songs, and database
   zip -r country_music_complete.zip . -x "venv/*" ".git/*"
   ```

### Restoring Your Music Collection to a New Server

1. **Set up the basic application** by following the installation steps above

2. **Restore your database**:
   ```bash
   # For PostgreSQL databases - run this in your terminal
   pg_restore -U username -d your_new_database_name -v country_music_backup.dump
   ```

3. **Restore song files**:
   - Copy your backed-up `static/music` directory to the same location in the new installation
   - Make sure the file permissions allow the web server to read these files

4. **Fix song paths in the database** (if songs appear in the database but won't play):
   ```bash
   # Run the included fix_paths.py script
   python fix_paths.py
   ```
   
   This script automatically corrects all file paths in the database to match your current server setup.

### Quick Database Check

To check if your database has been properly restored and all songs are accessible:

```bash
# Connect to your PostgreSQL database
psql -U username your_database_name

# Run these queries to verify data
SELECT COUNT(*) FROM artist;  -- Should show the number of artists
SELECT COUNT(*) FROM song;    -- Should show the number of songs

# Check if file paths are correctly set
SELECT name, file_path FROM song LIMIT 5;
```

## Browser Compatibility

Country Music Paradise is tested and works on all modern browsers:
- Chrome 60+
- Firefox 60+
- Safari 10+
- Edge 15+
- Opera 50+
- Mobile browsers (iOS Safari, Android Chrome)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- All music is freely available through legal channels like Tubidy and user uploads
- Music metadata is provided by various free music APIs
- Special thanks to the open-source community for the tools and libraries used in this project