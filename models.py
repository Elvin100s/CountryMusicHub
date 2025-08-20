from extensions import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Association table for playlists and songs (many-to-many relationship)
playlist_songs = db.Table('playlist_songs',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True)
)

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    songs = db.relationship('Song', backref='artist', lazy=True)
    
    def __repr__(self):
        return f'<Artist {self.name}>'

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    source = db.Column(db.String(50), nullable=True)  # Where the song was downloaded from
    source_url = db.Column(db.String(255), nullable=True)  # Original URL of the song
    download_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with playlists through the association table
    playlists = db.relationship('Playlist', secondary=playlist_songs, 
                              back_populates='songs')
    
    def __repr__(self):
        return f'<Song {self.name}>'

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_public = db.Column(db.Boolean, default=True)  # If True, anyone can view this playlist
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with songs through the association table
    songs = db.relationship('Song', secondary=playlist_songs,
                          back_populates='playlists')
    
    def add_song(self, song):
        """Add a song to the playlist if it's not already there"""
        if song not in self.songs:
            self.songs.append(song)
            return True
        return False
        
    def remove_song(self, song):
        """Remove a song from the playlist"""
        if song in self.songs:
            self.songs.remove(song)
            return True
        return False
    
    def __repr__(self):
        return f'<Playlist {self.name} with {len(self.songs)} songs>'

