#! /usr/bin/python3
# randomCultFilm.py - Choose a randomcult film from
#               the wikipedia list of cult films

import random, shelve, pprint
with shelve.open('film') as filmShelf:
    while True :
        names = list(filmShelf.keys())
        choice = random.choice(names)
        print(f'The random film I choose is *** {choice} ***')
        pprint.pprint(filmShelf[choice])
        a = input(' Push Enter\n\n')
