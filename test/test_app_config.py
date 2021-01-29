from flask_testing import TestCase
from flask import current_app
from main import app
from app import load_user
from app.firestore_services import user_put
import datetime

from app.models import UserData


def create_user():
    user_data = UserData(
        'test_user',
        'fake-test-mail@fake-test-mail.com',
        'test-password',
        confirmed=False,
        confirmed_on=datetime.datetime.now()
    )
    user_put(user_data)


class AppConfigTest(TestCase):
    """App Configuration"""

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exist(self):
        '''App exist'''
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        '''App Config is TESTING'''
        self.assertTrue(current_app.config['TESTING'])

    def test_auto_blueprint_exist(self):
        '''Blueprints exists'''
        self.assertIn('auth', self.app.blueprints)

    def test_load_user(self):
        create_user()
        user = load_user('fake-test-mail@fake-test-mail.com')
        self.assertEqual(user.id, 'fake-test-mail@fake-test-mail.com')
