#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

# from test_base import BucketlistTestCase

from tests.test_base import BaseTestCase

URL = '/api/v1.0/bucketlists/'


class BucketListTestCase(BaseTestCase):

    """Tests various endpoints to a bucketlist """

    def test_create_bucketlist_no_bucketlist_name(self):
        """ Test create bucketlist and no bucketlist name provided """

        data = {}
        response = self.client.post(URL, data=data,
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('No bucketlist name provided', str(data['message']))

    def test_create_bucketlist_duplicate(self):
        """ Test user cannot create an existing bucketlist """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        response = self.client.post(URL, data=data,
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['error']
                        == 'bucketlist_name Watch Anime already exists')

    def test_create_bucketlist(self):
        """ Test user can create bucketlist """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        response = self.client.post(URL, data=data,
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['message']
                        == 'New bucketlist created successfully')

    def test_get_bucketlist(self):
        """ Test user can get bucketlist """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        response = self.client.get(URL, headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('Watch Anime', str(data['bucketlists']))

    def test_get_bucketlist_by_id(self):
        """ Test user can get bucketlist by bucketlist ID """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        response = self.client.get(URL + '1/', headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['bucket_name']), 'Watch Anime')

    def test_get_bucketlist_by_query(self):
        """ Test user can get bucketlist by query """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        query = data['bucketlist_name']
        self.client.post(URL, data=data, headers=self.headers)
        response = self.client.get(URL + '?q=' + query,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('Watch Anime', str(data['bucketlists']))

    def test_get_bucketlist_limit_results(self):
        """ Test user can limit bucketlists output"""

        data_1 = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data_1, headers=self.headers)
        data = {
            'bucketlist_name': 'Watch Animee'
        }
        self.client.post(URL, data=data, headers=self.headers)
        response = self.client.get(URL + '?limit=1',
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('http://localhost' + URL + '?page=2&limit=1',
                      str(data['message']))
        self.assertIn('2', str(data['message']))

    def test_get_bucketlist_limit_results_has_previous_page(self):
        """ Test user can navigate through pages on limited output """

        data_1 = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data_1, headers=self.headers)
        data = {
            'bucketlist_name': 'Watch Animee'
        }
        self.client.post(URL, data=data, headers=self.headers)
        response = self.client.get(URL + '?page=2&limit=1',
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('http://localhost' + URL + '?page=1&limit=1',
                      str(data['message']))
        self.assertIn('2', str(data['message']))

    def test_update_bucketlist(self):
        """ Test user can update bucketlist """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        edit_data = {
            'bucketlist_name': 'Watch Animee'
        }
        response = self.client.put(URL + '1/', data=edit_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('Update was successfull', str(data['message']))

    def test_update_bucketlist_non_existant(self):
        """ Test user cannot update a non existant bucketlist """

        edit_data = {
            'bucketlist_name': 'Watch Animee'
        }
        response = self.client.put(URL + '1/', data=edit_data,
                                   headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['error']),
                      'bucketlist with id 1 does not exists')

    def test_delete_bucketlist(self):
        """ Test user can delete bucketlist """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        response = self.client.delete(URL + '1/', data=data,
                                      headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['message']),
                      'bucketlist with id 1 has been deleted')

    def test_delete_bucketlist_non_existant(self):
        """ Test user cannot delete a non existant bucketlist """

        data = {
            'bucketlist_name': 'Watch Anime'
        }
        self.client.post(URL, data=data, headers=self.headers)
        response = self.client.delete(URL + '2/', data=data,
                                      headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn(str(data['error']),
                      'bucketlist with id 2 does not exists')
