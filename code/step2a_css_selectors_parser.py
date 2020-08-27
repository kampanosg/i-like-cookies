import os
import requests
import time
import argparse
import datetime
import sqlite3

from helpers import is_path_correct

IDCAC_URL = 'https://www.i-dont-care-about-cookies.eu/abp/'
INSERT_STATEMENT = 'INSERT OR IGNORE INTO cookie_css_selectors (selector) VALUES (?)'


def save_css_selectors_to_db(db_path, css_selectors):
    sqlite_connection = sqlite3.connect(db_path)
    sqlite_connection.text_factory = lambda x: unicode(x, 'utf-8', 'ignore')
    sqlite_cursor = sqlite_connection.cursor()
    for css_selector in css_selectors:
        sqlite_cursor.execute(INSERT_STATEMENT, (css_selector, ))
    sqlite_connection.commit()
    sqlite_connection.close()


def download_updated_cookie_selectors_list(idcac_path):
    """Saves an updated 'I don't care about cookies' list"""
    selectors_list_file = os.path.join(idcac_path, 'idcac_cookie_selectors.txt')
    r = requests.get(IDCAC_URL)

    with open(selectors_list_file, 'wb') as outfile:
        outfile.write(r.content)

    return selectors_list_file


def parse_css_selector_lists_and_update_db(db_path, idcac_path):

    selectors_list_file = download_updated_cookie_selectors_list(idcac_path)
    css_selectors = ['#qcCmpUi',
                     '#qc-cmp2-ui',
                     '.cookieinfo',
                     '#CybotCookiebotDialog',
                     '.cookie-bubble',
                     'div.cc-window.cc-floating',
                     '.cc_banner.cc_container',
                     '#ns-cookie-popup',
                     '.cookie-pop',
                     '#cadre_alert_cookies',
                     '.cookies-widget-container',
                     '#cookie-law-info-bar',
                     '#consentPrompt',
                     '.cb-cookiesbox',
                     'div.cookies',
                     '#hw_cookie_law',
                     'div#accept',
                     '#ckieconsent',
                     '#cookies_rep',
                     '.mpp-box.mpp-popup',
                     '.prvmodal-wrapper.prvmodal-transition',
                     'div#cookies',
                     '.gdpr',
                     '#sid-container',
                     '#cookies-agreed-wrapper',
                     '#popup_cookie_law',
                     '#cpolicyPanel',
                     '.gdprModal__placeholder',
                     '#ccc',
                     '.gdpr.gdpr-privacy-bar',
                     '.cc-bar',
                     '.qc-cmp-ui-content',
                     '.gdpr_accept_cookie',
                     '#moove_gdpr_cookie_info_bar',
                     '.cb-cookiesbox',
                     '.consent',
                     '.glcn_accept_cookie',
                     '.cc-dialog',
                     '#brands-galaxy-cookie',
                     '.gdpr-cookies-warning-float-box',
                     '#_evidon_banner',
                     '.gdpr-cookie-modal',
                     '#cookies-accept-container',
                     '#ck_cookies',
                     '#cookies_box',
                     '#cp-inner',
                     '.pleaseaccept',
                     '#cookie-main',
                     '#cookieprefs',
                     '#cookieDialogue',
                     '#cookieconsent:desc',
                     '#cookies-settings-modal',
                     '.setCookies',
                     '.nasa-cookie-notice-container',
                     '#notif--privacy',
                     '.cookie_popup_bottom',
                     '#btm_terms',
                     '#mstm-cookie',
                     '#ct-ultimate-gdpr-cookie-popup',
                     '#gdpr-cookie-block',
                     '#divCookiealert',
                     '#coi-banner-wrapper',
                     '#cookiepolicybox',
                     '.cookies-tooltip']

    with open(selectors_list_file) as f:
        for line in f:

            first_character = line[0]
            banned_characters = {'!', '[', '@', '|', '/'}

            # Ignore the lines starting with !. They are comments
            if first_character in banned_characters:
                continue

            # If the line starts with ~ then this indicates a global rule. e.g.: ~site1.com, site2.com###cookie-notice
            if first_character == '~':
                selector_index = line.find('#')
                if selector_index != -1:
                    selector = line[selector_index + 2:]
                    css_selectors.append(selector.strip())
                continue

            # If the line starts with ## then this indicates a selector. e.g.: ###cookie-notice
            if line[0:2] == '##':
                selector = line[2:]
                css_selectors.append(selector.strip())
                continue

            # If the line starts with a domain name then site specific selectors. e.g.: site.com###cookie-notice-1,...
            selector_index = line.find('#')
            if selector_index != -1:
                selectors = line[selector_index + 2:].split(',')
                for selector in selectors:
                    css_selectors.append(selector.strip())

    save_css_selectors_to_db(db_path, css_selectors)
    return css_selectors


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description='Process values for the IDCAC parser.')
    parser.add_argument('--db', type=is_path_correct, default='./outp/cookies.sqlite')
    parser.add_argument('--idcac-path', type=is_path_correct, default='./outp')
    args = parser.parse_args()

    parse_css_selector_lists_and_update_db(args.db, args.idcac_path)

    elapsed_time = time.time() - start_time
    print('Time Elapsed: {}'.format(datetime.timedelta(seconds=elapsed_time)))
