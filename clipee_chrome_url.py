"""
Copy URL from Chrome
"""

import subprocess

def set_clipboard_value(value):
    # Use subprocess to call the pbcopy command on macOS to set the clipboard value
    subprocess.run("pbcopy", universal_newlines=True, input=value)

def get_chrome_active_tab_url():
    try:
        script = '''
        tell application "Google Chrome"
            set activeTabUrl to URL of active tab of front window
            return activeTabUrl
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        url = result.stdout.strip()
        print(f"\n🚹  Active tab URL: {url}")
        return url
    except Exception as e:
        print(f"Error: {e}")
        return None

active_tab_url = get_chrome_active_tab_url()

if active_tab_url.endswith('/'):
    active_tab_url = active_tab_url[:-1]

set_clipboard_value(active_tab_url)