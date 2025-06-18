import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MUSIC_FOLDER = os.path.join('static', 'music')
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///country_music.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///test_country_music.db'

class ProductionConfig(Config):
    # For PythonAnywhere, we'll use MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://{username}:{password}@{hostname}/{databasename}'.format(
            username=os.environ.get('MYSQL_USERNAME', 'your_username'),
            password=os.environ.get('MYSQL_PASSWORD', 'your_password'),
            hostname=os.environ.get('MYSQL_HOST', 'your_username.mysql.pythonanywhere-services.com'),
            databasename=os.environ.get('MYSQL_DATABASE', 'your_username$default')
        )
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Log to stderr in production
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 