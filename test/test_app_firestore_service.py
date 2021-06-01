import datetime
from flask_testing import TestCase
from main import app
from app.models import UserData
from app.firestore_services import get_users, get_user, user_put, user_confirmed_update, user_delete, get_pomodoros


def create_user():
    user_data = UserData(
        'test_user',
        'fake-test-mail@fake-test-mail.com',
        'test-password',
        confirmed=False,
        confirmed_on=datetime.datetime.now()
    )
    user_put(user_data)


class AppFirestoreServiceTest(TestCase):
    """App Configuration"""

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_firestore_get_users(self):
        create_user()
        users = get_users()
        self.assertTrue(True, users)

    def test_firestore_get_user(self):
        create_user()
        test_user = get_user('fake-test-mail@fake-test-mail.com').id
        self.assertEqual('fake-test-mail@fake-test-mail.com', test_user)

    def test_user_put(self):
        user_data = UserData(
            'test_user',
            'fake-test-mail@fake-test-mail.com',
            'test-password',
            confirmed=False,
            confirmed_on=datetime.datetime.now()
        )
        user_put(user_data)
        response = get_user('test_user')
        self.assertEqual('test_user', response.id)

    def test_user_confirmed_update(self):
        create_user()
        user_data = UserData(
            'test_user',
            'fake-test-mail@fake-test-mail.com',
            'test-password',
            confirmed=True,
            confirmed_on=datetime.datetime.now()
        )

        user_confirmed_update(user_data)
        response = get_user('fake-test-mail@fake-test-mail.com').to_dict()
        self.assertTrue(True, response['confirmed'])

    def test_user_delete(self):
        create_user()
        user_delete('fake-test-mail@fake-test-mail.com')
        self.assertFalse(get_user('fake-test-mail@fake-test-mail.com').exists)

    def tearDown(self):
        user_delete('fake-test-mail@fake-test-mail.com')
