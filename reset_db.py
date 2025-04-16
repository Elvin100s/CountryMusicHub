"""
Reset and initialize the database with default artists and admin.
This script will add the new artists including Bryan Adams.
"""
import logging
from app import app, db
from models import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    """Drop all tables and recreate them with fresh data."""
    with app.app_context():
        logger.info("Dropping all tables...")
        db.drop_all()
        
        logger.info("Creating all tables...")
        db.create_all()
        
        logger.info("Initializing default data (admin and artists)...")
        init_db()
        
        logger.info("Database reset and initialized successfully!")

if __name__ == "__main__":
    reset_database()