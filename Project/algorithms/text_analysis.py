import sqlite3
import pandas as pd
import json
import operator as op
import numpy as np
import gensim
from collections import defaultdict 

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
    d = {}
    i = 0
    for i_d in biz_data["business_id"]:
        d[i] = i_d
        i += 1
    return d

def tokenize_to_vect(doc_list):
    '''
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
    '''
    tfidf = gensim.models.TfidfModel(corp)
    c_tfidf = tfidf[corp]
    lsi = gensim.models.LsiModel(c_tfidf, id2word=dictionary, num_topics=50)
    corpus_lsi = lsi[c_tfidf]
    return lsi, corpus_lsi

def list_to_test(test_corp, lsi):
    '''
    '''
    return lsi[test_corp]

def similarity_scoring(training_docs, test_doc):
    '''
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
    
def get_similarities(training_docs, target_reviews):
    '''
    '''
    score_list = []
    for i in range(len(target_reviews)):
        score = similarity_scoring(training_docs, target_reviews[i])
        score_list.append((i, score))

    return score_list
# make sure there is a record of which restaurant goes with which document in doc list
# make sure that training docs are each a long string of all the reviews for a given restaurant

def get_names_and_addresses(sims, biz_data):
    '''
    Used code from PA3
    '''
    for x in sims:
        name = d[x[0]]

    pass
# LDA