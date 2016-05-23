from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'GroupMe to ICS'


@app.route('/full.ics')
def full_ics():
    return 'Full calendar will go here.'


@app.route('/recent.ics')
def recent_ics():
    return 'Soon!'
