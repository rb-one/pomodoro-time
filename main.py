"""Pomodoro time main"""
from flask import request, make_response, redirect, render_template, session
import unittest

from app import create_app
from app.firestore_services import get_users, get_pomodoros


app = create_app()

todos = ['Comprar café', 'Enviar solicitud de compra',
         'Entregar video a productor']


@app.errorhandler(404)
def error_404(error):
    """error 404 route"""
    return render_template("404.html", error=error)


@app.errorhandler(500)
def internal_server_error(error):
    '''Internal server error route'''
    return render_template('500.html', error=error)


@app.route('/')
def index():
    """index route"""
    user_ip = request.remote_addr
    response = make_response(redirect('/pomodoro'))
    session['user_ip'] = user_ip
    return response


@app.route('/pomodoro')
def pomodoro_time():
    """pomodoro board route"""
    user_ip = session.get('user_ip')
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'pomodoros': get_pomodoros(user_id='rusbel')
    }

    users = get_users()
    for user in users:
        print(user.id)
        print(user.to_dict()['password'])

    return render_template('pomodoro.html', **context)


@app.cli.command()
def test():
    test = unittest.TestLoader().discover('test')
    unittest.TextTestRunner().run(test)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
