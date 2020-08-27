import sqlite3
import argparse
import time, datetime 

from bs4 import BeautifulSoup
from bs4.element import Comment

from helpers import is_path_correct
from DbCookieBanner import DbCookieBanner
from CookieBannerOptions import CookieBannerOptions


INSERT_STATEMENT = 'INSERT INTO cookie_options ' \
                    '(website, privacy_text, has_accept_btn, cta_accept, has_decline_btn, cta_decline, has_options_btn, cta_options, has_info_btn, cta_info) ' \
                    'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
SELECT_STATEMENT = 'SELECT * FROM cookies WHERE banner_exists = 1'

elements_to_flatten = ['span', 'p', 'b', 'i', 'u', 'html', 'body', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 
                       'label', 'strong', 'section', 'ul', 'li', 'font', 'table', 'tr', 'td', 'th', 'thead', 
                       'tbody', 'tfoot', 'aside', 'center', 'form', 'em', 'small', 'ol', 'select', 'option', 
                       'fieldset', 'nav', 'header', 'footer']
elements_to_remove = ['a', 'button', 'img', 'script', 'svg', 'input', 'br', 'style', 'head', 'hr']


def file_to_set(file_path):
    with open(file_path, 'r') as f:
        return set(map(lambda l: str. rstrip(l), f.readlines()))


def extract_privacy_text_from_cookie_banner(soup):
    cb = soup
    banned_elements = cb.find_all(elements_to_remove) + \
                      cb.findAll(text=lambda text:isinstance(text, Comment))

    for element in banned_elements:
        element.extract()

    for match in cb.findAll(elements_to_flatten):
        match.replaceWithChildren()

    return cb.prettify().replace('\n', ' ').replace('\r', '')


def extract_privacy_options_from_cookie_banner(soup):
    cb = soup
    actions = cb.find_all(['a', 'button'])
    cookie_banner = CookieBannerOptions()

    for action in actions:
        if action.string is not None:
            action_str = str.strip(str.lower(action.string))

            if action_str in terms_accept:
                cookie_banner.has_accept_btn = 1
                cookie_banner.cta_accept = action_str
            elif action_str in terms_decline:
                cookie_banner.has_decline_btn = 1
                cookie_banner.cta_decline = action_str
            elif action_str in terms_options:
                cookie_banner.has_options_btn = 1
                cookie_banner.cta_options = action_str
            elif action_str in terms_info:
                cookie_banner.has_info_btn = 1
                cookie_banner.cta_info = action_str
    return cookie_banner


def save_cookie_banner_options_to_db(cookie_banner_options):
    sqlite_cursor.execute(INSERT_STATEMENT, cookie_banner_options.as_tuple())
    

if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description='Process values for the Cookie Banner Options parser.')
    parser.add_argument('--db', type=is_path_correct, default='./outp/cookies.sqlite')
    parser.add_argument('--terms-accept', type=is_path_correct, default='./cb_terms/terms_accept.txt')
    parser.add_argument('--terms-decline', type=is_path_correct, default='./cb_terms/terms_decline.txt')
    parser.add_argument('--terms-options', type=is_path_correct, default='./cb_terms/terms_options.txt')
    parser.add_argument('--terms-info', type=is_path_correct, default='./cb_terms/terms_info.txt')
    args = parser.parse_args()

    sqlite_connection = sqlite3.connect(args.db)
    sqlite_cursor = sqlite_connection.cursor()
    sqlite_cursor.execute(SELECT_STATEMENT)
    rows = sqlite_cursor.fetchall()

    terms_accept = file_to_set(args.terms_accept)
    terms_decline = file_to_set(args.terms_decline)
    terms_options = file_to_set(args.terms_options)
    terms_info = file_to_set(args.terms_info)

    for row in rows:
        db_cookie_banner = DbCookieBanner(row)
        soup = BeautifulSoup(db_cookie_banner.html, 'lxml')

        cookie_banner = extract_privacy_options_from_cookie_banner(soup)
        cookie_banner.privacy_text = extract_privacy_text_from_cookie_banner(soup)
        cookie_banner.website = db_cookie_banner.website
        save_cookie_banner_options_to_db(cookie_banner)
        
        print('{} --- Accept: {} --- Decline: {} --- Options: {} --- Info: {}'
            .format(cookie_banner.website, cookie_banner.has_accept_btn, cookie_banner.has_decline_btn, cookie_banner.has_options_btn, cookie_banner.has_info_btn))

    sqlite_connection.commit()
    sqlite_connection.close()

    elapsed_time = time.time() - start_time
    print()
    print('Time Elapsed: {}'.format(datetime.timedelta(seconds=elapsed_time)))
