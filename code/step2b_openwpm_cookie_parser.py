import argparse
import time
import sqlite3
import logging
import datetime
import os


from helpers import is_path_correct
from OpenWPM.automation import CommandSequence, TaskManager
from OpenWPM.automation.Commands.utils.cookie_utils import *


SELECT_STATEMENT = """
    select url
    from websites 
        join robots_compliance as robots using(website_id)
        join tos_compliance as tos using(website_id)
    where robots.robots_allows_crawling = 1 and tos.tos_allows_crawling = 1
"""

def get_crawlable_sites():
    sqlite_cursor.execute(SELECT_STATEMENT)
    rows = sqlite_cursor.fetchall()
    return list(map(lambda x: x[0], rows))


def get_css_selectors():
    sqlite_cursor.execute('SELECT selector FROM cookie_css_selectors')
    rows = sqlite_cursor.fetchall()
    return list(map(lambda x: x[0], rows))


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(description='Process values for the IDCAC parser.')
    parser.add_argument('--db', type=is_path_correct, default='./outp/cookies.sqlite')
    parser.add_argument('--out-path', type=is_path_correct, default='./outp')
    parser.add_argument('--browsers', type=int, default=4)
    args = parser.parse_args()

    NUM_BROWSERS = args.browsers
    logger = logging.getLogger('openwpm')

    # Set up the database connection
    sqlite_connection = sqlite3.connect(args.db)
    sqlite_cursor = sqlite_connection.cursor()

    # Get the required data from the database & close db connection as OpenWPM will create a new one
    sites = get_crawlable_sites()
    css_selectors = get_css_selectors()
    sqlite_connection.close()

    # Loads the default manager params
    # and NUM_BROWSERS copies of the default browser params
    manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

    # Update per-browser configuration
    for i in range(NUM_BROWSERS):
        # Record HTTP Requests and Responses
        browser_params[i]['http_instrument'] = True

        # Record cookie changes
        browser_params[i]['cookie_instrument'] = True

        # Record Navigations
        browser_params[i]['navigation_instrument'] = True

        # Record JS Web API calls
        browser_params[i]['js_instrument'] = True

        # Record the callstack of all WebRequests made
        browser_params[i]['callstack_instrument'] = True

        # Bot mitigation
        browser_params[i]['bot_mitigation'] = True

        # Run headless ff
        browser_params[i]['display_mode'] = 'headless'

    # Update TaskManager configuration (use this for crawl-wide settings)
    manager_params['data_directory'] = os.path.join(args.out_path, 'OpenWPM')
    manager_params['log_directory'] = os.path.join(args.out_path, 'OpenWPM')
    manager_params['cookie_db'] = args.db
    manager_params['cookie_directory'] = args.out_path
    manager_params['cookie_css_selectors'] = css_selectors

    # Instantiates the measurement platform
    # Commands time out by default after 60 seconds
    manager = TaskManager.TaskManager(manager_params, browser_params)

    # Visits the sites
    for site in sites:

        # Parallelize sites over all number of browsers set above.
        # (To have all browsers go to the same sites, add `index='**'`)
        command_sequence = CommandSequence.CommandSequence(
            site, reset=True,
            callback=lambda val=site: print("CommandSequence {} done".format(val)))

        # Start by visiting the page
        command_sequence.get(sleep=3, timeout=60)

        # Find the cookie notice
        command_sequence.dump_cookie_notice(suffix=site)

        # Take a screenshot of the page
        command_sequence.screenshot_cookie_notice()

        command_sequence.mark_done()

        # Run commands across the three browsers (simple parallelization)
        manager.execute_command_sequence(command_sequence)

    elapsed_time = time.time() - start_time
    print()
    print('Time Elapsed: {}'.format(datetime.timedelta(seconds=elapsed_time)))
    print()

    # Shuts down the browsers and waits for the data to finish logging
    try:
        manager.close()
    except Exception as _:
        pass


