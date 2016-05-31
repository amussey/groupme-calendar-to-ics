# GroupMe Calendar to ICS

Turn your GroupMe event calendar into an ICS feed (for Google Calendar, Apple Calendar, Outlook, etc.).

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/amussey/groupme-calendar-to-ics)

## Installing

When you set up this app, you'll be required to configure four environment variables:

 * `GROUPME_GROUP_ID` - The ID for the GroupMe group.
 * `GROUPME_API_KEY` - A [GroupMe Developer Access Token](https://dev.groupme.com/docs/v3) for a user in the GroupMe group.
 * `GROUPME_STATIC_NAME` - A static name for the group.  This will lock a name for the calendar, even if the group decides to change their name.
 * `CACHE_DURATION` - The duration for which the GroupMe calendar is cached.  `0` will disable caching.
 * `GROUPME_PROXY_URL` - *(Optional)* A proxy URL to provide for the calendar.ics.

## Deploy to Heroku

To get started, you'll need the following:

 * The Group ID for the group's calendar
 * A GroupMe API Developer Token


### Default Settings

 * **Cache Rate** - By default, the GroupMe calendar is refreshed and cached by one request every 60 minutes.  The caching rate can be modified or disabled by setting it to `0`.
