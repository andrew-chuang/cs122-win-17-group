# CS 122 Arif-Chuang-Hori-Teehan Yelp Recommender Project
#
# 
#

import sys

from oauth2client import client
from googleapiclient import sample_tools
import os
from oauth2client.file import Storage


def main(argv):
    # Authenticate and construct service.
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

def add_event(argv):
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar')

    try:
        page_token = None
        while True:
            


if __name__ == '__main__':
    main(sys.argv)  



