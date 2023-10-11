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

list_headers = text.split('\t')

count = -1

print_string = 'print('

for header in list_headers:
    count += 1
    header = str(header.lower())

    if '/' in header:
        header = header.replace('/', '_')
    if 'first' in header:
        header = 'first'
    if 'last' in header:
        if not 'activity' in header and not 'seen' in header:
            header = 'last'
    if 'title' in header:
        header = 'title'
    if 'phone' in header:
        header = 'phone'

    header = header.replace(' ', '_')

    x = header

    # if any(ele in header.lower() for ele in ['date', 'found', 'twitter', 'linkedin', 'country']):
    #     header = f"{header} = row[{count}].value"
    # else:
    #     header = f"{header} = row[{count}].value.strip()"
    header = f"{header} = row[{count}].value"

    if output == '':
        output = f"{header}"
    else:
        output = f"{output}\n{header}"
    print_string = f"{print_string}{x}, "

print_string = f"{print_string})"

output = f"{output}\n\n{print_string}"

write_to_clipboard(output)

# keyb = Controller()
# with keyb.pressed(Key.cmd):
#     keyb.press('f')
#     keyb.release('f')

# print(f'\nOutput copied to clipboard:\n\n{output}\n')
print(f'\nOutput copied to clipboard')

print()

###
