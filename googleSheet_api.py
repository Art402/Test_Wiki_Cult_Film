#! /usr/bin/python3
# googleSheet_api.py - put the loaded shelf in to a google sheet



import shelve, gspread

# Download the list from the shelf dictionnary

with shelve.open('film') as filmShelf:
    gspread_list = [['Title','Year','Director']]
    for name in list(filmShelf.keys()):
        gspread_list.append([filmShelf[name]['Title'],
                             filmShelf[name]['Year'],
                             filmShelf[name]['Director']
                             ])


print(f'gspread_list done. len = {len(gspread_list)}. Uploading to Gsheet.')

# Upload the list in the google sheet

gc = gspread.oauth()
worksheet = gc.open('Wiki Cult').sheet1
worksheet.update(f'A2', gspread_list)
print('Done.')
