#! /usr/bin/env python3

from functools import wraps

from flask import Flask, request, render_template, url_for,\
                  redirect, abort, flash, jsonify

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Entry, User

import string
import random
from flask import session as login_session
from oauth2client import client
import requests
import httplib2
import json


# <=======================================================>
# <==================== Initial Setup ====================>
# <=======================================================>


app = Flask(__name__)

# link to the database
engine = create_engine('sqlite:///codemap.db')

Base.metadata.bind = engine

Session = sessionmaker(bind=engine)

# Categories can only be added and deleted by siteAdmin
# so only need to be queried once
session = Session()
categories = session.query(Category).all()


# <=======================================================>
# <====================== Security =======================>
# <=======================================================>


def generate_random_token(length=32):
    """generate a random string

    Args:
        length (int, optional): length of the string

    Returns:
        TYPE: Description
    """
    return ''.join([random.choice(string.ascii_letters + string.digits)
                    for _ in range(length)])


@app.before_request
def csrf_protect():
    """Protect all post requests with anti-forgery token
    """

    # If a token isn't present, create one in the session
    if request.method == 'GET':
        csrf_token = login_session.pop('csrf_token', None)

        if not csrf_token:
            csrf_token = generate_random_token()

        login_session['csrf_token'] = csrf_token

        # Make the token available for templates
        app.jinja_env.globals['csrf_token'] = csrf_token

    elif request.method == 'POST':
        # pop token once it's used to force create new one in future requests
        csrf_token = login_session.pop('csrf_token', None)

        # Check CSRF token, abort if not matching
        if not csrf_token or \
                (csrf_token != request.args.get('csrf_token') and
                    csrf_token != request.form.get('csrf_token')):
            abort(403)


# <=======================================================>
# <=================== User Management ===================>
# <=======================================================>


# Login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


# Google sign in
@app.route('/gconnect/', methods=['POST'])
def gconnect():
    auth_code = request.data

    CLIENT_SECRET_FILE = 'client_secret.json'

    # Exchange auth code for access token
    try:
        credentials = client.credentials_from_clientsecrets_and_code(
            CLIENT_SECRET_FILE,
            ['profile', 'email'],
            auth_code)

    # Couldn't get access token
    except client.FlowExchangeError:
        return jsonify(message='Server could not get an access token'), 401


    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    data = requests.get(userinfo_url, params=params).json()

    # Extract profile data
    uid = data['id']
    name = data['name']
    email = data['email']
    pic = data['picture']

    # Store data in user session
    login_session['uid'] = uid
    login_session['pic'] = pic
    # store credentials for future use
    login_session['credentials'] = credentials.to_json()

    # Store or update data in the db
    session = Session()
    user = session.query(User).filter(User.uid == uid).one_or_none()
    # New user
    if not user:
        user = User(uid=uid, name=name, email=email)
    # Existing user
    else:
        user.name = name
        user.email = email

    session.add(user)
    session.commit()

    flash('You logged in successful with your Google account', 'alert-success')

    return jsonify(message='logged in successfully')


# log out handler
@app.route('/logout/', methods=['POST'])
def logout():
    credentials_json = login_session.get('credentials')
    # Revoke access if credentials are found
    if credentials_json:
        credentials = client.Credentials.new_from_json(credentials_json)
        credentials.revoke(httplib2.Http())

    # Clean user session
    clean_session(login_session)

    flash('You successfully logged out!', 'alert-success')

    return redirect(url_for('home'))


def requires_login(f):
    """function wrapper for pages that require authenticated users

    Args:
        f (function): any routing function
    """
    @wraps(f)
    def wrapped(*args, **kwargs):
        user = get_user_from_session(login_session)
        uid = login_session.get('uid')
        if user:
            # user is logged in, pass the user instance to the function
            return f(*args, **kwargs, user=user)

        # User is not logged in, redirect
        return redirect(url_for('login', redir=request.path, **request.args))

    return wrapped


def clean_session(login_session):
    """clear user session

    Args:
        login_session (flask.session): user session
    """
    # Use pop instead of del to avoid errors with non-existing keys
    login_session.pop('credentials', None)
    login_session.pop('uid', None)
    login_session.pop('pic', None)


def get_user_from_session(login_session):
    """get User instance for logged in users

    Args:
        login_session (flask.session): user session

    Returns:
        User: single User instance or None
    """
    uid = login_session.get('uid')
    if uid:
        session = Session()
        user = session.query(User).filter(User.uid == uid).one_or_none()
        return user


# <=======================================================>
# <======================= Routing =======================>
# <=======================================================>


# Home page
@app.route('/')
def home():
    user = get_user_from_session(login_session)
    # Get user photo url from session
    app.jinja_env.globals['pic'] = login_session.get('pic')

    return render_template('home.html', categories=categories, user=user)


# List items in a given category
@app.route('/categories/<string:cat>/')
def category(cat):
    user = get_user_from_session(login_session)

    session = Session()
    cat_obj = session.query(Category) \
        .filter(Category.name == cat) \
        .one_or_none()

    # If category doesn't exit, raise 404
    if not cat_obj:
        abort(404)

    # Get user photo url from session
    app.jinja_env.globals['pic'] = login_session.get('pic')

    entries = session.query(Entry).filter(Entry.category == cat).all()

    return render_template(
                'category.html',
                this_cat=cat_obj,
                categories=categories,
                entries=entries,
                user=user)


# Add entry
@app.route('/entries/add/', methods=['GET', 'POST'])
@requires_login
def add_entry(user):
    # New Entry form
    if request.method == 'GET':
        # Get user photo url from session
        app.jinja_env.globals['pic'] = login_session.get('pic')

        cat = request.args.get('category')
        return render_template(
                    'add_entry.html',
                    def_cat=cat,
                    categories=categories,
                    user=user)

    # Handle new entry
    elif request.method == 'POST':
        data = request.form

        entry = Entry(
            name=data['name'],
            description=data['description'],
            link=data['link'],
            category=data['category'],
            poster_uid=user.uid)

        session = Session()
        session.add(entry)
        session.commit()

        flash('A new entry was successfully created!', 'alert-success')

        return redirect(url_for('category', cat=data['category']))


# Edit an entry
@app.route('/entries/<int:id>/edit/', methods=['GET', 'POST'])
@requires_login
def edit_entry(id, user):
    # acquire entry from db
    session = Session()
    entry = session.query(Entry).filter(Entry.id == id).one_or_none()

    # no such entry
    if not entry:
        abort(404)

    # Check if user is not the rightful owner
    if user.uid != entry.poster_uid:
        abort(403)

    # Edit entry form
    if request.method == 'GET':
        # Get user photo url from session
        app.jinja_env.globals['pic'] = login_session.get('pic')

        return render_template(
                    'edit_entry.html',
                    entry=entry,
                    categories=categories,
                    user=user)

    # Store edits
    elif request.method == 'POST':
        data = request.form

        entry.name = data['name']
        entry.description = data['description']
        entry.link = data['link']
        entry.category = data['category']

        session.add(entry)
        session.commit()

        flash('Entry #' + str(entry.id) + ' was successfully edited!',
              'alert-success')

        return redirect(url_for('category', cat=data['category']))


# Delete an entry
@app.route('/entries/<int:id>/delete/', methods=['GET', 'POST'])
@requires_login
def delete_entry(id, user):
    # Acquire the entry from db
    session = Session()
    entry = session.query(Entry).filter(Entry.id == id).one_or_none()

    # If entry is non-existing, abort
    if not entry:
        abort(404)

    # Check if user is not the rightful owner
    if user.uid != entry.poster_uid:
        abort(403)

    # Delete confirmation form
    if request.method == 'GET':
        # Get user photo url from session
        app.jinja_env.globals['pic'] = login_session.get('pic')

        return render_template(
                    'delete_entry.html',
                    entry=entry,
                    categories=categories,
                    user=user)

    # Delete entry from db
    elif request.method == 'POST':
        session.delete(entry)
        session.commit()

        flash('Entry #' + str(entry.id) + ' was successfully deleted!',
              'alert-success')

        return redirect(url_for('category', cat=entry.category))


# <=======================================================>
# <========================= API =========================>
# <=======================================================>


# List all categories
@app.route('/api/categories/')
def api_categories():
    session = Session()
    cats = session.query(Category).all()

    return jsonify(categories=[cat.serialize() for cat in cats])


# List entries in specific category
@app.route('/api/categories/<string:cat>/entries/')
def api_entries(cat):
    session = Session()
    entries = session.query(Entry).filter(Entry.category == cat).all()

    return jsonify(entries=[entry.serialize() for entry in entries])


# List details of a specific entry
@app.route('/api/entries/<int:id>/')
def api_entry(id):
    session = Session()
    entry = session.query(Entry).filter(Entry.id == id).one_or_none()

    return jsonify({'error': 'item not found'} if not entry
                   else entry.serialize())


if __name__ == '__main__':
    app.secret_key = '90maf89j2489dnmo23aeqduemc'
    app.debug = True
    app.run('0.0.0.0', 5000)
