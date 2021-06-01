"""App factory Pomodoro Time"""
from flask import Flask
from .config import Config
from .auth import auth
from .models import UserModel
from .extensions import mail, bootstrap, login_manager


@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    '''returns an instance of Flask Class'''
    app = Flask(__name__)

    app.config.from_object(Config)

    app.register_blueprint(auth)

    mail.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    return app
