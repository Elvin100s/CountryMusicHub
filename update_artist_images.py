
import os
from app import app
from models import Artist
from routes import get_artist_image

def update_all_artist_images():
    with app.app_context():
        artists = Artist.query.all()
        for artist in artists:
            print(f"Downloading image for {artist.name}...")
            get_artist_image(artist.name)

if __name__ == "__main__":
    update_all_artist_images()
    print("Artist image update complete!")
