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
    Function takes in a list of restaurants 
    (preordered according to schedule)
    and produces HTML string of directions between the restaurants. 
    
    Inputs:
        rest_list (list of restaurant addresses)

    Outputs:
        dir_list (list) 
    '''
    dir_list = []
    for index in range(1, rest_list):
        rest1 = rest_list[index - 1]
        rest2 = rest_list[index]
        directions_object = gmaps.directions(rest1, rest2)

def direct_mapper(rest_pair):
	'''
	Function to potentially produce a static map with
	direction lines between the restaurant markers. 

	Inputs:
	    rest_list
	'''
	pass


def static_mapper(address_list):
	'''
	Function creates a static map URL based on the list of addresses
	provided to the function as an input. 

	Mechanics of this function revolve around concatenating
	the different components of the URL together into a valid
	HTML img tag that can then be returned to Django and displayed
	as a static map with markers. 

	Input:
	    rest_list:

	Output:
	    map_url (string): url that produces a map when placed in 
	    <img> tags on the Django site
	'''
	base_url = '<img src = "https://maps.googleapis.com/maps/api/staticmap?'
	marker = "markers=color:red%7Clabel:S"
	breaker = "%7C"
	key = '&key='
	end_tag = '">'

	if len(rest_list) == 1:
		encode_address = urllib.parse.quote_plus(rest_list[0])
		map_url = base_url + 'center=Chicago,IL' + '&' + marker \
		+ breaker + encode_address + key + API_KEY + end_tag
		return map_url
	elif len(rest_list) > 1:
		places = ""
	    for rest in rest_list:
	    	encode_rest = urllib.parse.quote_plus(rest)
	    	places = places + breaker + encode_rest
	    map_url = base_url + marker + breaker + places + key + \
	    API_KEY + end_tag
	    return map_url
	else:
		map_url = base_url + 'center=Chicago,IL' + key + API_KEY + end_tag
		return map_url 


def photo_producer(rest):
	'''
	Function uses Google's Places API to find the picture 
	attribution of a place and concatenates these attributes
	into a URL that can be used to display the picture
	of the restaurant in question. 

	Inputs:
	    restaurant name

	Outputs:
        image_url

    '''
    pic_dict = gmaps.places(rest)
    pic_dict["photos"][""]

        














