#! /usr/bin/env python3

from flask import Flask


app = Flask(__name__)


# Home page
@app.route('/')
def home():
    return 'You are visiting the home page'


# List items in a given category
@app.route('/categories/<string:cat>/')
def category(cat):
    return 'You are visiting the listings in category: ' + cat


# Show entry details
@app.route('/entries/<int:id>/')
def entry(id):
    return 'You are previewing entry ' + str(id)


# Edit an entry
@app.route('/entries/<int:id>/edit/', methods=['GET', 'POST'])
def edit_entry(id):
    return 'You are editing entry ' + str(id)


# Delete an entry
@app.route('/entries/<int:id>/delete/', methods=['GET', 'POST'])
def delete_entry(id):
    return 'You are deleting entry ' + str(id)


# Login page
@app.route('/login/')
def login():
    return 'You are logging in'


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 5000)
