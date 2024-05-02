## 2024-05-01 20:46 moved to Linkedinee ConnecteeOne

# # Mark as Connected in DB from Linkedin link
# # Use with Alfred as CL = "Connected on Linkedin"

# from datetime import datetime
# import subprocess
# from pync import Notifier
# from DB.tools import select_all_records, update_record
# import os
# import my_utils

# from dotenv import load_dotenv
# load_dotenv()
# # PATH_QUEUE_AI_FILE = os.getenv("PATH_QUEUE_AI_FILE")
# DB = os.getenv("DB_BTOB")

# clipboard_content = subprocess.check_output(['pbpaste']).decode('utf-8')

# all_people_by_linkedin_handle = {my_utils.linkedin_handle_from_url(x.linkedin):x.rowid for x in select_all_records(DB, 'people') if x.linkedin}

# table_name = 'people'

# try:

#     if clipboard_content.startswith('https://www.linkedin.com'):

#         linkedin_handle = my_utils.linkedin_handle_from_url(clipboard_content)

#         print(f"\n{linkedin_handle=}\n")

#         rowid = all_people_by_linkedin_handle[linkedin_handle]

#         print(f"\n{rowid=}\n")

#         updating_record = update_record(DB, table_name, {
#                     'rowid': rowid,
#                     'visited': f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
#                     'connected': f"{datetime.now().strftime('%Y-%m-%d')} pending",
#                     'updated': f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
#                     })
        
#         if not updating_record:
#             Notifier.notify(
#                         title=f'FAIL with clipboard_content: {clipboard_content}',
#                         message=f'🔴🔴🔴 NOTHING TO UPDATE',
#                     )

#         else:
#             Notifier.notify(
#             title=f'UPDATED {linkedin_handle} in {table_name} table',
#             message='🟢🟢🟢',
#         )
        
# except Exception as e:

#     Notifier.notify(
#         title=f'FAIL with clipboard_content: {clipboard_content}',
#         message=f'🔴🔴🔴 ERROR: {e}',
#     )

