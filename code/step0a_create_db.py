
import sqlite3
import argparse

from helpers import is_path_correct

CREATE_WEBSITES_TABLE_STATEMENT = \
    'CREATE TABLE IF NOT EXISTS websites (website_id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
    '                                     url TEXT NOT NULL UNIQUE)'

CREATE_ROBOTS_COMPLIANCE_TABLE_STATEMENT = \
    'CREATE TABLE IF NOT EXISTS robots_compliance (id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
    '                                     website_id INTEGER NOT NULL UNIQUE, ' \
    '                                     robots_allows_crawling INTEGER, ' \
    '                                     FOREIGN KEY(website_id) REFERENCES websites(website_id))'

CREATE_TOS_COMPLIANCE_TABLE_STATEMENT = \
    'CREATE TABLE IF NOT EXISTS tos_compliance (id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
    '                                     website_id INTEGER NOT NULL UNIQUE, ' \
    '                                     tos_found INTEGER, ' \
    '                                     tos_allows_crawling INTEGER, ' \
    '                                     FOREIGN KEY(website_id) REFERENCES websites(website_id))'

CREATE_COOKIE_CSS_SELECTORS_TABLE_STATEMENT = \
    'CREATE TABLE IF NOT EXISTS cookie_css_selectors (id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
    '                                                 selector TEXT NOT NULL UNIQUE)'

CREATE_COOKIES_TABLE_STATEMENT = \
    'CREATE TABLE IF NOT EXISTS cookies (id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
    '                                    html TEXT, ' \
    '                                    width INTEGER, ' \
    '                                    height INTEGER, ' \
    '                                    position_x INTEGER, ' \
    '                                    position_y INTEGER, ' \
    '                                    banner_exists INTEGER, ' \
    '                                    website TEXT, ' \
    '                                    hash TEXT,' \
    '                                    selector TEXT, '\
    '                                    visit_id INTEGER)'

CREATE_COOKIE_OPTIONS_TABLE_STATEMENT = \
    'CREATE TABLE IF NOT EXISTS cookie_options (id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
    '                                           has_accept_btn INTEGER, ' \
    '                                           cta_accept TEXT, ' \
    '                                           has_decline_btn INTEGER, ' \
    '                                           cta_decline TEXT, ' \
    '                                           has_options_btn INTEGER, ' \
    '                                           cta_options TEXT, ' \
    '                                           has_info_btn INTEGER, ' \
    '                                           cta_info TEXT, ' \
    '                                           privacy_text TEXT, ' \
    '                                           website TEXT)'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process values for the Cookie DB Creator.')
    parser.add_argument('--db', type=is_path_correct, default='./outp/cookies.sqlite')
    args = parser.parse_args()

    sqlite_connection = sqlite3.connect(args.db)
    sqlite_cursor = sqlite_connection.cursor()
    sqlite_cursor.execute(CREATE_WEBSITES_TABLE_STATEMENT)
    sqlite_cursor.execute(CREATE_ROBOTS_COMPLIANCE_TABLE_STATEMENT)
    sqlite_cursor.execute(CREATE_TOS_COMPLIANCE_TABLE_STATEMENT)
    sqlite_cursor.execute(CREATE_COOKIE_CSS_SELECTORS_TABLE_STATEMENT)
    sqlite_cursor.execute(CREATE_COOKIES_TABLE_STATEMENT)
    sqlite_cursor.execute(CREATE_COOKIE_OPTIONS_TABLE_STATEMENT)
    sqlite_connection.commit()
    sqlite_connection.close()

