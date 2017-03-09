import sqlite3
import pandas as pd
#import json
#import operator as op
import numpy as np
import gensim
from collections import defaultdict 
from textblob import TextBlob
from overlap import count_intersections
#from overlap import count_intersections

# include sql calls for text data, should return a list where each entry is the text of a review

# LSI

#remove from file
def sql_to_df(database):
    con = sqlite3.connect(database)
    with con:
        all_biz_data = 'select * from business;'
        all_biz_reviews = 'select * from biz_reviews;'
        all_user_reviews = 'select * from user_reviews;'
        biz_data = pd.read_sql(all_biz_data, con)
        biz_reviews = pd.read_sql(all_biz_reviews, con)
        user_reviews = pd.read_sql(all_user_reviews, con)
    return biz_data, biz_reviews, user_reviews


def name_to_doc_num(biz_data):
    '''
    Creates a dictionary to match business name to document number

    inputs:
        dataframe

    returns:
        dictionary
    '''
    d = {}
    i = 0
    for i_d in biz_data["business_id"]:
        d[i] = i_d
        i += 1
    return d

def tokenize_to_vect(doc_list):
    '''
    Takes a document list and returns a dictionary and a corpora consisting of
    vectors 
    inputs:
         list of strings
    returns:
         corpora
    '''
    stoplist = set('for a of the and to in'.split())
    text_lists = [[word for word in document.lower().split() if word not in stoplist] for document in doc_list]
    freq = defaultdict(int)
    for text in text_lists:
        for k in text:
            freq[k] += 1
    attribute_list = ["service", "quality", "romantic", "atmosphere"]
    text_list2 = [[k for k in text if freq[k] > 1 and k not in attribute_list] for text in text_lists]
    dictionary = gensim.corpora.Dictionary(text_lists)
    corp = [dictionary.doc2bow(text) for text in text_list2]
    return corp, dictionary

def apply_lsi(corp, dictionary):
    '''
    Applies latent semantic indexing to a corpora given a dictionary 

    inputs
        corp - corpora
        dictionary - dict

    returns:   
        lsi = LsiModel
        corpus_lsi - transformed corpus
    '''
    tfidf = gensim.models.TfidfModel(corp)
    c_tfidf = tfidf[corp]
    lsi = gensim.models.LsiModel(tfidf[c_tfidf], id2word=dictionary, num_topics=50)
    corpus_lsi = lsi[c_tfidf]
    return lsi, corpus_lsi

def list_to_test(test_corp, lsi):
    '''
    '''
    return lsi[test_corp]

def similarity_scoring(training_docs, test_doc):
    '''
    Scores a string against a list of training strings

    inputs:
        training_docs - list of strings
        test_doc - string

    returns:
        int
    '''
    # remember to get rid of special characters
    corp, dictionary = tokenize_to_vect(training_docs)
    lsi, c_lsi = apply_lsi(corp, dictionary)
    v = dictionary.doc2bow(test_doc.lower().split())
    vec_lsi = lsi[v]
    ind = gensim.similarities.MatrixSimilarity(lsi[corp])
    sim = ind[vec_lsi]
    #sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    score = 0
    for s in sim:
        score += s
    score = score / len(sim)
    return score
    
def get_scores(business_reviews, user_reviews):
    '''
    Gets reviews for inputted businesses and reviews from top rating users
    and returns DataFrames with sentiment scores and averaged similarity
    scores

    inputs:
        business_reviews - dataframe
        user_reviews - dataframe

    returns:
        sim_frame - DataFrame
        sent_frame - dataframe
    '''
    '''
    grouped = business_reviews.groupby(business_reviews["business_id"])["text"].sum()
    
    if len(grouped.axes[0]) < 2:
        grouped = business_reviews
    '''
    overlap_dict = count_intersections(user_reviews)

    l= []

    for text in business_reviews.text:
        blob = TextBlob(text)
        l.append(blob.sentiment.polarity)

    br_array = np.array(l)
    avg = np.mean(br_array)

    users_grouped = user_reviews.groupby(user_reviews["business_id"])["text"].sum()
    
    score_list = []
    for i in range(len(users_grouped)):
        #if grouped.equals(business_reviews):
        #    sim = similarity_scoring(grouped['text'], users_grouped[i])
        #else:
        sim = similarity_scoring(business_reviews.text, users_grouped[i])
        if len(users_grouped[i]) > 300:
            keywords = gensim.summarization.keywords(users_grouped[i])
            keywords = keywords.split('\n')
        else:
            keywords = "Review is too small for keywords"
        


        blob = TextBlob(users_grouped[i])
        sent = blob.sentiment.polarity
        sent = sent - avg
        #sent_list.append((users_grouped.axes[0][i], sent))

        overlap_score = overlap_dict[users_grouped.axes[0][i]]
        score_list.append((users_grouped.axes[0][i], sim, keywords, sent, overlap_score))


    #sim_list = sorted(sim_list, key = lambda k: -k[1])
    #sent_list = sorted(sent_list, key = lambda k: -k[1])

    
    #sim_frame = pd.DataFrame(sim_list)
    #sent_frame = pd.DataFrame(sent_list)

    score_frame = pd.DataFrame(score_list)

    score_frame.columns = ['id', 'sims', 'keywords', 'sents', 'overlaps']

    factor = len(score_frame.overlaps)
    score_frame = pd.concat([score_frame, 2 * (factor // 3) * (.5 * score_frame.sents + score_frame.sims) + \
        (factor // 3) * score_frame.overlaps], 1)

    score_frame.columns = ['id','similarity', 'keywords', 'sentiment', 'overlaps', 'sums']


    score_frame = score_frame[['id', 'sums', 'keywords', 'similarity', 'sentiment', 'overlaps']]

    score_frame = score_frame.sort_values('sums', ascending = False)

    return score_frame
'''
def sentiment_scoring(business_reviews, user_reviews):
    
    Returns a DataFrame of sentiment scores

    inputs
        business_reviews - DataFrame
        user_reviews - DataFrame

    returns:
        score_frame - DataFrame
    
    grouped = business_reviews.groupby(business_reviews["business_id"])["text"].sum()
    l = []
    for text in grouped:
        blob = TextBlob(text)
        l.append(blob.sentiment.polarity)
    br_array = np.array(l)
    avg = np.mean(br_array)
    users_grouped = user_reviews.groupby(user_reviews["business_id"])["text"].sum()
    score_list = []
    for i in range(len(users_grouped.axes[0])):
        blob = TextBlob(users_grouped[i])
        score = blob.sentiment.polarity
        score = score - avg
        score_list.append((users_grouped.axes[0][i], score))
    
    score_list = sorted(score_list, key = lambda k: -k[1])
    score_frame = pd.DataFrame(score_list)

    return score_frame
'''
'''
def combine_scores(overlap_score, sim_score, sent_score):
    
    Combines the similarity score and sentiment score

    inputs
        sim_score - DataFrame
        sent_score - DataFrame
    returns 
        score_frame - DataFrame

    sorted_sims = sim_score.sort_values(0)
    sorted_sents = sent_score.sort_values(0)
    sorted_overlaps = overlap_score.sort_values(0)

    sorted_sents = sorted_sents.drop(0, 1)
    sorted_overlaps = sorted_overlaps.drop(0, 1)

    score_frame = pd.concat([sorted_sims, sorted_sents, sorted_overlaps], 1)
    score_frame = score_frame.fillna(0)
    score_frame.columns = ['id', 'sims', 'keywords', 'sents', 'overlaps']

    factor = len(score_frame.overlaps)
    score_frame = pd.concat([score_frame, 2 * (factor // 3) * (.5 * score_frame.sents + score_frame.sims) + \
        (factor // 3) * score_frame.overlaps], 1)

    
    score_frame.columns = ['id','similarity', 'keywords', 'sentiment', 'overlaps', 'sums']

    
    score_frame = score_frame[['id', 'sums', 'keywords', 'similarity', 'sentiment', 'overlaps']]

    score_frame = score_frame.sort_values('sums', ascending = False)

    return score_frame
    '''
'''
def scoring(business_reviews, user_reviews):
    
    Gets a DataFrame of restaurants and scores

    inputs
        business_reviews - DataFrame
        user_reviews - DataFrame

    returns
        scores - sorted DataFrame

    overlaps = count_intersections(user_reviews)
    sims, sents = get_scores(business_reviews, user_reviews)

    scores = combine_scores(overlaps, sims, sents)

    return scores
'''

# make sure there is a record of which restaurant goes with which document in doc list
# make sure that training docs are each a long string of all the reviews for a given restaurant

def get_names_and_addresses(sims, biz_data):
    '''
    Used code from PA3
    '''
    for x in sims:
        name = d[x[0]]

    pass

# KMeans clusering algorithm

