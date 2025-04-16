# Country Music Paradise

A beautiful website to browse, play, and download free, legal country music featuring legendary artists like Bryan Adams, Dolly Parton, and many more. No registration required!

![Country Music Paradise Screenshot](static/img/screenshot.png)

## Features

- **No Login Required**: Listen to and download music without creating an account
- **Country Music Legends**: Browse music from artists like Bryan Adams, Kenny Rogers, Dolly Parton, and more
- **Upload Music**: Upload your own MP3 files directly to any artist's collection
- **Tubidy Integration**: Search and add songs from Tubidy and other free music sources
- **Mobile-Friendly**: Works on all modern browsers including mobile devices
- **Modern Design**: Beautiful interface with a focus on usability

## How to Run Locally

### Prerequisites

- Python 3.7+
- PostgreSQL database

### Installation Steps

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/country-music-paradise.git
   cd country-music-paradise
   ```

2. Set up a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
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

1. Organize your MP3 files in a directory structure:
   ```
   /music_to_add
     /Bryan Adams
       - Summer of 69.mp3
       - Everything I Do.mp3
     /Kenny Rogers
       - The Gambler.mp3
   ```

2. Use the bulk upload script (requires SSH access to server):
   ```
   python bulk_upload.py /path/to/music_to_add
   ```

3. The songs will be automatically added to the database with artist matching

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