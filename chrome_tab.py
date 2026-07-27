"""
Read the active tab URL from Chrome's front window.

Headless Chrome registers under the same bundle id as the GUI app, so Apple Events can land on a
headless instance instead of the real browser: you then get a window that is not yours, or none at
all. Hung render jobs are cleared before asking. Screenshot renders take seconds, so anything
older than STALE_AFTER_SECONDS is hung, never live work.
"""

# Keeps the str | None hints working if a hotkey runs this under the system python (3.9).
from __future__ import annotations

import subprocess
import sys
import time

STALE_AFTER_SECONDS = 300

CHROME_EXECUTABLE = 'Google Chrome.app/Contents/MacOS/Google Chrome'

URL_SCRIPT = '''
tell application "Google Chrome"
    if (count of windows) is 0 then error "no Chrome window open"
    return URL of active tab of front window
end tell
'''

def query_active_tab_url() -> tuple[str | None, str]:
    """The front window's active tab URL, plus Chrome's complaint if it would not answer."""
    result = subprocess.run(['osascript', '-e', URL_SCRIPT], capture_output=True, text=True)
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip() or None, ''

def elapsed_seconds(etime: str) -> int:
    """Convert the ps etime column ([[dd-]hh:]mm:ss) to seconds."""
    days, _, clock = etime.rpartition('-')
    seconds = 0
    for part in clock.split(':'):
        seconds = seconds * 60 + int(part)
    if days:
        seconds += int(days) * 86400
    return seconds

def is_headless_browser(command: str) -> bool:
    """True only for a headless Chrome browser process, never a helper or a script naming one."""
    index = command.find(CHROME_EXECUTABLE)
    if index < 0:
        return False
    # Chrome must be the command being run, not an argument to a script that merely names it:
    # everything before its path has to be the directory holding it.
    directory = command[:index]
    if not directory.startswith('/') or ' ' in directory:
        return False
    flags = command[index + len(CHROME_EXECUTABLE):]
    if flags and not flags.startswith(' '):
        return False
    # Renderer/GPU/zygote children carry --type=; only the browser process answers Apple Events.
    return '--headless' in flags and '--type=' not in flags

def parse_headless_pids(ps_output: str) -> tuple[list[str], list[str]]:
    """Headless Chrome PIDs from ps output, split into (hung, running) on STALE_AFTER_SECONDS."""
    hung, running = [], []
    for line in ps_output.splitlines():
        fields = line.split(maxsplit=2)
        if len(fields) < 3:
            continue
        pid, etime, command = fields
        if not is_headless_browser(command):
            continue
        if elapsed_seconds(etime) >= STALE_AFTER_SECONDS:
            hung.append(pid)
        else:
            running.append(pid)
    return hung, running

def start_process_scan() -> subprocess.Popen:
    """Start the process scan so it runs while Chrome is answering, not before."""
    return subprocess.Popen(['ps', '-Ao', 'pid=,etime=,command='],
                            stdout=subprocess.PIPE, text=True)

def kill_hung_headless(pids: list[str]) -> None:
    """Clear hung headless instances so Apple Events reach the real browser."""
    print(f"🧹 Killing {len(pids)} hung headless Chrome instance(s): {', '.join(pids)}")
    subprocess.run(['kill'] + pids)
    time.sleep(1)

def get_chrome_active_tab_url() -> str | None:
    """The active tab URL of Chrome's front window, or None if Chrome has no window to read."""
    scan = start_process_scan()
    url, error = query_active_tab_url()
    hung, running = parse_headless_pids(scan.communicate()[0])

    if hung:
        # The answer above may have come from a hung instance, so ask again once they are gone.
        kill_hung_headless(hung)
        url, error = query_active_tab_url()

    if url is None:
        print(f"❌ No URL from Chrome. Is a Chrome window open? {error}", file=sys.stderr)
        return None

    if running:
        print(f"⚠️  Headless Chrome is rendering (pid {', '.join(running)}) - URL may come from it",
              file=sys.stderr)

    return url
