#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

# from test_base import BucketlistTestCase

from tests.test_base import BaseTestCase

URL = '/api/v1.0/bucketlists/'


class BucketListTestCase(BaseTestCase):

    """This class represents the bucketlist(s) item(s) test cases"""

    def test_create_bucketlist_item_no_item_name(self):
        """ Test create bucketlist item and no item name provided """
        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        item_data = {}
        response = self.client.post(URL + '1/items/', data=item_data,
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('No item name provided', str(data['message']))

    def test_create_bucketlist_item_non_existant_bucketlist(self):
        """ Test create bucketlist item and bucket list does not exist """
        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        response = self.client.post(URL + '2/items/', data=item_data,
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['error']), 'Bucketlist id 2 does not exists')

    def test_create_bucketlist_item(self):
        """ Test create bucketlist item """
        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        response = self.client.post(URL + '1/items/', data=item_data,
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('New bucketlist item created successfully', str(data['message']))
