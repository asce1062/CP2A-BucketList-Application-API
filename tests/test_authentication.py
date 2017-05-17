import json

# from test_base import BucketlistTestCase
from tests.test_base import BaseTestCase

URL = "/api/v1.0/auth/"


class AuthTestCase(BaseTestCase):
    """ Testsuite for Login API """

    def test_login(self):
        """ Test user login """
        data = json.dumps(dict(
            email='tnkratos@gmail.com',
            password='onepiece'
        ))
        response = self.client.post(URL + 'login/', data=data,
                                    content_type='application/json')
        self.assertTrue(response.status_code, 200)

    def test_register(self):
        """ Test user registration """
        data = json.dumps(dict(
            username='asce1062',
            first_name='Alex',
            last_name='Ngugi',
            email='tnkratos@gmail.com',
            password='onepiece'
        ))
        response = self.client.post(URL + 'register/', data=data,
                                    content_type='application/json')
        self.assertIn(response.data.decode('utf-8'), 'Registration successful')
