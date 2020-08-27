
import sqlite3
from lxml import html


def find_cookie_banner_website(css_selectors=None, page_source=''):
    if css_selectors is None:
        return None

    tree = html.fromstring(page_source)
    found_cookie_selector = None

    for selector in css_selectors:
        try:
            tree_css_elements = tree.cssselect(selector)
        except Exception as _:
            continue

        if len(tree_css_elements) > 0:
            found_cookie_selector = selector
            break
    return found_cookie_selector


def save_cookie_banner_to_db(db_path='', cookie_banner=None):
    if cookie_banner is None:
        return

    con = sqlite3.connect(db_path)
    c = con.cursor()

    sqlite_insert_statement = '''
        INSERT OR IGNORE INTO cookies (html, width, height, position_x, position_y, banner_exists, website, hash, selector, visit_id) 
                    VALUES  (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    c.execute(sqlite_insert_statement, cookie_banner.as_tuple())
    con.commit()
    con.close()
