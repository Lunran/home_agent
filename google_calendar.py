from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = '~/home_agent/client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

try:
    import argparse
    parser = argparse.ArgumentParser(parents=[tools.argparser])
    parser.add_argument('day', choices=['today', 'tomorrow'], help='day to check the schedule')
    flags = parser.parse_args()
except ImportError:
    flags = None

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        file_path = os.path.expanduser(CLIENT_SECRET_FILE)
        flow = client.flow_from_clientsecrets(file_path, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)

    return credentials

def get_schedule_events():
    """Creates a Google Calendar API service object and return the events
    """

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    from datetime import datetime, timedelta
    days = {'today': 0, 'tomorrow': 1}
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start = (today + timedelta(days=days[flags.day])).isoformat() + '+09:00'
    end = (today + timedelta(days=days[flags.day], hours=23, minutes=59)).isoformat() + '+09:00'
    eventsResult = service.events().list(calendarId='primary', timeMin=start, timeMax=end,
                                         singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return flags.day, events

if __name__ == '__main__':
    day, events = get_schedule_events()
    if events:
        print('You have a plan ' + day + '. Get ready.')
        for event in events:
            print(event['summary'])
    else:
        print('No upcoming events.')
