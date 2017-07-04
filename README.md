# Codemap
A dynamic website providing links to articles, videos, and courses for new web developers.

A project for Udaciy Full Stack NanoDegree

## Usage
### Setup
Make sure these dependencies are satisfied
```
sudo pip3 install sqlalchemy flask oauth2client
```
Clone the repository to your machine
```
git clone https://github.com/sarmadmjg/codemap.git
cd codemap
```
You'll need to setup a database with dummy data
```
python3 dummy_data.py
```
### Start The Server
```
python3 codemap.py
```
By default, the server will run on port 5000, to visit the site from your brower, navigate to: `localhost:5000`
