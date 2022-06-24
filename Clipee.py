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

d = datetime.now()


date = d.strftime('%Y%m%d-%H%M%S')


def cleanurl(url: str) -> str:
    from urllib.parse import urlparse
    purl = urlparse(url)
    scheme = purl.scheme + '://' if purl.scheme else ''
    return f'{scheme}{purl.netloc}{purl.path}'


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


text = clipboard_get()

if "vimeo.com" in text:
    print(f'\nInput Vimeo: {type(text)}, {text}')
    src = re.search(r'(?<=src=").*?(?=[\?"])', text)
    text = src[0]
    write_to_clipboard(text)
    print(f'\nOutput: {text}\n')
# elif "https://cdn-akamai.6connex.com" in text:

elif 'fantastical' in text:
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
    print(f'\nInput Mailto: {type(text)}, {text}')
    text = text.replace('mailto:', '').strip()
    write_to_clipboard(text)
    print(f'\nOutput: {text}\n')

elif "?" in text:
    print(f'\nInput URL with query params: {type(text)}, {text}')
    short_url = cleanurl(text)
    write_to_clipboard(short_url)
    print(f'\nOutput: {short_url}\n')

elif "." in text:
    print(f'\nInput Long URL: {type(text)}, {text}')
    tsd, td, tsu = extract(text)  # prints abc, hostname, com
    domain = td + '.' + tsu  # will prints as hostname.com
    write_to_clipboard(domain)
    print(f'\nOutput domain: {domain}\n')

elif ".gif" in text:
    print(f'\nInput code with .gif: {type(text)}, {text}')
    print('Download Starting...')
    url = text
    r = requests.get(url)
    # this will take only -1 splitted part of the url
    filename = f'/Users/nicolas/Dropbox/GIF/{date}.gif'

    with open(filename, 'wb') as output_file:
        output_file.write(r.content)
        print('Download Completed!!!')

elif '(Event Time Zone)' in text:
    text = text.replace(' (Event Time Zone)', '')
    write_to_clipboard(text)
    print(f'\nOutput: {text}\n')

    # write_to_clipboard(text)
    # print(f'\nOutput: {text}\n')

# Add logic to download GIF from Giphy embed code
# elif "giphy.com" in text:

#     pattern = re.compile('src="(.+)')
#     url =

#     soup = BeautifulSoup(open(
#         f'{directoryStr}/{filename}'), "html.parser")

#     url = text
#     r = requests.get(url)
#     # this will take only -1 splitted part of the url
#     filename = f'/Users/nicolas/Dropbox/GIF/{date}.gif'

#     with open(filename, 'wb') as output_file:
#         output_file.write(r.content)
#         print('Download Completed!!!')
