
import requests
import urllib.request
import os
from pathlib import Path

# WIP
def download_podcast(url_path, destination):
    '''
    accepts path of podcast episode, and destination for download
    downloads the mp3 file to local machine in specified dir.
    '''
    full_url = f"https://dev.to/{url_path}"

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agen', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(full_url, destination)


url_path = "/iphreaks/ips-292-evolving-apps-and-hacking-around-with-eric-crichlow"

directory = os.path.expanduser("~/mp3_files")

if not os.path.exists(directory):
    print("Directory does not exist. Creating...")
   #  os.mkdir(os.path.expanduser("~/Desktop/downloaded"))

    os.system(f"mkdir {directory}")
else:
    print("Directory does exist.")

download_podcast(url_path, f"{directory}/test_file.mp3")
