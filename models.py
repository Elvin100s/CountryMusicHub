from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
    
    def __repr__(self):
        return f'<Song {self.name}>'

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
        {"name": "George Jones", "description": "George Jones was an American musician, singer, and songwriter regarded as one of the most important and influential country singers of all time."}
    ]
    
    for artist_data in default_artists:
        artist = Artist.query.filter_by(name=artist_data["name"]).first()
        if not artist:
            artist = Artist(name=artist_data["name"], description=artist_data["description"])
            db.session.add(artist)
    
    db.session.commit()

# Initialize default data
def init_db():
    create_default_admin()
    create_default_artists()
