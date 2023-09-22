from datetime import datetime
import os
ts_db = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
ts_time = f"{datetime.now().strftime('%H:%M:%S')}"
print(f"\n---------- {ts_time} starting {os.path.basename(__file__)}")
import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()
DB_TWITTER = os.getenv("DB_TWITTER")
DB_BTOB = os.getenv("DB_BTOB")
DB_MAILINGEE = os.getenv("DB_MAILINGEE")
DB_EMAILEE = os.getenv("DB_EMAILEE")

import pprint
pp = pprint.PrettyPrinter(indent=4)

####################
# SCRIPT_TITLE

# IMPORTS (script-specific)

import my_utils
from DB.tools import select_all_records, update_record, create_record, delete_record
import sys
import sqlite3

from instantly import update_lead_status

# GLOBALS



count_total = 0
count = 0
count_row = 0

test = True
v = True # verbose mode


# FUNCTIONS


def clean_email(clipboard_content):

    if '@' in clipboard_content:

        # Cleaning

        if '║' in clipboard_content:
            clipboard_content = clipboard_content.replace('║', '')
        if '>>> email' in clipboard_content:
            clipboard_content = clipboard_content.replace('>>> email', '')
        if ':' in clipboard_content:
            clipboard_content = clipboard_content.replace(':', '')
        if clipboard_content.startswith('mailto:'):
            clipboard_content = clipboard_content.replace('mailto:', '')
        if clipboard_content.startswith('mailto'):
            clipboard_content = clipboard_content.replace('mailto', '')
            
        clipboard_content = clipboard_content.strip().lower()

        print(f"\nclean clipboard_content: {clipboard_content}\n")

        return clipboard_content
    
    else:

        return False




def mark_dne(email):

    marked = False

    # Update email record in Mailingee table

    print(f"\n\n==== MAILINGEE TABLES\n")

    all_campaigns = my_utils.get_all_mailingee_campaigns()

    for campaign in all_campaigns:

        # print(f"Processing campaign: {campaign}")

        db_mailingee = sqlite3.connect(DB_MAILINGEE)
        cm = db_mailingee.cursor()
        cm.execute(f"""
                SELECT rowid
                FROM {campaign}
                WHERE email IS '{email}';
                """)
        result_mailingee = cm.fetchone()
        db_mailingee.close()
        if result_mailingee is not None:

            rowid_mailingee = result_mailingee[0]

            print()

            update_record(DB_MAILINGEE, campaign, {
                    'rowid': rowid_mailingee,
                    'status': 'DNE',
                    'notes': 'MDS',
                    'updated': ts_db,
                }
                )
            
            marked = True

    if not marked:
        print("\nNo record found in Mainlingee tables.\n")

        # else:
        #     print(f"\nNo record found in {campaign} table.")

    # Update email record in people table

    print(f"\n\n==== PEOPLE TABLE\n")

    db = sqlite3.connect(DB_BTOB)
    c = db.cursor()
    c.execute(f"""
            SELECT rowid
            FROM people
            WHERE email IS '{email}';
            """)
    result = c.fetchone()
    db.close()
    if result is not None:
        rowid = result[0]

        print()

        update_record(DB_BTOB, 'people', {
                'rowid': rowid,
                'dne': 1,
                'notes': f'{ts_db} MDS from Mailingee',
                'updated': ts_db,
            }
            )
        
        marked = True


    else:
        print("\nNo record found in 'people' table.\n")

    # UPDATE INSTANTLY LEAD STATUS
    print(f"\n\n==== INSTANTLY LEAD STATUS\n")

    update_lead_status(email)

    return marked


    # conn = sqlite3.connect(DB_BTOB)
    # c = conn.cursor()
    # c.execute(f"UPDATE people SET status = 1, updated = '{ts_db}' WHERE email = '{email}'")
    # conn.commit()
    # conn.close()


# MAIN


if __name__ == '__main__':

    """
    Mark Do Not Email
    Use in conjuction with Alfred
    Keyword 'md' for Mark Dne, with a valid email in clipboard
    """
        

    clipboard_content = sys.stdin.read().strip()

    # print(f"\nclipboard_content: {clipboard_content}\n")

    mark_as_dne = mark_dne(clean_email(clipboard_content))

    # Add to emailee.bounce_instantly table if not found in either Mailingee or People table
    """
    keeps track of emails that bounce from Instantly warmup
    to be shared with Instantly 
    """
    if not mark_as_dne:

        print(f"\n==== ADDING TO EMAILEE.BOUNCE_INSTANTLY TABLE\n")

        create_record(DB_EMAILEE, 'bounce_instantly', {
                'email': clipboard_content,
                'created': ts_db,
        })

    print(f"\n\n\n")

    run_time = round((time.time() - start_time), 3)
    if run_time < 1:
        print(f'\n{os.path.basename(__file__)} finished in {round(run_time*1000)}ms at {datetime.now().strftime("%H:%M:%S")}.\n')
    elif run_time < 60:
        print(f'\n{os.path.basename(__file__)} finished in {round(run_time)}s at {datetime.now().strftime("%H:%M:%S")}.\n')
    elif run_time < 3600:
        print(f'\n{os.path.basename(__file__)} finished in {round(run_time/60)}mns at {datetime.now().strftime("%H:%M:%S")}.\n')
    else:
        print(f'\n{os.path.basename(__file__)} finished in {round(run_time/3600, 2)}hrs at {datetime.now().strftime("%H:%M:%S")}.\n')