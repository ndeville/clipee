from pandas.io.clipboard import clipboard_get
import subprocess
from datetime import datetime
import time
import subprocess   

import os

from dotenv import load_dotenv
load_dotenv()
PATH_PASTED_CLIPBOARD_FILE = os.getenv("PATH_PASTED_CLIPBOARD_FILE")

start_time = time.time()

d = datetime.now()

date = d.strftime('%Y%m%d-%H%M%S')

### Functions

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD\n")

def clipee_atom(text, v=False):

    file_path = f"{PATH_PASTED_CLIPBOARD_FILE}{date}.txt"

    with open(file_path, 'w') as file:
        file.write(text)

    # path_to_atom = '/Applications/Atom.app'
    path_to_sublime = '/Applications/Sublime Text.app'
    path_to_file = 'file_path'

    subprocess.call([path_to_sublime, path_to_file])
    
text = clipboard_get()
print(f"\nProcessing: {repr(text)}\n")

clipee_atom(text)