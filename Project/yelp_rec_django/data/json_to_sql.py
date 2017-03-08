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
'''

import json
import sqlite3

def import_json_data():
    
    business_data = []
    count = 1
    with open('yelp_academic_dataset_business.json') as json_data:
        for dict in json_data:
            if count < 1000:
                row = json.loads(dict)
                business_data.append(row)
                count +=1
            else:
                break

    review_data = []
    count = 1
    with open('yelp_academic_dataset_review.json') as json_data:
        for dict in json_data:
            if count < 100:
                row = json.loads(dict)
                review_data.append(row)
                count +=1
            else:
                break
            
    return business_data, review_data

def create_tables(db):
    con = sqlite3.connect(db)
    with con:
        cursor = con.cursor()
        
        #Create business table
        cursor.execute("CREATE TABLE business(business_id TEXT)")
        '''
        #Create attributes table ==> for business
        cursor.execute("CREATE TABLE attributes(business_id TEXT, credit_cards \
            TEXT, alcohol TEXT, attire TEXT, caters TEXT, delivery TEXT, \
            drive_thru TEXT, good_for_groups TEXT, good_for_kids TEXT, has_tv \
            TEXT, noise_level \
            TEXT, outdoor_seating TEXT, price_range INTEGER, take_out TEXT, \
            takes_res TEXT, waiters TEXT, wheelchairs TEXT, wifi TEXT, \
            apple_pay TEXT, android_pay TEXT, bike_parking TEXT, music TEXT, \
            coat_check TEXT, smoking TEXT, dogs TEXT, pool_table TEXT, \
            happy_hour TEXT, dancing TEXT, order_at_counter TEXT, byob_corkage \
            TEXT, corkage TEXT, byob TEXT, all_hours TEXT, neutral_restrooms TEXT)")
        
        #Create neighborhoods table ==> for business
        cursor.execute("CREATE TABLE neighborhoods(business_id TEXT, \
            neighborhood TEXT)")
        
        #Create categories table ==> for business
        cursor.execute("CREATE TABLE categories(business_id TEXT, \
            category TEXT)")
        '''
        #Create biz_reviews table
        cursor.execute("CREATE TABLE biz_reviews(business_id TEXT, stars INTEGER, \
            text TEXT, user_id TEXT)")
        
        #Create user_reviews table
        cursor.execute("CREATE TABLE user_reviews(business_id TEXT, \
            stars INTEGER, text TEXT, user_id TEXT)")
        
        
#First create a database in sqlite3 called 'data.db'
#The database cannot store all data, because some data is in dictionaries or
#   lists: neightborhoods, attributes, categories, hours
def business_to_db(db, business_data):
    con = sqlite3.connect(db)
    with con:
        cursor = con.cursor()
        for biz_id in business_data:
            print(biz_id)
            s = "INSERT INTO business (business_id) VALUES (?)"
            print(s)
            cursor.execute(s, (biz_id,))
    '''
            attributes = dictionary['attributes']
            columns = ['business_id']
            values = ['"{}"'.format(dictionary['business_id'])]
            d = {'Accepts Credit Cards': 'credit_cards', 'Good for Groups': \
                 'good_for_groups', 'Good for Kids': 'good_for_kids', 'Has TV': \
                 'has_tv', 'Noise Level': 'noise_level', 'Outdoor Seating':\
                 'outdoor_seating', 'Price Range': 'price_range', 'Take-out': \
                 'take_out', 'Takes Reservations': 'takes_res', 'Waiter Service': \
                 'waiters', 'Wheelchair Accessible': 'wheelchairs', \
                 'Accepts Apple Pay': 'apple_pay', 'Accepts Android Pay': 'android_pay', \
                 'Bike Parking': 'bike_parking', 'Coat Check': 'coat_check', \
                 'Wi-Fi': 'wifi', 'Dogs Allowed': 'dogs', 'Has Pool Table': \
                 'pool_table', 'Happy Hour': 'happy_hour', 'Good For Dancing': \
                 'dancing', 'Drive-Thru': 'drive_thru', 'BYOB/Corkage': \
                 'byob_corkage', 'Order at Counter': 'order_at_counter', \
                 'Open 24 Hours': 'all_hours', 'Gender Neutral Restrooms': \
                 'neutral_restrooms'}
            for key, value in attributes.items():
                if key == 'Parking' or key == 'Ambience' or key == 'Good For' \
                    or key == 'Best Nights' or key == "By Appointment Only" \
                    or key == "Accepts Insurance" or key == \
                    "Hair Types Specialized In":
                    continue
                if key in d:
                    columns.append(d[key])
                else:  
                    columns.append(key.lower())
                values.append('"{}"'.format(value))
            columns = ", ".join(columns)
            for item in values:
                values[values.index(item)] = str(item)
            values = ", ".join(values)
            s = "INSERT INTO attributes " + "(" + columns + ")" + \
                " VALUES " + "(" + values + ")"
            cursor.execute(s)
            
            neighborhoods = dictionary['neighborhoods']
            for place in neighborhoods:
                values = ['"{}"'.format(dictionary['business_id']), \
                    '"{}"'.format(place)]
                values = ', '.join(values)
                s = "INSERT INTO neighborhoods (business_id, neighborhood) \
                VALUES (" + values + ")"
                cursor.execute(s)
                
            categories = dictionary['categories']
            for category in categories:
                values = ['"{}"'.format(dictionary['business_id']), \
                    '"{}"'.format(category)]
                values = ', '.join(values)
                s = "INSERT INTO categories (business_id, category) VALUES (" \
                    + values + ")"
                cursor.execute(s)
    '''
        
def review_to_db(db, review_data, table):
    con = sqlite3.connect(db)
    with con:
        cursor = con.cursor()
        for review in review_data:
            columns = []
            items = []
            for key, value in review.items():
                if key == 'votes' or key == 'type' or key == 'date':
                    continue
                else:
                    columns.append(key)
                    items.append(value)
            columns = ", ".join(columns)
            s = "INSERT INTO " + table + "(" + columns + ")" + \
                    " VALUES (?,?,?,?)"
            cursor.execute(s, (items[0], items[1], items[2], items[3]))
            
def clear_tables(db, biz = True, br = True, ur = True):
    con = sqlite3.connect(db)
    with con:
        cursor = con.cursor()
        if biz:
            cursor.execute("DELETE FROM business")
            cursor.execute("VACUUM")
        if br:
            cursor.execute("DELETE FROM biz_reviews")
            cursor.execute("VACUUM")
        if ur:
            cursor.execute("DELETE FROM user_reviews")
            cursor.execute("VACUUM")
        
