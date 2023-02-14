from pandas.io.clipboard import clipboard_get
import subprocess
from tldextract import extract
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib import request
from urllib.parse import urlparse
import tldextract
import os

print("----------")
ts_file = f"{datetime.now().strftime('%y%m%d-%H%M')}"
ts_db = f"{datetime.now().strftime('%Y-%m-%d %H:%M')}"
ts_time = f"{datetime.now().strftime('%H:%M:%S')}"
print(f"{ts_time} starting {os.path.basename(__file__)}")

import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()
USER = os.getenv("USER")

import sys
sys.path.append(f"/Users/{USER}/Python/indeXee")

import grist_BB

from inspect import currentframe
def get_linenumber():
    """
    print line numbers with f"{get_linenumber()}"
    """
    cf = currentframe()
    return cf.f_back.f_lineno

import pprint
pp = pprint.PrettyPrinter(indent=4)
print()
count = 0
count_row = 0

print(f"{os.path.basename(__file__)} boilerplate loaded -----------")
print()
####################
# Clipee Grist - Add Recruiters

import webbrowser

### UI
# from tkinter import simpledialog
import pymsgbox
# import pymsgbox.native as pymsgbox

### GLOBAL VARIABLES
test = False 
v = True # verbose mode

doc_id = os.getenv("DOC_ID_BB_RECRUITERS")
api_key = os.getenv("GRIST_API_KEY")

# Create Recruiters document in Grist

recruiters_data = grist_BB.Recruiters.fetch_table('Master')
if v:
    print(f"\n{len(recruiters_data)} Recruiters in Grist.\n")

existing_domains = [x.domain for x in recruiters_data]

### 


### Functions

def separator(count=50, lines=3, symbol='='):
    separator = f"{symbol * count}" + '\n'
    separator = f"\n{separator * lines}"
    print(separator)

sep = separator()

def cleanurl(url: str) -> str:
    from urllib.parse import urlparse
    purl = urlparse(url)
    scheme = purl.scheme + '://' if purl.scheme else ''
    return f'{scheme}{purl.netloc}{purl.path}'

def root_url(url):
    o = urlparse(url)
    root_website = f"{o.scheme}//{}.{o.suffix}".lower()
    if 'www.' in domain:
        domain = domain.replace('www.','')
    return domain

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

def add_to_grist(name, url, summary, slug, domain, raw_url, raw_title, raw_header):
    grist_BB.Recruiters.add_records('Master', [
                                    {   'name': name,
                                        'url': url,
                                        'summary': summary,
                                        'slug': slug,
                                        'domain': domain,
                                        'raw_url': raw_url,
                                        'raw_title': raw_title,
                                        'raw_header': raw_header,
                                        }
                                ])

name_summary_split = [
    '|',
    ':',
    '-',
    '·',
]

### Main

def add_recruiter(text, v=v):
    raw_url = text.strip()
    url = cleanurl(raw_url)
    if url.startswith('http'):
        print(f"{get_linenumber()} {url=}")

        name = ''
        summary = ''
        logo = ''
        raw_title = ''
        raw_header = ''


        domain = domain_from_url(url)
        slug = domain_name_from_url(url)
        app_type = 'SaaS'
        if v:
            print(f"\n{get_linenumber()} {url=}")
            print(f"{get_linenumber()} {domain=}")
            print(f"{get_linenumber()} {slug=}")
            print(f"{get_linenumber()} {app_type=}")

        if domain not in existing_domains:

            # download logo
            clearbit_path = f"https://logo.clearbit.com/{domain}"
            print(f"\nLOGO\ndownloading for {domain} with {clearbit_path}")
            time.sleep(1)
            logo = requests.get(clearbit_path)
            logo_path = f"/Users/{USER}/Github/btobsales.github.io/img/logos/{slug}.png"
            if v:
                f"#{get_linenumber()} {logo_path=}"
            open(logo_path, "wb").write(logo.content)
            print(f"downloaded at {logo_path}\n")

            try:
                html = request.urlopen(url).read().decode('utf8')
                if test:
                    print(f"\n{html=}")

                try:
                    soup = BeautifulSoup(html, "html.parser")
                    if test:
                        print(f"\n{soup=}")

                    try:
                        title = soup.title.text
                        if '\n' in title:
                            title = title.replace('\n', ' ').strip()
                        raw_title = title
                        if v:
                            print(f"\n{get_linenumber()} {title=}")

                        try:
                            header = soup.find('h1').text
                            if '\n' in header:
                                header = header.replace('\n', ' ').strip()
                            raw_header = header
                            if v:
                                print(f"{get_linenumber()} {header=}")
                            if header in title:
                                header = domain
                            name = title
                            summary = header
                            for split_char in name_summary_split:
                                if split_char in name:
                                    parts = name.split(split_char)
                                    name = parts[0].strip()
                                    summary = parts[1].strip()
                            if v:
                                print(f"{get_linenumber()} {name=}")
                                print(f"{get_linenumber()} {summary=}")

                        except Exception as e:
                            print(f"\n{get_linenumber()} h1 ERROR: {e}")
                            name = title
                    
                    except Exception as e:
                        print(f"\n{get_linenumber()} title ERROR: {e}")

                except Exception as e:
                    print(f"\n{get_linenumber()} soup ERROR: {e}")

            except Exception as e:
                print(f"\n{get_linenumber()} html ERROR: {e}")

            print(f"\n{get_linenumber()} Data passed to function add_to_grist:")
            print(f"{name=}")
            print(f"{url=}")
            print(f"{summary=}")
            print(f"{slug=}")
            print(f"{domain=}\n\n")

            add_to_grist(name, url, summary, slug, domain, raw_url, raw_title, raw_header)


            webbrowser.get('chrome').open_new_tab(f'https://nic.getgrist.com/c4yWEja7RmrL/Recruiters')

        else:
            msg224 = f"{domain} already in Grist"
            print(f"\n\n{msg224}")
            pymsgbox.alert(msg224)

    else:
        print(f"\n{url} is NOT a URL.")
        pymsgbox.alert(f"\n{url} is NOT a URL.")
        

text = clipboard_get()
print(f"\nProcessing:\n{repr(text)}\n")

add_recruiter(text)

run_time = round((time.time() - start_time), 1)
print(f'finished in {run_time}s.\n')