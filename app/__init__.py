from flask import Flask
from flask_security.utils import hash_password

from config import config
from flask_security import Security, SQLAlchemyUserDatastore
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

from app.models import User,Role

mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from app.forms import ExtendedRegisterForm

    # Setup Flask-Security
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security = Security(app, user_datastore, register_form=ExtendedRegisterForm)

    from .Aggregator import feeds as feeds_blueprint
    app.register_blueprint(feeds_blueprint)

    from .Users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    with app.app_context():
        db.init_app(app)
        mail.init_app(app)

        # user_role = Role(name='user')
        # author_role = Role(name='author')
        # super_user_role = Role(name='admin')
        # db.session.add(user_role)
        # db.session.add(super_user_role)
        # db.session.add(author_role)
        # db.session.commit()

        # super_user_role = db.session.query(Role).filter_by(id = 3).first()
        #
        # test_user = user_datastore.create_user(
        #     username='RssAdmin',
        #     email='admin@admin.com',
        #     password=hash_password('admin'),
        #     roles=[super_user_role]
        # )


    return app