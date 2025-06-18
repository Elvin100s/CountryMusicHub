import os
import sys

# Add your project directory to the sys.path
path = '/home/your_username/CountryMusicHub'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_CONFIG'] = 'production'

# Import your app
from app import app as application 