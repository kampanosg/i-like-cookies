
import os
import sqlite3
import subprocess

sqlite_connection = sqlite3.connect('./outp/cookies_uk.sqlite')
sqlite_cursor = sqlite_connection.cursor()

sqlite_cursor.execute('SELECT id, hash, website, banner_exists, html FROM cookies WHERE banner_exists = 0')
rows = sqlite_cursor.fetchall()

index = 0
total_entries = len(rows)


def update_db_entry(val_id, val):
    sqlite_cursor.execute('UPDATE cookies SET banner_exists = ? WHERE id = ?', (val, val_id))
    sqlite_connection.commit()


for row in rows:
    entry_id = row[0]
    entry_hash = row[1]
    entry_url = row[2]
    entry_has_banner = row[3]
    entry_html = row[4]

    index += 1
    print('{}/{}:'.format(index, total_entries), end=' ')

    if 'virginmedia.com' in entry_url:
        print('URL was virgin media. Will mark website as without banner')
        update_db_entry(entry_id, 0)
        continue

    print(entry_html)

    if entry_has_banner == 0:
        print('{} --- NO COOKIE BANNER --- Correct:'.format(entry_url), end=' ')
    else:
        print('{} --- YES COOKIE BANNER --- Correct:'.format(entry_url), end=' ')

    try:
        user_choice = int(input())
        if user_choice == -1:
            break
            
        elif user_choice != 1:
            update_db_entry(entry_id, -1)
    except:
        continue

sqlite_connection.close()
