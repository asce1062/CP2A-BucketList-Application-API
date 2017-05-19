#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Base for all tests """

import json

# Python unittesting framework.


import unittest

from app import create_app, db
from app.models import Users


class BaseTestCase(unittest.TestCase):

    """This class represents the bucketlist test cases"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app('testing')

        # Given that an application can be running in multiple threads
        # and serving multiple clients at once, context management will prove
        # very helpful in keeping things organized.
        # Get the current context we are in, either setup, active or in between
        # Captures variables in that context and make them available only when
        # needed.

        self.app_context = self.app.app_context()

        # Request context internally works like a stack
        # Add current context to the very top of the stack.

        self.app_context.push()
        db.create_all()

        # self.client attribute is an APIClient instance.

        self.client = self.app.test_client()

        new_user = Users(
            username='asce1062',
            first_name='Alex',
            last_name='Ngugi',
            email='tnkratos@gmail.com'
        )

        new_user.hash_this_pass('onepiece')
        db.session.add(new_user)
        db.session.commit()

        data = {
            'email':'tnkratos@gmail.com',
            'password':'onepiece'
            }

        response = self.client.post('/api/v1.0/auth/login/', data=data)

        # Convert response to string and string to dict.

        data = json.loads(response.data.decode())

        # Authentication token is the string with 'auth_token' key.

        auth_token = data['auth_token']

        # 'Authorization' : Set authorization type.
        # 'Accept' : Add ability to accept a JSON encoded entity from the request body.
        # 'Content-Type' : Designates the content to be in a specific format.

        self.headers = {'Authorization': 'Token' + auth_token,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'}

    def tearDown(self):
        """ Clear resources after tests are run """

        db.session.remove()
        db.drop_all()

        # Remove the context from the top of the stack.

        self.app_context.pop()
