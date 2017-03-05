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
    for biz_id in user_input:
        biz_data, b_reviews, user_list = scraping.scraping.scrape_biz_reviews(biz_id)
        biz_reviews += b_reviews
        business_data.append(biz_reviews)
        for user_id in user_list:
            u_reviews = scraping.scraping.scrape_user_reviews(user_id)
            if u_reviews:
                user_reviews += u_reviews
    return business_data, biz_reviews, user_reviews



#Convert the data into a sql database
def convert_to_sql(business_data, biz_reviews, user_reviews, database):
    '''
    '''
    create_tables(database)
    business_to_db(database, business_data)
    review_to_db(database, biz_reviews, 'biz_reviews')
    review_to_db(database, user_reviews, 'user_reviews')
     

#Run algorithms
def run_algorithms():
    #Ryan will add sql call within his algorithms to get the pandas df from db
    pass

#Sort and filter results

#Display in Django