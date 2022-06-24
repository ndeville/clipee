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


text = clipboard_get()

output = str()

print()

list_values = text.split('\n')

count = -1

output = 'list_values = ['

for row in list_values:
    count += 1
    if row not in [None, '', '\r']:
        if '\r' in row:
            row = row.replace('\r', '')
        output = output + repr(row) + ', '

output = output + ']'

print(output)
print()

write_to_clipboard(output)

print(f'\nOutput copied to clipboard')

print()

###
