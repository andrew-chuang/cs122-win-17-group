import sqlite3
import pandas as pd
import json
import operator as op
import numpy as np
import gensim
from collections import defaultdict
# lsa stuff
 

# include sql calls for text data, should return a list where each entry is the text of a review


def tokenize_to_vect(doc_list):
    '''
    inputs:
         list of strings
    returns:
         corpora
    '''
    stoplist = set('for a of the and to in'.split())
    text_lists = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
    freq = defaultdict(int)
    for text in test_lists:
        for k in text:
            freq[k] += 1
    attribute_list = ["service", "quality", "romantic", "atmosphere"]
    text_list2 = [[k for k in text if frequency[token] > 1 and k not in attribute_list] for text in texts]
    dictionary = gensim.corpora.Dictionary(texts)
    corp = [dictionary.doc2bow(text) for text in text_list2]
    return corp

def apply_lsi(corp):
    '''
    '''
    tfidf = models.TfidfModel(corp)
    c_tfidf = tfidf[corpus]
    lsi = models.LsiModel(c_tfidf, id2word=dictionary, num_topics=50)
    corpus_lsi = lsi[c_tfidf]
    return lsi, corpus_lsi

def list_to_test(test_corp, lsi):
    '''
    '''
    return lsi[test_corp]

def similarity_scoring(training_docs, test_doc):
    '''
    '''
    corp = tokenize_to_vect(training_docs)
    lsi, c_lsi = apply_lsi(corp)
    v = dictionary.doc2bow(test_doc.lower().split())
    vec_lsi = lsi[vec_bow]
    ind = similarities.MatrixSimilarity(lsi[corpus])
    sim = index[vec_lsi]
    sorted_sims = sims = sorted(enumerate(sims), key=lambda item: -item[1])
    return sorted_sims
    

    
