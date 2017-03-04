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
CID = "524235097766-rphuop3n0jtp9utcallhoavm16a9miaq.apps.googleusercontent.com"
CIS = "AIzaSyCHgCLQKPNQDVJvycSL0kRh1AdTVYTwm9Q"

def get_credentials():

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    cred_path = os.path.join(credential_dir,'mycroft-googlecalendar-skill.json')
    store = oauth2client.file.Storage(cred_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        credentials = tools.run_flow(OAuth2WebServerFlow(client_id=CID,client_secret=CIS,\
          scope=SCOPES,user_agent=APPLICATION_NAME),store)

    return credentials


def yelp_scheduler(restaurant_list, user_requests, ):
    '''
    Function takes in list of recommended restaurants and 
    returns list of dictionaries after. Hopefully list is sorted
    by preference? 
    
    Inputs:
        user_requests (list)
        restaurant_list (list) list of dictionaries for each restaurant
        containing name, address, type of food and opening/closing time
    '''
    for rt in restaurant_list:
      pass
      

def event_calendar_adder(schedule_list):
    '''
    Function takes in a list of dictionaries that is in the order of the 
    schedule and changes them to the correct format that needs 
    to be in place for the official Google event input. 
    '''

    event_dict = {}

    


ex_event_dict = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2017-03-05T09:00:00-00:00',
    'timeZone': 'America/Chicago',
  },
  'end': {
    'dateTime': '2017-03-05T10:00:00-00:00',
    'timeZone': 'America/Chicago',
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


def calendar_selector(event):
    '''
    '''
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    c_list = []
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
        c_list.append(calendar_list_entry['id'])

    if not "yelp_cal" in c_list:
        yelp_cal = {'summary': 'Yelp Calendar', 'timeZone': 'America/Chicago'}
        service.calendars().insert(body=yelp_cal).execute()

    return c_list

############################################################################################


def insert_event(event_dict):
    '''
    '''
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

##############################################################################################

if __name__ == '__main__':
    insert_event(ex_event_dict)