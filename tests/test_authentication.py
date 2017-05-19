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

    def test_login_no_email_provided(self):
        """ Test user login and no email is provided """

        data = {
            'password': 'onepiece'
        }
        response = self.client.post(URL + 'login/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('No email address provided', str(data['message']))

    def test_register_user_already_exists(self):
        """ Test user registration and user already exists """

        data = {
            'username': 'asce1062',
            'first_name': 'Alex',
            'last_name': 'Ngugi',
            'email': 'tnkratos@gmail.com',
            'password': 'onepiece'
        }

        self.client.post(URL + 'register/', data=data)
        response = self.client.post(URL + 'register/', data=data)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['message']), 'User already exists')

    def test_register_user(self):
        """ Test user registration new user """

        data = {
            'username': 'asce10622',
            'first_name': 'Alexx',
            'last_name': 'Ngugii',
            'email': 'tnkratoss@gmail.com',
            'password': 'onepiecee'
        }

        response = self.client.post(URL + 'register/', data=data)
        self.assertTrue(str(response.data),
                        'Registration successfull.')
