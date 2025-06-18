import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from config import config

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load the appropriate configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Set up proxy fix for HTTPS
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize the app with the extension
    db.init_app(app)
    
    with app.app_context():
        # Import the models
        import models
        
        # Create all tables
        db.create_all()
        
        # Import and register routes
        from routes import register_routes
        from admin import register_admin_routes
        from playlist_routes import register_playlist_routes
        
        register_routes(app)
        register_admin_routes(app)
        register_playlist_routes(app)
        
        return app

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    # Get the port from environment variable or use 8080
    port = int(os.environ.get('PORT', 8080))
    # Run the app
    app.run(host='0.0.0.0', port=port)
