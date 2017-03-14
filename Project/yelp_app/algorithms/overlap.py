from math import sqrt, erf, log


# weighting function


#lognormal cdf function
#ended up not using because it makes all values the same 
def weighting(x, u, s):
    '''
    Weights the values

    inputs:
        x - float
        u - mean, float
        s - std deviation, float
    returns:
        float
    '''
    return  (1 / 2) * (1 + erf((x - u)/(log(s) * sqrt(2))))

# counts

def count_intersections(user_reviews):
    '''
    Counts the number of times a restaurant appears in the user_reviews
    and normalizes it

    inputs:
        DataFrame

    returns:
        dictionary
    '''

    count_dict = {}
    for i_d in user_reviews["business_id"]:
        if i_d not in count_dict:
            count_dict[i_d] = 1
        else:
            count_dict[i_d] += 1

    # normalizes the scores 
    for key in count_dict:
        count_dict[key] = count_dict[key] / len(user_reviews["business_id"])
    
    
    return count_dict

