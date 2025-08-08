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



def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))
    print(f"\nOUTPUT COPIED TO CLIPBOARD: {output}\n")

import re

def clean_markdown(text):
    print("Processing as MARKDOWN CLEANING...\n")

    # Process line by line to preserve empty lines
    lines = text.split('\n')
    processed_lines = []
    
    for line in lines:
        # Skip processing empty lines
        if not line.strip():
            processed_lines.append(line)
            continue
            
        # Remove bold and italic markers
        line = re.sub(r'\*\*.*?\*\*|\*.*?\*|__.*?__|_.*?_', lambda m: m.group(0).strip('*_'), line)
        
        # Remove headers but keep content
        line = re.sub(r'^\s*#+\s*(.*)$', r'\1', line)
        
        # Remove inline code while preserving content
        line = re.sub(r'`([^`]+)`', r'\1', line)
        
        # Completely remove [oai...] links
        line = re.sub(r'\[oai[^\]]*\]\([^)]*\)', '', line)

        # Remove other links and images while keeping text/alt text
        line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)  # Regular links
        line = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', line)  # Images
        
        # Remove blockquotes but preserve text
        line = re.sub(r'^>\s?', '', line)

        # Remove "• "
        line = re.sub(r'^•\s?', '', line)
        
        # Preserve horizontal rules
        line = re.sub(r'^\s*[-*]{3,}\s*$', '---', line)
        
        # Handle lists
        line = re.sub(r'^\s*\d+\.\s+', '- ', line)  # Convert numbered lists to dashes
        line = re.sub(r'^\s*[+*]\s+', '- ', line)   # Convert other list markers to dashes
        
        processed_lines.append(line)

    # Handle code blocks separately to preserve spacing
    text = '\n'.join(processed_lines)
    text = re.sub(r'```.*?\n(.*?)```', r'\n\1', text, flags=re.DOTALL)
    
    # Preserve original line endings without collapsing
    return text

def main():
    try:
        text = clipboard_get()
        print(f"\nProcessing:\n{text}\n")
        cleaned_text = clean_markdown(text)
        write_to_clipboard(cleaned_text)
        print("Cleaning complete!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()




