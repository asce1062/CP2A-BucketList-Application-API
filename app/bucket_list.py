#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, Flask, g, request
from flask_httpauth import HTTPTokenAuth
from flask_restful import Api, Resource, fields, marshal, reqparse

from app import create_app, db
from app.models import BucketItem, Bucketlist, Users

blueprint = Blueprint('bucket_list', __name__)
api = Api(blueprint)

auth_user = HTTPTokenAuth(scheme='Token')


@auth_user.verify_token
def verify_token(token):
    """ Validate token passes """

    user = Users.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True


bucket_item_fields = {
    'item_id': fields.Integer,
    'item_name': fields.String,
    'bucket_id': fields.Integer,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean,
}

bucketlist_fields = {
    'bucket_id': fields.Integer,
    'bucket_name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.Integer,
    'items': fields.Nested(bucket_item_fields),
}


class BucketListAPI(Resource):

    """ Create endpoints for BucketListAPI """

    decorators = [auth_user.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'bucketlist_name',
            type=str,
            required=True,
            help='No bucketlist name provided'
        )
        super(BucketListAPI, self).__init__()

    def get(self, id=None):
        """ List all created bucketlists """

        if id:
            this_bucketlist = Bucketlist.query.filter_by(bucket_id=id,
                                                         created_by=g.user.user_id).first()
            return (marshal(this_bucketlist, bucketlist_fields), 200)
        else:
            self.reqparse = reqparse.RequestParser()
            self.reqparse.add_argument(
                'q',
                type=str,
                location='args'
            )
            self.reqparse.add_argument(
                'limit',
                type=int,
                location='args',
                default=20
            )
            self.reqparse.add_argument(
                'page',
                type=int,
                location='args',
                default=1
            )

            args = self.reqparse.parse_args()
            query = args['q']
            limit = args['limit']
            page = args['page']

            if query:
                bucketlists = \
                    Bucketlist.query.filter(
                        Bucketlist.bucket_name.like(
                            '%' + query + '%'),
                        Bucketlist.created_by == g.user.user_id).paginate(page, limit, False)
            else:
                bucketlists = \
                    Bucketlist.query.filter_by(created_by=g.user.user_id).paginate(page,
                                                                                   limit, False)
            if not bucketlists:
                return (
                    {
                        'message': 'Bucketlist not found'
                    }, 400
                )
            if bucketlists.has_prev:
                prev_page = request.url_root + 'api/v1.0/bucketlists/' \
                    + '?page=' + str(page - 1) + '&limit=' + str(limit)
            else:
                prev_page = 'None'
            if bucketlists.has_next:
                next_page = request.url_root + 'api/v1.0/bucketlists/' \
                    + '?page=' + str(page + 1) + '&limit=' + str(limit)
            else:
                next_page = 'None'
            return (
                {
                    'message':
                    {
                        'next_page': next_page,
                        'prev_page': prev_page,
                        'total_pages': bucketlists.pages
                    },
                    'bucketlists': marshal(
                        bucketlists.items,
                        bucketlist_fields
                    )
                }, 200
            )

    def post(self):
        """ Create a new bucket list """

        args = self.reqparse.parse_args()
        name = args['bucketlist_name']

        check_duplicate = Bucketlist.query.filter_by(bucket_name=name,
                                                     created_by=g.user.user_id).first()

        if check_duplicate:
            return (
                {
                    'error': 'bucketlist_name {} already exists'.format(name)
                }, 403
            )

        new_bucketlist = Bucketlist(bucket_name=name,
                                    created_by=g.user.user_id)
        db.session.add(new_bucketlist)
        db.session.commit()

        return (
            {
                'message': 'New bucketlist created successfully',
                'bucketlist': marshal(
                    new_bucketlist,
                    bucket_item_fields
                )
            }, 201
        )

    def put(self, id):
        """ Update a bucket list """

        this_bucket_list = Bucketlist.query.filter_by(bucket_id=id,
                                                      created_by=g.user.user_id).first()
        if not this_bucket_list:
            return (
                {
                    'error': 'bucketlist with id {} does not exists'.format(id)
                }, 400
            )
        args = self.reqparse.parse_args()
        name = args['bucketlist_name']

        update_bucketlist = \
            Bucketlist.query.filter_by(bucket_id=id).first()
        update_bucketlist.bucket_name = name
        db.session.commit()

        return (
            {
                'message': 'Update was successfull',
                'bucketlist': marshal(
                    update_bucketlist,
                    bucket_item_fields
                )
            }, 201
        )

    def delete(self, id):
        """ Delete a single bucket list """

        this_bucket_list = Bucketlist.query.filter_by(bucket_id=id,
                                                      created_by=g.user.user_id).first()
        if not this_bucket_list:
            return (
                {
                    'error': 'bucketlist with id {} does not exists'.format(id)
                }, 400
            )

        db.session.delete(this_bucket_list)
        db.session.commit()

        return (
            {
                'message': 'bucketlist with id {} has been deleted'.format(id)
            }, 202
        )


class BucketItemAPI(Resource):

    """ Create endpoints for BucketItemAPI """

    decorators = [auth_user.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'item_name',
            type=str,
            required=True,
            help='No item name provided'
        )
        self.reqparse.add_argument('done', default=False, type=bool)
        super(BucketItemAPI, self).__init__()

    def get(self, bucketlist_id=None, item_id=None):
        """ Fetch all created items """

        if item_id:
            this_item = \
                BucketItem.query.filter_by(
                    bucket_id=bucketlist_id, item_id=item_id).first()
            return (marshal(this_item, bucket_item_fields), 200)

        if bucketlist_id:
            this_item = \
                BucketItem.query.filter_by(bucket_id=bucketlist_id).all()
            if not this_item:
                return (
                    {
                        'error': 'No items found'
                    }, 400
                )
            return (marshal(this_item, bucket_item_fields), 200)

        else:
            items = BucketItem.query.filter().all()
            if not items:
                return (
                    {
                        'error': 'No items found'
                    }, 400
                )
            return (
                {
                    'items': marshal(
                        items,
                        bucket_item_fields
                    )
                }, 200
            )

    def post(self, bucketlist_id):
        """ Create a new item in bucket list based on the bucketlist_id """

        args = self.reqparse.parse_args()
        name = args['item_name']
        bucketlist_exists = \
            Bucketlist.query.filter_by(bucket_id=bucketlist_id,
                                       created_by=g.user.user_id).first()

        if not bucketlist_exists:
            return (
                {
                    'error': 'Bucketlist id {} does not exists'.format(bucketlist_id)
                }, 400
            )

        new_item = BucketItem(item_name=name, bucket_id=bucketlist_id)
        db.session.add(new_item)
        db.session.commit()

        return (
            {
                'message': 'New bucketlist item created successfully',
                'bucketlist': marshal(
                    new_item,
                    bucket_item_fields)
            }, 201
        )

    def put(self, bucketlist_id, item_id):
        """ Update a bucket list item """

        bucketlist_exists = \
            Bucketlist.query.filter_by(bucket_id=bucketlist_id).first()

        if bucketlist_exists:
            item_exists = \
                BucketItem.query.filter_by(item_id=item_id).first()

            if item_exists:
                args = self.reqparse.parse_args()
                name = args['item_name']
                done = args['done']

                if name:
                    item_exists.item_name = name

                if done in [True, False]:
                    item_exists.done = done

                db.session.commit()

                return marshal(item_exists, bucket_item_fields)
            else:

                return (
                    {
                        'error': 'item id does not exists'
                    }, 400
                )
        else:

            return (
                {
                    'error': 'bucketlist id does not exists'
                }, 400
            )

    def delete(self, bucketlist_id, item_id):
        """ Delete an item in a bucket list """

        bucketlist_exists = \
            Bucketlist.query.filter_by(bucket_id=bucketlist_id).first()
        item_exists = \
            BucketItem.query.filter_by(item_id=item_id).first()

        if not (bucketlist_exists or item_exists):
            return (
                {
                    'error': 'bucketlist id or item_id does not exists'
                }, 400
            )

        db.session.delete(item_exists)
        db.session.commit()

        return (
            {
                'message': 'Item with id {} has been deleted'.format(item_id)
            }, 202
        )


api.add_resource(BucketListAPI, '/api/v1.0/bucketlists/<int:id>/',
                 '/api/v1.0/bucketlists/', endpoint='bucketlists')
api.add_resource(BucketItemAPI,
                 '/api/v1.0/bucketlists/<int:bucketlist_id>/items/',
                 '/api/v1.0/bucketlists/<int:bucketlist_id>/items/<int:item_id>',
                 '/api/v1.0/bucketlists/items/', endpoint='items')
