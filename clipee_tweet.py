# Tweet from clipboard 

from operator import mul
from pandas.io.clipboard import clipboard_get
import os
import time
start_time = time.time()

from dotenv import load_dotenv
load_dotenv()

# bearer_token = os.getenv("TOKEN")

import tweepy
import webbrowser

# from tkinter import simpledialog
import pymsgbox

# credentials
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# authentication of consumer key and secret
auth = tweepy.OAuthHandler(api_key, api_secret)
# authentication of access token and secret
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

import pprint
pp = pprint.PrettyPrinter(indent=4)


def char_count(text):
    '''
    What IS Counted:
    - any character in the text of your post, including spaces
    - emojis (1 emoji registers as 2 characters)
    - hashtags
    - Twitter handles (when mentioning an account)
    - Links
    
    What IS NOT Counted:

    - visual content (images, GIFs, and videos)
    - polls
    Quote Tweets
    Twitter handles (only when you are replying to a Tweet)
    '''

multimedia_extensions = (
    'jpg', 
    'png',
    'gif',
)

def tweet(text, v=False):

    try:

        multimedia = False

        char_count = len(text)

        if char_count < 280:

            parts = text.split('\n')
            print()
            print(f"\nParts:")
            print(parts)
            print(len(parts))
            print()
            for part in parts:
                part = part.strip()
                print()
                print(f"{part=}")
                # if part.startswith('http') and part.endswith('jpg'):
                if part.startswith('/Users') and part.endswith(multimedia_extensions):
                    multimedia = True
                    image_path = part
                    text = text.replace(image_path, '') # remove the path URL from the tweet text
                    print(f"\n{image_path=}\n")

            if multimedia:
                approval = pymsgbox.prompt(f"Sure? {char_count} characters\n\nReady to send WITH IMAGE attached:\n\n{text}\n\nReally?\n(y to confirm)")
            else:
                approval = pymsgbox.prompt(f"Sure? {char_count} characters\n\nReady to send:\n\n{text}\n\nReally?\n(y to confirm)")

            if approval == 'y':

                if multimedia:
                    api.update_status_with_media(text, image_path)
                else:
                    api.update_status(status=text)
                
                webbrowser.get('chrome').open_new_tab(f'https://twitter.com/ndeville')
            else:
                m = f"NOT SENDING - {char_count} characters"
                print(m)
                pymsgbox.alert(m)
        else:
            m = f"ALERT: NOT SENDING - {char_count} characters"
            print(m)
            pymsgbox.alert(m)

    except Exception as e:
        m = f"ERROR: {e}"
        print(m)
        pymsgbox.alert(m)

text = clipboard_get()
print(f"\nProcessing:\n{repr(text)}\n")

tweet(text)

run_time = round((time.time() - start_time), 1)
print(f'finished in {run_time}s.\n')