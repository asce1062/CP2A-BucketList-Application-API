#!/usr/bin/python
# -*- coding: utf-8 -*-

# Blueprint : Keep a record of functions that will be called with a class.

from flask import Blueprint

# Api : Main entry point of the application.
# Resource : Represent an abstract RESTful resource.

from flask_restful import Api, Resource, fields, inputs, reqparse

from app.models import Users
from app import db

# Declare our Blueprint

user_blueprint = Blueprint('user_endpoint', __name__)

# Define application entry point

auth_api = Api(user_blueprint)

user_fields = {
    'user_id': fields.Integer,
    'username': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password_hash': fields.String,
}


class LoginAPI(Resource):

    """ Create endpoints for LoginAPI """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            type=str,
            required=True,
            help='No email address provided'
        )
        self.reqparse.add_argument(
            'password',
            type=str,
            required=True,
            help='No password provided'
        )
        super(LoginAPI, self).__init__()

    def post(self):
        """ Login a user """

        args = self.reqparse.parse_args()

        # Fetch the user data

        user_data = Users.query.filter_by(email=args['email']).first()

        try:
            if user_data:
                if user_data.verify_pass(args['password']):
                    give_token = user_data.generate_auth_token()
                    json_response = {
                        'message': 'Login Successful',
                        'auth_token': give_token.decode('utf-8')
                    }
                    return (json_response, 200)
                else:

                    json_response = {
                        'error': 'Invalid password'
                    }
                    return (json_response, 401)
            else:

                json_response = \
                    {
                        'error': 'User with email {} does not exist.'.format(args['email'])
                    }
                return (json_response, 404)
        except:

            json_response = {
                'error': 'Login Failed'
            }
            return (json_response, 500)


class RegisterAPI(Resource):

    """ Create endpoints for RegisterAPI """

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            type=str,
            required=True,
            help='No username provided'
        )
        self.reqparse.add_argument(
            'first_name',
            type=str,
            required=True,
            help='No first name provided'
        )
        self.reqparse.add_argument(
            'last_name',
            type=str,
            required=True,
            help='No last name provided'
        )
        self.reqparse.add_argument(
            'email',
            type=inputs.regex(r'[^@]+@[^@]+\.[^@]+'),
            required=True,
            help='Invalid email'
        )
        self.reqparse.add_argument(
            'password',
            type=str,
            required=True,
            help='No password provided'
        )
        super(RegisterAPI, self).__init__()

    def post(self):
        """ Register a user """

        args = self.reqparse.parse_args()

        # Check whether user already exists.

        user_data = Users.query.filter_by(email=args['email']).first()

        if not user_data:
            try:
                user_data = Users(
                    username=args['username'],
                    first_name=args['first_name'],
                    last_name=args['last_name'],
                    email=args['email'],
                    password_hash=args['password']
                )

                # Hash password before saving to db

                user_data.hash_this_pass(args['password'])

                # Save user to db

                db.session.add(user_data)
                db.session.commit()
                json_response = {
                    'message': 'Registration successfull.'
                }
                return (json_response, 201)
            except:
                json_response = \
                    {
                        'message': 'Unable to register new user {} .'.format(args['username'])
                    }
                return (json_response, 400)
        else:
            json_response = {
                'message': 'User already exists'
            }
            return (json_response, 409)


auth_api.add_resource(
    LoginAPI,
    '/api/v1.0/auth/login/',
    endpoint='login'
)
auth_api.add_resource(
    RegisterAPI,
    '/api/v1.0/auth/register/',
    endpoint='register'
)
