# CS 122 Yelp Recommender Project
# Arif-Chuang-Hori-Teehan
#
# 

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
import g_config_secret

import json
from json import JSONEncoder

import googlemaps 
from datetime import datetime


# Group keys are held in a separate file for security reasons.
# The credential function requires a CID and CIS. Can
# be found in the client_secrets.json file as well. 
# These functions were written for the purpose of being used
# in conjunction with the Django site, but are not currently
# being included in the project presentation. 

SCOPES = 'https://www.googleapis.com/auth/calendar'
APPLICATION_NAME = "Yelp Recommender"

# Following initializes Google Maps client due to its
# planned use for scheduling and detail display. 
# Confidential keys imported from Google Secrets file. 

CID = g_config_secret.CID
CIS = g_config_secret.CIS
API_KEY = g_config_secret.API_KEY
GMAPS = googlemaps.Client(API_KEY)


# Following get_credentials function written using 
# the Google API Quickstart page for syntactical help. 


def get_credentials():

    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    cred_path = os.path.join(credential_dir,'client_secrets.json')
    store = oauth2client.file.Storage(cred_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        credentials = tools.run_flow(OAuth2WebServerFlow(client_id=CID,client_secret=CIS,\
          scope=SCOPES,user_agent=APPLICATION_NAME),store)

    return credentials


def yelp_scheduler(restaurant_list, user_requests):
    '''
    Function takes in list of recommended restaurants and 
    returns list of dictionaries after. 
    
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

    Input:
        schedule_list (list)

    Output:
        event_list (list)
    '''
    gmaps = googlemaps.Client(API_KEY)
    event_list = []
    for event in schedule_list:
        event_dict = {}
        event_dict['summary'] = event['restaurant']
        rest_details = gmaps.place(event_dict['summary'])
        event_dict['location'] = rest_details['address']
        event_list.append(event_dict)
    return event_list


    
# Following calendar taken from the Quickstart.py file
# on the Google API Developers page. Used to successfully
# test the capabilities of the Event Adding File. 

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


def calendar_selector():
    '''
    Function tries to determine whether or not the Yelp API calendar 
    has already been added to the users' list of calenders. 
    If so, the calendar does not return or adjust anything. 
    The calendar is added if the function detects that the user
    has not already added a Yelp Recommender function to their 
    calendars list. 
    '''
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    c_list = []
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
        c_list.append(calendar_list_entry['id'])

    if not "yelp_cal" in c_list:
        yelp_cal = {'summary': 'Yelp Calendar', 'timeZone': 'America/Chicago', \
        'id': 'yelp_cal'}
        service.calendars().insert(body=yelp_cal).execute()


def insert_event(event_list):
    '''
    Function inserts event into the calendar of the user. Created
    with the help of the Quickstart.py file of the Google and 
    by extensively using the Google API documentation. 

    Inputs:
        event_list (list) list of dictionaries that are formatted in the
        correct input for Google Calendar API
    
    Outputs:
        No direct outputs from Python, but API adds event to specified calendar. 
    '''
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
    for event in event_list:
        event = service.events().insert(calendarId='primary', body=event_dict).execute()

    status = event.get('status')
    htmlLink = event.get('htmlLink')

    if status == 'confirmed':
        print ('confirmed')
    else:
        print ('error')



if __name__ == '__main__':
    insert_event(ex_event_dict)

