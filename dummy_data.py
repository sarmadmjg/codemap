#! /usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Category, Entry, User

users = [
    {
        'uid': '112131393312150644034',
        'name': 'Sarmad John',
        'email': 'sarmadmjg@gmail.com'
    }
]

categories = [
    {
        'name': 'first_steps',
        'long_name': 'First Steps',
        'description': 'Guides on were to begin and what to expect'
    },
    {
        'name': 'comp_fund',
        'long_name': 'Computer Fundamentals',
        'description': 'Learn the inner workings of computers'
    },
    {
        'name': 'prog_fund',
        'long_name': 'Programming Fundamentals',
        'description': 'Basic guides to master programming'
    },
    {
        'name': 'networks',
        'long_name': 'Networks',
        'description': 'Understand how computers talk to each other'
    },
    {
        'name': 'databases',
        'long_name': 'Databases',
        'description': 'Learn how web applications store data'
    }
]

entries = [
    {
        'name': 'Changing Careers To Be A Developer: 3 Misconceptions to Avoid',
        'description': 'Essential tips',
        'link': 'https://www.nerdery.com/blog/changing-careers-to-be-a-developer-3-misconceptions-to-avoid',
        'category': 'first_steps',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'The Career Changer’s Guide to Becoming a Software Developer',
        'description': 'What to expect and where to begin',
        'link': 'https://www.thoughtworks.com/insights/blog/career-changer-s-guide-becoming-software-developer',
        'category': 'first_steps',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'Thinking About a Career Change to Tech? Here’s How',
        'description': 'An important article',
        'link': 'http://www.huffingtonpost.com/suzanne-grossman/thinking-about-a-career-c_b_6869398.html',
        'category': 'first_steps',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'How Microprocessors Work',
        'description': 'A simplified approach',
        'link': 'http://computer.howstuffworks.com/microprocessor.htm',
        'category': 'comp_fund',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'Fundamentals of Computing Specialization',
        'description': 'Prepare for Advanced Computer Science Courses',
        'link': 'https://www.coursera.org/specializations/computer-fundamentals',
        'category': 'comp_fund',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'Introduction to Computer Science and Programming Using Python',
        'description': 'A new and updated introduction to computer science as a tool to solve real-world analytical problems using Python 3.5',
        'link': 'https://www.edx.org/course/introduction-computer-science-mitx-6-00-1x-10',
        'category': 'prog_fund',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'Code Academy',
        'description': 'Learn to code by taking baby steps',
        'link': 'https://www.codecademy.com',
        'category': 'prog_fund',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'Intro to Programming Nanodegree',
        'description': 'Udacity\'s Intro to Programming is your first step towards careers in Web and App Development, Machine Learning, Data Science, AI, and more! This program is perfect for beginners.',
        'link': 'https://www.udacity.com/course/intro-to-programming-nanodegree--nd000',
        'category': 'prog_fund',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'Hackerrank',
        'description': 'Test yourself by solving programming challenges',
        'link': 'https://www.hackerrank.com',
        'category': 'prog_fund',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'Understanding the Open Systems Interconnection Model',
        'description': 'The OSI model is a visual representation of how network functions work',
        'link': 'https://www.lifewire.com/g00/open-systems-interconnection-model-816290',
        'category': 'networks',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'TLS Basics',
        'description': 'How HTTPS works',
        'link': 'http://www.internetsociety.org/deploy360/tls/basics/',
        'category': 'networks',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'HTTP Basics',
        'description': 'How the web works',
        'link': 'https://www.ntu.edu.sg/home/ehchua/programming/webprogramming/HTTP_Basics.html',
        'category': 'networks',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'Intro To Relational Databases',
        'description': 'SQL, DB-API, and More!',
        'link': 'https://www.udacity.com/course/intro-to-relational-databases--ud197',
        'category': 'databases',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'Intro to SQL: Querying and managing data',
        'description': 'Learn how to use SQL to store, query, and manipulate data. SQL is a special-purpose programming language designed for managing data in a relational database, and is used by a huge number of apps and organizations.',
        'link': 'https://www.khanacademy.org/computing/computer-programming/sql',
        'category': 'databases',
        'poster_uid': '112131393312150644034'
    },
    {
        'name': 'MongoDB in 30 Minutes',
        'description': 'NoSQL db',
        'link': 'https://www.youtube.com/watch?v=pWbMrx5rVBE',
        'category': 'databases',
        'poster_uid': '112131393312150644034'
    },
]

# Connect to db and create new session
engine = create_engine('sqlite:///codemap.db')

Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()

# Populate users
for user in users:
    u = User(
            uid=user['uid'],
            name=user['name'],
            email=user['email'])
    session.add(u)
    session.commit()

# Populate categories
for cat in categories:
    c = Category(
            name=cat['name'],
            long_name=cat['long_name'],
            description=cat['description'])
    session.add(c)
    session.commit()

# Populate entries
for entry in entries:
    e = Entry(
            name=entry['name'],
            description=entry['description'],
            link=entry['link'],
            category=entry['category'],
            poster_uid=entry['poster_uid'])

    session.add(e)
    session.commit()

session.close()
