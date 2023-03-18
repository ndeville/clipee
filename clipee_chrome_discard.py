"""
Copy URL from Chrome and add to text file for batch processing
"""

import time
import os
import subprocess

from dotenv import load_dotenv
load_dotenv()
PATH_DISCARD_TEXT_FILE = os.getenv("PATH_DISCARD_TEXT_FILE")

## for pasting
from pynput.keyboard import Key, Controller
keyb = Controller()

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

def add_to_linkedin_discard_txt(url):
    if url.startswith('https://www.linkedin.com'):
        with open(PATH_DISCARD_TEXT_FILE, 'a') as f:
            print(url, file=f)

def set_clipboard_value(value):
    # Use subprocess to call the pbcopy command on macOS to set the clipboard value
    subprocess.run("pbcopy", universal_newlines=True, input=value)

# Main

## keep old clipboard content
old_clipboard_content = get_clipboard_content()

## get URL from Chrome
select_content_from_chrome_address_bar()
time.sleep(0.2)

## copy URL to clipboard
copy()

## get URL from clipboard
url = get_clipboard_content()
time.sleep(0.2)

## add URL to text file
add_to_linkedin_discard_txt(url)

## restore old clipboard content
set_clipboard_value(old_clipboard_content)