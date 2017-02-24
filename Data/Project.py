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
     
    user_data = []
    count = 1
    with open('yelp_academic_dataset_user.json') as json_data:
        for dict in json_data:
            if count < 100:
                row = json.loads(dict)
                user_data.append(dict)
                count += 1
            else:
                break
            
    return business_data, review_data, user_data



#First create a database in sqlite3 called 'data.db'
#The database cannot store all data, because some data is in dictionaries or
#   lists: neightborhoods, attributes, categories, hours
def business_to_db(db, business_data):
    con = sqlite3.connect(db)
    with con:
        cursor = con.cursor()
        
        #Create business table
        cursor.execute("CREATE TABLE business(business_id TEXT, name TEXT, \
            address TEXT, city TEXT, state TEXT, latitude FLOAT, longitude \
            FLOAT, stars FLOAT, review_count INTEGER, is_open TEXT, type TEXT)")
        
        #Create attributes table ==> for business
        cursor.execute("CREATE TABLE attributes(business_id TEXT, credit_cards \
            TEXT, alcohol TEXT, attire TEXT, caters TEXT, delivery TEXT, \
            drive_thru TEXT, good_for_groups TEXT, good_for_kids TEXT, has_tv \
            TEXT, noise_level \
            TEXT, outdoor_seating TEXT, price_range INTEGER, take_out TEXT, \
            takes_res TEXT, waiters TEXT, wheelchairs TEXT, wifi TEXT, \
            apple_pay TEXT, android_pay TEXT, bike_parking TEXT, music TEXT, \
            coat_check TEXT, smoking TEXT, dogs TEXT, pool_table TEXT, \
            happy_hour TEXT, dancing TEXT)")
        
        #Create neighborhoods table ==> for business
        cursor.execute("CREATE TABLE neighborhoods(business_id TEXT, \
            neighborhood TEXT)")
        
        #Create categories table ==> for business
        cursor.execute("CREATE TABLE categories(business_id TEXT, \
            category TEXT)")
        
        #cursor.execute("CREATE TABLE hours()")
        
        for dictionary in business_data:
            
            cursor.execute("INSERT INTO business VALUES \
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                (dictionary['business_id'], dictionary['name'], \
                dictionary['full_address'], dictionary['city'], \
                dictionary['state'], dictionary['latitude'], \
                dictionary['longitude'], dictionary['stars'], \
                dictionary['review_count'], dictionary['open'], \
                dictionary['type']))
        
            attributes = dictionary['attributes']
            columns = ['business_id']
            values = [dictionary['business_id']]
            d = {'Accepts Credit Cards': 'credit cards', 'Good For Groups': \
                 'good_for_groups', 'Good for Kids': 'good_for_kids', 'Has TV': \
                 'has_tv', 'Noise Level': 'noise_level', 'Outdoor Seating':\
                 'outdoor_seating', 'Price Range': 'price_range', 'Take-out': \
                 'take_out', 'Takes Reservations': 'takes_res', 'Waiter Service': \
                 'waiters', 'Wheelchair Accessible': 'wheelchairs', 'Accepts \
                 Apple Pay': 'apple_pay', 'Accepts Android Pay': 'android_pay', \
                 'Bike Parking': 'bike_parking', 'Coat Check': 'coat_check', \
                 'Wi-Fi': 'wifi', 'Dogs Allowed': 'dogs', 'Has Pool Table': \
                 'pool_table', 'Happy Hour': 'happy_hour', 'Good For Dancing': \
                 'dancing'}
            for key, value in attributes.items():
                if key == 'Parking' or key == 'Ambience' or key == 'Good For' \
                    or key == 'Best Nights':
                    continue
                if key in d:
                    columns.append(d[key])
                else:  
                    columns.append(key.lower())
                values.append(value)
            columns = ", ".join(columns)
            for item in values:
                values[values.index(item)] = str(item)
            values = ", ".join(values)
            s = "INSERT INTO attributes " + "(" + columns + ")" + \
                " VALUES " + "(" + values + ")"
            cursor.execute(s)
            
            neighborhoods = dictionary['nightborhoods']
            #columns = ['business_id', 'neighborhood']
            for place in neighborhoods:
                values = [dictionary['business_id'], place]
                s = "INSERT INTO neighborhoods (business_id, neighborhood) \
                VALUES (" + values + ")"
                cursor.execute(s)
                
            categories = dictionary['categories']
            #columns = ['business_id', 'category']
            for category in categories:
                values = [dictionary['business_id'], category]
                s = "INSERT INTO categories (business_id, category) VALUES (" \
                    + values + ")"
                cursor.execute(s)
            
            
            #Tables remaining to be created:\hours
        

        #Need: ambience, good_for, parking, best_nights, 
        
def review_to_db(db, review_data):
    con = sqlite3.connect(db)
    with con:
        cursor = con.cursor()
        
        #Create review table
        cursor.execute("CREATE TABLE review(business_id TEXT, date TEXT, \
            review_id TEXT, stars INTEGER, text TEXT, type TEXT, \
            user_id TEXT)")
        
        cursor.exectue("CREATE TABLE votes(cool INTEGER, funny INTEGER, \
            useful INTEGER)")
        columns = []
        items = []
        for review in review_data:
            for key, value in review_data.items():
                if key == 'votes':
                    continue
                else:
                    column.append(key)
                    items.append(value)
            columns = ", ".join(columns)
            items = ", ".join(items)
            s = "INSERT INTO review " + "(" + columns + ")" + \
                    " VALUES " + "(" + values + ")"
            cursor.execute(s)
                    
            columns = []
            items = []
            votes = review['votes']
            c = votes['cool']
            f = votes['funny']
            s = 'INSERT INTO votes (cool, funny, useful) VALUES (?,?,?)'
            cursor.execute(s, (dictionary['cool'], dictionary['funny'], \
                dictionary['useful']))
            
#def 
        
