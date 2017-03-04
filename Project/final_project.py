import sys
import algorithms.overlap
import data.json_to_sql
import scraping.scraping

#Take user input
def find_correct_biz():
    pass


#Scrape the data
def scrape_data():
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
    for restaurant in user_input:
        biz_data, b_reviews, user_list = scraping.scrape_biz_reviews(biz_id)
        biz_reviews += b_reviews
        business_data.append(biz_reviews)
        for user in user_list:
            u_reviews = scraping.scrape_user_reviews(user_id)
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
    pass

#Sort and filter results

#Display in Django