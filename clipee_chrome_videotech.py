# # Copy URL from Chrome and add to Videotech vendors table

import sys
sys.path.append(f"/Users/nic/Python/indeXee")

from datetime import datetime
from pync import Notifier

import time
import os
import subprocess

from dotenv import load_dotenv
load_dotenv()
PATH_QUEUE_AI_FILE = os.getenv("PATH_QUEUE_AI_FILE")

# for pasting
from pynput.keyboard import Key, Controller
keyb = Controller()

DB = '/Users/nic/db/btob.db'

# FUNCTIONS

def get_clipboard_content():
    clipboard_content = subprocess.check_output(['pbpaste']).decode('utf-8')
    return clipboard_content


def select_content_from_chrome_address_bar():
    with keyb.pressed(Key.ctrl):
            keyb.press('l')
            keyb.release('l')

def copy():
    with keyb.pressed(Key.cmd):
            keyb.press('d')
            keyb.release('d')



def add_to_db(url):

    from DB.tools import create_record
    import my_utils

    if url.startswith('http'):


        # ADD to videotech table

        try:

            create_record(DB, 'videotech', {
                'url': url,
                'domain': my_utils.domain_from_url(url),
                'notes': 'manual capture',
                'created': f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
                })
            
            Notifier.notify(
                title='SUCCESS',
                message=f'🟢🟢🟢\nadded to VIDEOTECH table in BTOB DB',
            )

        except Exception as e:
            
            Notifier.notify(
                title='FAIL',
                message=f'🔴🔴🔴 ERROR: {e}',
            )



        # ADD to companies table

        try:
            
            create_record(DB, 'companies', {
                'url': my_utils.clean_url(url),
                'domain': my_utils.domain_from_url(url),
                'notes': 'manual capture',
                'created': f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
                })
            
            Notifier.notify(
                title='SUCCESS',
                message=f'🟢🟢🟢\nadded to COMPANIES table in BTOB DB',
            )


        except Exception as e:
            
            Notifier.notify(
                title='FAIL - companies table',
                message=f'🔴🔴🔴 ERROR: {e}',
            )


    else:
        
        Notifier.notify(
                title='FAIL',
                message=f'🔴🔴🔴 NOT A URL {url}',
            )



# MAIN

select_content_from_chrome_address_bar()

time.sleep(0.2)

copy()

url = get_clipboard_content()

url = url.lower().strip()
if url.endswith('/'):
    url = url[:-1]

Notifier.notify(
                title='COPIED',
                message=f'{url}',
            )

# time.sleep(0.2)

add_to_db(url)

