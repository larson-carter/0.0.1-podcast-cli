
import requests
import urllib.request
import os

# WIP
def download_podcast(url_path, destination):
    '''
    accepts path of podcast episode, and destination for download
    downloads the mp3 file to local machine in specified dir.
    '''
    full_url = f"https://dev.to/{url_path}"
    # headers={'User-Agent': 'Mozilla/5.0'}
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agen', 'Mozilla/5.0')]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(full_url, destination)


url_path = "/iphreaks/ips-292-evolving-apps-and-hacking-around-with-eric-crichlow"

os.mkdir("./test_py_download")
download_podcast(url_path, './test_py_download/test.mp3')
