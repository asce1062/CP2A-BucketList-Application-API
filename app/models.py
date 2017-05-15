#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime

from app import db


class Users(db.Model):

    """ Model for Users table """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    bucketlist = db.relationship('Bucketlist', backref='users')

    def __repr__(self):

        # Print object in debugging.

        return '<User {}>'.format(self.email)

    @property
    def id(self):

        # Create and return property object of user_id

        return self.user_id


class Bucketlist(db.Model):

    """ Model for Bucketlist table """

    __tablename__ = 'bucketlist'

    bucket_id = db.Column(db.Integer, primary_key=True)
    bucket_name = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_modified = db.Column(db.DateTime,
                              default=datetime.datetime.now,
                              onupdate=datetime.datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                           nullable=False)
    items = db.relationship('BucketItem', backref='bucketlist')


class BucketItem(db.Model):

    """ Model for BucketItem table """

    __tablename__ = 'bucketitem'

    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(50), nullable=False)
    bucket_id = db.Column(db.Integer,
                          db.ForeignKey('bucketlist.bucket_id',
                                        ondelete='CASCADE'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_modified = db.Column(db.DateTime,
                              default=datetime.datetime.now,
                              onupdate=datetime.datetime.now)
    done = db.Column(db.Boolean, default=False)
