from app import app, db
from models import Artist

with app.app_context():
    if not Artist.query.filter_by(name="Frank Sinatra").first():
        frank = Artist(name="Frank Sinatra", description="Frank Sinatra was an American singer and actor, one of the most popular and influential musical artists of the 20th century.")
        db.session.add(frank)
        db.session.commit()
        print("Frank Sinatra added!")
    else:
        print("Frank Sinatra already exists.")
