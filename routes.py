import os
import logging
import requests
from flask import render_template, request, redirect, url_for, flash, jsonify, send_file, abort, session
import os

# Set max upload size from environment or default to 300MB
MAX_CONTENT_LENGTH = int(os.getenv('BODY_SIZE_LIMIT', 314572800))  # 300MB in bytes
from app import db, app
from models import Artist, Song
from music_api import search_songs, download_song

def get_artist_image(artist_name):
    """Download and resize artist image from Wikipedia"""
    try:
        from PIL import Image
        from io import BytesIO
        
        # Search for artist on Wikipedia with smaller thumbnail
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=pageimages&titles={artist_name}&pithumbsize=300"
        response = requests.get(search_url)
        
        if response.status_code == 200:
            data = response.json()
            pages = data['query']['pages']
            
            for page_id in pages:
                page = pages[page_id]
                if 'thumbnail' in page:
                    image_url = page['thumbnail']['source']
                    
                    # Download image
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        # Open and resize image
                        img = Image.open(BytesIO(img_response.content))
                        img = img.convert('RGB')  # Convert to RGB mode
                        img.thumbnail((200, 200))  # Resize keeping aspect ratio
                        
                        # Save resized image
                        os.makedirs('static/img/artists', exist_ok=True)
                        filename = f"static/img/artists/{artist_name.lower().replace(' ', '_')}.jpg"
                        img.save(filename, 'JPEG', quality=85)
                        return True
                        
        # Fallback to a default profile image if no Wikipedia image found
        default_url = "https://t4.ftcdn.net/jpg/05/49/98/39/360_F_549983970_bRCkYfk0P6PP5YWy2Zj7wEhZYPE9Ur0k.jpg"
        img_response = requests.get(default_url)
        if img_response.status_code == 200:
            os.makedirs('static/img/artists', exist_ok=True)
            filename = f"static/img/artists/{artist_name.lower().replace(' ', '_')}.jpg"
            with open(filename, 'wb') as f:
                f.write(img_response.content)
            return True
    except Exception as e:
        logger.error(f"Error getting artist image: {str(e)}")
    return False

logger = logging.getLogger(__name__)

def register_routes(app):

    @app.route('/')
    def home():
        artists = Artist.query.order_by(Artist.name).all()
        return render_template('home.html', artists=artists)

    @app.route('/artist/<int:artist_id>')
    def artist_page(artist_id):
        artist = Artist.query.get_or_404(artist_id)
        songs = Song.query.filter_by(artist_id=artist_id).order_by(Song.name).all()
        playlists = Playlist.query.filter_by(is_public=True).all()
        return render_template('artist.html', artist=artist, songs=songs, playlists=playlists)

    @app.route('/api/search_songs')
    def api_search_songs():
        query = request.args.get('query', '')
        artist = request.args.get('artist', '')

        if not query and not artist:
            return jsonify({'error': 'Please provide a search query or artist name'}), 400

        try:
            results = search_songs(query, artist)
            return jsonify(results)
        except Exception as e:
            logger.error(f"Error searching songs: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/download/<int:artist_id>', methods=['POST'])
    def api_download_song(artist_id):
        data = request.json
        song_name = data.get('song_name')
        source_url = data.get('source_url')
        source = data.get('source', 'user_upload')

        if not song_name or not artist_id:
            return jsonify({'error': 'Missing required data'}), 400

        artist = Artist.query.get_or_404(artist_id)

        # Check if song already exists
        existing_song = Song.query.filter_by(name=song_name, artist_id=artist_id).first()
        if existing_song:
            return jsonify({'message': 'Song already exists', 'song_id': existing_song.id}), 200

        try:
            # Download the song
            file_path = download_song(song_name, artist.name, source_url, source)

            if file_path:
                # Create new song record
                new_song = Song(
                    name=song_name,
                    artist_id=artist_id,
                    file_path=file_path,
                    source=source,
                    source_url=source_url
                )

                db.session.add(new_song)
                db.session.commit()

                return jsonify({
                    'success': True,
                    'message': 'Song downloaded successfully',
                    'song_id': new_song.id
                })
            else:
                return jsonify({'error': 'Failed to download song'}), 500

        except Exception as e:
            logger.error(f"Error downloading song: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/play/<int:song_id>')
    def play_song(song_id):
        song = Song.query.get_or_404(song_id)
        return send_file(song.file_path)

    @app.route('/download/<int:song_id>')
    def download_song_file(song_id):
        song = Song.query.get_or_404(song_id)

        # Increment download count
        song.download_count += 1
        db.session.commit()

        return send_file(
            song.file_path, 
            as_attachment=True, 
            download_name=f"{song.name}.mp3"
        )

    @app.route('/user_upload_song', methods=['POST'])
    def user_upload_song():
        """Allow any user to upload songs without requiring admin login
        Supports multiple file uploads and auto-extracts song names from filenames"""

        # Increase request timeouts for large uploads
        request.environ['wsgi.input'].stream.read_timeout = 300  # 5 minutes
        request.environ['wsgi.input'].stream.write_timeout = 300  # 5 minutes

        try:
            artist_id = request.form.get('artist_id')

            if not artist_id or 'song_file' not in request.files:
                flash('Artist and at least one song file are required', 'danger')
                return redirect(url_for('artist_page', artist_id=artist_id)) if artist_id else redirect(url_for('home'))

            artist = Artist.query.get(artist_id)
            if not artist:
                flash('Artist not found', 'danger')
                return redirect(url_for('home'))

            # Make sure the MUSIC_FOLDER exists
            music_folder = app.config.get('MUSIC_FOLDER', 'static/music')
            if not os.path.exists(music_folder):
                os.makedirs(music_folder)

            from werkzeug.utils import secure_filename

            # Handle multiple file uploads (uploaded with same field name)
            song_files = request.files.getlist('song_file')

            success_count = 0
            skip_count = 0
            error_count = 0

            for song_file in song_files:
                if song_file and song_file.filename:
                    # Extract song name from the filename
                    original_filename = song_file.filename
                    # Get rid of the extension and use as song name
                    song_name = os.path.splitext(original_filename)[0]

                    # Check if song already exists for this artist
                    existing_song = Song.query.filter_by(name=song_name, artist_id=artist_id).first()
                    if existing_song:
                        logger.info(f"Song '{song_name}' already exists for {artist.name}. Skipping.")
                        skip_count += 1
                        continue

                    # Save the file with a secure artist_songname format
                    filename = secure_filename(f"{artist.name}_{original_filename}")
                    file_path = os.path.join(music_folder, filename)

                    try:
                        song_file.save(file_path)

                        # Create song record
                        new_song = Song(
                            name=song_name,
                            artist_id=artist_id,
                            file_path=file_path,
                            source='user_upload'
                        )

                        db.session.add(new_song)
                        success_count += 1
                        logger.info(f"Successfully added song '{song_name}' for {artist.name}")
                    except Exception as e:
                        logger.error(f"Error saving file {original_filename}: {str(e)}")
                        error_count += 1

            if success_count > 0:
                db.session.commit()

                if success_count == 1:
                    flash(f'Song uploaded successfully', 'success')
                else:
                    flash(f'{success_count} songs uploaded successfully', 'success')

                if skip_count > 0:
                    flash(f'{skip_count} songs were skipped (already exist)', 'warning')
                if error_count > 0:
                    flash(f'{error_count} songs failed to upload', 'danger')
            else:
                if skip_count > 0:
                    flash(f'No new songs added. {skip_count} songs already exist.', 'warning')
                else:
                    flash('No valid songs were uploaded', 'danger')

            return redirect(url_for('artist_page', artist_id=artist_id))

        except Exception as e:
            logger.error(f"Error uploading songs: {str(e)}")
            flash(f'Error uploading songs: {str(e)}', 'danger')
            return redirect(url_for('artist_page', artist_id=artist_id)) if 'artist_id' in locals() else redirect(url_for('home'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error="Page not found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('base.html', error="Server error occurred"), 500