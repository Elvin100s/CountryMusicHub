"""
Playlist-related routes for Country Music Paradise

This file contains all routes related to playlists functionality:
- Creating playlists
- Viewing playlists
- Adding songs to playlists
- Removing songs from playlists
"""

import os
import logging
from flask import render_template, request, redirect, url_for, jsonify, flash, session
from app import db
from models import Playlist, Song, Artist

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def register_playlist_routes(app):
    """Register all playlist-related routes with the Flask app"""
    
    @app.route('/playlists')
    def playlists():
        """Display all public playlists"""
        playlists = Playlist.query.filter_by(is_public=True).all()
        return render_template('playlists.html', playlists=playlists)
    
    @app.route('/playlist/<int:playlist_id>')
    def view_playlist(playlist_id):
        """View a specific playlist and its songs"""
        playlist = Playlist.query.get_or_404(playlist_id)
        return render_template('playlist.html', playlist=playlist)
    
    @app.route('/playlist/create', methods=['GET', 'POST'])
    def create_playlist():
        """Create a new playlist"""
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            is_public = 'is_public' in request.form
            
            if not name:
                flash('Playlist name is required', 'danger')
                return redirect(url_for('create_playlist'))
            
            # Create new playlist
            playlist = Playlist(name=name, description=description, is_public=is_public)
            db.session.add(playlist)
            db.session.commit()
            
            flash(f'Playlist "{name}" created successfully!', 'success')
            return redirect(url_for('view_playlist', playlist_id=playlist.id))
        
        return render_template('create_playlist.html')
    
    @app.route('/api/playlist/<int:playlist_id>/add/<int:song_id>', methods=['POST'])
    def add_to_playlist(playlist_id, song_id):
        """Add a song to a playlist"""
        playlist = Playlist.query.get_or_404(playlist_id)
        song = Song.query.get_or_404(song_id)
        
        success = playlist.add_song(song)
        db.session.commit()
        
        if success:
            flash(f'"{song.name}" added to playlist "{playlist.name}"', 'success')
            logger.info(f'Added song {song.id} to playlist {playlist.id}')
            return jsonify({'success': True})
        else:
            flash(f'"{song.name}" is already in playlist "{playlist.name}"', 'warning')
            return jsonify({'success': False, 'message': 'Song already in playlist'})
    
    @app.route('/api/playlist/<int:playlist_id>/remove/<int:song_id>', methods=['POST'])
    def remove_from_playlist(playlist_id, song_id):
        """Remove a song from a playlist"""
        playlist = Playlist.query.get_or_404(playlist_id)
        song = Song.query.get_or_404(song_id)
        
        success = playlist.remove_song(song)
        db.session.commit()
        
        if success:
            flash(f'"{song.name}" removed from playlist "{playlist.name}"', 'success')
            logger.info(f'Removed song {song.id} from playlist {playlist.id}')
            return jsonify({'success': True})
        else:
            flash(f'"{song.name}" is not in playlist "{playlist.name}"', 'warning')
            return jsonify({'success': False, 'message': 'Song not in playlist'})
    
    @app.route('/playlist/<int:playlist_id>/edit', methods=['GET', 'POST'])
    def edit_playlist(playlist_id):
        """Edit a playlist's details"""
        playlist = Playlist.query.get_or_404(playlist_id)
        
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            is_public = 'is_public' in request.form
            
            if not name:
                flash('Playlist name is required', 'danger')
                return redirect(url_for('edit_playlist', playlist_id=playlist.id))
            
            # Update playlist
            playlist.name = name
            playlist.description = description
            playlist.is_public = is_public
            db.session.commit()
            
            flash(f'Playlist updated successfully!', 'success')
            return redirect(url_for('view_playlist', playlist_id=playlist.id))
        
        return render_template('edit_playlist.html', playlist=playlist)
    
    @app.route('/playlist/<int:playlist_id>/delete', methods=['POST'])
    def delete_playlist(playlist_id):
        """Delete a playlist"""
        playlist = Playlist.query.get_or_404(playlist_id)
        
        name = playlist.name
        db.session.delete(playlist)
        db.session.commit()
        
        flash(f'Playlist "{name}" has been deleted', 'success')
        return redirect(url_for('playlists'))