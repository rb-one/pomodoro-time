import datetime
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from app.forms import SignupForm, LoginForm
from app.firestore_services import get_user, user_put, user_confirmed_update
from app.models import UserModel, UserData
from app.auth.tokens import generate_confirmation_token, confirm_token

from app.email import send_email


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

        # get email/user_id from database (if it exists)
        user_doc = get_user(email)

        if user_doc.to_dict() is None:
            password_hashed = generate_password_hash(password)
            user_data = UserData(username, email, password_hashed)

            # register user data on database
            user_put(user_data)

            # email preparation
            token = generate_confirmation_token(user_data.email)
            confirm_url = url_for(
                'auth.confirm_email',
                token=token,
                external=True)
            html = render_template(
                'activate_user.html',
                confirm_url=confirm_url)
            subject = 'Please confirm your email'

            # Send email
            send_email(email, subject, html)

            flash('Please check your email and validate your account')

            return redirect(url_for('auth.login'))

        else:
            flash('Username already exists')

    return render_template('signup.html', **context)


@auth.route('/confirm/<token>')
def confirm_email(token):
    '''Confirm email route'''
    email = confirm_token(token)
    user = get_user(email).to_dict()
    if user:
        user_data = UserData(user['username'], email, user['password'])

        if user_data.confirmed == False:
            user_data.confirmed = True
            user_data.confirmed_on = datetime.datetime.now()
            user_confirmed_update(user_data)
            flash('You have confirmed your account. Thanks!')
            
            return redirect(url_for('auth.login'))
        elif user_data.confirmed == True:
            flash('Account already confirmed, please login')


    else:
        flash('The confirmation link is invalid or has expired.', 'danger')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Login route'''
    no_login_message = 'Please check your email and password again'
    login_form = LoginForm()

    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        # get form data
        email = login_form.email.data
        password = login_form.password.data

        # Get data from database
        user_doc = get_user(email)

        # User Verification
        if user_doc.to_dict() is not None:
            password_db = user_doc.to_dict()['password']
            # passwords verification
            if check_password_hash(password_db, password):
                username = user_doc.to_dict()['username']
                confirmed = user_doc.to_dict()['confirmed']
                user_data = UserData(
                    username,
                    email,
                    password_db,
                    confirmed=confirmed)
                user = UserModel(user_data)
                # confirm user and login
                if user.confirmed:
                    login_user(user)
                    flash(f'Welcome back {user.username}')
                    redirect(url_for('pomodoro_time'))
                    return redirect(url_for('index'))
                else:
                    flash('Please before Login validate your email')
            else:
                flash(no_login_message)

        else:
            flash(no_login_message)

    return render_template('login.html', **context)


@auth.route('/logout')
@login_required
def logout():
    '''Logout route'''
    logout_user()
    flash('Comeback Soon!')

    return redirect(url_for('auth.login'))
