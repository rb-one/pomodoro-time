from flask import render_template, redirect, url_for, flash
from flask_login import login_user

from . import auth
from app.forms import SignupForm, LoginForm
from app.firestore_services import get_user
from app.models import UserModel, UserData


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
        # get data from form
        form_username = login_form.username.data
        form_password = login_form.password.data

        # get data from firestore
        user_doc = get_user(form_username)

        # Check if user exists
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            # passwords verification
            if form_password == password_from_db:
                user_data = UserData(form_username, password_from_db)
                user = UserModel(user_data)

                # login user
                login_user(user)
                flash('Bienvenido de nuevo')
                redirect(url_for('pomodoro_time'))

            else:
                flash('La informacion no coincide')

        else:
            flash('El usuario no existe')

        return redirect(url_for('index'))

    return render_template('login.html', **context)
