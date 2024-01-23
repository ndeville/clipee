import subprocess
# from tldextract import extract
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib import request
import tldextract
import os
import requests

# for pasting
from pynput.keyboard import Key, Controller
keyb = Controller()

import sys
# sys.path.append(f"/Users/nic/Python/indeXee")
# sys.path.append(f"/Users/nic/Python/metaurl")

import pymsgbox

# from get.soup import without_js_rendering, with_js_rendering

import time
start_time = time.time()

d = datetime.now()

date = d.strftime('%Y%m%d-%H%M%S')

count_url = 0

# FUNCTIONS

# def separator(count=50, lines=3, symbol='='):
#     separator = f"{symbol * count}" + '\n'
#     separator = f"\n{separator * lines}"
#     print(separator)

# sep = separator()

def get_clipboard_content():
    clipboard_content = subprocess.check_output(['pbpaste']).decode('utf-8')
    return clipboard_content

def domain_from_url(url):
    o = tldextract.extract(url)
    domain = f"{o.domain}.{o.suffix}".lower()
    if 'www.' in domain:
        domain = domain.replace('www.','')
    return domain

def domain_name_from_url(url):
    o = tldextract.extract(url)
    domain_name = o.domain.lower()
    if 'www.' in domain_name:
        domain_name = domain_name.replace('www.','')
    return domain_name

def download_logo(domain, domain_name):
    print(f"\nChecking logo for {domain}...")

    logos_folder = "/Users/nic/Dropbox/Design/Logos"
    logo_path = os.path.join(logos_folder, f"{domain_name}_logo.png")

    if os.path.exists(logo_path):
        print(f"Logo for {domain} already exists at {logo_path}")
    else:
        print(f"Downloading logo for {domain}...")
        response = requests.get(f"https://logo.clearbit.com/{domain}?size=500")
        
        if response.status_code == 200:
            with open(logo_path, "wb") as logo_file:
                logo_file.write(response.content)
            print(f"Logo downloaded at {logo_path}")
        else:
            print(f"Error downloading logo for {domain}. Status code: {response.status_code}")


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD\n")

def paste():
    with keyb.pressed(Key.cmd):
        keyb.press('f')
        keyb.release('f')

# MAIN

def fetch_logo(url, v=False):

    url = url.strip()

    if url.startswith('http'):

        domain = domain_from_url(url)
        domain_name = domain_name_from_url(url)
        if v:
            print(f"\n{url=}")
            print(f"{domain=}")
            print(f"{domain_name=}")

        download_logo(domain, domain_name)


text = get_clipboard_content()


print(f"\nProcessing: {repr(text)}\n")

fetch_logo(text)

run_time = round((time.time() - start_time), 3)
print(f'finished in {run_time}s.\n')


