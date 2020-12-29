from flask import render_template, redirect, url_for
from . import auth
from app.forms import SignupForm, LoginForm


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Signup route'''
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('signup.html', **context)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Login route'''
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }
    if login_form.validate_on_submit():
        return redirect(url_for('index'))

    return render_template('login.html', **context)
