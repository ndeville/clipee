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
# UPDATE DB WITH PEOPLE WHO LEFT COMPANY

# IMPORTS (script-specific)

# import my_utils
# from DB.tools import select_all_records, update_record, create_record, delete_record
# import sys
import sqlite3
import subprocess

from pync import Notifier

# from instantly import update_lead_status

# GLOBALS



count_total = 0
count = 0
count_row = 0

test = True
verbose = True # verbose mode


# FUNCTIONS

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



def mark_left_company():
    global verbose

    # clipboard_content = get_clipboard_content()

    clipboard_content = get_chrome_active_tab_url()

    # if "@" in clipboard_content:
    #     email = clean_email(clipboard_content)
    #     if verbose:
    #         print(f"\nemail: {repr(email)}\n")

    #     db = sqlite3.connect(DB_BTOB)
    #     c = db.cursor()
    #     c.execute(f"""
    #         SELECT rowid
    #         FROM people
    #         WHERE email LIKE '{email}';
    #         """)
    #     result = c.fetchone()
    #     db.close()
        
    #     if result is not None:

    #         rowid = result[0]

    #         print(f"Updating record #{rowid} for {email} in people table.")

    #         db = sqlite3.connect(DB_BTOB)
    #         c = db.cursor()
    #         c.execute(f"""
    #             UPDATE people 
    #             SET email_old = ?,
    #                 domain = NULL,
    #                 company = NULL,
    #                 title = NULL,
    #                 lead_rank = NULL,
    #                 email = NULL,
    #                 email_status = NULL,
    #                 connect25 = NULL,
    #                 updated = ?
    #             WHERE rowid = ?""", (email, ts_db, rowid))
    #         db.commit()
    #         db.close()
            
    #         print(f"\n✅Updated record #{rowid} for {email} in people table.\n")

    #         # Display success dialog and then close the tab when OK is clicked
    #         os.system(f'''
    #         osascript -e '
    #             display dialog "🟢🟢🟢 LEFT COMPANY\n\nChanges made for {email}:\n\n- Moved email to email_old\n- Set domain to NULL\n- Set company to NULL\n- Set title to NULL\n- Set lead_rank to NULL\n- Set email to NULL\n- Set email_status to NULL\n- Set connect25 to NULL\n- Updated timestamp to {ts_db}" with title "SUCCESS" buttons {{"OK"}} default button "OK" giving up after 5
    #         '
    #         ''')

    #         return True
    #     else:
    #         print("\n❌No record found in 'people' table.\n")

    #         # Display error dialog without buttons
    #         os.system(f'''
    #         osascript -e '
    #             display dialog "❌No record found in 'people' table.\n\n{email}" with title "ERROR"
    #         '
    #         ''')

    #         return False
        
    if "linkedin.com" in clipboard_content:
        linkedin = clipboard_content.strip()
        if linkedin.endswith('/'):
            linkedin = linkedin[:-1]
        if verbose:
            print(f"\nlinkedin: {repr(linkedin)}\n")

        db = sqlite3.connect(DB_BTOB)
        c = db.cursor() 
        # Fetch rowid and current email
        c.execute(f"""
            SELECT rowid, email
            FROM people
            WHERE linkedin LIKE '{linkedin}';
        """)
        result = c.fetchone()
        db.close()

        if result is not None:
            rowid = result[0]
            current_email = result[1]
            print(f"Updating record #{rowid} for {linkedin} in people table.")

            db = sqlite3.connect(DB_BTOB)
            c = db.cursor()
            if current_email is not None and current_email != "":
                # If email is not null, copy it to email_old
                c.execute(f"""
                    UPDATE people 
                    SET email_old = ?,
                        domain = NULL,
                        company = NULL,
                        company_domain = NULL,
                        comp1_name = NULL,
                        title = NULL,
                        lead_rank = NULL,
                        email = NULL,
                        email_status = NULL,
                        connect25 = NULL,
                        updated = ?
                    WHERE rowid = ?""", (current_email, ts_db, rowid))
            else:
                # If email is null, just update the other fields
                c.execute(f"""
                    UPDATE people 
                    SET domain = NULL,
                        company = NULL,
                        company_domain = NULL,
                        comp1_name = NULL,
                        title = NULL,
                        lead_rank = NULL,
                        email = NULL,
                        email_status = NULL,
                        connect25 = NULL,
                        updated = ?
                    WHERE rowid = ?""", (ts_db, rowid))
            db.commit()
            db.close()
            
            print(f"\n✅Updated record #{rowid} for {linkedin} in people table.\n")

            # Display success dialog and then close the tab when OK is clicked
            Notifier.notify(
                f"🟢🟢🟢 LEFT COMPANY\n\nChanges made for {linkedin}:\n\n"
                "- Set domain to NULL\n"
                "- Set company to NULL\n"
                "- Set title to NULL\n"
                "- Set lead_rank to NULL\n"
                "- Set email to NULL\n"
                "- Set email_status to NULL\n"
                "- Set connect25 to NULL\n"
                f"- Updated timestamp to {ts_db}",
                title="SUCCESS"
            )

            return True
        else:
            print("\n❌No record found in 'people' table.\n")

            # Display error dialog without buttons
            Notifier.notify(
                f"❌No record found in 'people' table.\n\n{linkedin}",
                title="ERROR"
            )

            return False



# MAIN

mark_left_company()



run_time = round((time.time() - start_time), 3)
if run_time < 1:
    print(f'\n{os.path.basename(__file__)} finished in {round(run_time*1000)}ms at {datetime.now().strftime("%H:%M:%S")}.\n')
elif run_time < 60:
    print(f'\n{os.path.basename(__file__)} finished in {round(run_time)}s at {datetime.now().strftime("%H:%M:%S")}.\n')
elif run_time < 3600:
    print(f'\n{os.path.basename(__file__)} finished in {round(run_time/60)}mns at {datetime.now().strftime("%H:%M:%S")}.\n')
else:
    print(f'\n{os.path.basename(__file__)} finished in {round(run_time/3600, 2)}hrs at {datetime.now().strftime("%H:%M:%S")}.\n')