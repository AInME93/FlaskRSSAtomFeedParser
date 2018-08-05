#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Feed, FeedEntry, User, Role
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


#The make_shell_context() function registers the application and database instances and the models
# so that they are automatically imported into the shell
def make_shell_context():
    return dict(app=app, db=db, Feed=Feed, FeedEntry = FeedEntry, User = User, Role = Role)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

