import requests
import urllib.request
import os
import sys
from pathlib import Path
import lxml.html

def download_podcast(directory, url_path):
    '''
    accepts path of podcast episode, and {directory} for download
    downloads the mp3 file to local machine in specified dir.
    '''
    full_url = f"https://dev.to/{url_path}"
    res = requests.get(full_url)

    if res.status_code != 200:
        print(f"Status Code: {res.status_code} for {full_url}")
        exit(1)

    tree = lxml.html.fromstring(res.text)
    for element in tree.xpath("//*[@src]"):
        if element.attrib['src'][-3:] == "mp3":
            mp3_url = element.attrib['src']

    if not mp3_url:
        print(f"MP3 URL not found")

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    return urllib.request.urlretrieve(full_url, f"{directory}/{url_path}")


def create_dir(directory):
    '''
    Attempts to save the downloaded podcast file to the location {directory}
    '''

    if not os.path.exists(directory):
        os.system(f"mkdir -p {directory}")


if __name__ == "__main__":
    # print(len(sys.argv))
    directory = os.path.expanduser("~/podcasts/mp3_files")
    print(directory)
    create_dir(directory)
    podcast_name, episode_name = os.path.split(sys.argv[1]) 
    if podcast_name != None:
        create_dir(directory + "/" + podcast_name)

    download_podcast(directory, sys.argv[1])

