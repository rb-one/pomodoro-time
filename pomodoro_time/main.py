"""Pomodoro time main"""
from flask import Flask, request, make_response, redirect, render_template, session, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import unittest

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'MI LLAVE SECRETA'


todos = ['Comprar café', 'Enviar solicitud de compra',
         'Entregar video a productor']


class LoginForm(FlaskForm):
    '''Signup form email validation pendent'''
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')


class SignupForm(LoginForm):
    '''Signup form email validation pendent'''
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')


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


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Signup route'''
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        return redirect(url_for('index'))

    return render_template('signup.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Login route'''
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('login.html', **context)


@app.route('/pomodoro')
def pomodoro_time():
    """pomodoro board route"""
    user_ip = session.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos
    }
    return render_template('pomodoro.html', **context)


@app.cli.command()
def test():
    test = unittest.TestLoader().discover('test')
    unittest.TextTestRunner().run(test)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
