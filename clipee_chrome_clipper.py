# Copy URL from Chrome and add to Clipper queue file

import time
import sqlite3

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
    conn = sqlite3.connect('/Users/nic/db/clipee.db')
    cur = conn.cursor()
    current_date = time.strftime('%Y-%m-%d %H:%M')
    cur.execute("INSERT INTO clips (url, created, src) VALUES (?, ?, ?)", (url, current_date, "clipee_chrome_clipper"))
    conn.commit()
    conn.close()


select_content_from_chrome_address_bar()

time.sleep(0.2)

copy()

url = get_clipboard_content()
if url.endswith('/'):
    url = url[:-1]

time.sleep(0.2)

add_to_clipper_txt(url)