from pandas.io.clipboard import clipboard_get
import subprocess
from tldextract import extract
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib import request
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

import grist_PE

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
# Clipee Grist - Add Apps

### GLOBAL VARIABLES
test = False 
v = True # verbose mode

doc_id = os.getenv("DOC_ID_PE_APPS")
api_key = os.getenv("GRIST_API_KEY")

apps_data = grist_PE.Apps.fetch_table('Master')
if v:
    print(f"\n{len(apps_data)} apps in Grist.\n")

existing_domains = [x.domain for x in apps_data]

# Categories & Tags
categories_in_grist = set()
tags_in_grist = set()
for app in apps_data:
    categories = app.category
    if categories != None:
        # print(f"{categories=}")
        for cat in categories:
            if cat != 'L':
                categories_in_grist.add(cat.lower())
    tags = app.tags
    if tags != None:
        for tag in tags:
            if tag != 'L':
                tags_in_grist.add(tag.lower())


# TODO build dicts for categories and tags to match

category_keywords = list(categories_in_grist) + [
                    # ' ai ',
                    # 'ai-',
                    ] 

tag_keywords = list(tags_in_grist) + [

] 

### 


import webbrowser

### UI
# from tkinter import simpledialog
import pymsgbox
# import pymsgbox.native as pymsgbox

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

def add_to_grist(name, url, summary, app_type, category, tags, slug, domain):
    grist_PE.Apps.add_records('Master', [
                                    {   'name': name,
                                        'url': url,
                                        'status': 'radar',
                                        'summary': summary,
                                        'type': app_type,
                                        'category': category,
                                        'tags': tags,
                                        'slug': slug,
                                        'domain': domain,
                                        }
                                ])

def find_category(text):
    category_list = ['L']
    for keyword in category_keywords:
        if keyword.lower() in text.lower():
            category_list.append(keyword.lower())
    return category_list


def find_tags(text):
    tags_list = ['L']
    for keyword in tag_keywords:
        if keyword.lower() in text.lower():
            tags_list.append(keyword.lower())
    return tags_list

### Main

def add_app(text, v=v):
    url = cleanurl(text.strip())
    if url.startswith('http'):
        print(f"{get_linenumber()} {url=}")

        name = ''
        summary = ''
        logo = ''
        category = ['L']
        tags = ['L']

        domain = domain_from_url(url)
        slug = domain_name_from_url(url)
        app_type = 'SaaS'
        if v:
            print(f"\n{get_linenumber()} {url=}")
            print(f"{get_linenumber()} {domain=}")
            print(f"{get_linenumber()} {slug=}")
            print(f"{get_linenumber()} {app_type=}")
        

        # download logo
        clearbit_path = f"https://logo.clearbit.com/{domain}"
        print(f"\nLOGO\ndownloading for {domain} with {clearbit_path}")
        time.sleep(1)
        logo = requests.get(clearbit_path)
        logo_path = f"/Users/nic/Python/homee/notes/content/images/logos/{slug}.png"
        if v:
            f"#{get_linenumber()} {logo_path=}"
        open(logo_path, "wb").write(logo.content)
        print(f"downloaded at {logo_path}\n")
        # # prep for upload to Grist
        # response = requests.post(
        #     f"https://docs.getgrist.com/api/docs/{doc_id}/attachments",
        #     files={"upload": open(logo_path, "rb")},
        #     headers={"Authorization": f"Bearer {api_key}"},
        # )
        # if v:
        #     f"#{get_linenumber()} {response=}"
        # attachment_id = response.json()[0]
        # logo = ["L", attachment_id]
        # if v:
        #     f"#{get_linenumber()} {logo=}"

        if domain not in existing_domains:

            try:
                html = request.urlopen(url).read().decode('utf8')
                # if v:
                #     print(f"\n{html=}")

                try:
                    soup = BeautifulSoup(html, "html.parser")
                    # if v:
                    #     print(f"\n{soup=}")

                    try:
                        title = soup.title.text
                        if '\n' in title:
                            title = title.replace('\n', ' ').strip()
                        if v:
                            print(f"\n{get_linenumber()} {title=}")

                        try:
                            header = soup.find('h1').text
                            if '\n' in header:
                                header = header.replace('\n', ' ').strip()
                            if v:
                                print(f"{get_linenumber()} {header=}")
                            if header in title:
                                header = domain
                            if not test:
                                name = title
                                if test:
                                    print(f"{get_linenumber()} {name=}")
                                summary = header
                                if test:
                                    print(f"{get_linenumber()} {summary=}")
                                text = f"{name} {summary}"
                                category = find_category(text)
                                if test:
                                    print(f"{get_linenumber()} {category=}")
                                tags = find_tags(text)
                                if test:
                                    print(f"{get_linenumber()} {tags=}")
                                # add_to_grist(name, url, summary, app_type, category, tags, slug, domain, logo)

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
            print(f"{app_type=}")
            print(f"{category=}")
            print(f"{tags=}")
            print(f"{slug=}")
            # print(f"{logo=}")
            print(f"{domain=}\n\n")
            print(f"line {get_linenumber()} passed.")

            add_to_grist(name, url, summary, app_type, category, tags, slug, domain)

            if not test:
                webbrowser.get('chrome').open_new_tab(f'https://nic.getgrist.com/v7AKnANHVBxd/Apps')

    else:
        print(f"\n{url} is NOT a URL.")
        pymsgbox.alert(f"\n{url} is NOT a URL.")
        

    

text = clipboard_get()
print(f"\nProcessing:\n{repr(text)}\n")

add_app(text)

run_time = round((time.time() - start_time), 1)
print(f'finished in {run_time}s.\n')