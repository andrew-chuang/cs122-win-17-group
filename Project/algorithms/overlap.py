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

# weighting functions to try out


#lognormal cdf function
def weighting(x, u, s):
    '''
    '''
    return  (1 / 2) * (1 + erf((x - u)/(log(s) * sqrt(2))))

# counts

def count_intersections(user_reviews):
    '''
    '''

    count_dict = {}
    sum = 0
    for i_d in user_reviews["business_id"]:
        if i_d not in count_dict:
            count_dict[i_d] = 1
        else:
            count_dict[i_d] += 1
            sum += 1
    #  normalizes the scores so that they add to 1
    # might not be useful, not sure yet

    for key, value in count_dict.items():
        value = value / sum
        weighting(value, 0 , .125)
    
    rests_sorted =  sorted(count_dict.items(), key=op.itemgetter(1), reverse = True)
    
    return rests_sorted

