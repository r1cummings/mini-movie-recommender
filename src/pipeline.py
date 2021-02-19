import pandas as pd
import numpy as np
#import sys
#sys.path.append('~/Users/ryan/anaconda3/lib/python3.7/site-packages')

def get_input():
    your_fav_movies = input("\n\nTo find the list of movies I can read go to data/movie_names.csv and choose all your favorites (include exactly how it is shown)\n\n\n\nWhat is/are your all time favorite movie(s)? (seperate with ;) \N{movie camera}\n")
    return your_fav_movies

def get_ratings(movie_lst):
    x = np.array([5])
    return pd.Series(data = np.repeat(x, [len(movie_lst)], axis=0), index = movie_lst)

def generate_reviews_matrix():
    r_cols = ['user_id', 'movie_id', 'rating']
    ratings = pd.read_csv('data/u.data', sep='\t', names=r_cols, usecols=range(3), encoding="ISO-8859-1")

    m_cols = ['movie_id', 'title']
    movies = pd.read_csv('data/u.item', sep='|', names=m_cols, usecols=range(2), encoding="ISO-8859-1")

    ratings = pd.merge(movies, ratings)


    ratings['title'] = [i.replace('(','').replace(')','') for i in ratings['title'].values]

    user_ratings = ratings.pivot_table(index=['user_id'],columns=['title'],values='rating')


    corrMatrix = user_ratings.corr(method='pearson', min_periods=100)
    return corrMatrix

def get_top_3(corrMatrix, movie_lst):
    print("\n\n\nNice! I don't know if I've seen those. I'll have to check them out!")
    myRatings = get_ratings(movie_lst)
    simCandidates = pd.Series()
    for i in range(0, len(myRatings.index)):
        # Retrieve similar movies to this one that was rated
        sims = corrMatrix[myRatings.index[i]].dropna()
        # Now scale its similarity by how well I rated this movie
        sims = sims.map(lambda x: x * myRatings[i])
        # Add the score to the list of similarity candidates
        simCandidates = simCandidates.append(sims)

    simCandidates.sort_values(inplace = True, ascending = False)
    simCandidates = simCandidates.groupby(simCandidates.index).sum()
    simCandidates.sort_values(inplace = True, ascending = False)
    filteredSims = simCandidates.drop(myRatings.index)
    
    
    print('\nFor you, the top 3 movies I recommend are:\n')

    print('\n'.join(list(filteredSims.index[0:3].values)))
    print('\n')
    return