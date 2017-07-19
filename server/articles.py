#!/usr/bin/env python
#
# Copyright 2017 Gianni Valdambrini, Develer s.r.l. <aleister@develer.com>
# All rights reserved.

from flask import Flask
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from http.client import CREATED
from http.client import NO_CONTENT
from http.client import NOT_FOUND
from http.client import OK
from peewee import CharField
from peewee import Model
from peewee import SqliteDatabase
from peewee import UUIDField
from flask_cors import CORS
import uuid

app = Flask(__name__)
api = Api(app)
CORS(app)

DATABASE_FN = 'articles.db'
database = SqliteDatabase(DATABASE_FN)

@app.before_request
def _db_connect():
    if database.is_closed():
        database.connect()

@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()


class BaseModel(Model):
    class Meta:
        database = database


class ArticleModel(BaseModel):
    aid = UUIDField(unique=True)
    title = CharField()
    content = CharField()

    def json(self):
        return {
            'aid': str(self.aid),
            'title': self.title,
            'content': self.content
        }


def create_tables():
    database.connect()
    ArticleModel.create_table(fail_silently=True)


def non_empty_str(val, name):
    if not str(val).strip():
        raise ValueError('The argument {} is not empty'.format(name))
    return str(val)


class Articles(Resource):
    """Article collection endpoints"""

    def get(self):
        return [o.json() for o in ArticleModel.select()], OK

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=non_empty_str, required=True)
        parser.add_argument('content', type=non_empty_str, required=True)
        args = parser.parse_args(strict=True)

        obj = ArticleModel.create(
            aid=uuid.uuid4(),
            title=args['title'],
            content=args['content']
        )
        return obj.json(), CREATED


class Article(Resource):
    """Article endpoints"""
    def get(self, aid):
        try:
            return ArticleModel.get(aid=aid).json(), OK
        except ArticleModel.DoesNotExist:
            return None, NOT_FOUND

    def put(self, aid):
        try:
            obj = ArticleModel.get(aid=aid)
        except ArticleModel.DoesNotExist:
            return None, NOT_FOUND

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=non_empty_str, required=True)
        parser.add_argument('content', type=non_empty_str, required=True)
        args = parser.parse_args(strict=True)

        obj.title = args['title']
        obj.content = args['content']
        obj.save()

        return obj.json(), OK

    def delete(self, aid):
        try:
            obj = ArticleModel.get(aid=aid)
        except ArticleModel.DoesNotExist:
            return None, NOT_FOUND

        obj.delete_instance()
        return None, NO_CONTENT


create_tables()
api.add_resource(Articles, '/articles/')
api.add_resource(Article, '/articles/<uuid:aid>')
