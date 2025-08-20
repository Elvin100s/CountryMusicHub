from app import db

def create_default_admin():
    from models import Admin
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin')
        admin.set_password('country_admin')
        db.session.add(admin)
        db.session.commit()

def create_default_artists():
    from models import Artist
    from routes import get_artist_image
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
    for artist_data in default_artists:
        artist = Artist.query.filter_by(name=artist_data["name"]).first()
        if not artist:
            get_artist_image(artist_data["name"])
            artist = Artist(name=artist_data["name"], description=artist_data["description"])
            db.session.add(artist)
    db.session.commit()

def create_default_playlist():
    from models import Playlist
    default_playlist = Playlist.query.filter_by(name='My Favorites').first()
    if not default_playlist:
        default_playlist = Playlist(
            name='My Favorites',
            description='A collection of my favorite country songs',
            is_public=True
        )
        db.session.add(default_playlist)
        db.session.commit()

def init_db():
    create_default_admin()
    create_default_artists()
