import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:cantcrackthis123@localhost/NewRSSApp'
    SECRET_KEY = 'reallydifficulttoguesskey313455664'
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'fhasdgihwntlgy8f'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'imranabdallah254@gmail.com'
    MAIL_PASSWORD = 'Gunners93@ChIll'

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