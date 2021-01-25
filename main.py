"""Pomodoro time main"""
import unittest
from flask import request, make_response, redirect, render_template, session
from flask_login import login_required, current_user

from app import create_app
from app.firestore_services import get_pomodoros


app = create_app()

todos = ['Comprar café', 'Enviar solicitud de compra',
         'Entregar video a productor']


@app.errorhandler(404)
def error_404(error):
    """error 404 route"""
    return render_template("404.html", error=error)


@app.route('/')
def index():
    """index route"""
    user_ip = request.remote_addr
    response = make_response(redirect('/pomodoro'))
    session['user_ip'] = user_ip
    return response


@app.route('/pomodoro')
@login_required
def pomodoro_time():
    """pomodoro board route"""
    user_ip = session.get('user_ip')
    username = current_user.id

    context = {
        'user_ip': user_ip,
        'pomodoros': get_pomodoros(user_id='rusbel'),
        'username': username
    }

    return render_template('pomodoro.html', **context)


@app.cli.command()
def test():
    test = unittest.TestLoader().discover('test')
    unittest.TextTestRunner().run(test)

