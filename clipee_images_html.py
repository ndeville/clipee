'''
Complement script to the "Generate HTML snippet for last image" Hazel rule. 
- get full URL from Hazel
- generate HTML snippet
- copy HTML to clipboard
'''

import subprocess
import sys


def generate_short_path(filepath, v=False, test=False):
    if filepath.startswith('/Users/nic/Python/homee/notes/content/images/') and '/logos/' not in filepath:
        filepath = filepath.replace('/Users/nic/Python/homee/notes/content/images/', '')
    return filepath
    
def generate_html_snippet(short_filepath, v=False, test=False):

    html_snippet = f"<img class=\"screenshot\" src=\"https://notes.nicolasdeville.com/images/{short_filepath}\" alt=\"{short_filepath}\"/>"  

    return html_snippet


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD\n")


def process(filepath, v=False, test=False):

    short_path = generate_short_path(filepath)

    output = generate_html_snippet(short_path)

    write_to_clipboard(output)


if __name__ == '__main__':
    filepath = sys.argv[1] # get filepath from Hazel
    process(filepath)    