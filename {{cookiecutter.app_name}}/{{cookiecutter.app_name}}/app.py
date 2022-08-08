#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

# Flask
from flask import Flask, render_template, request, redirect
from flask import session, flash, url_for
from forms import *

# Logging
import logging
from logging import Formatter, FileHandler

# Utilities
import os
import gunicorn
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Database
from flask_sqlalchemy import SQLAlchemy
from models.users import Users, Db
from passlib.hash import sha256_crypt

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# Initialize app
app = Flask(__name__)
app.database_key = os.environ.get('DATABASE_KEY')
#db = SQLAlchemy({{cookiecutter.app_name}})

# Initialize DB
Db = SQLAlchemy()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY') # Make sure this is set in Heroku dashboard for this new app!
Db.init_app(app)

# Define default route parameters
MAX_STRING_LENGTH = 64
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 20

# All null values! This is just for POST routes!!!
POST_USER_REGISTER_DEFAULTS = {
    "username": None,
    "first_name": None,
    "last_name": None,
    "email": None,
    "password": None
}
POST_USER_LOGIN_DEFAULTS = {
    "username": None,
    "password": None
}


# Pages
@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


'''User management'''
# Register and create a User
@app.route('/register', methods=['GET'])
def register():

    # Redirect already logged in user
    if logged_in_user():
        flash('You are already logged in!')
        return redirect(url_for('home'))

    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form, form_purpose='create_user')


@app.route('/user/create', methods=['POST'])
def create_user():

    try:

        # Init credentials from form request
        username = check_string(request.form['username'], 'username', MAX_STRING_LENGTH)
        password, verify = verify_password(request.form['password'], request.form['confirm'],
                                           MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)
        first_name = check_string(request.form['first_name'], "first_name")
        last_name = check_string(request.form['last_name'], "last_name")
        email = check_string(request.form['email'], "email")

        # Does the user already exist?
        user = Users.query.filter_by(username = username).first()

        if user:
            flash(f'User with username "{username}" already exists! Please choose another username.', 'danger')
            # redirect back to signup page
            redirect(url_for('register'))

        # User is unique, so let's create a new one
        user = Users(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = sha256_crypt.hash(password)
        )

        # commit to the db
        Db.session.add(user)
        Db.session.commit()

        # set user as logged in
        session['username'] = username

        # Message Flashing
        # https://flask.palletsprojects.com/en/2.0.x/patterns/flashing/#flashing-with-categories
        flash('Congratulations, you are now a registered user!', 'success')

        # Redirect to login page
        return redirect(url_for('login'))

    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # redirect back to signup page
        return redirect(url_for('register'))


@app.route('/login', methods = ['GET', 'POST'], defaults = POST_USER_LOGIN_DEFAULTS)
def login(username, password, messages=[], errors=[]):

    if request.method == 'GET':

        # Redirect already logged in user
        if logged_in_user():
            flash('You are already logged in!', 'success')
            return redirect(url_for('home'))

        form = LoginForm(request.form)
        return render_template('forms/login.html', form=form)

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        # Sanitize the input
        try:
            username = check_string(username, "username")
            password = check_string(password, "password")

            # Does User Exist?
            user = Users.query.filter_by(username = username).first()

            if user is None:
                flash('Invalid username or password.', 'danger')

                # redirect back to login page
                return redirect(url_for('login'))

            # Check User & Password
            sha256_crypt.verify(password, user.password)

            # set the logged in user's username in the session
            session['username'] = username

            # let the user know login was successful
            flash(f'{username} is now logged in!', 'success')

            return home()

        except Exception as e:
            # show the error
            flash(get_error(e), 'danger')

            # redirect back to login page
            return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()

    flash('Successfully logged out.', 'success')

    # Go back to the login page.
    return redirect(url_for('login'))


@app.route('/user/update/form')
def user_update_form():

    try:

        user = logged_in_user()
        if user is None:
            flash('You are not logged in!')
            return redirect(url_for('login'))

        else:

            form = UpdateUserInfo(request.form)

            # Use the process method and the data attribute to pre-populate each fields data.
            form.process(data = {'username': user.username,
                                 'first_name': user.first_name,
                                 'last_name': user.last_name,
                                 'email': user.email})

            return render_template('forms/user_update.html', form=form, form_purpose='update_user')

    except Exception as e:
        flash(e)
        return redirect(url_for('login'))


# Update User
@app.route('/user/update', methods = ['POST'])
def user_update():

    try:
        # user must be logged in to view user profiles!
        user = logged_in_user()
        if user is None:
            flash('You are not logged in!', 'danger')

            # redirect back to login page
            return redirect(url_for('login'))

        # sanitize input
        username = check_string(request.form['username'], 'username')
        first_name = check_string(request.form['first_name'], "first_name")
        last_name = check_string(request.form['last_name'], "last_name")
        email = check_string(request.form['email'], "email")

        # The logged in user can only update their own profile!
        if username != user.username:
            flash('Unauthorized action!', 'danger')

            # redirect back to login page
            return redirect(url_for('login'))

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        Db.session.commit()

        # Go back to user profile
        #TODO: change this redirect to go to a profile page and flash a message that your info was updated.
        return redirect(url_for('home'))

    # Not authorized, go to login page
    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # redirect to login
        return redirect(url_for('login'))

    # Any other error
    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # redirect back to index page (or referrer)
        return go_back(request.referrer)


@app.route('/user/update_password/form', methods = ['GET'])
def user_update_password_form():

    try:

        user = logged_in_user()
        if user is None:
            flash('You are not logged in!')
            return redirect(url_for('login'))

        else:

            form = UpdatePasswordForm(request.form)

            return render_template('forms/update_password.html', form=form, form_purpose='update_password')

    except Exception as e:
        flash(e)
        return redirect(url_for('login'))


# Update User password
@app.route('/user/update_password', methods = ['POST'])
def user_update_password():

    try:
        # user must be logged in to view user profiles!
        user = logged_in_user()
        if user is None:
            flash('You are not logged in!', 'danger')

            # redirect back to login page
            return redirect(url_for('login'))

        # sanitize & check that the passwords match
        new_password, verify = verify_password(request.form['new_password'], request.form['verify'],
                                               MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH)

        # set the password
        user.password = sha256_crypt.hash(new_password)

        # commit to Db
        Db.session.commit()

        # flash a message to the user
        flash('Password successfully changed!', 'success')

        return redirect(url_for('home'))

    # Any other error
    except Exception as e:
        # show the error
        flash(get_error(e), 'danger')

        # go back to where we came from
        return go_back(request.referrer)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# Error handlers.
@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


def get_error(e):
    return e.message if hasattr(e, 'message') else str(e)


# Sanitize user input methods
# CITATION: Lab 5 app.py
def check_string(string=None, label="", max_length=MAX_STRING_LENGTH):
    # can't have a null value!
    if string is None:
        raise ValueError(f'Variable {label} cannot be null!')
    # strip the string of leading & trailing whitespace
    string = string.strip()

    if string == "":
        raise ValueError(f'Variable {label} is empty!')
    elif len(string) > max_length:
        raise ValueError(f'Variable {label} is too long! {len(string)} > {max_length}')

    return string


def check_int(num=None, label="", min=float('-inf'), max=float('inf')):
    try:
        num = int(num)
    except:
        raise ValueError(f'Variable {label} malformed! ({num})')

    if num < min or num > max:
        raise ValueError(f'Variable {label} is out of range! ({num} <> [{min},{max}])')

    return num


def check_float(num=None, label="", min=float('-inf'), max=float('inf')):
    try:
        num = float(num)
    except:
        raise ValueError(f'Variable {label} malformed! ({num})')

    if num < min or num > max:
        raise ValueError(f'Variable {label} is out of range! ({num} <> [{min},{max}])')

    return num


# This is only to sanitize passwords for NEW users. Why don't we want to do these checks
# when someone is authenticating? (Hint: security)
def check_password(password=None, label="password", min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH):
    # can't have a null value!
    if password is None:
        raise ValueError(f'Variable {label} cannot be null!')

    # Note: we don't want to strip any characters from the password!

    # string can't be empty
    if password == "":
        raise ValueError(f'Variable {label} is empty!')

    # Need a minimum number of chars
    if len(password) < min_length:
        raise ValueError(f'Variable {label} is too short! {len(password)} < {min_length}')

    # Need a maximum number of chars
    if len(password) > max_length:
        raise ValueError(f'Variable {label} is too long! {len(password)} > {max_length}')

    return password


# This is to ensure the passwords are both valid and the same
def verify_password(password=None, verify=None, min_length=MIN_PASSWORD_LENGTH, max_length=MAX_PASSWORD_LENGTH):
    password = check_password(password, 'password', min_length, max_length)
    verify = check_password(verify, 'verify', min_length, max_length)

    if password != verify:
        raise ValueError('Passwords do not match!')

    return password, verify  # returns both password & verification


# Get the currently logged in user
def logged_in_user():
    # Three checks:
    # 1. if the username key exists in a session
    # 2. if the username isn't empty
    # 3. if the username is actually valid
    if 'username' in session and session['username'] != "":
        # Will return None if no such user exists
        return Users.query.filter_by(username = session['username']).first()
    else:
        return None


# Go back to where we came from
def go_back(referrer=None):
    last_page = referrer if referrer else url_for('home')
    return redirect(last_page)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
