import os
import logging
from functools import wraps
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app, db
from models import Admin, Artist, Song, create_default_admin, create_default_artists, init_db

logger = logging.getLogger(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def register_admin_routes(app):
    with app.app_context():
        init_db()
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            admin = Admin.query.filter_by(username=username).first()
            
            if admin and admin.check_password(password):
                login_user(admin)
                flash('Logged in successfully', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password', 'danger')
        
        return render_template('admin/login.html')
    
    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        logout_user()
        flash('Logged out successfully', 'success')
        return redirect(url_for('home'))
    
    @app.route('/admin')
    @admin_required
    def admin_dashboard():
        artists = Artist.query.order_by(Artist.name).all()
        songs_count = Song.query.count()
        return render_template('admin/dashboard.html', artists=artists, songs_count=songs_count)
    
    @app.route('/admin/artist/add', methods=['POST'])
    @admin_required
    def add_artist():
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Artist name is required', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        existing_artist = Artist.query.filter_by(name=name).first()
        if existing_artist:
            flash('Artist already exists', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        new_artist = Artist(name=name, description=description)
        db.session.add(new_artist)
        db.session.commit()
        
        flash(f'Artist {name} added successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    
    @app.route('/admin/artist/<int:artist_id>/edit', methods=['POST'])
    @admin_required
    def edit_artist(artist_id):
        artist = Artist.query.get_or_404(artist_id)
        
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Artist name is required', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        # Check if the updated name conflicts with another artist
        existing_artist = Artist.query.filter_by(name=name).first()
        if existing_artist and existing_artist.id != artist_id:
            flash('Another artist with this name already exists', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        artist.name = name
        artist.description = description
        db.session.commit()
        
        flash(f'Artist {name} updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    
    @app.route('/admin/artist/<int:artist_id>/delete', methods=['POST'])
    @admin_required
    def delete_artist(artist_id):
        artist = Artist.query.get_or_404(artist_id)
        
        # Delete all songs for this artist
        songs = Song.query.filter_by(artist_id=artist_id).all()
        for song in songs:
            try:
                if os.path.exists(song.file_path):
                    os.remove(song.file_path)
            except Exception as e:
                logger.error(f"Error deleting song file {song.file_path}: {str(e)}")
            
            db.session.delete(song)
        
        # Delete the artist
        db.session.delete(artist)
        db.session.commit()
        
        flash(f'Artist {artist.name} and all their songs deleted successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    
    @app.route('/admin/upload', methods=['GET', 'POST'])
    @admin_required
    def upload_song():
        if request.method == 'POST':
            artist_id = request.form.get('artist_id')
            song_name = request.form.get('song_name')
            song_file = request.files.get('song_file')
            
            if not artist_id or not song_name or not song_file:
                flash('All fields are required', 'danger')
                artists = Artist.query.order_by(Artist.name).all()
                return render_template('admin/upload.html', artists=artists)
            
            artist = Artist.query.get(artist_id)
            if not artist:
                flash('Artist not found', 'danger')
                artists = Artist.query.order_by(Artist.name).all()
                return render_template('admin/upload.html', artists=artists)
            
            # Check if song already exists for this artist
            existing_song = Song.query.filter_by(name=song_name, artist_id=artist_id).first()
            if existing_song:
                flash('Song already exists for this artist', 'danger')
                artists = Artist.query.order_by(Artist.name).all()
                return render_template('admin/upload.html', artists=artists)
            
            # Save the file
            filename = secure_filename(f"{artist.name}_{song_name}.mp3")
            file_path = os.path.join(app.config['MUSIC_FOLDER'], filename)
            
            try:
                song_file.save(file_path)
                
                # Create song record
                new_song = Song(
                    name=song_name,
                    artist_id=artist_id,
                    file_path=file_path,
                    source='admin_upload'
                )
                
                db.session.add(new_song)
                db.session.commit()
                
                flash(f'Song {song_name} uploaded successfully', 'success')
                return redirect(url_for('admin_dashboard'))
            
            except Exception as e:
                logger.error(f"Error uploading song: {str(e)}")
                flash(f'Error uploading song: {str(e)}', 'danger')
        
        artists = Artist.query.order_by(Artist.name).all()
        return render_template('admin/upload.html', artists=artists)
    
    @app.route('/admin/song/<int:song_id>/delete', methods=['POST'])
    @admin_required
    def delete_song(song_id):
        song = Song.query.get_or_404(song_id)
        
        # Delete the file
        try:
            if os.path.exists(song.file_path):
                os.remove(song.file_path)
        except Exception as e:
            logger.error(f"Error deleting song file {song.file_path}: {str(e)}")
        
        # Delete the record
        db.session.delete(song)
        db.session.commit()
        
        flash(f'Song {song.name} deleted successfully', 'success')
        return redirect(url_for('artist_page', artist_id=song.artist_id))
