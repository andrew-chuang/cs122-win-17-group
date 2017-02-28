
import httplib2
import os

from googleapiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file
from oauth2client.client import OAuth2WebServerFlow

import calendar
import datetime
import time
import sys
import config

import json
from json import JSONEncoder


SCOPES = 'https://www.googleapis.com/auth/calendar'
APPLICATION_NAME = "Yelp Recommender"

def get_credentials():

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    cred_path = os.path.join(credential_dir,'mycroft-googlecalendar-skill.json')
    store = oauth2client.file.Storage(cred_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        credentials = tools.run_flow(OAuth2WebServerFlow(client_id=CID,client_secret=CIS,scope=SCOPES,user_agent=APPLICATION_NAME),store)

    return credentials

def yelp_scheduler():
    

def event_dict_creator():
    event_dict = {}

    return event_dict

event_dict = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-27T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}


def insert_event():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    event = service.events().insert(calendarId='primary', body=event_dict).execute()

    status = event.get('status')
    htmlLink = event.get('htmlLink')

    if status == 'confirmed' and len(htmlLink) > 43:
        print ('confirmed')
    else:
        print ('error')

if __name__ == '__main__':
    insert_event()