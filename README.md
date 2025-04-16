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

## Running the Application Locally

### Setting Up Your Development Environment

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/country-music-paradise.git
   cd country-music-paradise
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. **Install the required packages**:
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

### Setting Up the PostgreSQL Database

1. **Install PostgreSQL** if you don't already have it:
   - For Ubuntu/Debian: `sudo apt install postgresql postgresql-contrib`
   - For macOS (using Homebrew): `brew install postgresql`
   - For Windows: Download from [PostgreSQL website](https://www.postgresql.org/download/windows/)

2. **Create a new database**:
   ```bash
   # Login to PostgreSQL
   sudo -u postgres psql

   # Inside PostgreSQL command prompt
   CREATE DATABASE country_music;
   CREATE USER countryuser WITH PASSWORD 'yourpassword';
   GRANT ALL PRIVILEGES ON DATABASE country_music TO countryuser;
   \q
   ```

3. **Set the environment variable** to connect to your database:
   ```bash
   # For Linux/macOS
   export DATABASE_URL=postgresql://countryuser:yourpassword@localhost/country_music

   # For Windows (Command Prompt)
   set DATABASE_URL=postgresql://countryuser:yourpassword@localhost/country_music

   # For Windows (PowerShell)
   $env:DATABASE_URL="postgresql://countryuser:yourpassword@localhost/country_music"
   ```

### Starting the Application

1. **Initialize the database with sample data**:
   ```bash
   python reset_db.py
   ```
   This will create the database tables and add some default country artists including Bryan Adams.

2. **Start the application** using one of these methods:

   **Method A: Using Flask's development server** (good for development):
   ```bash
   # Set Flask environment variables
   export FLASK_APP=main.py
   export FLASK_ENV=development

   # Run the development server (with hot-reload)
   flask run --host=0.0.0.0 --port=5000
   ```

   **Method B: Using Gunicorn** (better for production):
   ```bash
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

3. **Open your browser** and go to http://localhost:5000

### Understanding the Directory Structure and Files

The application is organized as follows:

```
country-music-paradise/
├── static/                 # Static assets directory
│   ├── css/               # CSS stylesheets
│   │   └── style.css      # Main stylesheet for the application
│   ├── js/                # JavaScript files
│   │   ├── admin.js       # Admin dashboard functionality
│   │   ├── audio-player.js # Custom audio player implementation
│   │   └── sw.js          # Service Worker for offline functionality
│   ├── img/               # Images directory
│   └── music/             # Where uploaded songs are stored
├── templates/             # HTML templates directory
│   ├── admin/            # Admin-specific templates
│   │   ├── dashboard.html # Admin control panel
│   │   ├── login.html    # Admin login page
│   │   └── upload.html   # Song upload form
│   ├── artist.html       # Artist profile page
│   ├── base.html         # Base template with common elements
│   └── home.html         # Homepage template
```

### Core Application Files

- `main.py`: Main entry point of the application, starts the Flask server
- `app.py`: Core application configuration, database setup, and middleware
- `models.py`: Database models for Artists, Songs, Playlists, and Admin users
- `routes.py`: Main application routes for browsing and playing music
- `admin.py`: Admin-specific routes for managing content
- `playlist_routes.py`: Routes for playlist creation and management
- `music_api.py`: Integration with music APIs for song discovery

### Utility Scripts

- `backup_site.py`: Creates complete backups of the database and music files
- `bulk_upload.py`: Utility for batch uploading multiple songs at once
- `fix_paths.py`: Repairs song file paths after moving/restoring backups
- `reset_db.py`: Initializes the database with default data

### Configuration Files

- `.replit`: Replit-specific configuration for running the application
- `pyproject.toml`: Python project dependencies and metadata
- `replit.nix`: Nix package configuration for Replit environment

Each file serves a specific purpose in making the application modular and maintainable:

1. **Core Files**:
   - `main.py` and `app.py` handle the application startup and configuration
   - `models.py` defines the database structure
   - `routes.py` manages user interactions and page rendering

2. **Feature Modules**:
   - `admin.py` provides the admin interface
   - `playlist_routes.py` handles playlist functionality
   - `music_api.py` manages music discovery and downloads

3. **Maintenance Tools**:
   - `backup_site.py` ensures data can be safely backed up
   - `bulk_upload.py` makes it easy to add multiple songs
   - `fix_paths.py` maintains database integrity

4. **Templates and Static Files**:
   - HTML templates in `/templates` define the user interface
   - CSS and JavaScript in `/static` handle styling and interactivity
   - Uploaded music files are stored in `/static/music`


### How The Components Connect

1. **Frontend to Backend Connection**:
   - The Flask application serves HTML templates from the `templates/` directory
   - Static files (CSS, JS, images) are served from the `static/` directory
   - User requests are handled by routes defined in `routes.py` and `admin.py`
   - When you upload or play songs, the files are stored in/served from `static/music/`

2. **Backend to Database Connection**:
   - The PostgreSQL database connection is established via the `DATABASE_URL` environment variable
   - Database models are defined in `models.py`
   - All database interactions happen through SQLAlchemy ORM
   - Songs in the database have file paths that point to the `static/music/` directory

## Hosting Your Music Website

### Hosting on Replit (Recommended)

Replit provides a simple and free way to host your country music website:

1. **Deploy Your App**:
   - Click the "Deploy" button in your Replit workspace
   - Replit will automatically build and deploy your application
   - You'll get a public URL like `your-app.username.repl.co`

2. **Configure Environment**:
   - Use Replit's Secrets tool to store sensitive data like API keys
   - Access the Secrets tool from the Tools panel
   - Add your database URL and other environment variables

3. **Database Setup**:
   - Replit provides a free SQLite database out of the box
   - Your database file is automatically persisted
   - No additional configuration needed

4. **SSL/HTTPS**:
   - Replit automatically provides SSL certificates
   - Your site will be served over HTTPS by default

5. **Scaling**:
   - Replit's free tier includes:
     - Always-on hosting
     - Automatic HTTPS
     - Global CDN
     - DDoS protection

6. **Maintaining Your Site**:
   - Make changes directly in the Replit editor
   - Changes are automatically deployed
   - Use the Console to monitor your application
   - View logs in real-time

### Option 1: Hosting on Your Own Server or VPS

This option gives you complete control over your music website and database.

#### Steps to Set Up on a Linux Server (Ubuntu/Debian)

1. **Install required system packages**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv postgresql nginx
   ```

2. **Set up a new user and directory for the application**:
   ```bash
   sudo adduser countrymusic
   sudo mkdir -p /var/www/countrymusic
   sudo chown countrymusic:countrymusic /var/www/countrymusic
   ```

3. **Copy your application files to the server**:
   ```bash
   # If using scp (from your local machine)
   scp -r /path/to/your/local/project/* user@your-server-ip:/var/www/countrymusic/

   # If using git
   cd /var/www/countrymusic
   git clone https://github.com/yourusername/country-music-paradise.git .
   ```

4. **Set up a Python virtual environment**:
   ```bash
   cd /var/www/countrymusic
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt  # or install packages manually
   ```

5. **Set up PostgreSQL database**:
   ```bash
   sudo -u postgres psql
   CREATE DATABASE countrymusic;
   CREATE USER countryuser WITH PASSWORD 'your-secure-password';
   GRANT ALL PRIVILEGES ON DATABASE countrymusic TO countryuser;
   \q
   ```

6. **Configure environment variables** by creating a systemd service file:
   ```bash
   sudo nano /etc/systemd/system/countrymusic.service
   ```

   Add the following content:
   ```
   [Unit]
   Description=Country Music Paradise
   After=network.target

   [Service]
   User=countrymusic
   Group=www-data
   WorkingDirectory=/var/www/countrymusic
   Environment="PATH=/var/www/countrymusic/venv/bin"
   Environment="DATABASE_URL=postgresql://countryuser:your-secure-password@localhost/countrymusic"
   ExecStart=/var/www/countrymusic/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 main:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Set up Nginx as a reverse proxy**:
   ```bash
   sudo nano /etc/nginx/sites-available/countrymusic
   ```

   Add the following configuration:
   ```
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;

       location / {
           proxy_pass http://localhost:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static {
           alias /var/www/countrymusic/static;
       }
   }
   ```

   Enable the site:
   ```bash
   sudo ln -s /etc/nginx/sites-available/countrymusic /etc/nginx/sites-enabled
   sudo nginx -t  # Test configuration
   sudo systemctl restart nginx
   ```

8. **Initialize the database**:
   ```bash
   cd /var/www/countrymusic
   source venv/bin/activate
   python reset_db.py
   ```

9. **Start the service**:
   ```bash
   sudo systemctl enable countrymusic
   sudo systemctl start countrymusic
   sudo systemctl status countrymusic  # Check if running
   ```

10. **Set up SSL with Let's Encrypt** (optional but recommended):
    ```bash
    sudo apt install certbot python3-certbot-nginx
    sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
    ```

### Option 2: Hosting on PythonAnywhere

PythonAnywhere offers a simpler deployment process and includes PostgreSQL hosting.

1. **Sign up for a PythonAnywhere account** at [pythonanywhere.com](https://www.pythonanywhere.com)

2. **Upload your project files**:
   - Use the Files tab to create a new directory (e.g., countrymusic)
   - Upload your project files or clone from GitHub

3. **Set up a PostgreSQL database**:
   - Go to the Databases tab
   - Create a new PostgreSQL database
   - Note your database credentials

4. **Create a new web app**:
   - Go to the Web tab
   - Click "Add a new web app"
   - Select "Manual configuration" and "Python 3.8" (or newer)
   - Set the path to your project directory

5. **Configure the WSGI file**:
   - Edit the WSGI file (there will be a link in the Web tab)
   - Delete everything except the Flask section
   - Modify the Flask section to:
     ```python
     import sys
     path = '/home/yourusername/countrymusic'
     if path not in sys.path:
         sys.path.append(path)

     from main import app as application
     import os
     os.environ['DATABASE_URL'] = 'postgresql://yourusername:password@yourusername-postgres.pythonanywhere-services.com:10001/yourusername$countrymusic'
     ```

6. **Install required packages**:
   - Go to the Consoles tab
   - Start a Bash console
   - Navigate to your project directory and run:
     ```bash
     pip install --user Flask Flask-Login Flask-SQLAlchemy gunicorn psycopg2-binary requests trafilatura
     ```

7. **Initialize the database**:
   ```bash
   cd ~/countrymusic
   python reset_db.py
   ```

8. **Reload your web app** from the Web tab

### Option 3: Hosting on Heroku

Heroku offers easy deployment and scaling, perfect for moderate traffic.

1. **Sign up for a Heroku account** at [heroku.com](https://www.heroku.com)

2. **Install the Heroku CLI** and log in:
   ```bash
   # Install Heroku CLI (instructions vary by OS)
   heroku login
   ```

3. **Prepare your project for Heroku**:
   - Create a `Procfile` in your project root:
     ```
     web: gunicorn main:app
     ```
   - Create a `runtime.txt` file:
     ```
     python-3.9.16
     ```

4. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Heroku deployment"
   ```

5. **Create a Heroku app and add PostgreSQL**:
   ```bash
   heroku create your-app-name
   heroku addons:create heroku-postgresql:hobby-dev
   ```

6. **Deploy your application**:
   ```bash
   git push heroku master
   ```

7. **Initialize the database**:
   ```bash
   heroku run python reset_db.py
   ```

8. **Open your application**:
   ```bash
   heroku open
   ```

### Important Hosting Considerations

1. **Storage Space**: Ensure your hosting plan has enough storage for uploaded music files
2. **Database Backups**: Schedule regular backups using the backup_site.py script
3. **Traffic Limits**: Be aware of bandwidth limits on your hosting plan
4. **Legal Considerations**: Ensure all hosted music is legally free for distribution
5. **Security**: Keep your server and dependencies updated regularly

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