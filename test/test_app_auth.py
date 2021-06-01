from flask_testing import TestCase
from flask import url_for
from main import app
from app.auth.tokens import generate_confirmation_token, confirm_token
from app.firestore_services import user_delete


class AppAuthTest(TestCase):
    """App Configuration"""

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

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

        token = generate_confirmation_token(
            'fake-test-mail@fake-test-mail.com')
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
        token = generate_confirmation_token(
            'fake-test-mail@fake-test-mail.com')
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
        token = generate_confirmation_token(
            'fake-test-mail@fake-test-mail.com')
        self.client.get(url_for('auth.confirm_email',  token=token))
        # Login
        self.client.post(url_for('auth.login'), data=user_form)
        # Logout
        response = self.client.get(url_for('auth.logout'))
        self.assert_redirects(response, url_for('auth.login'))

    def test_generate_and_confirm_token(self):
        token = generate_confirmation_token(
            'fake-test-mail@fake-test-mail.com')
        self.assertEqual('fake-test-mail@fake-test-mail.com',
                         confirm_token(token))

    def test_bad_token(self):
        confirmed_token = confirm_token('wrong-token')
        self.assertFalse(confirmed_token)

    def tearDown(self):
        user_delete('fake-test-mail@fake-test-mail.com')
