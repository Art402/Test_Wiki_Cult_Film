#! /usr/bin/python3
##imdb_api.py       adds some imdb metadata to the google
##                  sheet Wikipedia list of Cult Films

import logging
logging.basicConfig(level=logging.INFO, format='''%(asctime)s -  %(levelname)s
-  %(message)s''')
logging.info('Start of program')



def load_wiki_list_of_cult_films(gc):
    # TODO : Load films name year and director from the google sheet.
    
    worksheet = gc.open('Wiki Cult').sheet1
    wiki_list_of_cult_films = worksheet.get_all_values()
    return(wiki_list_of_cult_films)



def search_corresponding_imdb_movie(wiki_movie,ia):
    # TODO : For each film find the corresponding film in the imdb database
    title, year, director = wiki_movie[0:3]
    logging.info(f'title, year, director {title, year, director}')
    imdb_movies = ia.search_movie(title)
    # Find the good movie in the search list
    good_imdb_movie = None
    try :
        for imdb_movie in imdb_movies:
            logging.info(f"imdb_movie['year'] {imdb_movie['year']}")
            if 'year' in imdb_movie.keys() and int(imdb_movie['year']) == int(year):
                good_imdb_movie = imdb_movie
                break
            else:
                continue
    except Exception as err:
        logging.info(f'''{title} not in search_movie() : {imdb_movies} \n
                     err : {err}''')
    return(good_imdb_movie)
    

def load_list(good_imdb_movie, ia):
# TODO : Load every interesting infos from the imdb database film
    imdb_list = [good_imdb_movie['smart long imdb canonical title'],
                 good_imdb_movie['year'],
                 good_imdb_movie['full-size cover url']]

    ia.update(good_imdb_movie, info=['main'])
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
        if key in good_imdb_movie.keys():
            imdb_list.append(str(good_imdb_movie[key]))
        else:
            imdb_list.append(None)
            
    main_personkeys = ['director',
                       'composer'
                       ]
    for key in main_personkeys:
        if key in good_imdb_movie.keys():
            temp = []
            for person in good_imdb_movie[key]:
                temp.append(person['name'])
            imdb_list.append(str(temp))
        else:
            imdb_list.append(None)
    logging.info(f'''imdb_list done. {imdb_list}''')
    
    return(imdb_list)
    
    
    

def update_gcp(imdb_list, gc, i):
# TODO : Update the Google sheet
    spreadsheet = gc.open('Wiki Cult')
    worksheet = spreadsheet.worksheet('imdb_api')
    worksheet.update(f'A{i}', [imdb_list])


def main():
    import gspread
    gc = gspread.oauth()
    wiki_list_of_cult_films = load_wiki_list_of_cult_films(gc)
    import imdb
    ia = imdb.IMDb()
    i = 0
    n = len(wiki_list_of_cult_films)
    for wiki_movie in wiki_list_of_cult_films :
        i+=1
        good_imdb_movie = search_corresponding_imdb_movie(wiki_movie,ia)
        if good_imdb_movie == None :
            imdb_list = wiki_movie+['IMDB NOT FOUND']
        else : 
            imdb_list = load_list(good_imdb_movie, ia)
        update_gcp(imdb_list, gc, i)
        logging.info(f'''
************************
Done Uploading {imdb_list[0:3]}
************************
film n°{i} / {n}
************************
''')

if __name__=='__main__':
    main()
