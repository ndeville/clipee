from pandas.io.clipboard import clipboard_get
import subprocess
from datetime import datetime
import time
import subprocess    

start_time = time.time()

d = datetime.now()

date = d.strftime('%Y%m%d-%H%M%S')

### Functions

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD\n")

def clipee(text, v=False):

    print()

    if '\"' in text:
            text = text.replace('\"', '\\"')

    parts = text.split('\n')

    for part in parts:

        print(f'"{part}",',)

        # TODO write_to_clipboard
        # right now, just copy/paste from print


text = clipboard_get()
print(f"\nProcessing: {repr(text)}\n")

clipee(text)

run_time = round((time.time() - start_time), 1)
print(f'\n\nfinished in {run_time}s.\n')
