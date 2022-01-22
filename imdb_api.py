#! /usr/bin/python3
##imdb_api.py       adds some imdb metadata to the google
##                  sheet Wikipedia list of Cult Films


logging.basicConfig(level=logging.INFO, format='''%(asctime)s -  %(levelname)s
-  %(message)s''')
logging.info('Start of program')


# TODO : Load films name year and director from the google sheet.
import gspread
gc = gspread.oauth()
worksheet = gc.open('Wiki Cult').sheet1
list_of_lists = worksheet.get_all_values()
end_list = []
# TODO : For each film find the corresponding film in the imdb database

import imdb
ia = imdb.IMDb()

for sheet_movie in list_of_lists :
    title, year, director = sheet_movie[0:3]
    imdb_movies = ia.search_movie(title)
    # Verify the first movie of the search is the good one
    try:
        for imdb_movie in imdb_movies:
            if imdb_movie['year'] == year:
                end_movie = imdb_movie
                
            else:
                continue
    except Exception as err:
        logging.info(f'{sheet_movie} not in search_movie() : {imdb_movies}')
        end_movie = None
    
# TODO : Load every interesting infos from the imdb database film
    smart_long_imdb_canonical_title = end_movie['smart long imdb canonical title']
    full-size_cover_url = end_movie['full-size cover url']
    
    
    end_list.append([
        ,
        ,
        ])

# TODO : Update the Google sheet
