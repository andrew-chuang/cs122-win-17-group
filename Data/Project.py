'''
                        Arif-Chuang-Hori-Teehan
                            Salman Arif
                            Andrew Chuang
                            Jonathan Hori
                            Ryan Teehan
    
                        Yelp Recommendation Engine
                            CMSC 12200
                            Winter 2017

###############################################################################

Overview of Yelp Functions and Data:
    
https://github.com/Yelp/dataset-examples

Yelp provided functions:
    json_to_csv converter - convert dataset from json to csv
    category predictor - given some text, predict likely categories
    review_autopilot - use a markov chain to finish a review
    positive_category_words - generates positivity scores for words either
        globally or per-category

###############################################################################

Inputs:
        review text, review star count
        list of restaurants
        restaurant categories/properties/attributes
        time of day
        location (zip code, neighborhood, city)
        
Returns:
        list of restaurants
        itinerary for night out
        
Procedure:
    1) Input restaurant list
        a) us business_data and review_data to 
        
'''

import json
import sqlite3

def import_json_data():
    business_data = []
    with open('yelp_academic_dataset_business.json') as json_data:
        for dict in json_data:
            row = json.loads(dict)
            business_data.append(row)
      
    #If we choose to use the checkin data    
    
    #checkin_data = []
    #with open('yelp_academic_dataset_checkin.json') as json_data:
    #    for dict in json_data:
    #        row = json.loads(dict)
    #        checkin_data.append(row)
        
    review_data = []
    with open('yelp_academic_dataset_review.json') as json_data:
        for dict in json_data:
            row = json.loads(dict)
            review_data.append(row)
       
    #If we choose to use the tip data
    
    #tip_data = []
    #with open('yelp_academic_dataset_tip.json') as json_data:
    #    for dict in json_data:
    #        row = json.loads(dict)
    #        data.append(row)
        
    user_data = []
    with open('yelp_academic_dataset_user.json') as json_data:
        for dict in json_data:
            row = json.laods(dict)
            user_data.append(dict)

#First create a database in sqlite3 called 'data.db'
#The database cannot store all data, because some data is in dictionaries or
#   lists: neightborhoods, attributes, categories, hours
def business_to_db(db):
    con = sqlite3.connect(db)
    with con:
        cursor = con.cursor()
        
        #Must change this to omit the dictionary/list data
        cursor.execute("CREATE TABLE Business(business_id TEXT, name TEXT, \
            neighborhoods ???, address TEXT, city TEXT, state TEXT, \
            latitude FLOAT, longitude FLOAT, stars FLOAT, review_count \
            INTEGER, is_open TEXT, attributes ???, categories ???, hours \
            ???, type TEXT)")
        
        counter = 0
        for dict in business_data:
            counter += 1
            
            a = dict['business_id']   
            b = dict['name']
            c = dict['neighborhoods']
            d = dict['full_address']
            e = dict['city']
            f = dict['state']
            g = dict['latitude']
            h = dict['longitude']
            i = dict['stars']
            j = dict['review_count']
            k = dict['open']
            l = dict['attributes']
            #l_ = []
            #for attribute, value in l.items():
            #    l_.append((attribute, value))
            m = dict['categories']
            n = dict['hours']
            #n_ = []
            #for day, value in n.items():
            #    n_.append((day, value))
            o = dict['type']
            cursor.execute("INSERT INTO Business VALUES \
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                (a, b, c, d, e, f, g, h, i, j, k, l, m, n, o))
    
'''
Outline of project structure

1. Function to specify search to a particular city/area

2. Focusing on a number of metrics to determine similarity

    Search for keywords in the text, ex. "service" and match what follows
    to similar statements

    Compute "distance" between the sets of reviews of two different restaurants

    Latent semantic analysis

    Compute average positivity scores

    Each of these can be given a weight, then they're returned in a sorted list
    of most similar restaurants as a tuple with a list of attributes that matched 
    in order

3. Combining with recommendations for entertainment
    
    Includes time and type of venue

    Produces a list of "schedules": tuples with venue and time


'''

def select_location(location, db):
    '''
    Selects only restaurants in the relevant location

    Inputs: 
        location - string
        db - database
    '''

def identify_similar(training, testing):
    '''
    Takes a set of reviews from the database and identifies similar phrases 
    in reviews in the testing set

    Inputs:
        training - strings
        testing - strings

    returns: 
        tuple of restaurant and int for similarity score 
    '''

def lsa(terms, db):
    '''
    Performs latent semantic analysis on the reviews to return a list of words related to the terms

    Inputs:
        terms - list of strings
        db - database

    returns:
        list of related strings
    '''

def compute_scores(results):
    '''
    Takes the results of other functions and returns a set of scores

    Inputs:
        results - list of ints
    Returns:
        list of ints
    '''

def add_weights(scores, terms):
    '''
    This adds weights to the scores that come from other analyses

    Inputs:
        scores - list of ints
        terms - list of strings

    Returns:
        list of ints
    '''


# Begin coding


