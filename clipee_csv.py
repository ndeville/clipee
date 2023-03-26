'''
CLIPEE CSV
CSV HEADERS TO PYTHON
Input: path to .csv file
Output: python row code for headers
'''

from pandas.io.clipboard import clipboard_get
import subprocess

import time
start_time = time.time()

import csv
import pymsgbox
import os

# pymsgbox.alert(f"Starting {os.path.basename(__file__)}...")

count_col_csv = 0

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD\n")

def process_csv(text, v=False):
    global count_col_csv

    headers = ''

    try:

        path_to_csv = text.strip()
        if path_to_csv.startswith('/Users'):
            
            with open(path_to_csv, 'r', newline='', encoding='UTF-8') as h:
                reader = csv.reader(h, delimiter=",")
                header_row = list(reader)[0]

                count_for = -1

                for title in header_row:
                    count_col_csv += 1
                    count_for += 1
                    title = title.lower()
                    if ' ' in title:
                        title = title.replace(' ', '_').lower()
                    if '/' in title:
                        title = title.replace('/', '_').lower()
                    print(f"{title} = row[{count_for}]\n")

                    headers = headers + f"{title} = row[{count_for}]\n"

        write_to_clipboard(headers)

        pymsgbox.alert(f"SUCCESS\nCopied to clipboard: {headers}")

    except Exception as e:
        pymsgbox.alert(f"ERROR: {e}")

text = clipboard_get()

print(f"\nProcessing: {repr(text)}\n")

process_csv(text)