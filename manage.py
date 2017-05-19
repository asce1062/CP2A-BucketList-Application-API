#!/usr/bin/python
# -*- coding: utf-8 -*-

# manage.py

import os

  # Controller class for handling a set of commands

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import db, create_app
from app import models

app = create_app(config_name=os.getenv('APP_SETTINGS'))
with app.app_context():
    from app.models import Users, BucketItem, Bucketlist
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates database with tables"""

    os.system('createdb flask_api')
    os.system('createdb test_db')
    db.create_all()
    db.session.commit()


@manager.command
def drop_db():
    """Deletes database"""

    os.system('dropdb test_db')
    os.system('dropdb flask_api')

if __name__ == '__main__':
    manager.run()
