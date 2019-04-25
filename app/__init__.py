#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_api import FlaskAPI

# Add basic SQLAlchemy support to our app.

from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

# Control the SQLAlchemy integration for our Flask application
# provide access to all the SQLAlchemy functions and classes

db = SQLAlchemy()


# wraps the creation of a new Flask object

def create_app(config_name):
    """create_app

    :param config_name:
    """
    # load configuration variables from an instance folder

    app = FlaskAPI(__name__, instance_relative_config=True)

    # Updates values from a given object. Object can be a string
    # or an actual object reference.

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Update the config from a python file.
    # load the specified file from the instance/ directory.

    app.config.from_pyfile('config.py')

    from app.user import user_blueprint
    app.register_blueprint(user_blueprint)

    from app.bucket_list import blueprint
    app.register_blueprint(blueprint)

    # connect to the db
    # Initialize the app for use with this database instance.

    db.init_app(app)

    return app
