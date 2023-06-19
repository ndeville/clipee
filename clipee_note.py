# from pandas.io.clipboard import clipboard_get
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
sys.path.append(f"/Users/nic/Python/metaurl")


from get.soup import without_js_rendering, with_js_rendering

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

    logos_folder = "/Users/nic/Python/homee/notes/content/images/logos"
    logo_path = os.path.join(logos_folder, f"{domain_name}.png")

    if os.path.exists(logo_path):
        print(f"Logo for {domain} already exists at {logo_path}")
    else:
        print(f"Downloading logo for {domain}...")
        response = requests.get(f"https://logo.clearbit.com/{domain}")
        
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

def html_for_note(text, v=False):
    url = text.strip()

    if url.startswith('http'):

        domain = domain_from_url(url)
        domain_name = domain_name_from_url(url)
        if v:
            print(f"\n{url=}")
            print(f"{domain=}")
            print(f"{domain_name=}")

        download_logo(domain, domain_name)

        # try:
        #     html = request.urlopen(url).read().decode('utf8')
        #     if v:
        #         print(f"\n{html=}")

        try:
            # soup = BeautifulSoup(html, "html.parser")

            soup = without_js_rendering(url).soup

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

                print(f'\nOutput:\n\n{output}\n')
                write_to_clipboard(output)
                paste()
            
            except Exception as e:
                print(f"\ntitle ERROR: {e}\nReturning empty div:")
                output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
                print(f'\nOutput:\n{output}\n')
                write_to_clipboard(output)
                paste()

        except Exception as e:
            print(f"\soup ERROR: {e}\nReturning empty div:")
            output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
            print(f'\nOutput:\n\n{output}\n')
            write_to_clipboard(output)
            paste()

        # except Exception as e:
        #     print(f"\nhtml ERROR: {e}\nReturning empty div:")
        #     output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
        #     print(f'\nOutput:\n\n{output}\n')
        #     write_to_clipboard(output)
        #     paste()


# text = clipboard_get()
text = get_clipboard_content()


print(f"\nProcessing: {repr(text)}\n")

html_for_note(text)

run_time = round((time.time() - start_time), 3)
print(f'finished in {run_time}s.\n')


