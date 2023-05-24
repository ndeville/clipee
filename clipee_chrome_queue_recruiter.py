"""
Copy URL from Chrome and add as recruiter in people table in DB
"""

import time
from datetime import datetime
import os
import subprocess
import sqlite3

import sys
sys.path.append(f"/Users/nic/Python/indeXee")

from dotenv import load_dotenv
load_dotenv()
# PATH_DISCARD_TEXT_FILE = os.getenv("PATH_DISCARD_TEXT_FILE")
DB = os.getenv("DB_BTOB")

## for pasting
from pynput.keyboard import Key, Controller
keyb = Controller()

# from DB.tools import update_record
import my_utils

from pync import Notifier

# Functions

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



TODO Finish


def set_clipboard_value(value):
    # Use subprocess to call the pbcopy command on macOS to set the clipboard value
    subprocess.run("pbcopy", universal_newlines=True, input=value)


def add_to_db(url):

    from DB.tools import create_record
    import my_utils

    if url.startswith('http'):

        # ADD to vendors table

        try:

            create_record(DB, 'vendors', {
                'url': url,
                'domain': my_utils.domain_from_url(url),
                'notes': 'manual capture',
                'created': f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
                })
            
            Notifier.notify(
                title='SUCCESS',
                message=f'🟢🟢🟢',
            )

        except Exception as e:
            
            Notifier.notify(
                title='FAIL - vendors table',
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
                message=f'🟢🟢🟢',
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

## keep old clipboard content
old_clipboard_content = get_clipboard_content()

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

## restore old clipboard content
set_clipboard_value(old_clipboard_content)
