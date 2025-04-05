"""
Add to Call List: Copy URL from Chrome and update people table in DB.
Works in conjunction with Alfred to add people to call list from their Linkedin profile.
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

def set_clipboard_value(value):
    # Use subprocess to call the pbcopy command on macOS to set the clipboard value
    subprocess.run("pbcopy", universal_newlines=True, input=value)



def get_people_rowid_from_linkedin_handle(linkedin_handle):
    # Establish a database connection
    conn = sqlite3.connect(DB)

    # SQL query to get rowid from people table
    sql = """
        SELECT rowid FROM people
        WHERE linkedin LIKE ?
        """
    # Execute the SQL query and retrieve the row
    cursor = conn.execute(sql, ('%' + linkedin_handle + '%',))
    row = cursor.fetchone()

    # Close the database connection
    conn.close()

    # Check if a row was found and return the rowid
    if row is not None:
        rowid = row[0]
        return rowid
    else:
        # Handle the case when no matching row is found
        return None


def get_chrome_active_tab_url():
    try:
        script = '''
        tell application "Google Chrome"
            set activeTabUrl to URL of active tab of front window
            return activeTabUrl
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        url = result.stdout.strip()
        print(f"\n🚹  Active tab URL: {url}")
        return url
    except Exception as e:
        print(f"Error: {e}")
        return None




def update_db(linkedin_handle):
    from DB.tools import update_record

    try:
        rowid = get_people_rowid_from_linkedin_handle(linkedin_handle)
        
        # Get person details before updating
        conn = sqlite3.connect(DB)
        cursor = conn.execute("""
            SELECT first, last, title, company, connected 
            FROM people 
            WHERE rowid = ?""", (rowid,))
        person = cursor.fetchone()
        conn.close()

        update_record(DB, 'people', {
            'rowid': rowid,
            'call': 1,
            # 'lead_rank': 'D',
            # 'notes': f"{datetime.now().strftime('%Y-%m-%d %H:%M')} discarded manually",
            'updated': f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            })
        
        # Format person details for notification
        if person:
            person_details = f"{linkedin_handle}\n\n{person[0]} {person[1]}\n{person[2]}\n{person[3]}\n\nconnected: {person[4]}"
        else:
            person_details = linkedin_handle

        # Display success dialog and then close the tab when OK is clicked
        os.system(f'''
        osascript -e '
            display dialog "🟢🟢🟢 ADDED TO CALL LIST\n\n{person_details}" with title "SUCCESS" buttons {{"OK"}} default button "OK"

        '
        ''')

    except Exception as e:
        Notifier.notify(
            title='FAIL - people table',
            message=f'🔴🔴🔴 ERROR: {e}\nwith {linkedin_handle}',
        )


# MAIN

# ## keep old clipboard content
# old_clipboard_content = get_clipboard_content()

# select_content_from_chrome_address_bar()

# time.sleep(0.2)

# copy()

# url = get_clipboard_content()

# url = url.lower().strip()
# if url.endswith('/'):
#     url = url[:-1]

# linkedin_handle = my_utils.linkedin_handle_from_url(url)


linkedin = get_chrome_active_tab_url()

linkedin_handle = my_utils.linkedin_handle_from_url(linkedin)




# Notifier.notify(
#                 title='COPIED',
#                 message=f'Linkedin handle {linkedin_handle} from {url}',
#             )

update_db(linkedin_handle)

## restore old clipboard content
# set_clipboard_value(old_clipboard_content)


