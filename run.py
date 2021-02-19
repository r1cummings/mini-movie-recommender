import sys
sys.path.insert(0, 'src') #getting the directory of our etl file in order to import etl since it is in a different folder
from pipeline import generate_reviews_matrix, get_top_3, get_input


if __name__ ==  '__main__':
    
    your_fav_movies = get_input()
    your_fav_movies = your_fav_movies.split(';')
    movie_lst = [i.lstrip() for i in your_fav_movies]
    
    corrMatrix = generate_reviews_matrix()
    get_top_3(corrMatrix, movie_lst)