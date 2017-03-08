# CS 122 Yelp Recommender
# Arif-Chuang-Hori-Teehan
#
#

import sqlite3
import pandas as pd
import json
import operator as op
import numpy as np
import scipy as sp
from math import sqrt, erf, log

# include function for sql calls
# include function that sends sqlcall to pandas database
# pandas db w/ column for each user where row is for a different rest.

def count_intersections(user_reviews):
    '''
    Function counts the number of reviews that each 
    user has produced, in 

    Inputs:
        user_reviews (dictionary)

    Outputs:
        
    '''

    count_dict = {}
    for i_d in user_reviews["business_id"]:
        if i_d not in count_dict:
            count_dict[i_d] = 1
        else:
            count_dict[i_d] += 1

    # normalizes the scores so that they add to 1
    for key in count_dict:
        count_dict[key] = count_dict[key] / len(user_reviews["business_id"])
        #count_dict[key] = weighting(count_dict[key], 0 , .125)
    
    rests_sorted =  sorted(count_dict.items(), key=op.itemgetter(1), \
        reverse = True)
    rests_sorted = pd.DataFrame(rests_sorted)
    
    return rests_sorted


##########################################################################
#---------------------------- UNUSED FUNCTIONS ---------------------------
#
#       Wrote these and had been using them but ended up 
#       deciding to change weighing function and incorporate
#       the weighing within the count_intersections function. 
#
##########################################################################

def weighting(x, u, s):
    '''
    Function to assign weights. 

    Inputs:
        x value
        mean
        standard deviation

    Outputs:
        weighted value
    '''
    return  (1 / 2) * (1 + erf((x - u)/(log(s) * sqrt(2))))




