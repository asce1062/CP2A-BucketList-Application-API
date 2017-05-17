import json

# from test_base import BucketlistTestCase
from tests.test_base import BaseTestCase

URL = "/api/v1.0/bucketlists/"


class BucketListTestCase(BaseTestCase):
    """This class represents the bucketlist(s) item(s) test cases"""

    def test_create_bucketlist_item(self):
        """ Test user can create bucketlist item """
        new_bucketlist = json.dumps(dict(bucket_name='Anime'))
        self.client.post(URL, data=new_bucketlist,
                         content_type='application/json', headers=self.headers)
        new_bucketlist_item = json.dumps(dict(bucket_name="Watch One Piece"))
        url = "/api/v1.0/bucketlists/1/items/"
        response = self.client.post(url, data=new_bucketlist_item,
                                    content_type='application/json',
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['bucket_name'] == 'Watch One Piece')

    def test_create_bucketlist_item_non_existant_bucketlist_id(self):
        """ Test user creates a bucketlist item for a non-existant bucketlist """
        url = "/api/v1.0/bucketlists/1062/items/"
        new_bucketlist_item = json.dumps(dict(bucket_name="Watch One Piece"))
        response = self.client.post(url, data=new_bucketlist_item,
                                    content_type='application/json',
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['error'] == 'Bucketlist_id 1062 does not exists')

    def test_update_bucketlist_item_non_existant_item_id(self):
        """ Test user updating a non-existsnt bucketlist item """
        new_bucketlist = json.dumps(dict(bucket_name='Anime'))
        self.client.post(URL, data=new_bucketlist,
                         content_type='application/json', headers=self.headers)
        url = "/api/v1.0/bucketlists/1/items/1062"
        new_bucketlist_item = json.dumps(dict(bucket_name="Watch One Piece"))
        response = self.client.post(url, data=new_bucketlist_item,
                                    content_type='application/json',
                                    headers=self.headers)
        data = json.loads(response.data.decode('utf-8'))
        self.assertTrue(data['error'] == 'item_id does not exists')
