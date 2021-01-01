from flask_testing import TestCase
from flask import current_app, url_for, redirect
from main import app
from app.firestore_services import get_users, get_user, get_pomodoros


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exist(self):
        '''test if app exist'''
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        '''test app config is TESTING'''
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirect(self):
        '''test if app redirects from index to pomodoro_time'''
        response = self.client.get(url_for('index'))
        self.assert_redirects(response, url_for('pomodoro_time'))

    def test_auto_blueprint_exist(self):
        self.assertIn('auth', self.app.blueprints)

    def test_pomodoro_time_logged_user_get(self):
        '''test post form and redirect on signup'''
        fake_form = {
            'username': 'fake',
            'email': 'fake@email.com',
            'password': 'password-fake'
        }
        response = self.client.post(url_for('auth.signup'), data=fake_form)
        response = self.client.get(url_for('index'))
        self.assert_redirects(response, url_for('pomodoro_time'))

    # Signup Tests
    def test_signup_post(self):
        '''test post form and redirect on signup'''
        fake_form = {
            'username': 'fake',
            'email': 'fake@email.com',
            'password': 'password-fake'
        }

        response = self.client.post(url_for('auth.signup'), data=fake_form)
        self.assert_redirects(response, url_for('index'))

    def test_signup_get(self):
        response = self.client.get(url_for('auth.signup'))
        self.assert200(response)

    def test_auth_signup_templete(self):
        self.client.get(url_for('auth.signup'))
        self.assertTemplateUsed('signup.html')

    # Login tests
    def test_login_post(self):
        '''test post form and redirect on login'''
        fake_form = {
            'username': 'fake',
            'password': 'password-fake'
        }

        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assert_redirects(response, url_for('index'))

    def test_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_auth_login_templete(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')


    def test_firestore_get_users(self):
        users = get_users()
        self.assertTrue(True, users)

    def test_firestore_get_user(self):
        test_user = get_user('test-user').id
        self.assertEqual('test-user', test_user)

    def test_get_pomodoros(self):
        test_pomodoros = get_pomodoros('test-user')
        self.assertTrue(True, test_pomodoros[0].to_dict())



