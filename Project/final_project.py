#                        Arif-Chuang-Hori-Teehan
#                            Salman Arif
#                            Andrew Chuang
#                            Jonathan Hori
#                            Ryan Teehan
#    
#                        Yelp Recommendation Engine
#                            CMSC 12200
#                            Winter 2017
#
###############################################################################

import algorithms.overlap
import algorithms.text_analysis
import data.json_to_sql
import scraping.scraping
'''
class DataCount:
    data_count = 0
    
    def __init__(self):
        self.data_count += 1
        #self.data_count = count
'''    
#Take user input
def find_correct_biz():
    pass


#Scrape the data
def scrape_data(user_input):
    '''
    Returns:
            biz_reviews - list of dictionaries, each dictionary is a review 
                for a restaurant (NOT ALL THE SAME RESTAURANT)
            user_reviews - list of dictionaries, each dictionary is a review 
                for a restuarant (NOT ALL THE SAME USER OR RESTAURANT)
    '''
    biz_reviews = []
    user_reviews = []
    business_data = []
    bd = None
    for biz_id in user_input:
        print('# # # # # # # # # # # # #', biz_id)
        biz_data, b_reviews, user_list = scraping.scraping.scrape_biz_reviews(biz_id)
        biz_reviews += b_reviews
        if biz_data != bd:
            business_data.append(biz_data)
            bd = biz_data
        for user_id, count in user_list:
            print('######### NEW USER ##########', user_id)
            u_reviews = scraping.scraping.scrape_user_reviews(user_id, count)
            if u_reviews:
                user_reviews += u_reviews
    return business_data, biz_reviews, user_reviews


#Convert the data into a sql database
def convert_to_sql(business_data, biz_reviews, user_reviews, database):
    '''
    Inputs:
            business_data, biz_reviews, user_reviews - from scraped Yelp pages
            database - unique .db filename as a string
        
    Returns:
            Nothing. Database file is now updated
    '''
    #count = DataCase()
    #count.data_count += 1
    data.json_to_sql.create_tables(database)
    data.json_to_sql.business_to_db(database, business_data)
    data.json_to_sql.review_to_db(database, biz_reviews, 'biz_reviews')
    data.json_to_sql.review_to_db(database, user_reviews, 'user_reviews')
     

#Run algorithms
def run_algorithms(database):
    '''
    Inputs:
            database - completed from convert_to_sql
    '''
    biz_data, biz_reviews, user_reviews = algorithms.text_analysis.sql_to_df(database)
    #intersections = algorithms.overlap.count_intersections()
    similarity_list = algorithms.text_analysis.get_similarities(biz_reviews, user_reviews)
    return similarity_list

#Sort and filter results

#Display in Django

def go(user_input, db):
    bd, br, ur = scrape_data(user_input)
    convert_to_sql(bd, br, ur, db)
    l = run_algorithms(db)
