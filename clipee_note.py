from pandas.io.clipboard import clipboard_get
import subprocess
from tldextract import extract
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib import request
import tldextract

# for pasting
from pynput.keyboard import Key, Controller
keyb = Controller()

# from inspect import currentframe
# import string
# from urllib.parse import urlparse
# from urllib.parse import urlparse
# from datetime import date
# import re

import time
start_time = time.time()

# import sys
# sys.path.append("/Users/nic/Python/indeXee")
# import grist_PE

d = datetime.now()

date = d.strftime('%Y%m%d-%H%M%S')

count_url = 0

def separator(count=50, lines=3, symbol='='):
    separator = f"{symbol * count}" + '\n'
    separator = f"\n{separator * lines}"
    print(separator)

sep = separator()

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

# def get_linenumber():
#     cf = currentframe()
#     return cf.f_back.f_lineno

### Functions

# 220927 stop cleaning URLs
# def cleanurl(url: str) -> str:
#     from urllib.parse import urlparse
#     purl = urlparse(url)
#     scheme = purl.scheme + '://' if purl.scheme else ''
#     return f'{scheme}{purl.netloc}{purl.path}'


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD\n")

def paste():
    with keyb.pressed(Key.cmd):
        keyb.press('f')
        keyb.release('f')

# 220927 stop cleaning URLs
# do_not_clean = [
#     'ycombinator',
# ]

def html_for_note(text, v=False):
    url = text.strip()

    if url.startswith('http'):

        domain = domain_from_url(url)
        domain_name = domain_name_from_url(url)
        if v:
            print(f"\n{url=}")
            print(f"{domain=}")
            print(f"{domain_name=}")

        # download logo
        print(f"\nDownloading logo for {domain}...")
        response = requests.get(f"https://logo.clearbit.com/{domain}")
        open(f"/Users/nic/Python/homee/notes/content/images/logos/{domain_name}.png", "wb").write(response.content)
        print(f"logo downloaded at images/logos/{domain_name}.png")

        try:
            html = request.urlopen(url).read().decode('utf8')
            if v:
                print(f"\n{html=}")

            try:
                soup = BeautifulSoup(html, "html.parser")
                if v:
                    print(f"\n{soup=}")

                try:
                    title = soup.title.text
                    if '\n' in title:
                        title = title.replace('\n', ' ').strip()
                    if v:
                        print(f"\n{title=}")

                    try:
                        header = soup.find('h1').text
                        if '\n' in header:
                            header = header.replace('\n', ' ').strip()
                        if v:
                            print(f"{header=}")
                        if header in title:
                            header = domain
                        output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{title}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"

                    except Exception as e:
                        print(f"\nheader ERROR: {e}")
                        print(f"NO Header found, returning with Title only")
                        output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{title}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"

                    print(f'\nOutput:\n{sep}\n{output}{sep}\n')
                    write_to_clipboard(output)
                    paste()
                
                except Exception as e:
                    print(f"\ntitle ERROR: {e}\nReturning empty div:")
                    output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
                    print(f'\nOutput:\n-{sep}\n{output}{sep}\n')
                    write_to_clipboard(output)
                    paste()

            except Exception as e:
                print(f"\soup ERROR: {e}\nReturning empty div:")
                output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
                print(f'\nOutput:\n{sep}\n{output}{sep}\n')
                write_to_clipboard(output)
                paste()

        except Exception as e:
            print(f"\nhtml ERROR: {e}\nReturning empty div:")
            output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
            print(f'\nOutput:\n{sep}\n{output}{sep}\n')
            write_to_clipboard(output)
            paste()


text = clipboard_get()
print(f"\nProcessing: {repr(text)}\n")

html_for_note(text)

run_time = round((time.time() - start_time), 1)
print(f'finished in {run_time}s.\n')

