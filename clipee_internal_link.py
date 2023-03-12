# from pandas.io.clipboard import clipboard_get
import subprocess
# from tldextract import extract
# import requests
# from datetime import datetime
# from bs4 import BeautifulSoup
# from urllib import request
# import tldextract

# for pasting
from pynput.keyboard import Key, Controller
keyb = Controller()

# from inspect import currentframe
# import string
# from urllib.parse import urlparse
# from urllib.parse import urlparse
# from datetime import date
# import re

# import time
# start_time = time.time()

# import sys
# sys.path.append("/Users/nic/Python/indeXee")
# import grist_PE

# d = datetime.now()

# date = d.strftime('%Y%m%d-%H%M%S')

# count_url = 0

import os
from dotenv import load_dotenv
load_dotenv()

# set homee path from HOMEe_PATH env variable
homee_path = os.getenv("HOMEe_PATH")

def get_clipboard_content():
    clipboard_content = subprocess.check_output(['pbpaste']).decode('utf-8')
    return clipboard_content

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD\n")

def paste():
    with keyb.pressed(Key.cmd):
        keyb.press('f')
        keyb.release('f')


def get_category_and_page_name(path):
    # keep only category and page name
    output = path.replace('/Users/nic/Python/homee/notes/content/articles/', '')
    if " " in output:
        output = output.replace(' ', '-')
    # remove .md
    output = output[:-3]

    return output


def internal_link_for_note(path, v=False):
    
    if path.startswith('note'):
        path = f"{homee_path}{path}"

    # open file with path and get first row from text (= title)
    with open(path, 'r') as f:
        first_line = f.readline().strip()
        title = first_line.replace('Title: ','')

    category_and_page_name = get_category_and_page_name(path)

    output = f"[[Nic Note: {title}](../../{category_and_page_name}/index.html)]"

    return output

text = get_clipboard_content()

write_to_clipboard(internal_link_for_note(text))

paste()

