from app import db
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

# Create initial admin if it doesn't exist
def create_default_admin():
    from app import db
    
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin')
        admin.set_password('country_admin')
        db.session.add(admin)
        db.session.commit()

# Create initial artists
def create_default_artists():
    from app import db
    
    default_artists = [
        {"name": "Don Williams", "description": "Don Williams was an American country music singer, songwriter, and 2010 inductee to the Country Music Hall of Fame."},
        {"name": "Kenny Rogers", "description": "Kenny Rogers was an American singer, songwriter, musician, actor, and entrepreneur known for his raspy voice and hits like 'The Gambler'."},
        {"name": "Dolly Parton", "description": "Dolly Parton is an American singer, songwriter, multi-instrumentalist, actress, author, businesswoman, and humanitarian, known for her work in country music."},
        {"name": "Johnny Cash", "description": "Johnny Cash was an American singer, songwriter, musician, and actor known for his deep, calm bass-baritone voice."},
        {"name": "Patsy Cline", "description": "Patsy Cline was an American country music singer who helped popularize the genre in the early 1960s."},
        {"name": "Willie Nelson", "description": "Willie Nelson is an American musician, actor, and activist, a critical figure in outlaw country music."},
        {"name": "Tammy Wynette", "description": "Tammy Wynette was an American country music singer-songwriter known as the 'First Lady of Country Music'."},
        {"name": "George Jones", "description": "George Jones was an American musician, singer, and songwriter regarded as one of the most important and influential country singers of all time."},
        {"name": "Bryan Adams", "description": "Bryan Adams is a Canadian rock and country musician known for hits like 'Summer of '69' and 'Everything I Do (I Do It For You)'."},
        {"name": "Shania Twain", "description": "Shania Twain is a Canadian singer and songwriter who has sold over 100 million records, making her the best-selling female artist in country music history."},
        {"name": "Garth Brooks", "description": "Garth Brooks is an American singer and songwriter who has integrated pop and rock elements into country music and is one of the world's best-selling artists."},
        {"name": "Reba McEntire", "description": "Reba McEntire is an American country music singer, actress, and businesswoman known as 'The Queen of Country'."},
        {"name": "Tim McGraw", "description": "Tim McGraw is an American country singer, actor, and record producer who has released many hit albums and singles throughout his career."},
        {"name": "Faith Hill", "description": "Faith Hill is an American singer and record producer who is one of the most successful country artists of all time."},
        {"name": "Keith Urban", "description": "Keith Urban is an Australian-American musician, singer, guitarist, and songwriter known for his fusion of country with rock and pop elements."}
    ]
    
    from routes import get_artist_image
    
    for artist_data in default_artists:
        artist = Artist.query.filter_by(name=artist_data["name"]).first()
        if not artist:
            # Try to download artist image when creating default artists
            get_artist_image(artist_data["name"])
            artist = Artist(name=artist_data["name"], description=artist_data["description"])
            db.session.add(artist)
    
    db.session.commit()

# Create a default playlist
def create_default_playlist():
    from app import db
    
    default_playlist = Playlist.query.filter_by(name='My Favorites').first()
    if not default_playlist:
        default_playlist = Playlist(
            name='My Favorites',
            description='A collection of my favorite country songs',
            is_public=True
        )
        db.session.add(default_playlist)
        db.session.commit()

# Initialize default data
def init_db():
    create_default_admin()
    create_default_artists()
    create_default_playlist()
