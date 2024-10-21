import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    TESTING = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'database', 'database.db')
    DATABASE = os.path.join(basedir, 'database', 'database.db')

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True
    DATABASE = ':memory:'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
