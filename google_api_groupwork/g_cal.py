# CS 122 Arif-Chuang-Hori-Teehan Yelp Recommender Project
#
# Imports taken from the samples of Google API for Python Client 
# GitHub 
#

import sys

from oauth2client import client
from googleapiclient import sample_tools
import os
from oauth2client.file import Storage


def display_calendars(argv):
    '''

    '''
    # Authenticate and construct service.
    # Consider writing another function for
    # just authenticating the users' credentials?
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar')

    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(
                pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

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

    if len(event_details) > 6:
        event_details['attendees'].append(['email': event_list[6]])

    
    # Remember to talk to group about the best way to grab
    # the users' time zone and whether or not we should
    # be using Google's Timezone API?
    return event_details


def add_event(argv, event_list):
    '''
    Function adds event to the authorized users' calendar. 
    '''
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar')
    event_details = event_creator(event_list)

    try:
        page_token = None
        while True:
            service.events().insert(calendarId='primary', body = event_details).execute()
            print('Event created: %s' % (event.get('htmlLink')))

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

def delete_event(argv, event_list):
    pass

def something_event():
    pass



if __name__ == '__main__':
    display_calendars(sys.argv)  



