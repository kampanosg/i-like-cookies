import os
import sqlite3
import subprocess
import requests

sqlite_connection = sqlite3.connect('./outp/cookies_uk.sqlite')
sqlite_cursor = sqlite_connection.cursor()

sqlite_cursor.execute('SELECT id, hash, website, banner_exists, html FROM cookies WHERE banner_exists = 0')
rows = sqlite_cursor.fetchall()

index = 0
total_entries = len(rows)

for row in rows:
    entry_id = row[0]
    entry_hash = row[1]
    entry_url = row[2]
    entry_has_banner = row[3]
    entry_html = row[4]

    index += 1
    print()
    print('{}/{} --- {} --- (id = {})'.format(index, total_entries, entry_url, entry_id))

    if '.me.uk' in entry_url:
        print('[!] Not checking .me.uk domains - They are fake')
        continue

    if '.gov.uk' in entry_url:
        print('[!] Not checking .gov.uk domains')
        continue

    if '.nhs.uk' in entry_url:
        print('[!] Not checking .gov.uk domains')
        continue

    try:
        r = requests.get(entry_url, timeout=6)
    except Exception as e:
        print('[!] {}'.format(e))
        continue

    if r.status_code != 200:
        print('[!] Website is unreachable')
        continue

    if 'cookies' in r.text:
        print('[!] Found cookie in the html. Please check: ', end=' ')
        choice = int(input())
        if choice == -1:
            break
        continue

    print('[!] Cookie banner not found')
    
