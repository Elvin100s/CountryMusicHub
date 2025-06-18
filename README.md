markdown
# Serene Sounds - Country Music Collection

A beautiful website to browse, play, and download free country music. Features artists like Don Williams, Dolly Parton, George Jones and more.

## Table of Contents
- [Quick Deploy on Replit](#quick-deploy-on-replit)
- [Configuring Large File Uploads](#configuring-large-file-uploads)
- [Features](#features)
- [Music API Integration](#music-api-integration)
- [Environment Variables](#environment-variables)
- [Admin Dashboard](#admin-dashboard)
- [Troubleshooting](#troubleshooting)
- [Local Development](#local-development)
- [VS Code Development Setup](#vs-code-development-setup)
- [Pop!_OS Linux Setup](#pop_os-linux-setup)
- [WSL Development Setup](#wsl-development-setup)
- [File Structure](#file-structure)
- [Large Upload Optimization](#large-upload-optimization)
- [Hosting Options](#hosting-options)
- [Maintenance](#maintenance)
- [Contributing](#contributing)
- [License](#license)

## Quick Deploy on Replit

1. Fork this template by clicking "Use Template" button
2. Click the "Run" button to start the application
3. The website will be live at `your-repl-name.username.repl.co`

**Note on Replit Free Hosting:**
- Free tier Repls go to sleep after ~1 hour of inactivity
- When a user visits a sleeping site, it takes 15-30 seconds to wake up
- Your files and database persist even when the Repl sleeps
- For always-on service, upgrade to Replit Pro

## Configuring Large File Uploads (up to 300MB)

1. Open the Tools menu in Replit
2. Select "Secrets"
3. Add a new secret with:
   - Key: `BODY_SIZE_LIMIT`
   - Value: `314572800`

This sets the upload limit to 300MB (314,572,800 bytes)

### Using the Large Upload Server
For uploading multiple large files (like 50+ songs at once), use the dedicated Large Upload Server workflow:

1. Click the dropdown next to the Run button
2. Select "Start Large Upload Server"
3. Wait for the server to start

This server is configured with:
- 300-second timeout (5 minutes)
- 3 worker processes
- 3 threads per worker
- Optimized for handling multiple large files

**If you experience timeouts when uploading many files:**
- Upload fewer files at once (15-20 files recommended)
- Ensure each file is under 300MB
- Check your internet connection stability

### Upload Songs
1. Visit any artist's page
2. Click "Upload MP3 From Your Computer"
3. Select MP3 files (up to 300MB each)
4. Click "Upload"

## Features

### Music Browsing & Playback
- Browse artists by name, genre, or popularity
- Play songs directly in the browser with custom audio player
- Continuous playback while browsing the site
- Volume control and playback speed adjustment
- Mobile-friendly responsive controls

### File Management
- No login required for listening/downloading
- Upload MP3 files up to 300MB
- Multiple file uploads at once (batch processing)
- Automatic song name extraction
- Download songs with a single click

### Organization
- Create custom playlists
- Search songs by title, artist, or album
- Sort songs by length, upload date, or alphabetically
- Filter songs by genre or mood tags

### Admin Features
- Secure admin dashboard
- Bulk upload and management tools
- Artist profile management
- Usage statistics and logs

## Music API Integration
The application can search and download music from various free, legal sources:

- **Free Music Archive (FMA):** A library of high-quality, legal audio downloads
  - Access to thousands of Creative Commons licensed tracks
  - Filtered to ensure country music focus
  - Automatic metadata extraction

- **Jamendo:** A platform offering free music under Creative Commons licenses
  - Artist attribution automatically added
  - Genre-specific API endpoints utilized
  - License validation on download

- **ccMixter:** A community music site featuring remixes licensed under Creative Commons
  - Remix and original track information preserved
  - Direct integration with artist profiles
  - License-compliant embedding

- **User Uploads:** Direct MP3 uploads from your computer
  - Local file validation
  - Metadata extraction when available
  - Automatic artist matching

The `music_api.py` file handles connections to these sources and ensures all downloads comply with licensing requirements.

## Environment Variables
The application uses the following environment variables:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| DATABASE_URL | PostgreSQL connection string | `sqlite:///country_music.db` | No |
| SESSION_SECRET | Secret key for session management | `country_music_app_secret` | No |
| BODY_SIZE_LIMIT | Maximum upload size in bytes | `314572800` (300MB) | No |
| ADMIN_USERNAME | Custom admin username | `admin` | No |
| ADMIN_PASSWORD | Custom admin password | `country_admin` | No |
| FMA_API_KEY | Free Music Archive API key | `None` | No |
| JAMENDO_CLIENT_ID | Jamendo API client ID | `None` | No |
| DEBUG | Enable debug mode | `False` | No |

## Admin Dashboard Access
The application comes with a default admin account:
- URL: `/admin/login`
- Username: `admin`
- Password: `country_admin`

### Admin Dashboard Features
**Content Management**
- Add/edit/delete artists
- Manage song metadata
- Create featured playlists
- Flag inappropriate content

**Upload Management**
- Bulk upload interface
- Batch processing tools
- File validation options
- Error logging

**System Settings**
- Configure API integrations
- Adjust upload limits
- Manage database backups
- View system logs

**Statistics**
- View most popular songs
- Track download counts
- Monitor storage usage
- User engagement metrics

## Troubleshooting

### Upload Issues
If uploads fail:
1. Check file size (must be under 300MB)
2. Ensure file is MP3 format
3. Check if `BODY_SIZE_LIMIT` secret is set
4. Try refreshing the page
5. For batches of 20+ files, use the Large Upload Server option
6. Check server logs for specific error messages
7. Verify write permissions on the storage directory

### Playback Problems
If songs won't play:
1. Check if the file exists on the server
2. Verify the audio format is supported by your browser
3. Check browser console for JavaScript errors
4. Try a different browser or device
5. Ensure the audio file isn't corrupted

### Server Errors
If the artist page shows a server error:
1. Check that Playlist is imported in routes.py
2. Verify the database connection is working
3. Ensure the static/music directory exists and is writable
4. Look for missing module imports
5. Check server logs for detailed error information
6. Verify all required packages are installed

### Database Issues
If database errors occur:
1. Verify PostgreSQL is running (if using PostgreSQL)
2. Check DATABASE_URL environment variable is correct
3. Ensure database user has proper permissions
4. Try running reset_db.py to recreate tables
5. Check database logs for connection issues

Need more help? Check Replit's documentation or ask in the community.

## Local Development

### Prerequisites
- Python 3.7+
- PostgreSQL database (optional, SQLite works too)
- 500MB+ free disk space for application and music files

### Running the Application Locally

#### Setting Up Your Development Environment
1. Clone this repository:
   ```bash
   git clone https://github.com/Elvin100s/country-music-paradise.git
   cd country-music-paradise
Set up a virtual environment (optional but recommended):

bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
Install the required packages:

bash
pip install -r requirements.txt
The requirements.txt file contains:

# Flask Framework and Extensions
Flask==2.3.3
Flask-Login==0.6.2
Flask-SQLAlchemy==3.1.1
Werkzeug==2.3.7
Jinja2==3.1.2
itsdangerous==2.1.2
SQLAlchemy==2.0.23
# Database Drivers
psycopg2-binary==2.9.9
# HTTP and Networking
requests==2.31.0
urllib3==2.0.7
# File Processing
python-dotenv==1.0.0
# Web Server
gunicorn==23.0.0
# Utilities
email-validator==2.0.0
trafilatura==1.6.1
# Data Management
markupsafe==2.1.3
# Improved Performance
uwsgi==2.0.22
Setting Up the Database
Option 1: Using SQLite (Simplest)

No additional setup required

The application will automatically create a SQLite database

Option 2: PostgreSQL (Recommended for Production)

Install PostgreSQL if you don't already have it:

For Ubuntu/Debian: sudo apt install postgresql postgresql-contrib

For macOS (using Homebrew): brew install postgresql

For Windows: Download from PostgreSQL website

Create a new database:

bash
# Login to PostgreSQL
sudo -u postgres psql

# Inside PostgreSQL command prompt
CREATE DATABASE country_music;
CREATE USER countryuser WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE country_music TO countryuser;
\q
Set the environment variable to connect to your database:

bash
# For Linux/macOS
export DATABASE_URL=postgresql://countryuser:yourpassword@localhost/country_music

# For Windows (Command Prompt)
set DATABASE_URL=postgresql://countryuser:yourpassword@localhost/country_music

# For Windows (PowerShell)
$env:DATABASE_URL="postgresql://countryuser:yourpassword@localhost/country_music"
Configuring Large File Uploads for Local Development
To handle large file uploads in your local environment:

Set the BODY_SIZE_LIMIT environment variable:

bash
# For Linux/macOS
export BODY_SIZE_LIMIT=314572800

# For Windows (Command Prompt)
set BODY_SIZE_LIMIT=314572800

# For Windows (PowerShell)
$env:BODY_SIZE_LIMIT=314572800
Modify main.py to extend timeouts:

python
# Add these lines to main.py for local development
if __name__ == "__main__":
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    WSGIRequestHandler.timeout = 600  # 10 minutes timeout
    
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True,
           request_handler=WSGIRequestHandler)
Create necessary directories:

bash
mkdir -p static/music static/img/artists
chmod -R 755 static
Starting the Application
Initialize the database with sample data:

bash
python reset_db.py
This will create the database tables and add default country artists including Bryan Adams.

Start the application using one of these methods:

Method A: Using Flask's development server (good for development):

bash
# Set Flask environment variables
export FLASK_APP=main.py
export FLASK_ENV=development
# Run the development server (with hot-reload)
flask run --host=0.0.0.0 --port=5000
Method B: Using Gunicorn (better for production):

bash
gunicorn --bind 0.0.0.0:5000 main:app --timeout 300
Method C: Using the production script (optimized for large uploads):

bash
python run_production.py
Open your browser and go to http://localhost:5000

VS Code Development Setup
If you prefer using VS Code for development, follow these steps to configure your environment.

Setting Up VS Code Environment
Install Required VS Code Extensions:

Python (Microsoft)

SQLite Viewer

REST Client

Live Server

Markdown Preview

Configure Python Environment:

bash
cd /path/to/country-music-paradise
code .
python -m venv .venv
# On Windows: .venv\Scripts\activate
# On macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
Create VS Code Configuration Files:
Create a .vscode folder in your project root with these files:

settings.json:

json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "autopep8",
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": false,
  "python.testing.unittestEnabled": true,
  "python.testing.nosetestsEnabled": false,
  "python.testing.unittestArgs": [
    "-v",
    "-s",
    "./tests",
    "-p",
    "test_*.py"
  ],
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  },
  "files.watcherExclude": {
    "**/static/music/**": true
  }
}
launch.json for debugging:

json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flask",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "main.py",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "1",
        "BODY_SIZE_LIMIT": "314572800"
      },
      "args": [
        "run",
        "--no-debugger",
        "--host=0.0.0.0",
        "--port=5000"
      ],
      "jinja": true
    },
    {
      "name": "Large Upload Server",
      "type": "python",
      "request": "launch",
      "module": "gunicorn",
      "args": [
        "-w", "3",
        "-t", "300",
        "--threads", "3",
        "-b", "0.0.0.0:5000",
        "main:app"
      ],
      "env": {
        "BODY_SIZE_LIMIT": "314572800"
      }
    },
    {
      "name": "Reset Database",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/reset_db.py"
    }
  ]
}
Running Servers in VS Code
Development Server:

Press F5 or select Run > Start Debugging

Choose the "Flask" configuration

This will start the Flask development server with debugging enabled

Set breakpoints by clicking in the gutter next to line numbers

Large Upload Server:

Select Run > Start Debugging

Choose the "Large Upload Server" configuration

This starts Gunicorn with optimized settings for large uploads

Has a 5-minute timeout for handling large files

Custom Server Script:
Create a file called run_server.py:

python
import os
import sys
import argparse

def run_development_server():
    os.environ['FLASK_APP'] = 'main.py'
    os.environ['FLASK_ENV'] = 'development'
    os.environ['BODY_SIZE_LIMIT'] = '314572800'
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    WSGIRequestHandler.timeout = 600  # 10 minutes timeout
    
    from main import app
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True,
            request_handler=WSGIRequestHandler)

def run_large_upload_server():
    os.environ['BODY_SIZE_LIMIT'] = '314572800'
    from gunicorn.app.wsgiapp import WSGIApplication
    sys.argv = [
        'gunicorn',
        '-w', '3',
        '-t', '300',
        '--threads', '3',
        '-b', '0.0.0.0:5000',
        'main:app'
    ]
    WSGIApplication().run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run server with different configurations')
    parser.add_argument('--mode', choices=['dev', 'upload'], default='dev', 
                       help='Server mode: dev for development, upload for large file uploads')
    args = parser.parse_args()
    
    if args.mode == 'dev':
        run_development_server()
    else:
        run_large_upload_server()
Add this to your launch.json:

json
{
  "name": "Custom Server",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/run_server.py",
  "args": ["--mode", "dev"],
  "console": "integratedTerminal"
}
Environment Variables in VS Code
Create a .env file in your project root:

DATABASE_URL=postgresql://countryuser:yourpassword@localhost/country_music
BODY_SIZE_LIMIT=314572800
SESSION_SECRET=your_secret_key_here
Add this to the start of your main.py:

python
from dotenv import load_dotenv
load_dotenv()
Debugging Tips for VS Code
Set Conditional Breakpoints:

Right-click the gutter and select "Add Conditional Breakpoint"

Enter conditions like file_size > 100000000 to break on large files

Use Debug Console:

When paused at a breakpoint, use the Debug Console to inspect variables

Try expressions like request.files or os.path.getsize(file_path)

Profile Slow Operations:

python
import cProfile
def my_view_function():
    pr = cProfile.Profile()
    pr.enable()
    # Your code here
    pr.disable()
    pr.print_stats(sort='cumtime')
Pop!_OS Linux Development Setup
Pop!_OS provides an excellent development environment with its optimized performance and developer-friendly features.

Initial System Setup on Pop!_OS
Install Required System Packages:

bash
# Update package lists
sudo apt update
# Install required packages
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib git nginx
Start and Enable PostgreSQL:

bash
# Start PostgreSQL service
sudo systemctl start postgresql
# Enable PostgreSQL to start on boot
sudo systemctl enable postgresql
# Verify PostgreSQL is running
sudo systemctl status postgresql
Project Setup on Pop!_OS
Clone Repository and Create Virtual Environment:

bash
git clone https://github.com/yourusername/country-music-paradise.git
cd country-music-paradise
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure PostgreSQL Database:

bash
sudo -u postgres psql -c "CREATE USER countryuser WITH PASSWORD 'yourpassword';"
sudo -u postgres psql -c "CREATE DATABASE country_music OWNER countryuser;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE country_music TO countryuser;"
Setup Environment Variables:
Create a file named .env in your project directory:

DATABASE_URL=postgresql://countryuser:yourpassword@localhost/country_music
BODY_SIZE_LIMIT=314572800
SESSION_SECRET=your_secure_secret_key
Add environment variables to your shell profile:

bash
echo 'export FLASK_APP=main.py' >> ~/.bashrc
echo 'export FLASK_ENV=development' >> ~/.bashrc
echo 'export BODY_SIZE_LIMIT=314572800' >> ~/.bashrc
source ~/.bashrc
Create Required Directories:

bash
mkdir -p static/music static/img/artists
chmod -R 755 static
Initialize Database:

bash
python reset_db.py
Running the Application on Pop!_OS
Development Server:

bash
# Basic Flask development server
flask run --host=0.0.0.0 --port=5000

# Or with custom timeout settings for large file uploads
python3 -c "
from werkzeug.serving import WSGIRequestHandler
WSGIRequestHandler.protocol_version = 'HTTP/1.1'
WSGIRequestHandler.timeout = 600
from main import app
app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
"
Production Server with Gunicorn:

bash
# Optimized for large uploads
gunicorn --workers 3 --timeout 300 --threads 3 --bind 0.0.0.0:5000 main:app
Create a Convenient Start Script for Pop!_OS:
Create a file named pop_server.sh:

bash
#!/bin/bash
MODE=${1:-dev}  # Default to dev mode

# Set environment variables
export FLASK_APP=main.py
export BODY_SIZE_LIMIT=314572800

# Activate virtual environment
source venv/bin/activate

# Create directories if they don't exist
mkdir -p static/music static/img/artists
chmod -R 755 static

case "$MODE" in
  dev)
    echo "Starting development server on Pop!_OS..."
    export FLASK_ENV=development
    python -c "
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = 'HTTP/1.1'
    WSGIRequestHandler.timeout = 600
    from main import app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    "
    ;;
  large)
    echo "Starting large upload server on Pop!_OS..."
    gunicorn --workers 3 --timeout 300 --threads 3 --bind 0.0.0.0:5000 main:app
    ;;
  prod)
    echo "Starting production server on Pop!_OS..."
    export FLASK_ENV=production
    gunicorn --workers 4 --bind 0.0.0.0:5000 main:app
    ;;
  *)
    echo "Unknown mode: $MODE"
    echo "Usage: $0 [dev|large|prod]"
    exit 1
    ;;
esac
Make it executable:

bash
chmod +x pop_server.sh
Run it:

bash
# Development mode
./pop_server.sh dev

# Large upload mode
./pop_server.sh large

# Production mode
./pop_server.sh prod
Pop!_OS-Specific Optimizations
Take Advantage of Pop!_OS System76 Power Management:

bash
# Install System76 Power if not already installed
sudo apt install system76-power
# Set performance mode for better server response
sudo system76-power profile performance
Optimize PostgreSQL for Pop!_OS:

bash
sudo nano /etc/postgresql/*/main/postgresql.conf
Update these settings for Pop!_OS:

# Memory settings (adjust based on available RAM)
shared_buffers = 256MB                  # min 128kB
work_mem = 16MB                         # min 64kB
maintenance_work_mem = 64MB             # min 1MB
# Query planning
effective_cache_size = 1GB
# Write ahead log
wal_buffers = 16MB
Restart PostgreSQL:

bash
sudo systemctl restart postgresql
Pop!_OS Desktop Integration:

bash
# Create a desktop shortcut
nano ~/.local/share/applications/countrymusic.desktop
Add:

[Desktop Entry]
Name=Country Music App
Exec=bash -c "cd /path/to/country-music-paradise && ./pop_server.sh dev"
Icon=/path/to/country-music-paradise/static/img/favicon.ico
Type=Application
Terminal=true
Categories=Development;Audio;
WSL Development Setup
Windows Subsystem for Linux (WSL) provides a Linux environment directly in Windows. This section covers both Ubuntu WSL setup and VS Code integration with WSL.

Ubuntu WSL Setup
Install WSL and Ubuntu:

Open PowerShell as Administrator and run:

powershell
wsl --install -d Ubuntu
Install Required Packages in Ubuntu WSL:

bash
# Update packages
sudo apt update
sudo apt upgrade
# Install required packages
sudo apt install python3 python3-pip python3-venv postgresql postgresql-contrib git
Start PostgreSQL and Configure It:

bash
# Initialize PostgreSQL if needed (first time only)
sudo pg_createcluster 12 main --start  # Use your PostgreSQL version
# Start and enable PostgreSQL service
sudo service postgresql start
# Create database and user
sudo -u postgres psql -c "CREATE USER countryuser WITH PASSWORD 'yourpassword';"
sudo -u postgres psql -c "CREATE DATABASE country_music OWNER countryuser;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE country_music TO countryuser;"
Setup Project in Ubuntu WSL:

bash
# Clone repository
git clone https://github.com/yourusername/country-music-paradise.git
cd country-music-paradise
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
Configure Environment Variables:

bash
# Create .env file
cat > .env << EOL
DATABASE_URL=postgresql://countryuser:yourpassword@localhost/country_music
BODY_SIZE_LIMIT=314572800
SESSION_SECRET=your_secure_key
EOL

# Add to .bashrc
echo 'export FLASK_APP=main.py' >> ~/.bashrc
echo 'export FLASK_ENV=development' >> ~/.bashrc
echo 'export BODY_SIZE_LIMIT=314572800' >> ~/.bashrc
source ~/.bashrc
Create Server Script for Ubuntu WSL:

bash
# Create script file
cat > ubuntu_wsl_server.sh << 'EOL'
#!/bin/bash
MODE=${1:-dev}  # Default to dev mode

# Start PostgreSQL if not running
sudo service postgresql status > /dev/null || sudo service postgresql start

# Set environment variables
export FLASK_APP=main.py
export BODY_SIZE_LIMIT=314572800

# Activate virtual environment
source venv/bin/activate

# Create directories if they don't exist
mkdir -p static/music static/img/artists
chmod -R 755 static

case "$MODE" in
  dev)
    echo "Starting development server on Ubuntu WSL..."
    export FLASK_ENV=development
    python -c "
    from werkzeug.serving import WSGIRequestHandler
    WSGIRequestHandler.protocol_version = 'HTTP/1.1'
    WSGIRequestHandler.timeout = 600
    from main import app
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    "
    ;;
  large)
    echo "Starting large upload server on Ubuntu WSL..."
    gunicorn --workers 3 --timeout 300 --threads 3 --bind 0.0.0.0:5000 main:app
    ;;
  prod)
    echo "Starting production server on Ubuntu WSL..."
    export FLASK_ENV=production
    gunicorn --workers 4 --bind 0.0.0.0:5000 main:app
    ;;
  *)
    echo "Unknown mode: $MODE"
    echo "Usage: $0 [dev|large|prod]"
    exit 1
    ;;
esac
EOL

# Make executable
chmod +x ubuntu_wsl_server.sh
Initialize Database and Run Server:

bash
# Initialize database
python reset_db.py

# Run development server
./ubuntu_wsl_server.sh dev

# Or run large upload server
./ubuntu_wsl_server.sh large
Access Application from Windows:

Find the WSL IP address:

bash
hostname -I | awk '{print $1}'
Open browser in Windows and go to http://[WSL-IP]:5000

Or simply use http://localhost:5000 (Windows 10/11 has automatic port forwarding)

VS Code with WSL Integration
Install Required VS Code Extensions:

Open VS Code in Windows

Install Remote - WSL extension

Install Python extension

Open Project in VS Code with WSL:

bash
# In WSL terminal, navigate to your project
cd ~/country-music-paradise
# Launch VS Code from WSL
code .
VS Code will launch and connect to WSL automatically

Configure VS Code for WSL Development:
Create .vscode folder in your project with the following files:

settings.json:

json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.terminal.activateEnvironment": true,
  "terminal.integrated.defaultProfile.linux": "bash",
  "terminal.integrated.profiles.linux": {
    "bash": {
      "path": "bash",
      "icon": "terminal-bash"
    }
  },
  "files.watcherExclude": {
    "**/static/music/**": true,
    "**/venv/**": true,
    "**/__pycache__/**": true
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
launch.json:

json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flask (WSL)",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "main.py",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "1",
        "BODY_SIZE_LIMIT": "314572800"
      },
      "args": [
        "run",
        "--no-debugger",
        "--host=0.0.0.0",
        "--port=5000"
      ],
      "jinja": true
    },
    {
      "name": "Large Upload Server (WSL)",
      "type": "python",
      "request": "launch",
      "module": "gunicorn",
      "args": [
        "-w", "3",
        "-t", "300",
        "--threads", "3",
        "-b", "0.0.0.0:5000",
        "main:app"
      ],
      "env": {
        "BODY_SIZE_LIMIT": "314572800"
      }
    },
    {
      "name": "Reset DB (WSL)",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/reset_db.py"
    }
  ]
}
Create VS Code WSL Server Script:

bash
# Create script file
cat > vscode_wsl_server.sh << 'EOL'
#!/bin/bash
# Start PostgreSQL if not running
sudo service postgresql status > /dev/null || sudo service postgresql start

# Set environment variables
export FLASK_APP=main.py
export FLASK_ENV=development
export BODY_SIZE_LIMIT=314572800

# Run Flask
if [ "$1" = "large" ]; then
  echo "Starting large upload server..."
  gunicorn -w 3 -t 300 --threads 3 -b 0.0.0.0:5000 main:app
else
  echo "Starting development server..."
  python -m flask run --host=0.0.0.0 --port=5000
fi
EOL

# Make executable
chmod +x vscode_wsl_server.sh
Running the Application in VS Code:

Use the integrated terminal to run either:

bash
# Normal development server
./vscode_wsl_server.sh

# Large upload server
./vscode_wsl_server.sh large
Or use the VS Code debug configurations:

Press F5 or go to Run > Start Debugging

Select the "Flask (WSL)" or "Large Upload Server (WSL)" configuration

VS Code WSL Performance Optimizations:

Store project in Linux filesystem (/home/username/) not Windows filesystem (/mnt/c/)

Configure .wslconfig in Windows:
Create file at C:\Users\YourUsername\.wslconfig with:

[wsl2]
memory=4GB
processors=2
swap=2GB
Restart WSL: wsl --shutdown then reopen

Using WSL-Specific Tools in VS Code:

Use integrated terminal to run Linux commands

Access PostgreSQL: sudo -u postgres psql

View logs: tail -f /var/log/postgresql/postgresql-*.log

Monitor resources: htop (install with sudo apt install htop if needed)

Understanding the Directory Structure and Files
The application is organized as follows:

country-music-paradise/
├── static/                 # Static assets directory
│   ├── css/               # CSS stylesheets
│   │   ├── style.css      # Main stylesheet for the application
│   │   ├── admin.css      # Admin-specific styling
│   │   └── audio-player.css # Audio player styling
│   ├── js/                # JavaScript files
│   │   ├── admin.js       # Admin dashboard functionality
│   │   ├── audio-player.js # Custom audio player implementation
│   │   ├── upload-manager.js # Handles file upload UI
│   │   ├── playlist.js    # Playlist management functions
│   │   └── sw.js          # Service Worker for offline functionality
│   ├── img/               # Images directory
│   │   └── artists/       # Artist profile images
│   └── music/             # Where uploaded songs are stored
│       └── .gitkeep       # Ensures directory exists in git
├── templates/             # HTML templates directory
│   ├── admin/            # Admin-specific templates
│   │   ├── dashboard.html # Admin control panel
│   │   ├── login.html    # Admin login page
│   │   ├── upload.html   # Song upload form
│   │   ├── artist_mgmt.html # Artist management page
│   │   └── stats.html    # Statistics and metrics
│   ├── artist.html       # Artist profile page
│   ├── base.html         # Base template with common elements
│   ├── home.html         # Homepage template
│   ├── search.html       # Search results page
│   ├── playlist.html     # Playlist display
│   └── error.html        # Error page template
├── app.py                # Core application configuration
├── main.py               # Main entry point
├── models.py             # Database models
├── routes.py             # Main application routes
├── admin.py              # Admin routes and functionality
├── playlist_routes.py    # Playlist management
├── music_api.py          # Music API integration
├── helpers.py            # Utility functions
├── config.py             # Configuration settings
├── reset_db.py           # Database initialization
├── run_production.py     # Production server startup script
├── file_utils.py         # File handling utilities
├── tests/                # Test suite directory
│   ├── test_routes.py    # Route tests
│   ├── test_models.py    # Model tests
│   └── test_file_uploads.py # Upload functionality tests
├── requirements.txt      # Project dependencies
├── LICENSE               # Project license
├── .vscode/              # VS Code configuration
│   ├── settings.json     # VS Code settings
│   └── launch.json       # Debug configurations
└── README.md             # This file
Core Application Files Explained
main.py: Entry point of the application that configures and starts the Flask server. It handles command-line arguments and sets up logging.

app.py: Core application configuration that initializes Flask, configures extensions, registers blueprints, and sets up middleware. This is where the Flask app object is created.

models.py: Defines database models using SQLAlchemy ORM:

Artist: Stores artist information (name, bio, image path)

Song: Stores song details (title, artist, file path, duration)

Playlist: Manages user-created song collections

Admin: Stores admin user credentials for dashboard access

routes.py: Main application routes for browsing and playing music:

/: Homepage with featured artists and popular songs

/artist/<id>: Artist profile with songs and bio

/song/<id>: Individual song page with player

/search: Search functionality

/download/<id>: File download endpoint

admin.py: Admin-specific routes secured behind authentication:

/admin/login: Admin authentication

/admin/dashboard: Control panel

/admin/upload: Bulk upload interface

/admin/artists: Artist management

/admin/stats: Usage statistics

playlist_routes.py: Routes for playlist functionality:

/playlist/create: Create new playlist

/playlist/<id>: View playlist

/playlist/add/<id>: Add song to playlist

/playlist/remove/<id>: Remove song from playlist

music_api.py: Handles integration with external music sources:

FMA API client

Jamendo API integration

ccMixter connectivity

License validation

How The Components Connect
Frontend to Backend Connection:

The Flask application serves HTML templates from the templates/ directory

Templates use Jinja2 syntax to display dynamic data

Static files (CSS, JS, images) are served from the static/ directory

AJAX requests from JavaScript fetch data from backend endpoints

Form submissions are processed by route handlers

User requests are handled by routes defined in routes.py and admin.py

When you upload or play songs, the files are stored in/served from static/music/

Backend to Database Connection:

The PostgreSQL/SQLite database connection is established via the DATABASE_URL environment variable

Database models are defined in models.py using SQLAlchemy ORM

Route handlers query the database through model classes

Data validation happens before database operations

Transactions ensure data integrity

All database interactions happen through SQLAlchemy ORM

Songs in the database have file paths that point to the static/music/ directory

Optimizing for Large File Uploads
For better handling of large file uploads (especially when uploading multiple files):

Process Files in Batches:

Upload 15-20 files at a time for best performance

For 50+ files, split them into multiple upload sessions

Consider the backend process time based on file sizes

Server Configuration:

The Large Upload Server option extends timeouts and worker processes

Gunicorn workers are configured for optimal file handling

Timeouts are increased to accommodate large files

File descriptors are increased for multiple simultaneous connections

Progress Indication:

The upload process may take several minutes for large files

The page will appear to freeze during upload - this is normal

Do not refresh the page until the upload completes

Network timeouts may occur for very large files on slow connections

Error Handling:

Connection timeouts are automatically retried

Failed uploads are logged for troubleshooting

The application provides clear error messages

Interrupted uploads can be safely resumed

Filesystem Considerations:

Ensure adequate disk space (at least 3x the total upload size)

File storage is optimized for large media files

Quota warnings appear when storage is running low

Hosting Your Music Website
Hosting on Replit (Free Option)
Replit provides a simple and free way to host your country music website:

Create a New Replit Project:

Go to Replit.com

Click "Create Repl"

Choose "Python" as the template

Name your project (e.g., "SereneCountryMusic")

Click "Create Repl"

Upload Your Files:

You can drag and drop all your project files into the Replit file browser

Alternatively, connect your GitHub repository if your code is stored there

Make sure to preserve the directory structure

Configure Environment:

In the Replit sidebar, click on "Tools" then "Secrets"

Add the following secrets:

Key: BODY_SIZE_LIMIT - Value: 314572800 (for 300MB uploads)

Key: SESSION_SECRET - Value: [your secret key]

Key: ADMIN_USERNAME - Value: [custom admin username] (optional)

Key: ADMIN_PASSWORD - Value: [custom admin password] (optional)

Configure Run Button:

Create a .replit file at the root of your project with:

run = "python main.py"
language = "python3"
entrypoint = "main.py"
Set Up Multiple Run Configurations:

Click on the dropdown arrow next to the "Run" button

Select "Configure" then "Add new configuration"

Name it "Large Upload Server"

Set the run command: gunicorn -w 3 -t 300 --threads 3 -b 0.0.0.0:8080 main:app

Save the configuration

Add another configuration named "Initialize Database" with command: python reset_db.py

Save the configuration

Initialize the Database:

Select "Initialize Database" from the run dropdown

Click "Run" to create the initial database

Run Your Website:

Select "main.py" from the run dropdown

Click the "Run" button

The website will be live at yourrepl.username.repl.co

For Large File Uploads:

Select "Large Upload Server" from the run dropdown

Click "Run" to start the optimized server

Use this configuration when uploading large files

Free Tier Limitations

Your site will go to sleep after ~1 hour of inactivity (requires Replit Pro to stay always on)

Wake-up time of 15-30 seconds for the first visitor after sleep

Limited CPU and RAM resources

Limited storage space (about 500MB-1GB total)

Custom domain requires Replit Pro

Alternative Free Hosting Options
Fly.io (Free Tier):

3 shared-CPU VMs with 256MB RAM

3GB persistent volume storage (good for music files)

Free PostgreSQL (limited)

No sleep/idle time

Render (Free Tier):

Static sites are always free

Web services spin down after 15 minutes of inactivity

500MB storage

750 hours of runtime per month

Railway (Limited Free Tier):

$5 worth of resources per month for free

Support for Python/Flask applications

PostgreSQL database available

Maintenance and Troubleshooting
Regular Maintenance Tasks
Database Backups:
Run the backup script regularly to save your database and uploaded music:

bash
python backup_site.py
This will create a timestamped backup in the backups/ directory.

Check Disk Space:
MP3 files can quickly fill up space, especially with 300MB files.
Regularly check available disk space:

bash
df -h
Free up space by removing unused files or expanding your storage.

Verify File Integrity:
Run the integrity checking script periodically:

bash
python check_integrity.py
This will scan all database entries and verify that the referenced files exist.

Update Dependencies:
Periodically update your dependencies to get security patches:

bash
pip install --upgrade -r requirements.txt
Log Rotation:
If running in production, set up log rotation for application logs.
Check that logs are being rotated properly:

bash
sudo logrotate -d /etc/logrotate.d/countrymusic
Optimize Database:
For PostgreSQL, run vacuum operations periodically:

bash
sudo -u postgres psql
\c countrymusic
VACUUM ANALYZE;
\q
Common Issues and Solutions
File Upload Errors:

Check file permissions on the static/music directory

Verify the BODY_SIZE_LIMIT environment variable is set

Look for timeout errors in logs

Check Nginx/proxy configuration for body size limits

Increase worker timeout if necessary

Database Connection Issues:

Verify the DATABASE_URL environment variable

Check PostgreSQL is running: sudo systemctl status postgresql

Test database connection manually:

bash
psql postgresql://countryuser:password@localhost/countrymusic
Check database logs: sudo tail -f /var/log/postgresql/postgresql-*.log

Missing Artist Images:

Ensure the static/img/artists directory exists

Check permissions on the directory

The app will function without images, they're optional

Default placeholder images will be used if not found

Server Error on Artist Page:

Verify Playlist model is imported in routes.py

Check for Python stack trace in error logs

Test database connection to ensure it's working

Verify the artist exists in the database

Audio Playback Issues:

Check browser console for JavaScript errors

Verify the audio file exists and is correctly referenced

Test the file with a different audio player

Check file permissions on the audio file

Slow Performance:

Check server resource usage (CPU, memory)

Look for slow database queries

Consider adding indexes to frequently queried columns

Compress static assets

Implement caching for frequent requests

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository

Create your feature branch: git checkout -b my-new-feature

Commit your changes: git commit -am 'Add some feature'

Push to the branch: git push origin my-new-feature

Submit a pull request

License
This project is licensed under the MIT License - see the LICENSE file for details.

MIT License

Copyright (c) 2023 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
Contact & Support
For help and support with this application:

Open an issue on GitHub

Email: your.email@example.com

Visit: yourdomain.com/contact

Thank you for using Serene Sounds - Country Music Collection!


This comprehensive README.md provides all the necessary information for setting up, configuring, and maintaining your country music website across different environments. It includes detailed instructions for various development setups, troubleshooting tips, and hosting options.
