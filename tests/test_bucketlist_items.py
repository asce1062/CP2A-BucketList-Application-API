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
        self.assertIn(str(data['error']),
                      'Bucketlist id 2 does not exists')

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
        self.assertIn('New bucketlist item created successfully',
                      str(data['message']))

    def test_get_bucketlist_item_by_id_for_a_specific_bucketlist(self):
        """ Test get single bucketlist item by ID """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        self.client.post(URL + '1/items/', data=item_data,
                         headers=self.headers)
        response = self.client.get(URL + '1/items/1', data=item_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['item_name']), 'One Piece')

    def test_get_bucketlist_items_for_a_specific_bucketlist(self):
        """ Test get all bucketlist item(s) for a specific bucketlist """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        self.client.post(URL + '1/items/', data=item_data,
                         headers=self.headers)
        response = self.client.get(URL + '1/items/', data=item_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('One Piece', str(data))

    def test_get_bucketlist_items_non_existant_bucketlist(self):
        """ Test get all bucketlist item(s) for a non existant bucketlist """

        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        response = self.client.get(URL + '1/items/', data=item_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['error']), 'No items found')

    def test_get_bucketlist_items_no_items_created(self):
        """ Test get all bucketlist item(s) and no items created """

        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        response = self.client.get(URL + 'items/', data=item_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['error']), 'No items found')

    def test_get_bucketlist_items(self):
        """ Test get all bucketlist items """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        self.client.post(URL + '1/items/', data=item_data,
                         headers=self.headers)
        response = self.client.get(URL + 'items/', data=item_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('One Piece', str(data['items']))

    def test_update_bucketlist_item(self):
        """ Test update bucketlist item """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        self.client.post(URL + '1/items/', data=item_data,
                         headers=self.headers)
        edit_item_data = {
            'item_name': 'One Piece',
            'done': 'True'
        }
        response = self.client.put(URL + '1/items/1',
                                   data=edit_item_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('True', str(data['done']))

    def test_update_bucketlist_item_non_existant_bucketlist_id(self):
        """ Test update bucketlist item non existant bucketlist ID """

        edit_item_data = {
            'item_name': 'One Piece',
            'done': 'True'
        }
        response = self.client.put(URL + '1/items/1',
                                   data=edit_item_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['error']),
                      'bucketlist id does not exists')

    def test_update_bucketlist_item_non_existant_item(self):
        """ Test update bucketlist item non existant item ID """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        edit_item_data = {
            'item_name': 'One Piece',
            'done': 'True'
        }
        response = self.client.put(URL + '1/items/1',
                                   data=edit_item_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['error']), 'item id does not exists')

    def test_delete_bucketlist_item(self):
        """ Test delete bucketlist item """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        self.client.post(URL + '1/items/', data=item_data,
                         headers=self.headers)
        response = self.client.delete(URL + '1/items/1',
                                      data=item_data, headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['message']),
                      'Item with id 1 has been deleted')

    def test_delete_bucketlist_item_non_existant_item_bucketlist_or_both(self):
        """ Test delete bucketlist item non existant bucketlist, item or both """

        item_data = {
            'item_name': 'One Piece',
            'done': 'False'
        }
        response = self.client.delete(URL + '1/items/1',
                                      data=item_data, headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['error']),
                      'bucketlist id or item_id does not exists')
