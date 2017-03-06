import scraping
from multiprocessing.pool import ThreadPool
from itertools import starmap 


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
        biz_data, b_reviews, user_list = scraping.scrape_biz_reviews(biz_id)
        biz_reviews += b_reviews

        user_list = list(user_list)
        #usr = [x[0] for x in user_list]
        #cnt = [x[1] for x in user_list]

        #usr_list = [usr[i:i+3] for i in range(0, len(usr), 3)]
        #cnt_list = [cnt[i:i+3] for i in range(0, len(cnt), 3)]

        user_list = [user_list[i:i+5] for i in range(0, len(user_list), 5)]

        
        if biz_data != bd:
            business_data.append(biz_data)
            bd = biz_data

        for i in range(0, len(user_list)):
            #u_reviews = ThreadPool(3).starmap(scraping.scrape_user_reviews, (usr_list[i], cnt_list[i]))
            u_reviews = ThreadPool(5).starmap(scraping.scrape_user_reviews, user_list[i])
            #u_reviews = scraping.scraping.scrape_user_reviews(user_id, count)
            if u_reviews:
                user_reviews += (item for sublist in u_reviews for item in sublist)
    return business_data, biz_reviews, user_reviews