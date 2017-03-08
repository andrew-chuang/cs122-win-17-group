# CS 122 Winter 2017 Project
# Arif-Chuang-Hori-Teehan
# Google Maps API Work
#
# 
#

"""
import googlemaps 
from datetime import datetime

API_KEY = 'AIzaSyCHgCLQKPNQDVJvycSL0kRh1AdTVYTwm9Q'

from googlemaps import GoogleMaps
gmaps = GoogleMaps(API_KEY)

address = 'Constitution Ave NW & 10th St NW, Washington, DC'
lat, lng = gmaps.address_to_latlng(address)
print lat, lng

directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)
print(directions_result)
"""

import googlemaps
import urllib
from datetime import datetime

API_KEY = 'AIzaSyCHgCLQKPNQDVJvycSL0kRh1AdTVYTwm9Q'
gmaps = googlemaps.Client(key=API_KEY)
# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
directions = gmaps.directions('5500 S. University Ave, Chicago, IL', \
	"5300 S. Ellis Ave")
print(directions)


def get_directions(rest_list):
    ''''
    Function takes in a list of restaurants (preordered according to schedule)
    and produces HTML string of directions between the restaurants. 
    
    Inputs:
        rest_list (list of restaurant addresses)

    Outputs:
        dir_list (list) 
    '''
    for index in range(1, rest_list):
        rest1 = rest_list[index - 1]
        rest2 = rest_list[index]
        directions_object = gmaps.directions(rest1, rest1)

def static_mapper(address_list):
	'''
	Function creates a static map URL based on the list of addresses
	provided to the function as an input. 

	Input:
	    rest_list:

	Output:
	    map_url (string): url that produces a map when placed in 
	    <img> tags on the Django site
	'''
	base_url = 'https://maps.googleapis.com/maps/api/staticmap?'
	if len(rest_list) == 1:
		encode_address = urllib.parse.urlencode(rest_list[0])
		map_url = base_url + "center=Chicago,IL" + "&" + "&key=" + API_KEY
	for rest in rest_list:
        














