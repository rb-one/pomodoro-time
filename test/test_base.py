
from flask_testing import TestCase
from flask import current_app, url_for
from main import app
from app import load_user
from app.auth.views import confirm_email
from app.auth.tokens import generate_confirmation_token, confirm_token
from app.firestore_services import get_users, get_user, get_pomodoros, user_put, user_confirmed_update, user_delete
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
    
class App(TestCase):
    """App Configuration"""
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    # App Configuration
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
    # --------- Auth Tests ---------
    # SignUp Test
    def test_test_signup_get(self):
        response = self.client.get(url_for('auth.signup'))
        self.assert200(response)

    def test_auth_signup_templete(self):
        self.client.get(url_for('auth.signup'))
        self.assertTemplateUsed('signup.html')

    def test_signup_post_new_user(self):
        user_form = {
            'username': 'test_user',
            'email': 'fake-test-mail@fake-test-mail.com',
            'password': 'test_password',
        }
        
        response = self.client.post(url_for('auth.signup'), data=user_form)
        self.assert_redirects(response, url_for('auth.login'))

    def test_signup_user_already_exist(self):
        user_form = {
            'username': 'test_user',
            'email': 'fake-test-mail@fake-test-mail.com',
            'password': 'test_password',
        }
        
        self.client.post(url_for('auth.signup'), data=user_form)
        response = self.client.post(url_for('auth.signup'), data=user_form)
        response = response.data.decode('utf-8')
        self.assertIn('Username already exists', response)

    # Email Tests 
    def test_confirm_email(self):
        user_form = {
            'username': 'test_user',
            'email': 'fake-test-mail@fake-test-mail.com',
            'password': 'test_password',
        }
        self.client.post(url_for('auth.signup'), data=user_form)
        
        token = generate_confirmation_token('fake-test-mail@fake-test-mail.com')
        response = self.client.get(url_for('auth.confirm_email',  token=token))
        self.assert_redirects(response, url_for('auth.login'))

    # Login Tests
    def test_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_login_signup_templete(self):
        self.client.get(url_for('auth.login'))
        self.assertTemplateUsed('login.html')

    def test_login_unconfirmed_user(self):
        user_form = {
            'username': 'test_user',
            'email': 'fake-test-mail@fake-test-mail.com',
            'password': 'test_password',
        }
        self.client.post(url_for('auth.signup'), data=user_form)
        
        response = self.client.post(url_for('auth.login'), data=user_form)
        self.assert200(response)

    def test_login_user_wrong_password(self):
        user_form = {
            'username': 'test_user',
            'email': 'fake-test-mail@fake-test-mail.com',
            'password': 'test_password',
        }
        fake_form = {
            'email': 'fake-test-mail@fake-test-mail.com',
            'password': 'wrong-password',
        }
        self.client.post(url_for('auth.signup'), data=user_form)
                
        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assert200(response)

    def test_login_wrong_credentials(self):
        fake_form = {
            'email': 'wrong@gmail.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url_for('auth.login'), data=fake_form)
        response = response.data.decode('utf-8')
        self.assertIn('Please check your email and password again', response)

    def test_login_post_confirmed_user(self):
        user_form = {
            'username': 'test_user',
            'email': 'fake-test-mail@fake-test-mail.com',
            'password': 'test_password',
        }
        self.client.post(url_for('auth.signup'), data=user_form)
        # Confirm user with token
        token = generate_confirmation_token('fake-test-mail@fake-test-mail.com')
        self.client.get(url_for('auth.confirm_email',  token=token))
        
        # Login Confirmed user
        response = self.client.post(url_for('auth.login'), data=user_form)
        self.assert_redirects(response, url_for('index'))

    # Logout Tests
    def test_logout_get(self):
        user_form = {
            'username': 'test_user',
            'email': 'fake-test-mail@fake-test-mail.com',
            'password': 'test_password',
        }
        # Create User
        self.client.post(url_for('auth.signup'), data=user_form)
        # Confirm user with token
        token = generate_confirmation_token('fake-test-mail@fake-test-mail.com')
        self.client.get(url_for('auth.confirm_email',  token=token))
        # Login
        self.client.post(url_for('auth.login'), data=user_form)
        # Logout
        response = self.client.get(url_for('auth.logout'))
        self.assert_redirects(response, url_for('auth.login'))

    def test_generate_and_confirm_token(self):
        token = generate_confirmation_token('fake-test-mail@fake-test-mail.com')
        self.assertEqual('fake-test-mail@fake-test-mail.com', confirm_token(token))

    def test_bad_token(self):
        confirmed_token = confirm_token('wrong-token')
        self.assertFalse(confirmed_token)

    # --------- Firestore_service Tests -----------
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
        user_data = UserData(
            'test_user',
            'fake-test-mail@fake-test-mail.com',
            'test-password',
            confirmed=True,
            confirmed_on=datetime.datetime.now()
        )
        
        create_user()
        user_confirmed_update(user_data)
        response = get_user('fake-test-mail@fake-test-mail.com').to_dict()
        self.assertTrue(True, response['confirmed'])

    def test_user_delete(self):
        create_user()
        user_delete('fake-test-mail@fake-test-mail.com')
        self.assertFalse(get_user('fake-test-mail@fake-test-mail.com').exists)

    # # --------------- User Loader ----------------
    def test_load_user(self):
        create_user()
        user = load_user('fake-test-mail@fake-test-mail.com')
        self.assertEqual(user.id, 'fake-test-mail@fake-test-mail.com')

    # --------------- Main routes ----------------
    # 404 route
    def test_404_render_template(self):
        self.client.get('undefined_route')
        self.assertTemplateUsed('404.html')

    # # def test_get_pomodoros(self):
    # #     '''get user pomodoros from database
    # #     - before run create a test user with 2 tasks
    # #     move bellow this task when test create tast
    # #     finally create a test for delete task and
    # #     other to delete user as admin
    # #     '''
    # #     response = get_pomodoros('rusbel.bermudez.rivera@gmail.com')
    # #     self.assertEqual(2, len(response))

    def tearDown(self):
        user_delete('fake-test-mail@fake-test-mail.com')
