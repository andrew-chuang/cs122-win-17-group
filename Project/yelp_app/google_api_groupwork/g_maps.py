# CS 122 Winter 2017 Project
# Arif-Chuang-Hori-Teehan
# Google Maps API Work
#
# 
#

import googlemaps
import urllib
from datetime import datetime

API_KEY = 'AIzaSyCHgCLQKPNQDVJvycSL0kRh1AdTVYTwm9Q'
gmaps = googlemaps.Client(key=API_KEY)


def lat_lon_finder(address):
    '''
    Function takes address and reverse
    geocodes the address to find a latitude and longitude. 

    Input:
        address (string) address of restaurant

    Output: 
        lat, lon (string) coordinates of the restaurant
    '''
    geocode_object = gmaps.geocode(address)
    lat = geocode_object[0]["geometry"]["location"]["lat"]
    lon = geocode_object[0]["geometry"]["location"]["lng"]
    return lat, lon

def get_directions(rest1, rest2):
    '''
    Function takes in two restaurants 
    and produces a string of HTML containing
    directions between the restaurants. 
    
    Inputs:
        rest_list (list of restaurant addresses)

    Outputs:
        dir_list (string) string of html directions 
        between the restaurants in question 
    '''
    directions_obj = gmaps.directions(rest1, rest2)
    directions_obj = directions_obj[0]

    directions_string = ""

    for leg in directions_obj['legs']:
        for step in leg['steps']:
            html_instructions = step['html_instructions']
            directions_string += html_instructions + ' '
    return directions_string


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
        rest_list (list) list of addresses of restaurants
        list can be any length

    Output:
        map_url (string): url placed in HTML img that produces a map 
    '''

    if len(rest_list) == 1:
        lat, lon = lat_lon_finder(rest_list[0])
        url = ('<img src = "https://maps.googleapis.com/maps/api'
        '/staticmap?size=400x400&markers=color:blue%7Clabel:S%7C'
        '{},{}&key={}">'.format(lat, lon, API_KEY))
        return url
    elif len(rest_list) > 1:
        base = ('<img src = "https://maps.googleapis.com/maps/api'
        '/staticmap?size=400x400')
        key = ('&key={}">'.format(API_KEY))
        marker_list = "&markers=color:blue%7Clabel:S"
        for rest in rest_list:
            lat, lon = lat_lon_finder(rest)
            marker = ('%7C{},{}'.format(lat,lon))
            marker_list += marker
        map_url = base + marker_list + key
        return map_url
    else:
        map_url = ('<img src = "https://maps.googleapis.com/maps/api/'
            'staticmap?center=Chicago,IL'
            '&zoom=13&size=400x400&markers=color:blue%7C'
            'label:S%7C11211%7C11206%7C11222&key={}">'.format(API_KEY))
        return map_url

'''
def photo_producer(rest):
    
    Function uses Google's Places API to find the picture 
    attribution of a place and concatenates these attributes
    into a URL that can be used to display the picture
    of the restaurant in question. 

    Inputs:
        restaurant name

    Outputs:
        image_url

    
    pic_dict = gmaps.places(rest)
    photo_attri = pic_dict["photos"]
    first_photo = photo_attri[0]
'''









