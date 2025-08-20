import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask
from app import db, create_app
from models import Artist

app = create_app()

with app.app_context():
    if not Artist.query.filter_by(name="Frank Sinatra").first():
        frank = Artist(name="Frank Sinatra", description="Frank Sinatra was an American singer and actor, one of the most popular and influential musical artists of the 20th century.")
        db.session.add(frank)
        db.session.commit()
        print("Frank Sinatra added!")
    else:
        print("Frank Sinatra already exists.")
