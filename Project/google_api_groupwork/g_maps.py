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
from photobase import settings_base
API_KEY = 'AIzaSyCHgCLQKPNQDVJvycSL0kRh1AdTVYTwm9Q'

gmaps = googlemaps.Client(key=API_key)

# Geocoding an address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

print(geocode_result)

