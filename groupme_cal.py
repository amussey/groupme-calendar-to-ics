from flask import Flask, current_app, render_template, request
import os
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

    groupme_group_id = os.environ.get('GROUPME_GROUP_ID', None)
    if not groupme_group_id:
        return 'ERROR: The GROUPME_GROUP_ID is not set.'

    if datetime.datetime.now() - last_cache > datetime.timedelta(minutes=cache_duration) or cache_duration == 0:
        print('Cache miss.')

        # Perform a recache.
        groupme_api_key = os.environ.get('GROUPME_API_KEY', None)
        if not groupme_api_key:
            return 'ERROR: The GROUPME_API_KEY is not set.'

        successfully_load_json = utils.load_groupme_json(app=app, groupme_api_key=groupme_api_key, groupme_group_id=groupme_group_id)
        if not successfully_load_json:
            return 'There was a critical error loading the GroupMe Calendar.  Please investigate.'
        current_app.ics_cache = utils.groupme_json_to_ics(groupme_json=current_app.groupme_calendar_json_cache)
        current_app.last_cache = datetime.datetime.now()
    else:
        print('Cache hit.  Time remaining: {}'.format(datetime.timedelta(minutes=cache_duration) - (datetime.datetime.now() - last_cache)))

    ics_url = os.environ.get('GROUPME_PROXY_URL', None)
    if not ics_url:
        ics_url = request.url + '/calendar.ics'
        if request.url[-1] == '/':
            ics_url = request.url + 'calendar.ics'

    ics_url_http, ics_url_webcal, ics_url_google = utils.build_ics_urls(ics_url)

    params = {
        'title': getattr(current_app, 'groupme_calendar_name', 'GroupMe'),
        'groupme_id': groupme_group_id,
        'ics_url_http': ics_url_http,
        'ics_url_webcal': ics_url_webcal,
        'ics_url_google': ics_url_google,
    }

    # Return a template, but also some basic info about the latest cache time.
    return render_template('index.html', **params)


@app.route('/calendar.ics')
def full_ics():
    last_cache = getattr(current_app, 'last_cache', datetime.datetime(year=2000, month=1, day=1))
    cache_duration = int(os.environ.get('CACHE_DURATION', 60))
    if datetime.datetime.now() - last_cache > datetime.timedelta(minutes=cache_duration) or cache_duration == 0:
        print('Cache miss.')

        # Perform a reache.
        # A lot of the errors in here will look similar to the ones in index(),
        # but have been repeated and mapped through groupme_ics_error() for the
        # safety of the calendar client.
        groupme_api_key = os.environ.get('GROUPME_API_KEY', None)
        groupme_group_id = os.environ.get('GROUPME_GROUP_ID', None)
        if not groupme_api_key:
            return utils.return_ics_Response(utils.groupme_ics_error(error_text='GROUPME_API_KEY not set'))
        if not groupme_group_id:
            return utils.return_ics_Response(utils.groupme_ics_error(error_text='GROUPME_GROUP_ID not set'))

        successfully_load_json = utils.load_groupme_json(app=app, groupme_api_key=groupme_api_key, groupme_group_id=groupme_group_id)
        if not successfully_load_json:
            return utils.return_ics_Response(utils.groupme_ics_error(error_text='critical error loading calendar'))
        current_app.ics_cache = utils.groupme_json_to_ics(groupme_json=current_app.groupme_calendar_json_cache)
        current_app.last_cache = datetime.datetime.now()
    else:
        print('Cache hit.  Time remaining: {}'.format(datetime.timedelta(minutes=cache_duration) - (datetime.datetime.now() - last_cache)))

    return utils.return_ics_Response(getattr(current_app, 'ics_cache', None))


@app.route('/recent.ics')
def recent_ics():
    return 'Soon!'


if __name__ == "__main__":
    app.run(debug=True)
