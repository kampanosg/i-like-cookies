
import os
import argparse
import signal
import sqlite3
import multiprocessing as mp
import time
import datetime

from reppy.robots import Robots
from ParserTimeoutException import ParserTimeoutException
from helpers import is_path_correct

from pprint import pprint

INSERT_RECORD_STATEMENT = 'INSERT INTO robots_compliance (website_id, robots_allows_crawling) VALUES (?, ?);'


def cookie_parser_timeout_handler(signum, frame):
    raise ParserTimeoutException('End of time exception')


def write_crawl_status_to_db(statuses):
    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()
    cursor.executemany(INSERT_RECORD_STATEMENT, statuses)
    conn.commit()
    conn.close()


def get_crawl_status(url):
    robots_url = os.path.join(url, 'robots.txt')
    robot = Robots.fetch(robots_url)
    agent = robot.agent('msc-cookie-monster')
    try:
        return 1 if agent.allowed(url) else 0
    except Exception as _:
        return -1


def check_crawl_status_and_write_to_db(row):
    status = []
    website_id = row[0]
    website_url = row[1]

    print('Checking {} --- '.format(website_url), end=' ')

    signal.signal(signal.SIGALRM, cookie_parser_timeout_handler)
    signal.alarm(20)
    try:
        can_crawl = get_crawl_status(website_url)
    except (ParserTimeoutException, Exception) as _:
        can_crawl = -1

    signal.alarm(0)
    status.append((website_id, can_crawl))
    print(can_crawl)
    return status

if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description='Process values for the Robot.txt parser.')
    parser.add_argument('--db', type=is_path_correct, default='./outp/cookies.sqlite')
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    cursor = conn.cursor()
    cursor.execute('SELECT website_id, url FROM websites')
    urls = cursor.fetchall()
    conn.commit()
    conn.close()

    pool = mp.Pool(mp.cpu_count())
    statuses = pool.map(check_crawl_status_and_write_to_db, urls)
    statuses = [item for sublist in statuses for item in sublist]

    write_crawl_status_to_db(statuses)

    elapsed_time = time.time() - start_time
    print()
    print('Time Elapsed: {}'.format(datetime.timedelta(seconds=elapsed_time)))
