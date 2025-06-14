from datetime import datetime
import os
ts_db = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
ts_time = f"{datetime.now().strftime('%H:%M:%S')}"
print(f"\n---------- {ts_time} starting {os.path.basename(__file__)}")
import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()
DB_BTOB = os.getenv("DB_BTOB")


####################
# UPDATE DB WITH BOUNCED EMAI

# IMPORTS (script-specific)

# import my_utils
# from DB.tools import select_all_records, update_record, create_record, delete_record
# import sys
import sqlite3

# from instantly import update_lead_status

# GLOBALS



count_total = 0
count = 0
count_row = 0

test = True
verbose = True # verbose mode


# FUNCTIONS


def get_clipboard_content():
    """
    Fetch the current content of the clipboard using OS-specific command.
    Works on macOS using the 'pbpaste' command.
    """
    try:
        clipboard_content = os.popen('pbpaste').read()
        return clipboard_content
    except Exception as e:
        print(f"Error fetching clipboard content: {e}")
        return None




def clean_email(clipboard_content):
    global verbose

    if verbose:
        print(f"\nclipboard_content: {repr(clipboard_content)}\n")

    if '@' not in clipboard_content:
        return False

    words = clipboard_content.split()
    for word in words:
        if '@' in word:
            email = word # email now holds the most likely email segment
            break

    email = email.strip('[]()<>')

    if '║' in email:
        email = email.replace('║', '')
    if '>>> email' in email: # This phrase is less likely after isolating a word
        email = email.replace('>>> email', '')
    
    if ':' in email:
        email = email.replace(':', '')
    if email.startswith('mailto:'):
        email = email.replace('mailto:', '')
    if email.startswith('mailto'): # Kept for functional equivalence with original
        email = email.replace('mailto', '')
            
    email = email.strip().lower()

    if verbose:
        print(f"\nclean clipboard_content: {repr(email)}\n")

    return email




def mark_email_bounced():
    global verbose

    clipboard_content = get_clipboard_content()

    email = clean_email(clipboard_content)

    if verbose:
        print(f"\nemail: {repr(email)}\n")

    if email:

        db = sqlite3.connect(DB_BTOB)
        c = db.cursor()
        c.execute(f"""
            SELECT rowid
            FROM people
            WHERE email LIKE '{email}';
            """)
        result = c.fetchone()
        db.close()
        
        if result is not None:

            rowid = result[0]

            print(f"Updating record #{rowid} for {email} in people table.")

            db = sqlite3.connect(DB_BTOB)
            c = db.cursor()
            c.execute(f"""
                UPDATE people 
                SET email_old = ?,
                    email = NULL,
                    email_status = NULL,
                    updated = ?
                WHERE rowid = ?""", (email, ts_db, rowid))
            db.commit()
            db.close()
            
            print(f"\n✅Updated record #{rowid} for {email} in people table.\n")

            # Display success dialog and then close the tab when OK is clicked
            os.system(f'''
            osascript -e '
                display dialog "🟢🟢🟢 EMAIL BOUNCED\n\nChanges made for {email}:\n\n- Moved email to email_old\n- Set email to NULL\n- Set email_status to NULL\nUpdated timestamp to {ts_db}" with title "SUCCESS" buttons {{"OK"}} default button "OK"
            '
            ''')

            return True
        else:
            print("\n❌No record found in 'people' table.\n")

            # Display error dialog without buttons
            os.system(f'''
            osascript -e '
                display dialog "❌No record found in 'people' table.\n\n{email}" with title "ERROR"
            '
            ''')

            return False


mark_email_bounced()

# MAIN


# if __name__ == '__main__':

#     """
#     Mark Bounced Email
#     Use in conjuction with Alfred
#     Keyword 'be' for Bounced Email, with a valid email in clipboard
#     """

#     mark_email_bounced()

#     print(f"\n\n\n")

run_time = round((time.time() - start_time), 3)
if run_time < 1:
    print(f'\n{os.path.basename(__file__)} finished in {round(run_time*1000)}ms at {datetime.now().strftime("%H:%M:%S")}.\n')
elif run_time < 60:
    print(f'\n{os.path.basename(__file__)} finished in {round(run_time)}s at {datetime.now().strftime("%H:%M:%S")}.\n')
elif run_time < 3600:
    print(f'\n{os.path.basename(__file__)} finished in {round(run_time/60)}mns at {datetime.now().strftime("%H:%M:%S")}.\n')
else:
    print(f'\n{os.path.basename(__file__)} finished in {round(run_time/3600, 2)}hrs at {datetime.now().strftime("%H:%M:%S")}.\n')