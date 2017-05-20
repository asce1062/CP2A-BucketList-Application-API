#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

# from test_base import BucketlistTestCase

from tests.test_base import BaseTestCase

URL = '/api/v1.0/auth/'


class AuthTestCase(BaseTestCase):

    """ Testsuite for Login API """

    def test_login(self):
        """ Test user login """

        data = {
            'email': 'tnkratos@gmail.com',
            'password': 'onepiece'
        }
        response = self.client.post(URL + 'login/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['message'] == 'Login Successful')

    def test_login_invalid_password(self):
        """ Test user login on invalid password provided"""

        data = {
            'email': 'tnkratos@gmail.com',
            'password': 'pieceone'
        }
        response = self.client.post(URL + 'login/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['error'] == 'Invalid password')

    def test_login_invalid_or_non_existant_email(self):
        """ Test user login on invalid email provided on non existant user"""

        data = {
            'email': 'kratostn@gmail.com',
            'password': 'onepiece'
        }
        response = self.client.post(URL + 'login/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(
            data['error'] == 'User with email kratostn@gmail.com does not exist.'
        )

    def test_login_no_email_provided(self):
        """ Test user login and no email is provided """

        data = {
            'password': 'onepiece'
        }
        response = self.client.post(URL + 'login/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('No email address provided', str(data['message']))

    def test_login_no_password_provided(self):
        """ Test user login and no password is provided """

        data = {
            'email': 'tnkratos@gmail.com'
        }
        response = self.client.post(URL + 'login/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('No password provided', str(data['message']))

    def test_register_user(self):
        """ Test user registration new user """

        data = {
            'username': 'asce10622',
            'first_name': 'Alexx',
            'last_name': 'Ngugii',
            'email': 'tnkratoss@gmail.com',
            'password': 'onepiecee',
        }

        response = self.client.post(URL + 'register/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['message'] == 'Registration successfull.')

    def test_register_user_no_username_provided(self):
        """ Test user registration new user and no username provided """

        data = {
            'first_name': 'Alexx',
            'last_name': 'Ngugii',
            'email': 'tnkratoss@gmail.com',
            'password': 'onepiecee',
        }

        response = self.client.post(URL + 'register/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('No username provided', str(data['message']))

    def test_register_user_no_first_name_provided(self):
        """ Test user registration new user and no first name provided """

        data = {
            'username': 'asce10622',
            'last_name': 'Ngugii',
            'email': 'tnkratoss@gmail.com',
            'password': 'onepiecee',
        }

        response = self.client.post(URL + 'register/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('No first name provided', str(data['message']))

    def test_register_user_no_last_name_provided(self):
        """ Test user registration new user and no last name provided """

        data = {
            'username': 'asce10622',
            'first_name': 'Alexx',
            'email': 'tnkratoss@gmail.com',
            'password': 'onepiecee',
        }

        response = self.client.post(URL + 'register/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('No last name provided', str(data['message']))

    def test_register_user_invalid_email_provided(self):
        """ Test user registration and invalid email provided """

        data = {
            'username': 'asce10622',
            'first_name': 'Alexx',
            'last_name': 'Ngugii',
            'email': 'tnkratoss.com@gmail',
            'password': 'onepiecee',
        }

        response = self.client.post(URL + 'register/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('Invalid email', str(data['message']))

    def test_register_user_no_password_provided(self):
        """ Test user registration new user and no password provided """

        data = {
            'username': 'asce10622',
            'first_name': 'Alexx',
            'last_name': 'Ngugii',
            'email': 'tnkratoss@gmail.com',
        }

        response = self.client.post(URL + 'register/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('No password provided', str(data['message']))

    def test_register_user_already_exists(self):
        """ Test user registration and user already exists """

        data = {
            'username': 'asce1062',
            'first_name': 'Alex',
            'last_name': 'Ngugi',
            'email': 'tnkratos@gmail.com',
            'password': 'onepiece',
        }

        self.client.post(URL + 'register/', data=data)
        response = self.client.post(URL + 'register/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['message']), 'User already exists')
