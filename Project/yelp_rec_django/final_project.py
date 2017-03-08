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
from multiprocessing.pool import ThreadPool
from itertools import starmap 
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
    '''
    biz_reviews = []
    user_reviews = []
    business_data = []
    bd = None
    for biz_id in user_input:
        #biz_data, b_reviews, user_list = scraping.scraping.scrape_biz_reviews(biz_id)
        
        # ### No longer returning entire business information, just id
        busn_id, b_reviews, user_list = scraping.scraping.scrape_biz_reviews(biz_id)
        biz_reviews += b_reviews

        user_list = list(user_list)
        #usr = [x[0] for x in user_list]
        #cnt = [x[1] for x in user_list]

        #usr_list = [usr[i:i+3] for i in range(0, len(usr), 3)]
        #cnt_list = [cnt[i:i+3] for i in range(0, len(cnt), 3)]

        user_list = [user_list[i:i+5] for i in range(0, len(user_list), 5)]

        
        if busn_id != bd:
            business_data.append(busn_id)
            bd = busn_id

        for i in range(0, len(user_list)):
            #u_reviews = ThreadPool(3).starmap(scraping.scrape_user_reviews, (usr_list[i], cnt_list[i]))
            u_reviews = ThreadPool(5).starmap(scraping.scraping.scrape_user_reviews, user_list[i])
            #u_reviews = scraping.scraping.scrape_user_reviews(user_id, count)
            if u_reviews:
                user_reviews += (i for sublist in u_reviews for i in sublist)
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
    intersections = algorithms.overlap.count_intersections(user_reviews)
    similarities, sentiments = algorithms.text_analysis.get_scores(biz_reviews, user_reviews)
    scores = algorithms.text_analysis.combine_scores(intersections, similarities, sentiments)
    return scores

#Sort and filter results

#Display in Django

def go(user_input, db):
    bd, br, ur = scrape_data(user_input)
    convert_to_sql(bd, br, ur, db)
    l = run_algorithms(db)