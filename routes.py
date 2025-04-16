import os
import logging
from flask import render_template, request, redirect, url_for, flash, jsonify, send_file, abort, session
from app import db, app
from models import Artist, Song
from music_api import search_songs, download_song

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
        return render_template('artist.html', artist=artist, songs=songs)
    
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
        """Allow any user to upload songs without requiring admin login"""
        
        try:
            artist_id = request.form.get('artist_id')
            song_name = request.form.get('song_name')
            song_file = request.files.get('song_file')
            
            if not artist_id or not song_name or not song_file:
                flash('All fields are required', 'danger')
                return redirect(url_for('artist_page', artist_id=artist_id)) if artist_id else redirect(url_for('home'))
            
            artist = Artist.query.get(artist_id)
            if not artist:
                flash('Artist not found', 'danger')
                return redirect(url_for('home'))
            
            # Check if song already exists for this artist
            existing_song = Song.query.filter_by(name=song_name, artist_id=artist_id).first()
            if existing_song:
                flash('Song already exists for this artist', 'danger')
                return redirect(url_for('artist_page', artist_id=artist_id))
            
            # Make sure the MUSIC_FOLDER exists
            if not os.path.exists(app.config.get('MUSIC_FOLDER', 'static/music')):
                os.makedirs(app.config.get('MUSIC_FOLDER', 'static/music'))
            
            # Save the file
            from werkzeug.utils import secure_filename
            filename = secure_filename(f"{artist.name}_{song_name}.mp3")
            music_folder = app.config.get('MUSIC_FOLDER', 'static/music')
            file_path = os.path.join(music_folder, filename)
            
            song_file.save(file_path)
            
            # Create song record
            new_song = Song(
                name=song_name,
                artist_id=artist_id,
                file_path=file_path,
                source='user_upload'
            )
            
            db.session.add(new_song)
            db.session.commit()
            
            flash(f'Song {song_name} uploaded successfully', 'success')
            return redirect(url_for('artist_page', artist_id=artist_id))
        
        except Exception as e:
            logger.error(f"Error uploading song: {str(e)}")
            flash(f'Error uploading song: {str(e)}', 'danger')
            return redirect(url_for('artist_page', artist_id=artist_id) if artist_id else url_for('home'))

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', error="Page not found"), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return render_template('base.html', error="Server error occurred"), 500
