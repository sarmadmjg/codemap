#! /usr/bin/env python3

from flask import Flask, request, render_template, url_for, redirect, abort

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Entry


# <=======================================================>
# <==================== Initial Setup ====================>
# <=======================================================>

app = Flask(__name__)

# link to the database
engine = create_engine('sqlite:///codemap.db')

Base.metadata.bind = engine

Session = sessionmaker(bind=engine)

# Categories can only be added and deleted by siteAdmin, so only need to be queried once
session = Session()
categories = session.query(Category).all()


# <=======================================================>
# <======================= Routing =======================>
# <=======================================================>


# Home page
@app.route('/')
def home():
    return render_template('home.html', categories=categories)


# List items in a given category
@app.route('/categories/<string:cat>/')
def category(cat):
    session = Session()
    cat_obj = session.query(Category).filter(Category.name == cat).one_or_none()

    # If category doesn't exit, raise 404
    if not cat_obj:
        abort(404)

    entries = session.query(Entry).filter(Entry.category == cat).all()
    return render_template(
                'category.html',
                this_cat=cat_obj,
                categories=categories,
                entries=entries)


# Add entry
@app.route('/entries/add/', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'GET':
        return render_template(
                    'add_entry.html',
                    categories=categories)

    elif request.method == 'POST':
        # handle new entry
        data = request.form
        entry = Entry(name=data['name'], description=data['description'], link=data['link'], category=data['category'])
        session = Session()
        session.add(entry)
        session.commit()
        return redirect(url_for('category', cat=data['category']))

# Show entry details
@app.route('/entries/<int:id>/')
def entry(id):
    return 'You are previewing entry ' + str(id)


# Edit an entry
@app.route('/entries/<int:id>/edit/', methods=['GET', 'POST'])
def edit_entry(id):
    # Check if the entry id is valid
    session = Session()
    entry = session.query(Entry).filter(Entry.id == id).one_or_none()
    if not entry:
        abort(404)

    if request.method == 'GET':
        return render_template(
                    'edit_entry.html',
                    entry=entry,
                    categories=categories)

    elif request.method == 'POST':
        data = request.form

        entry.name = data['name']
        entry.description = data['description']
        entry.link = data['link']
        entry.category = data['category']

        session.add(entry)
        session.commit()

        return redirect(url_for('category', cat=data['category']))


# Delete an entry
@app.route('/entries/<int:id>/delete/', methods=['GET', 'POST'])
def delete_entry(id):
    # Check if the entry id is valid
    session = Session()
    entry = session.query(Entry).filter(Entry.id == id).one_or_none()
    if not entry:
        abort(404)

    if request.method == 'GET':
        return render_template(
                    'delete_entry.html',
                    entry=entry,
                    categories=categories)

    elif request.method == 'POST':
        session.delete(entry)
        session.commit()

        return redirect(url_for('category', cat=entry.category))


# Login page
@app.route('/login/')
def login():
    return 'You are logging in'


if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0', 5000)
