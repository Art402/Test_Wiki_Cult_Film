#! /usr/bin/python3
# film_gspread.py - Downloads the wikipedia list of cult films
#               And put it into a shelve, then to a google sheet



import shelve, gspread

with shelve.open('film') as filmShelf:
    gspread_list = []
    for name in list(filmShelf.keys()):
        gspread_list.append([filmShelf[name]['Title'],
                             filmShelf[name]['Year'],
                             filmShelf[name]['Director']
                             ])


print(f'gspread_list done. len = {len(gspread_list)}. Uploading to Gsheet.')


gc = gspread.oauth()
worksheet = gc.open('Wiki Cult').sheet1
worksheet.update(f'A2', gspread_list)
print('Done.')
