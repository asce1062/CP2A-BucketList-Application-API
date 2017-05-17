""" Base for tests """
import json
import unittest

from app import create_app, db
from app.models import Bucketlist, BucketItem, Users

class BaseTestCase(unittest.TestCase):
    """This class represents the bucketlist test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('testing')
        # Get the current context we are in, either setup, active or in between
        # Captures things in that context
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.client = self.app.test_client()

        new_user = Users(
            username='asce1062',
            first_name='Alex',
            last_name='Ngugi',
            email="tnkratos@gmail.com"
        )

        new_user.hash_this_pass("onepiece")
        db.session.add(new_user)
        db.session.commit()

        data = json.dumps(dict(
            email="tnkratos@gmail.com",
            password="onepiece"
        ))

        response = self.client.post("/api/v1.0/auth/login/", \
        data=data, content_type="application/json")
        data = json.loads(response.data.decode('utf-8'))
        auth_token = data['auth_token']

        self.headers = {
            'Authorization':'Token ' + auth_token,
            'Content-Type': 'application/json',
            'Accept':'application/json',
        }

    def tearDown(self):
        """ Clear resources after tests are run """
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
