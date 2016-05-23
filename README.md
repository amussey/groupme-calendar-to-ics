# GroupMe Calendar to ICS

Turn your GroupMe event calendar into an ICS feed (for Google Calendar, Apple Calendar, Outlook, etc.).


## Deploy to Heroku

To get started, you'll need the following:

 * The Group ID for the group's calendar
 * A GroupMe API Developer Token


### Default Settings

 * **Cache Rate** - By default, the GroupMe calendar is refreshed and cached by one request every 6 hours.  The caching rate can be modified or disabled by setting it to `0`.
