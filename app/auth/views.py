from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from app.forms import SignupForm, LoginForm
from app.firestore_services import get_user, user_put
from app.models import UserModel, UserData


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Signup route'''
    signup_form = SignupForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        username = signup_form.username.data
        email = signup_form.email.data
        password = signup_form.password.data

        # get user from database (if it exists)
        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hashed = generate_password_hash(password)
            user_data = UserData(username, email, password_hashed)
            # register user data on database
            user_put(user_data)
            # once registered do login
            user = UserModel(user_data)
            login_user(user)
            flash(f'Welcome to pomodoro {user}')

            return redirect(url_for('pomodoro_time'))

        else:
            flash('Username already exists')

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

        # get data from database
        user_doc = get_user(form_username)

        # Check if user exists
        if user_doc.to_dict() is not None:
            db_password = user_doc.to_dict()['password']
            # passwords verification
            if check_password_hash(db_password, form_password):
                email = user_doc.to_dict()['email']
                user_data = UserData(form_username, email, db_password)
                user = UserModel(user_data)

                # login user
                login_user(user)
                flash(f'Welcome back {user}')
                redirect(url_for('pomodoro_time'))

                return redirect(url_for('index'))

        else:
            flash('Please check your email and password again')


    return render_template('login.html', **context)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Comeback Soon!')

    return redirect(url_for('auth.login'))
