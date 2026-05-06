# Copy URL from active Chrome tab and add to indexall inbox

import sys
sys.path.append("/Users/nic/Python/indeXee")

from pync import Notifier
import my_utils

INBOX_FILE = "/Users/nic/lab/indexall/inbox.md"
INSERT_LINE = 5


def insert_url_to_inbox(url):
    if not url.startswith("http"):
        Notifier.notify(
            title="FAIL",
            message=f"🔴🔴🔴 NOT A URL: {url}",
        )
        return

    with open(INBOX_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entry = f"- {url}\n"

    if entry in lines:
        Notifier.notify(
            title="DUPLICATE",
            message=f"🟡 Already in inbox: {url}",
        )
        return

    lines.insert(INSERT_LINE, entry)

    with open(INBOX_FILE, "w", encoding="utf-8") as f:
        f.writelines(lines)

    Notifier.notify(
        title="SUCCESS",
        message=f"🟢 Added to indexall inbox:\n{url}",
    )


if __name__ == "__main__":
    url = my_utils.get_chrome_active_tab_url()

    Notifier.notify(
        title="COPIED",
        message=f"{url}",
    )

    insert_url_to_inbox(my_utils.clean_url(url))
