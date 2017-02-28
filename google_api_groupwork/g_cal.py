
import httplib2
import os

from googleapiclient import discovery
import oauth2client
from oauth2client import client
<<<<<<< Updated upstream
from oauth2client import tools
from oauth2client import file
from oauth2client.client import OAuth2WebServerFlow
=======
from googleapiclient import sample_tools
from oauth2client.file import Storage

SCOPES = "https://www.googleapis.com/auth/calendar"

def display_calendars(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar')

    return_list = []
    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(
                pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                return_list.append(calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break
        return return_list

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')




def calendar_chooser(argv):
    '''
    Function reads in the list of calendars that the users has access to. 
    If Yelp API has already authorized the construction 
    of a new function, then function directly returns the 
    '''
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar')
    try:
        page_token = None
        while True:
            calendar_list = display_calendars(argv)
            if not "Yelp Calendar" in calendar_list:
                yelp_calendar = {
                "kind": "calendar#calendar", # Type of the resource ("calendar#calendar").
                "description": "Yelp Recommendation Schedule", # Description of the calendar. Optional.
                "summary": "Yelp Recommendation Calendar", # Title of the calendar.
                "etag": "A String", # ETag of the resource.
                "location": "Chicago", # Geographic location of the calendar as free-form text. Optional.
                "timeZone": "American/Chicago", # The time zone of the calendar. 
                #(Formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich".) Optional.
                "id": "cs122yelp", # Identifier of the calendar. 
                #To retrieve IDs call the calendarList.list() method.
                }
                service.calendars().insert(body = yelp_calendar).execute
            else:
                cal_id = [cal for cal in calendar_list if "Yelp Calendar" in cal]
                return cal_id
                
    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')
 



def event_creator(event_list):
    '''
    Function takes in event_list, which contains the details for a Google
    account as its elements, and uses it to construct a dictionary
    that is later used to insert an event into the actual event of the user. 

    Inputs:
        event_list (list) contains the details of an event necessary to create 
        an event using the Google Calendar API

    Outputs:
        event_details (dictionary) 
    '''
    event_details = {
      'summary': '',
      'location': '',
      'description': '',
      'start': {
        'dateTime': '',
        'timeZone': '',
      },
      'end': {
        'dateTime': '',
        'timeZone': '',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
      'attendees': [],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event_details['summary'] = event_list[0]
    event_details['location'] = event_list[1]
    event_details['description'] = event_list[2]
    event_details['start']['dateTime'] = event_list[4]
    event_details['start']['timeZone'] = event_list[5]
    event_details['end']['dateTime'] = event_list[4]
    event_details['end']['timeZone'] = event_list[5]
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
    insert_event()
=======
    calendar_chooser(sys.argv)  



>>>>>>> Stashed changes
