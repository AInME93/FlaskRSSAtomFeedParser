from flask import Flask
from config import config
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail

from app.models import User,Role,db

mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore)

    from .Aggregator import feeds as feeds_blueprint
    app.register_blueprint(feeds_blueprint)

    from .Users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    with app.app_context():
        db.init_app(app)
        mail.init_app(app)


    return app