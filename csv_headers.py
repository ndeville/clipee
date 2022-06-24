from pandas.io.clipboard import clipboard_get
import subprocess
from datetime import date, datetime
# from pynput.keyboard import Key, Controller

d = datetime.now()

date = d.strftime('%Y%m%d-%H%M%S')


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


file_path = clipboard_get()

import csv

csv_file = file_path

count_row_csv = 0
count_column = -1

print()
print()

with open(csv_file, 'r', newline='', encoding='UTF-8') as h:
    reader = csv.reader(h, delimiter=",")
    data = list(reader)
    for row in data:
        count_row_csv += 1
        if count_row_csv == 1:
            for col in row:
                count_column += 1

                name = col.lower()

                if name == 'last name':
                    name = 'last'
                if name == 'first name':
                    name = 'first'
                if name == 'email address':
                    name = 'email'
                if name == 'job title':
                    name = 'title'

                name = name.replace(' ', '_')

                print(f"{name} = row[{count_column}]")


print(f"\n\n^^^^ COPY ABOVE ^^^^\n\n")




# output = f"{output}\n\n{print_string}"

# write_to_clipboard(output)

# print(f'\nOutput copied to clipboard')

print()

###
