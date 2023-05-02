# Check email with Bouncer

from datetime import datetime
import os
ts_file = f"{datetime.now().strftime('%y%m%d-%H%M')}"
ts_db = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
ts_time = f"{datetime.now().strftime('%H:%M:%S')}"
print(f"\n---------- {ts_time} starting {os.path.basename(__file__)}")
import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()
PROJECTS_FOLDER = os.getenv("PROJECTS_FOLDER")

import sys
sys.path.append(f"{PROJECTS_FOLDER}/indeXee")
sys.path.append(f"{PROJECTS_FOLDER}/emailee")

import subprocess

import bouncer

# for pasting
from pynput.keyboard import Key, Controller
keyb = Controller()


def get_clipboard_content():
    clipboard_content = subprocess.check_output(['pbpaste']).decode('utf-8')
    return clipboard_content


email = get_clipboard_content()

if '@' in email and '.' in email:
    print(f"\nChecking email: {email}")
    bouncer.verify_email_is_valid(email)
else:
    print(f"\nNo email found in clipboard: {email}")