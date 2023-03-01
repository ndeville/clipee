# Copy URL from Chrome and add to Clipper queue file

import time
import os

from dotenv import load_dotenv
load_dotenv()
PATH_CHROME_CLIPPER = os.getenv("PATH_CHROME_CLIPPER")

import subprocess

# for pasting
from pynput.keyboard import Key, Controller
keyb = Controller()


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

def add_to_clipper_txt(url):
    with open(PATH_CHROME_CLIPPER, 'a') as f:
    # with open(PATH_CHROME_CLIPPER, 'a') as f:
        print(url, file=f)

select_content_from_chrome_address_bar()

time.sleep(0.2)

copy()

url = get_clipboard_content()

time.sleep(0.2)

add_to_clipper_txt(url)


