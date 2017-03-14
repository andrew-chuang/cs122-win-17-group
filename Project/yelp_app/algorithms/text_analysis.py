import sqlite3
import pandas as pd
import numpy as np
import gensim
from collections import defaultdict 
from textblob import TextBlob
from . import overlap

# some of the work from LSI was taken from the tutorials
# here: https://radimrehurek.com/gensim/tutorial.html

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
    vectors. I referenced this part of the tutorial:
    http://radimrehurek.com/gensim/tut1.html
    inputs:
         list of strings
    returns:
         corpora
    '''
    # creates a list of works to get rid of
    stoplist = set(['a', 'and', 'for', 'in', 'of', 'the', 'to'])
    text_lists = [[word for word in document.lower().split() \
    if word not in stoplist] for document in doc_list]

    freq = defaultdict(int)
    # creates frequency dictionary
    for text in text_lists:
        for k in text:
            freq[k] += 1
    # small list of terms I thought would be important
    attribute_list = ["service", "quality", "romantic", "atmosphere"]
    # eliminates words that only appear once or are in the attributes list
    text_list2 = [[k for k in text if freq[k] > 1 and k not in attribute_list] for text in text_lists]
    dictionary = gensim.corpora.Dictionary(text_lists)
    corp = [dictionary.doc2bow(text) for text in text_list2]
    return corp, dictionary

def apply_lsi(corp, dictionary):
    '''
    Applies latent semantic indexing to a corpora given a dictionary 
    Used this section of the tutorial:
    http://radimrehurek.com/gensim/tut2.html
    inputs
        corp - corpora
        dictionary - dict

    returns:   
        lsi = LsiModel
        corpus_lsi - transformed corpus
    '''
    # creates term frequency–inverse document frequency
    tfidf = gensim.models.TfidfModel(corp)
    # transforms the corpus of documents
    c_tfidf = tfidf[corp]
    lsi = gensim.models.LsiModel(tfidf[c_tfidf], id2word=dictionary, num_topics=50)
    corpus_lsi = lsi[c_tfidf]
    return lsi, corpus_lsi

def similarity_scoring(training_docs, test_doc):
    '''
    Scores a string against a list of training strings
    Referenced this section of the tutorial:
    http://radimrehurek.com/gensim/tut3.html
    inputs:
        training_docs - list of strings
        test_doc - string

    returns:
        float
    '''
    # remember to get rid of special characters
    corp, dictionary = tokenize_to_vect(training_docs)
    lsi, c_lsi = apply_lsi(corp, dictionary)
    v = dictionary.doc2bow(test_doc.lower().split())
    vec_lsi = lsi[v]
    ind = gensim.similarities.MatrixSimilarity(lsi[corp])

    # gets the similarity score for each document
    sim = ind[vec_lsi]
    score = 0
    for s in sim:
        score += s

    # averages 
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
    # gets dictionary with overlap scores
    overlap_dict = overlap.count_intersections(user_reviews)

    # gets baseline sentiment score
    l= []
    for text in business_reviews.text:
        blob = TextBlob(text)
        l.append(blob.sentiment.polarity)
    br_array = np.array(l)
    avg = np.mean(br_array)

    # groups user reviews by restaurant
    users_grouped = user_reviews.groupby(user_reviews["business_id"])["text"].sum()
    
    # gets list of tuples with scores and keywords
    score_list = []
    for i in range(len(users_grouped)):
        # similarity scoring
        sim = similarity_scoring(business_reviews.text, users_grouped[i])
        # selects only reviews for which keywords can be generated
        if len(users_grouped[i]) > 450:
            keywords = gensim.summarization.keywords(users_grouped[i])
            keywords = keywords.split('\n')
        else:
            keywords = "Review is too small for keywords"  

        overlap_score = overlap_dict[users_grouped.axes[0][i]]

        # does sentiment analysis and subtracts baseline
        blob = TextBlob(users_grouped[i])
        sent = blob.sentiment.polarity
        sent = sent - avg


        score_list.append((users_grouped.axes[0][i], \
            sim, keywords, sent, overlap_score))


    score_frame = pd.DataFrame(score_list)

    score_frame.columns = ['id', 'sims', 'keywords', 'sents', 'overlaps']

    # weights the scores by the number of restaurants
    factor = len(score_frame.overlaps)
    score_frame = pd.concat([score_frame, 2 * (factor // 3) * \
        (.5 * score_frame.sents + score_frame.sims) + \
        (factor // 3) * score_frame.overlaps], 1)

    score_frame.columns = ['id','similarity', 'keywords', 'sentiment', 'overlaps', 'sums']

    score_frame = score_frame[['id', 'sums', 'keywords', 'similarity', 'sentiment', 'overlaps']]

    score_frame = score_frame.sort_values('sums', ascending = False)

    return score_frame



# unused functions that were mostly incorporated into the above functions
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


