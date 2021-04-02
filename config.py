import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:posgtres@localhost/jumla'
    SECRET_KEY = 'reallydifficulttoguesskey313455664'

    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_SALT = 'fhasdgihwntlgy8f'
    SECURITY_REGISTER_USER_TEMPLATE = 'security/register.html'
    SECURITY_LOGIN_USER_TEMPLATE = 'security/login.html'
    SECURITY_POST_LOGIN_VIEW =  '/feeds'
    SECURITY_POST_LOGOUT_VIEW = '/'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'imranabdallah254@gmail.com'
    MAIL_PASSWORD = 'Gunners93@ChIll'

    HOST = '0.0.0.0'
    # HOST = '127.0.0.1'

    PORT = '5000'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True #Set to false when deploying
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost/jumla'

config = {
'development': DevelopmentConfig,
'default': DevelopmentConfig
}