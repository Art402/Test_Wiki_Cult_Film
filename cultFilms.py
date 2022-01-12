#! /usr/bin/python3
# cultFilms.py - Downloads the wikipedia list of cult films
#               And put it into a shelve.


import requests, os, bs4, shelve, time


baseUrl = 'https://en.wikipedia.org/wiki/List_of_cult_films'
res = requests.get(baseUrl)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, 'html.parser')
pageList = soup.select('div.hlist ul li a')

for a in pageList:
    t1 = time.perf_counter()
    url = 'https://en.wikipedia.org/' + a.get('href')   # alphabetical letter film list

    # Download the alphabetical letter page
    print(f'Downloading page {a.get("href")}.')
    res = requests.get(url)
    res.raise_for_status()
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    # Find the URL of the film div.
    filmTable = soup.select('table tbody tr')
    
    with shelve.open('film') as filmShelf:
        # Adds film dict into the shelf        
        for film in filmTable[1:]:
            filmText = film.getText().split('\n')[1:4]
            filmDico = {'Title':filmText[0],
                        'Year':filmText[1],
                        'Director':filmText[2]
                        }
            # print(f'Adding {filmDico["Title"]} to the shelve')
            filmShelf[filmDico['Title']] = filmDico
    print(f'Page fully loaded in shelf, it took {round(time.perf_counter()-t1,2)}sec')



print('Done.')
