"""App factory Pomodoro Time"""
from flask import Flask
from flask_bootstrap import Bootstrap

from .config import Config
from .auth import auth

def create_app():
    '''retutns an instance of Flask Class'''
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    app.register_blueprint(auth)

    return app
