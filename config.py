import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:cantcrackthis123@localhost/NewRSSApp'
    SECRET_KEY = 'super-secret'
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'fhasdgihwntlgy8f'


    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True #Set to false when deploying
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:cantcrackthis123@localhost/NewRSSApp'

config = {
'development': DevelopmentConfig,
'default': DevelopmentConfig
}