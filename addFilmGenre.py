#! /usr/bin/python3
# addFilmGenre.py - Adds the film genre to the shelf.

import shelve, requests, bs4
import logging
logging.basicConfig(filename = 'rottenLOG.txt', level=logging.DEBUG, format='''%(asctime)s -  %(levelname)s
-  %(message)s''')
logging.debug('Start of program')


with shelve.open('film') as filmShelf:

    genreList = []
    numberLeft = len(list(filmShelf.keys()))
        
    for name in list(filmShelf.keys()):
        logging.debug(f'''filmShelf[name]{filmShelf[name]}\n
                        number left {numberLeft}''')
        print(f'''filmShelf[name]{filmShelf[name]}\n
                        number left {numberLeft}''')
        numberLeft-=1


        
        filmDict = filmShelf[name]
        title = '_'.join(filmDict['Title'].lower().split(' '))

        try:
            url = 'https://www.rottentomatoes.com/m/' + title
            res = requests.get(url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')

            scoreboard__info = soup.select('.scoreboard__info')[0].getText()
            year, genres, duration = scoreboard__info.split(', ')
            genreList = genres.split('/')
            
            logging.debug(f'year, genres, duration {year, genreList, duration}')           
            if filmDict['Year'] == year:
                filmDict['Genre'] = genreList
                filmDict['Duration'] = duration
                filmShelf[name] = filmDict
                logging.debug(f'filmShelf[name]{filmShelf[name]}\n')
                print(f'filmShelf[name]{filmShelf[name]}\n')
                
                for i in filmDict['Genre']:
                    if i not in genreList:
                        genreList.append(i)
            

        except Exception as err:
            logging.debug('An exception happened: ' + str(err))
    logging.debug(f'\n\n###\ngenreList{genreList}\n')
print('Done.')
