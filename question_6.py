import requests_with_caching
import json

def get_movies_from_tastedive(title):
    endpoint = 'https://tastedive.com/api/similar'
    param = {}
    param['q'] = title
    param['limit'] = 5
    param['type'] = 'movies'

    this_page_cache = requests_with_caching.get(endpoint, params=param)
    return json.loads(this_page_cache.text)

def extract_movie_titles(dict1):
    return ([x['Name'] for x in dict1['Similar']['Results']])

def get_related_titles(movie_lst):
    lst = []
    for movie in movie_lst:
        lst.extend(extract_movie_titles(get_movies_from_tastedive(movie)))
    return list(set(lst))

def get_movie_data(title):
    endpoint = 'http://www.omdbapi.com/'
    param = {}
    param['t'] = title
    param['r'] = 'json'
    dis_page_cache = requests_with_caching.get(endpoint, params=param)

    return json.loads(dis_page_cache.text)

print(get_movie_data("Black Panther")['Ratings'][1])

def get_movie_rating(dict1):
    tomatoes = dict1['Ratings']
    for tomato in tomatoes:
        if tomato['Source'] == 'Rotten Tomatoes':
            return int(tomato['Value'][:-1])
    return 0

def get_sorted_recommendations(movie_lst):
    dict2 = {}
    for title in get_related_titles(movie_lst):
        dict2[title] = get_movie_rating(get_movie_data(title))
    return [x[0] for x in sorted(dict2.items(), key=lambda item: (item[1], item[0]), reverse=True)]

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])

