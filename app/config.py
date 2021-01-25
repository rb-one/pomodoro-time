'''App Config'''
import os
from dotenv import load_dotenv
load_dotenv()


class Config:
    '''Base Configuration'''

    # Main Config
    SECRET_KEY = 'MY_TEST_SECRET_KEY'
    SECURITY_PASSWORD_SALT = 'MY_TEST_SALT_CONFIRMATION_USER_EMAIL'

    # Email Settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # Gmail Authentication
    MAIL_USERNAME = os.environ.get('APP_MAIL_USERNAME', None)
    MAIL_PASSWORD = os.environ.get('APP_MAIL_PASSWORD', None)

    # Email Sender Account
    MAIL_DEFAULT_SENDER = os.environ.get('APP_DEFAULT_SENDER', None)
