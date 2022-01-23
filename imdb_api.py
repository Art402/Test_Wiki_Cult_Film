#! /usr/bin/python3
##imdb_api.py       adds some imdb metadata to the google
##                  sheet Wikipedia list of Cult Films

import logging
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
i = 0
for sheet_movie in list_of_lists :
    i+=1
    title, year, director = sheet_movie[0:3]
    logging.info(f'title, year, director {title, year, director}')
    imdb_movies = ia.search_movie(title)
    # Find the good movie in the search list
    try :
        for imdb_movie in imdb_movies:
            logging.info(f"imdb_movie['year'] {imdb_movie['year']}")
            if 'year' in imdb_movie.keys() and int(imdb_movie['year']) == int(year):
                end_movie = imdb_movie
                break
            else:
                continue
    except Exception as err:
        logging.info(f'''{title} not in search_movie() : {imdb_movies} \n
                     err : {err}''')
        end_movie = None
        continue
    
# TODO : Load every interesting infos from the imdb database film
    movie_list = [end_movie['smart long imdb canonical title'],
                  end_movie['year'],
                  end_movie['full-size cover url']]

    ia.update(end_movie, info=['main'])
    main_keys = ['imdbID',
                'original title',
                'genres',
                'runtimes',
                'countries',
                'language codes',
                'color info',
                'rating',
                'votes',
                'plot outline'
                 ]
    for key in main_keys:
        if key in end_movie.keys():
            movie_list.append(end_movie[key])
        else:
            movie_list.append(None)
            
    main_personkeys = ['director',
                       'composer'
                       ]
    for key in main_personkeys:
        if key in end_movie.keys():
            temp = []
            for person in end_movie[key]:
                temp.append(person['name'])
            movie_list.append(temp)
        else:
            movie_list.append(None)
    
    end_list.append(movie_list)
    
    logging.info(f'''end_list done. {movie_list}''')
    
# TODO : Update the Google sheet

    gc = gspread.oauth()
    worksheet = gc.open('Wiki Cult').sheet1
    worksheet.update('A2', f'[{movie_list}]')
    print('Done.')
