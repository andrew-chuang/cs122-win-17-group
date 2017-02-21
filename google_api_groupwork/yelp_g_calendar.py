# CS 122 Winter 2017 Project
# Arif-Chuang-Hori-Teehan
# Yelp Restaurant Recommender Project 
#
# Note: "Imports" section of code highly influenced by the
# Google API Quickstarts page for guidance. All other functions
# were written by group members. 
#
#
#
#
#
############################################
#                                          #
#                  Imports                 #
#                                          #
############################################
#

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar for CS122 Yelp Project'












