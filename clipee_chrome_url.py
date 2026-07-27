"""
Copy URL from Chrome
"""

import subprocess
import sys

from chrome_tab import get_chrome_active_tab_url

def set_clipboard_value(value: str) -> None:
    subprocess.run("pbcopy", universal_newlines=True, input=value)

def main() -> int:
    url = get_chrome_active_tab_url()
    if url is None:
        return 1

    url = url.rstrip('/')
    set_clipboard_value(url)
    print(f"\n✅  Active tab URL: {url}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
