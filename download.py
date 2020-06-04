
import requests
import urllib.request
import os
import sys
from pathlib import Path

directory = os.path.expanduser("~/mp3_files")

# custom_path = print(sys.argv)[1]
# print(f"custom path: {custom_path}")

url_path = "/iphreaks/ips-292-evolving-apps-and-hacking-around-with-eric-crichlow"  # This will come from the ZSH

def download_podcast(url_path):
    '''
    accepts path of podcast episode, and {directory} for download
    downloads the mp3 file to local machine in specified dir.
    '''
    full_url = f"https://dev.to/{url_path}"

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agen', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    return urllib.request.urlretrieve(full_url, f"{directory}/test-file.mp3") # CHANGE IT LATER


def create_dir():
    '''
    Attempts to save the downloaded podcast file to the location {directory}
    '''

    if not os.path.exists(directory):
        print("Directory does not exist. Creating...")
        os.system(f"mkdir {directory}")
    else:
        print("Directory does exist.")


create_dir()
print(download_podcast(url_path))

# zsh podcast.zsh https://dev.to/iphreaks/ips-292-evolving-apps-and-hacking-around-with-eric-crichlow ./my_custom_dir