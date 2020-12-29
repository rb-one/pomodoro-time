"""App factory Pomodoro Time"""
from flask import Flask
from flask_bootstrap import Bootstrap

from .config import Config


def create_app():
    '''retutns an instance of Flask Class'''
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)

    return app
