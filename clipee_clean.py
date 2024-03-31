from pandas.io.clipboard import clipboard_get
import re
import subprocess
from urllib.parse import urlparse
from tldextract import extract
import requests
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib import request
import tldextract
from inspect import currentframe
import string

import sys
sys.path.append("/Users/nic/Python/indeXee")
import grist_PE

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

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

### Functions

def cleanurl(url: str) -> str:
    from urllib.parse import urlparse
    purl = urlparse(url)
    scheme = purl.scheme + '://' if purl.scheme else ''
    return f'{scheme}{purl.netloc}{purl.path}'


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD: {output}\n")


do_not_clean = [
    'ycombinator',
]

def html_for_note(text, v=False):
    url = text.strip()
    if not any(ele in url for ele in do_not_clean):
        url = cleanurl(text)
    domain = domain_from_url(url)
    domain_name = domain_name_from_url(url)
    if v:
        print(f"\n{url=}")

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

                # print("\nTitle : ",title)

                # headerlist = soup.find_all(re.compile('^h[1-6]'))
                # print("\nHeaders : ")
                # for header in headerlist:
                #     print(header.text)

                try:
                    header = soup.find('h1').text
                    if '\n' in header:
                        header = header.replace('\n', ' ').strip()
                    if v:
                        print(f"{header=}")
                    if header in title:
                        header = domain
                    output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://logo.clearbit.com/{domain}?size=35\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{title}</div>\n<div class=\"link_tagline\">{header}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"

                except Exception as e:
                    print(f"\nheader ERROR: {e}")
                    print(f"NO Header found, returning with Title only")
                    output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://logo.clearbit.com/{domain}?size=35\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{title}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"

                # print(f"{header=}")

                # output = f"<div class=\"link_border\">\n<div class=\"link_title\">{title}</div>\n<div class=\"link_title\">{header}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div>\n"
                print(f'\nOutput:\n--------\n{output}--------\n')
                write_to_clipboard(output)
            
            except Exception as e:
                print(f"\ntitle ERROR: {e}\nReturning empty div:")
                output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://logo.clearbit.com/{domain}?size=35\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
                print(f'\nOutput:\n--------\n{output}--------\n')
                write_to_clipboard(output)

        except Exception as e:
            print(f"\soup ERROR: {e}\nReturning empty div:")
            output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://logo.clearbit.com/{domain}?size=35\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
            print(f'\nOutput:\n--------\n{output}--------\n')
            write_to_clipboard(output)

    except Exception as e:
        print(f"\nhtml ERROR: {e}\nReturning empty div:")
        output = f"<div class=\"link_border\"><div class=\"link_logo_box\"><img class=\"link_logo\" src=\"https://logo.clearbit.com/{domain}?size=35\" alt=\"logo\"/></div><div class=\"link_content\">\n<div class=\"link_title\">{domain}</div>\n<div class=\"link_tagline\">{domain}</div>\n<div class=\"link_url\"><a href=\"{url}\" target=\"_blank\">{url}</a></div></div></div>\n"
        print(f'\nOutput:\n--------\n{output}--------\n')
        write_to_clipboard(output)

### Switches

def clipee_processing(text):
    global sep

    if "vimeo.com" in text:
        print(f"{sep}\nProcessing as VIMEO LINK EXTRACTION...")
        print(f'\nInput Vimeo: {type(text)}, {text}')
        src = re.search(r'(?<=src=").*?(?=[\?"])', text)
        text = src[0]
        write_to_clipboard(text)
        print(f'\nOutput: {text}\n')
    # elif "https://cdn-akamai.6connex.com" in text:

    elif 'fantastical' in text:
        print(f"{sep}\nProcessing as FANTASTICAL DATE LIST...")
        o = urlparse(text)
        uid = f'{o.path}'.replace('/p/', "")
        url = f'https://hub.flexibits.com/scheduling/public/{uid}/'
        html = requests.get(url).text
        soup = BeautifulSoup(open(html), "html.parser")
        name = soup.find(
            'div', class_='TimePicker_timePicker__5yclN')
        count = 0
        for div in name:
            count += 1
            div_name = ''
            for span in div:
                slot = span.find_all('span')
                slot = list(slot)
                join = ": ".join(map(str, slot)).replace(
                    '<span>', "").replace('</span>', "").replace(',', "")
                if join != '':
                    paste = f'{count}) {join}'
                    print(paste)
        print()

    elif "mailto" in text:
        print(f"{sep}\nProcessing as MAILTO CLEANING...\n")
        print(f'\nInput Mailto: {type(text)}, {text}')
        text = text.replace('mailto:', '').strip()
        write_to_clipboard(text)
        print(f'\nOutput: {text}\n')

    # elif "." in text:
    #     print(f'\nInput Long URL: {type(text)}, {text}')
    #     tsd, td, tsu = extract(text)  # prints abc, hostname, com
    #     domain = td + '.' + tsu  # will prints as hostname.com
    #     write_to_clipboard(domain)
    #     print(f'\nOutput domain: {domain}\n')

    elif ".gif" in text:
        print(f"{sep}\nProcessing as GIF DOWNLOAD...\n")
        print(f'\nInput code with .gif: {type(text)}, {text}')
        print('Download Starting...')
        url = text
        r = requests.get(url)
        # this will take only -1 splitted part of the url
        filename = f'/Users/nic/Dropbox/GIF/{date}.gif'

        with open(filename, 'wb') as output_file:
            output_file.write(r.content)
            print('Download Completed!!!')

    elif '(Event Time Zone)' in text:
        print(f"{sep}\nProcessing as TIMEZONE CLEANING...\n")
        text = text.replace(' (Event Time Zone)', '')
        write_to_clipboard(text)
        print(f'\nOutput: {text}\n')

    elif 'nic@NicolasacStudio' in text:
        print(f"{sep}\nProcessing as TERMINAL CLEANING...")
        text = text.replace('nic@NicolasacStudio', 'xxx@yyy')
        if '/Users/nic/' in text:
            text = text.replace('/Users/nic/', '/Users/xxxx/')
        print(f"\n{text=}\n")
        write_to_clipboard(text)

    elif '/Users/nic/' in text:
        print(f"{sep}\nProcessing as TERMINAL CLEANING...")
        text = text.replace('/Users/nic/', '/Users/xxxx/')
        print(f"\n{text=}\n")
        write_to_clipboard(text)

    elif '>>> ' in text:
        print(f"{sep}\nProcessing as CLEANING '>>'>...")
        text = text.replace('>>> ', '')
        print(f"\n{text=}\n")
        write_to_clipboard(text)

    elif text.strip().startswith('https://www.leaf'):
        print(f"{sep}Processing as LEAF LINK...\n")

        existing_leaf_links = [x.leaf for x in grist_PE.Strains.fetch_table('Master')]

        if text.strip() not in existing_leaf_links:

            name_raw = text.replace('https://www.leafly.com/strains/', '')
            if '-' in name_raw:
                name_raw = name_raw.replace('-', ' ')
            name = string.capwords(name_raw, sep=None)

            grist_PE.Strains.add_records('Master', [
                                            {   'leaf': text.strip(),
                                                'name': name,
                                                }
                                        ])
            print(f"\n+++\n{text.strip()} ADDED to Grist\n+++\n\n")
        else:
            print(f"---\nLeaf link ALREADY in Grist\n---\n\n")

    elif "nicolas.mediaspace.kaltura.com" in text:
        k_parts = text.split('/')
        for k in k_parts:
            if k.startswith('1_'):
                text = f"https://nicolas.mediaspace.kaltura.com/media/{k}"
        write_to_clipboard(text)

    elif (text.startswith("http") and "?" in text):
        print(f"{sep}\nProcessing as URL CLEANING...\n")
        print(f'\nInput URL with query params: {type(text)}, {text}')
        short_url = cleanurl(text)
        write_to_clipboard(short_url)
        print(f'\nOutput short URL: {short_url}\n')
    
    elif "\n" in text:
        print(f"{sep}\nProcessing as BREAKLINES CLEANING...\n")
        print(f'\nInput URL with query params: {type(text)}, {text}')
        clean_text = text.replace('\n', ' ')
        write_to_clipboard(clean_text)
        print(f'\nOutput short URL: {clean_text}\n')

    elif ("@" in text and ">" in text):
        print(f"{sep}\nProcessing as EMAIL CLEANING...\n")
        print(f'\nInput Email: {type(text)}, {text}')
        email = text.split('<')[1].replace('>', '')
        write_to_clipboard(email)
        print(f'\nOutput Email: {email}\n')

    elif text.startswith("+"):
        if '-' in text:
            text = text.replace('-', '')
        if '.' in text:
            text = text.replace('.', '')
        if '(' in text:
            text = text.replace('(', '')
        if ')' in text:
            text = text.replace(')', '')
        if ' ' in text:
            text = text.replace(' ', '')
        write_to_clipboard(text)

    else:
        print(f"\nNO LOGIC identified for this text.")

text = clipboard_get()
print(f"\nProcessing: {repr(text)}\n")

clipee_processing(text)

while count_url < 1000:
    print(f"[CLIPEE] Want to process another?...\n")
    valid = False
    new_url = input(f'Enter new URL: ')
    clipee_processing(new_url)