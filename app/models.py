#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os

# Add basic SQLAlchemy support to our app.

# Suit for password hashing and generation routines.

from passlib.apps import custom_app_context as pwd_context

# A module that implements various functions to deal with unstrusted
# sources. Mainly useful for web applications.
# TimedJSONWebSignatureSerializer: Implement JWS but also record time of signature signing.
# This will help in cases of expired signatures.
# BadSignature: Raise error if signature does not match.
# SignatureExpired: Catch signature timestamps that are older than required max_age.

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
    BadSignature, SignatureExpired

from app import db


class Users(db.Model):

    """ Model for Users table """

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    bucketlist = db.relationship('Bucketlist', backref='users')

    def hash_this_pass(self, password):
        """ Creates a hash value from password passed """

        self.password_hash = pwd_context.encrypt(password)

    def verify_pass(self, password):
        """ Compare hashed password from db with password """

        # returns bolean

        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=10000):
        """ Calculates and returns an auth token """

        serializer = Serializer(os.getenv('SECRET'),
                                expires_in=expiration)

        # return generated token

        return serializer.dumps({'id': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        """ verify authentication token """

        serializer = Serializer(os.getenv('SECRET'))
        try:
            data = serializer.loads(token)
        except SignatureExpired:

            # valid token that has expired

            return None
        except BadSignature:

            # invalid token

            return None
        user = Users.query.get(data['id'])
        return user


class Bucketlist(db.Model):

    """ Model for Bucketlist table """

    __tablename__ = 'bucketlist'

    bucket_id = db.Column(db.Integer, primary_key=True,
                          autoincrement=True)
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

    item_id = db.Column(db.Integer, primary_key=True,
                        autoincrement=True)
    item_name = db.Column(db.String(50), nullable=False)
    bucket_id = db.Column(db.Integer,
                          db.ForeignKey('bucketlist.bucket_id',
                                        ondelete='CASCADE'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    date_modified = db.Column(db.DateTime,
                              default=datetime.datetime.now,
                              onupdate=datetime.datetime.now)
    done = db.Column(db.Boolean, default=False)
