#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

# from test_base import BucketlistTestCase

from tests.test_base import BaseTestCase

URL = '/api/v1.0/bucketlists/'


class BucketListTestCase(BaseTestCase):

    """Tests various endpoints to a bucketlist """

    def test_create_bucketlist(self):
        """ Test user can create bucketlist """

        new_bucketlist = json.dumps(dict(bucket_name='Anime'))
        response = self.client.post(URL, data=new_bucketlist,
                                    content_type='application/json',
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['bucket_name'] == 'Anime')

    def test_get_bucketlist(self):
        """ Test user can get bucketlist """

        response = self.client.get(URL, content_type='application/json'
                                   , headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_update_bucketlist(self):
        """ Test user can update bucketlist """

        edit_bucketlist = json.dumps(dict(bucket_name='Game'))
        url = '/api/v1.0/bucketlists/1/'
        response = self.client.put(url, data=edit_bucketlist,
                                   content_type='application/json',
                                   headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_bucketlists(self):
        """ Test user can get all bucketlists saved in the database """

        new_bucketlist = json.dumps(dict(bucket_name='Kaizoku'))
        response = self.client.post(URL, data=new_bucketlist,
                                    content_type='application/json',
                                    headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_duplicate_bucketlist(self):
        """ Test endpoint behavior on creation of duplicate bucketlist """

        new_bucketlist = json.dumps(dict(bucket_name='Manga'))
        self.client.post(URL, data=new_bucketlist,
                         content_type='application/json',
                         headers=self.headers)
        response = self.client.post(URL, data=new_bucketlist,
                                    content_type='application/json',
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['error']
                        == 'bucketlist_name Asia already exists')
