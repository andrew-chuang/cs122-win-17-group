# CS 122 Winter 2017 Project
# Arif-Chuang-Hori-Teehan
# Google Maps API Work
#
# 
#

from google maps import convert
import httplib2

                     ###############################
                     #   Following function        #
                     # written by Google Maps API  #
                     # NOT a product of the group  #
                     ###############################

# Location for below function needs to be in coordinate form. 

def places(client, query, location=None, radius=None, language=None,
           min_price=None, max_price=None, open_now=False, type=None,
           page_token=None):
    """
    Places search.
    :param query: The text string on which to search, for example: "restaurant".
    :type query: string
    :param location: The latitude/longitude value for which you wish to obtain the
        closest, human-readable address.
    :type location: string, dict, list, or tuple
    :param radius: Distance in meters within which to bias results.
    :type radius: int
    :param language: The language in which to return results.
    :type langauge: string
    :param min_price: Restricts results to only those places with no less than
        this price level. Valid values are in the range from 0 (most affordable)
        to 4 (most expensive).
    :type min_price: int
    :param max_price: Restricts results to only those places with no greater
        than this price level. Valid values are in the range from 0 (most
        affordable) to 4 (most expensive).
    :type max_price: int
    :param open_now: Return only those places that are open for business at
        the time the query is sent.
    :type open_now: bool
    :param type: Restricts the results to places matching the specified type.
        The full list of supported types is available here:
        https://developers.google.com/places/supported_types
    :type type: string
    :param page_token: Token from a previous search that when provided will
        returns the next page of results for the same search.
    :type page_token: string
    :rtype: result dict with the following keys:
        results: list of places
        html_attributions: set of attributions which must be displayed
        next_page_token: token for retrieving the next page of results
    """
    return _places(client, "text", query=query, location=location,
                   radius=radius, language=language, min_price=min_price,
                   max_price=max_price, open_now=open_now, type=type,
                   page_token=page_token)




