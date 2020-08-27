import csv
import argparse
import sqlite3
import time
import datetime

from helpers import is_path_correct


def csv_to_set(csv_path, url_index=0, rank_index=-1):
    with open(csv_path) as f:
        rows = csv.reader(f, delimiter=',')
        return set(map(lambda x: x[url_index], rows))


def save_urls_to_db(db_path, urls):
    sqlite_connection = sqlite3.connect(db_path)
    sqlite_cursor = sqlite_connection.cursor()

    for url in urls:
        url = 'http://www.' + url
        sqlite_cursor.execute('INSERT OR IGNORE INTO websites (url) VALUES (?)', (url, ))

    sqlite_connection.commit()
    sqlite_connection.close()


def parse_url_lists_and_update_db(db_path, path_tranco, path_topgr, path_dead, tld='.gr'):
    tranco = csv_to_set(path_tranco, url_index=1)
    tranco_gr = set(url for url in tranco if url.endswith(tld))

    topgr = csv_to_set(path_topgr)
    dead = csv_to_set(path_dead)

    tranco_intersection_topgr = tranco.intersection(topgr)
    tranco_gr_union_with_rest = tranco_gr.union(tranco_intersection_topgr)
    urls = tranco_gr_union_with_rest.difference(dead)

    print('Total Tranco Websites: {}'.format(len(tranco)))
    print('Total Tranco {} Websites: {}'.format(tld, len(tranco_gr)))
    print('Total TopGR Websites: {}'.format(len(topgr)))
    print()

    print('Total Dead Websites: {}'.format(len(dead)))
    print()

    print('Total Websites to process: {}'.format(len(urls)))

    save_urls_to_db(db_path, urls)


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description='Process values for the Robot.txt parser.')
    parser.add_argument('--db', default='./outp/cookies.sqlite', type=is_path_correct)
    parser.add_argument('--tranco', default='./lists/list-tranco.csv', type=is_path_correct)
    parser.add_argument('--topgr', default='./lists/list-topgr.csv', type=is_path_correct)
    parser.add_argument('--dead', default='./lists/list-dead.csv', type=is_path_correct)
    parser.add_argument('--tld', default='.gr')
    args = parser.parse_args()

    parse_url_lists_and_update_db(args.db, args.tranco, args.topgr, args.dead, tld=args.tld)

    elapsed_time = time.time() - start_time
    print()
    print('Time Elapsed: {}'.format(datetime.timedelta(seconds=elapsed_time)))
