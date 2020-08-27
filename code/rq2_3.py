import argparse
import sqlite3

from helpers import is_path_correct

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--db', default='./outp/cookies.sqlite', type=is_path_correct)
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    cur = conn.cursor()

    cur.execute("SELECT has_accept_btn, has_decline_btn, has_options_btn, has_info_btn FROM cookie_options")
    rows = cur.fetchall()

    total_options = 0
    total_rows = len(rows)
    categories = {
        'accept': 0,
        'reject': 0,
        'info': 0,
        'options': 0
    }

    for row in rows:
        if row[0] == 1:
            total_options += 1
            categories['accept'] += 1
        
        if row[1] == 1:
            total_options += 1
            categories['reject'] += 1
        
        if row[2] == 1:
            total_options += 1
            categories['options'] += 1
        
        if row[3] == 1:
            total_options += 1
            categories['info'] += 1

    conn.close()

    print('Total options found: {}'.format(total_options))
    print('Total banners prorcessed: {}'.format(total_rows))
    print('Average options per banner: {}'.format(total_options / total_rows))
    print()

    print('Total affirmative options: {}'.format(categories['accept']))
    print('Total non-affirmative options: {}'.format(categories['reject']))
    print('Total managerial options: {}'.format(categories['options']))
    print('Total informational options: {}'.format(categories['info']))