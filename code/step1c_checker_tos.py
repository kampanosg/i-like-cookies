import sqlite3
import argparse
import requests
import time, datetime 
import multiprocessing as mp

from bs4 import BeautifulSoup
from bs4.element import Comment
from helpers import is_path_correct


TOS_PHRASES = {u'ΟΡΟΙ ΧΡΗΣΗΣ', u'Όροι Χρήσης', u'Όροι χρήσης', u'ΌΡΟΙ ΧΡΉΣΗΣ', u'όροι χρήσης',
               'Terms of service', 'Terms of Service', 'TERMS OF SERVICE',
               'Terms of use', 'Terms of Use', 'TERMS OF USE'}

SELECT_STATEMENT = '''
    SELECT id, url
    FROM websites JOIN robots_compliance AS robots USING(website_id)
    WHERE robots.robots_allows_crawling = 1
'''
INSERT_RECORD_STATEMENT = 'INSERT INTO tos_compliance (website_id, tos_found, tos_allows_crawling) VALUES (?, ?, ?);'


def write_tos_crawl_status_to_db(statuses):
    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()
    cursor.executemany(INSERT_RECORD_STATEMENT, statuses)
    conn.commit()
    conn.close()


def has_personal_use_only_clause(tos_url):
    try:
        r = requests.get(tos_url, timeout=6)
        page_source = r.text
        return ('αυστηρά για προσωπική χρήση' in page_source) or \
            ('μόνο για προσωπική χρήση' in page_source) or \
            ('personal use only' in page_source) or \
            ('only for personal use' in page_source)
    except requests.exceptions.RequestException as _:
        pass
    return -1


def get_tos_url(website):
    try:
        r = requests.get(website, timeout=6)
        soup = BeautifulSoup(r.text, 'lxml')
        for a in soup.find_all('a'):
            cta = a.text.strip()
            if cta in TOS_PHRASES:
                return a.get('href')
    except requests.exceptions.RequestException as _:
        pass
    return None


def get_tos_crawl_status(website):
    tos_found = 0
    tos_crawl_status = 1
    tos_url = get_tos_url(website)

    if tos_url is not None:
        tos_found = 1
        if has_personal_use_only_clause(tos_url):
            tos_crawl_status = 0

    return tos_found, tos_crawl_status

def parse_and_update_tos_crawl_status(row):
    status = []
    website_id = row[0]
    website_url = row[1]

    print('{} ---'.format(website_url), end=' ')

    tos_found, tos_crawl_status = get_tos_crawl_status(website_url)
    status.append((website_id, tos_found, tos_crawl_status))
    print('TOS found: {} --- Can crawl: {}'.format(tos_found, tos_crawl_status))
    return status 
    

if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description='Process values for the Cookie Banner Options parser.')
    parser.add_argument('--db', type=is_path_correct, default='./outp/cookies.sqlite')
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()
    cursor.execute(SELECT_STATEMENT)
    urls = cursor.fetchall()
    conn.commit()
    conn.close()

    pool = mp.Pool(mp.cpu_count())
    statuses = pool.map(parse_and_update_tos_crawl_status, urls)
    statuses = [item for sublist in statuses for item in sublist]
    write_tos_crawl_status_to_db(statuses)

    elapsed_time = time.time() - start_time
    print()
    print('Time Elapsed: {}'.format(datetime.timedelta(seconds=elapsed_time)))