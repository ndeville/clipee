'''
Complement script to the "Screenshot IINA" Apple Shortcuts. 
- moves file to notes folder
- renames file
- copy HTML to clipboard
'''

import subprocess
from inspect import currentframe
import os

import time
start_time = time.time()

import sys
import pymsgbox

output_folder = '/Users/nic/Python/homee/notes/content/images'

### Functions

def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD\n")

def process_iina_screenshot(filepath, v=False, test=False):
    if test:
        pymsgbox.alert(f"\nStarting process_iina_screenshot with {filepath}\n")

    image_path = filepath.replace(output_folder, '')[1:]
    if v:
        pymsgbox.alert(f"\n{image_path=}")
    if image_path not in [None, 'None', '']:

        image_name = image_path.split('.')[0]
        if image_name.endswith('-'):
            image_name.replace('-', '')
        if v:
            pymsgbox.alert(f"\n{image_name=}")

        output = f"<img class=\"screenshot\" src=\"https://notes.nicolasdeville.com/images/{image_path}\" alt=\"{image_name}\"/>"  
        if v:
            pymsgbox.alert(f"\n{output=}")
        
        write_to_clipboard(output)

run_time = round((time.time() - start_time), 1)
print(f'finished in {run_time}s.\n')


########################################################################################################

if __name__ == '__main__':
    print()
    filepath = sys.argv[1]
    # process_iina_screenshot(filepath, v=True, test=True)    
    process_iina_screenshot(filepath)    
    print()
    print('-------------------------------')
    print(f"{os.path.basename(__file__)}")
    print()
    run_time = round((time.time() - start_time), 1)
    if run_time > 60:
        print(f'{os.path.basename(__file__)} finished in {run_time/60} minutes.')
    else:
        print(f'{os.path.basename(__file__)} finished in {run_time}s.')
    print()