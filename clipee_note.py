# from pandas.io.clipboard import clipboard_get
import subprocess
# from tldextract import extract
# import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib import request
import tldextract
import os
# import requests

# for pasting
from pynput.keyboard import Key, Controller
keyb = Controller()

import sys
# sys.path.append(f"/Users/nic/Python/indeXee")
sys.path.append(f"/Users/nic/Python/metaurl")

import pymsgbox

from get.soup import without_js_rendering, with_js_rendering

import time
start_time = time.time()

d = datetime.now()

date = d.strftime('%Y%m%d-%H%M%S')

count_url = 0

# FUNCTIONS


def get_chrome_active_tab_url():
    try:
        script = '''
        tell application "Google Chrome"
            set activeTabUrl to URL of active tab of front window
            return activeTabUrl
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        url = result.stdout.strip()
        print(f"\n🚹  Active tab URL: {url}")
        return url
    except Exception as e:
        print(f"Error: {e}")
        return None

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
        curl_cmd = f"curl -s -o {logo_path} https://logo.clearbit.com/{domain}"
        result = subprocess.run(curl_cmd, shell=True)
        
        if result.returncode == 0:
            print(f"Logo downloaded at {logo_path}")
        else:
            print(f"Error downloading logo for {domain}. Curl returned code: {result.returncode}")


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD\n")

def paste():
    with keyb.pressed(Key.cmd):
        keyb.press('f')
        keyb.release('f')

def get_webpage_content(url):
    curl_cmd = f"curl -s -L {url}"
    result = subprocess.run(curl_cmd, shell=True, capture_output=True, text=True)
    return result.stdout

# MAIN

def html_for_note(url, v=False):
    print(f"\nℹ️  starting html_for_note for: {repr(url)}\n")

    if url.startswith('http'):
        domain = domain_from_url(url)
        domain_name = domain_name_from_url(url)
        if v:
            print(f"\nhtml_for_note with {url=}")
            print(f"{domain=}")
            print(f"{domain_name=}")

        download_logo(domain, domain_name)

        try:
            html_content = get_webpage_content(url)
            if v:
                print(f"\nHTML content length: {len(html_content)}")

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract og meta tags
            og_title = soup.find('meta', property='og:title')
            og_url = soup.find('meta', property='og:url')
            og_description = soup.find('meta', property='og:description')
            
            # Get content from og tags or fallback to other methods
            title = og_title['content'] if og_title else None
            if not title:
                title_tag = soup.find('title')
                title = title_tag.text.strip() if title_tag else domain
            
            link_url = og_url['content'] if og_url else url
            tagline = og_description['content'] if og_description else domain

            # Extract full text content
            full_text = soup.get_text(separator=' ', strip=True)

            output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{title}</div>\n<div class=\"link_tagline\">{tagline}</div>\n<div class=\"link_url\"><a href=\"{link_url}\" target=\"_blank\">{link_url}</a></div></div></div>\n"

            print(f'\nOutput:\n\n{output}\n')
            write_to_clipboard(output)
            return (output, full_text)
            
        except Exception as e:
            print(f"\nError processing webpage: {e}\nReturning empty div:")
            output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://notes.nicolasdeville.com/images/logos/{domain_name}.png\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
            if v:
                print(f'\nOutput:\n\n{output}')
            write_to_clipboard(output)
            return (output, "")

    # else:
    #     pymsgbox.alert(text=f'URL {text} does not start with http', title='❌ http?', button='OK')

if __name__ == "__main__":
    # text = get_clipboard_content()
    url = get_chrome_active_tab_url()

    html_for_note(url)

    paste()

    run_time = round((time.time() - start_time), 3)
    print(f'finished in {run_time}s.\n')




