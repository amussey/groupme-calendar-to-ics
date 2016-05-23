from flask import Flask, current_app, Response
import os
import sys
import datetime

import utils

app = Flask(__name__)
with app.app_context():
    current_app.groupme_calendar_name = 'GroupMe Calendar'
    if os.environ.get('GROUPME_STATIC_NAME', None):
        if os.environ.get('GROUPME_STATIC_NAME', None) != "":
            current_app.groupme_calendar_name = os.environ.get('GROUPME_STATIC_NAME', None)


@app.route('/')
def index():
    last_cache = getattr(current_app, 'last_cache', datetime.datetime(year=2000, month=1, day=1))
    cache_duration = int(os.environ.get('CACHE_DURATION', 60))
    if datetime.datetime.now() - last_cache > datetime.timedelta(minutes=60) or cache_duration == 0:
        # Perform a recache.
        groupme_api_key = os.environ.get('GROUPME_API_KEY', None)
        groupme_group_id = os.environ.get('GROUPME_GROUP_ID', None)
        if not groupme_api_key:
            return 'ERROR: The GROUPME_API_KEY is not set.'
        if not groupme_group_id:
            return 'ERROR: The GROUPME_GROUP_ID is not set.'

        successfully_load_json = utils.load_groupme_json(app=app, groupme_api_key=groupme_api_key, groupme_group_id=groupme_group_id)
        if not successfully_load_json:
            return 'There was a critical error loading the GroupMe Calendar.  Please investigate.'
        current_app.ics_cache = utils.groupme_json_to_ics(groupme_json=current_app.groupme_calendar_json_cache)
        current_app.last_cache = datetime.datetime.now()

    # Return a template, but also some basic info about the latest cache time.
    return 'Cached successfully.'


@app.route('/full.ics')
def full_ics():
    last_cache = getattr(current_app, 'last_cache', datetime.datetime(year=2000, month=1, day=1))
    cache_duration = int(os.environ.get('CACHE_DURATION', 60))
    if datetime.datetime.now() - last_cache > datetime.timedelta(minutes=60) or cache_duration == 0:
        # Perform a reache.
        # A lot of the errors in here will look similar to the ones in index(),
        # but have been repeated and mapped through groupme_ics_error() for the
        # safety of the calendar client.
        groupme_api_key = os.environ.get('GROUPME_API_KEY', None)
        groupme_group_id = os.environ.get('GROUPME_GROUP_ID', None)
        if not groupme_api_key:
            return utils.groupme_ics_error(error_text='GROUPME_API_KEY not set')
        if not groupme_group_id:
            return utils.groupme_ics_error(error_text='GROUPME_GROUP_ID not set')

        successfully_load_json = utils.load_groupme_json(app=app, groupme_api_key=groupme_api_key, groupme_group_id=groupme_group_id)
        if not successfully_load_json:
            return utils.groupme_ics_error(error_text='critical error loading calendar')
        current_app.ics_cache = utils.groupme_json_to_ics(groupme_json=current_app.groupme_calendar_json_cache)
        current_app.last_cache = datetime.datetime.now()

    return Response(getattr(current_app, 'ics_cache', None), mimetype='text/calendar', headers={'Content-Disposition': 'attachment'})


@app.route('/recent.ics')
def recent_ics():
    return 'Soon!'
