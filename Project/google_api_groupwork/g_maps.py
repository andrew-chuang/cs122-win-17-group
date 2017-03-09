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

'''
Test code to make sure that the Client object works; remove before turning in. 
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
directions = gmaps.directions('5500 S. University Ave, Chicago, IL', \
    "5300 S. Ellis Ave")
print(geocode_result)'''


def get_directions(rest_list):
    '''
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

def direct_lines(rest_pair):
    '''
    Function to potentially produce a static map with
    lines between the restaurant markers. These lines
    do not map "directions via street" between locations, just 
    direct lines between locations. 

    Inputs:
       rest_list
    '''
    pass


def static_mapper(rest_list):
    '''
    Function creates a static map URL based on the list of addresses
    provided to the function as an input. 

    Mechanics of this function revolve around concatenating
    the different components of the URL together into a valid
    HTML img tag that can then be returned to Django and displayed
    as a static map with markers. 

    Function returns a base map centered on the city of Chicago, IL
    if the list of addresses does not at least have one address. 
    (i.e. len(address_list) == 0)

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
        print(map_url)
    elif len(rest_list) > 1:
        map_list = []
        for rest in rest_list:
            places = ""
            encode_rest = urllib.parse.quote_plus(rest)
            places = places + breaker + encode_rest
            map_url = base_url + marker + breaker + places + key + \
            API_KEY + end_tag
            map_list.append(map_url)
        print(map_list) 
    else:
        map_url = ('<img src = "https://maps.googleapis.com/maps/api/'
            'staticmap?center=Chicago,IL'
            '&zoom=13&size=400x400&markers=color:blue%7C'
            'label:S%7C11211%7C11206%7C11222&key={}">'.format(API_KEY))
        print(map_url)


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
    photo_attri = pic_dict["photos"]
    first_photo = photo_attri[0]

address = ["5500 S. University Ave, Chicago, IL", "5300 S. Ellis Ave, Chicago, IL"]
add = ["5500 S. University Ave, Chicago, IL"]



if __name__ == '__main__':
    static_mapper(add)








