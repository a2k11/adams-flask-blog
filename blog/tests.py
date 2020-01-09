import os
import unittest
import pathlib
from flask import session
from slugify import slugify

from dotenv import load_dotenv
env_dir = pathlib.Path(__file__).parents[1]
load_dotenv(os.path.join(env_dir, '.flaskenv'))

from author.models import Author
from blog.models import Category, Post
from application import db
from application import create_app as create_app_base
from utils.test_db import TestDB

class PostTest(unittest.TestCase):
    def create_app(self):
        return create_app_base(
            SQLALCHEMY_DATABASE_URI=self.db_uri,
            TESTING=True,
            WTF_CSRF_ENABLED=False,
            SECRET_KEY='mySecret!'
        )

    def setUp(self):
        self.test_db = TestDB()
        self.db_uri = self.test_db.create_db()
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()
        with self.app_factory.app_context():
            db.create_all()

    def tearDown(self):
        with self.app_factory.app_context():
            db.drop_all()
        self.test_db.drop_db()

    def user_dict(self):
        return dict(
            full_name = "Johnny Walker",
            email = 'jwalk@example.com',
            password = '4567',
            confirm = '4567'
        )

    def post_dict(self):
        return dict(
            title = 'The Big Post',
            body = 'I want to make a toast, I mean post.',
            new_category = 'dumb'
        )

    def test_blog_post_create(self):
        rv = self.app.get('/post', follow_redirects = True)
        assert 'Please login to continue' in str(rv.data)

        rv = self.app.post('/register', data = self.user_dict())
        rv = self.app.post('/login', data = self.user_dict())

        rv = self.app.post('/post', data=self.post_dict(),
            follow_redirects = True)
        assert 'Article Posted' in str(rv.data)
        assert 'dumb' in str(rv.data)

    def test_blog_post_update_delete(self):
        rv = self.app.post('/register', data=self.user_dict())
        rv = self.app.post('/login', data=self.user_dict())
        rv = self.app.post('/post', data=self.post_dict())

        post2 = self.post_dict()
        post2['title'] = 'A funny post'
        rv = self.app.post('edit/1-' + slugify(self.post_dict()['title']),
            data = post2,
            follow_redirects = True
        )
        assert 'Article Edited' in str(rv.data)
        assert 'A funny post' in str(rv.data)

        rv = self.app.get('/delete/1-' + slugify(post2['title']),
            follow_redirects = True
        )
        assert 'Article Deleted' in str(rv.data)
