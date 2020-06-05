import requests
import json
import random
import sys
import shutil
import os

from typing import List
from download        import download_podcast


# base_dir that stores all download images
DIR = os.path.expanduser("~/podcasts")
IMG_DIR = f"{DIR}/images"
META_DATA_PATH = f"{DIR}/metadata.json"
INFO_WIDTH = 80

class PodcastEpisode:
    '''
    Represents a single podcast episode from the dev.to API.
    '''

    id = 0
    path = None
    title = None

    def __init__(self, id, path, title):
        self.id = id
        self.path = path
        self.title = title

    def __str__(self):
        return f"(PodcastEpisode) id={self.id} , path={self.path} , title={self.title}"


def parse_podcast_data(data):
    '''
    reusable method parses podcast json data returned by Dev.to API
    returns array of PodcastEpisode objects.
    '''
    podcast_episodes = []
    if not data:
        print("data is None. Something bad happened")

    for podcast_data in data:
        podcast_episode = PodcastEpisode(
            podcast_data["id"], podcast_data["path"], podcast_data["title"].lower()
        )

        podcast_episodes.append(podcast_episode)

    return podcast_episodes


def fetch_all_podcasts():
    '''
    fetches all podcasts available (up to 1000 most recent) via Dev.to API input
    no search param included
    '''
    response = requests.get(
        "https://dev.to/api/podcast_episodes?per_page=1000")
    data = json.loads(response.text)
    return parse_podcast_data(data)


def get_metadata():
    print("[Initialization] Downloading Metadata... This will open happen once")

    map = dict()
    response = requests.get(
        f"https://dev.to/api/podcast_episodes?per_page=100000")
    data = json.loads(response.text)


    for episode in data:
        map[episode["path"]] = episode


    print(f"{len(map)} podcast episodes metadata downloaded")
    with open(META_DATA_PATH, 'w+') as fp:
        json.dump(map, fp)

    print("Download complete.")


def fetch_podcasts_by_title(username: str) -> List[PodcastEpisode]:
    '''
    Fetches a list of podcasts from the dev.to API. (up to 1000)

    Parameters
    ----------
    username - title of the whole podcast series
    '''
    username = username.strip().replace(" ", "")
    response = requests.get(
        f"https://dev.to/api/podcast_episodes?per_page=1000&username={username}")
    data = json.loads(response.text)

    return parse_podcast_data(data)


#  we can edit this to search the description as well.
#  a title search may be effective enough
#  this func returns a list.  If we want just the most recent one, we can
# invoke most_recent_podcast on the return val of this func.
def fetch_podcasts_by_keyword(keyword: str):
    '''
    accepts a string argument, key word
    returns list of PodcastEpisode object with that keyword in the title.
    '''

    keyword_title_matches = []
    podcast_episode_list = fetch_all_podcasts()

    for episode in podcast_episode_list:
        if keyword in episode.title.split():
            keyword_title_matches.append(episode)

    return keyword_title_matches


def fetch_random_podcast():
    '''
    fetches podcasts via Dev.to API call w/no search param. Returns a single
    random podcast episode from list of episodes returned by API.
    '''

    podcast_episode_list = fetch_all_podcasts()
    random_episode = random.choice(podcast_episode_list)

    return random_episode


def fetch_paginated_podcasts(page, per_page):
    '''
    fetches podcasts page by page

    - Precondition: page and per_page are integers or numeric strings
    '''

    response = requests.get(
        f"https://dev.to/api/podcast_episodes?page={page}&per_page={per_page}")
    data = json.loads(response.text)

    return parse_podcast_data(data)


def most_recent_podcast(list):
    '''
    returns most recent podcast in a list of PodcastEpisodes
    according to Dev.to response, this will be first in list
    '''
    return list[0]


def save(url_path, destination):

    '''
    This will save the downloaded podcast file to "some" directory.
    e.g mp3-files2/ like in the shell script written by The Shell Guys.
    '''
    pass


def text_format(text, width):
    ''' 
    Returns a string with a length exactly equal to width. 
    If the original text is shorter than width, spaces are appended
    If the original text is longer than width, it is truncated with ellipses

    - Precondition: width > 3
    '''
    if len(text) <= width:
        text += ' ' * (width - len(text))
    else:
        text = text[:width - 3] + "..."
        
    assert len(text) == width
    return text

def print_podcast(podcast):
    title = text_format(podcast.title, 60)
    path = podcast.path
    print(f"{title}\t{path}")


def path_to_filepath(short_path: str, img_format="jpg", base_img_dir=IMG_DIR)-> (str, str):
    """:arg
    Given a dev.to short path, returns
    (1) a folder name (so it can be created) and
    (2) the relative full filepath.

    Given path = "/elixirmix/emx-095-adopting-elixir-at-findhotel-with-fernando-hamasaki-de-amorim"
    Returns
    ('./images/elixirmix',
    './images/elixirmix/emx-095-adopting-elixir-at-findhotel-with-fernando-hamasaki-de-amorim.jpg')
    """

    path_components = short_path.strip("/").split("/")
    folder = f"{base_img_dir}/{path_components[0]}"
    filename = "-".join(path_components[1:])
    filepath_out = f"{folder}/{filename}.{img_format}"

    return folder, filepath_out


def download_img(short_path: str, img_url: str):
    """:arg
    file_path: str - filepath where image is to be stored
    img_url: str - URL that points to the images

    Returns nothing
    """
    # TODO: handle conversion here
    img_format = img_url.split(".")[-1]
    folder, file_path = path_to_filepath(short_path, img_format)

    if not os.path.exists(folder):
        os.system(f"mkdir -p {folder}")

    if not os.path.exists(folder):
        os.makedirs(folder)

    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        with open(f"{file_path}", 'wb') as f:
            shutil.copyfileobj(r.raw, f)
            print("Image successfully download:", file_path)


def podcast_info(short_path: str):

    with open(META_DATA_PATH) as json_file:
        data_dict = json.load(json_file)

        podcast = data_dict.get(short_path, None)
        if not podcast:
            print(f"{short_path} is not a valid path")
            exit(1)

        try:
            title, ep_title, img_url = podcast["podcast"]["title"], podcast["title"], podcast["image_url"]
            image_format = img_url.split(".")[-1]

        except:
            print("Something went wrong, sorry. This is a product of a hackathon ><")
            exit(1)

        _, file_path = path_to_filepath(short_path, image_format)
        if not os.path.exists(file_path):
            download_img(short_path, img_url)

        COMMAND = f"zsh getAscii.zsh {file_path}"
        os.system(COMMAND)
        raw_title = f"Podcast: {title}"
        print(INFO_WIDTH * "=")
        print(raw_title)
        print(INFO_WIDTH * "=")
        print(f"Episode title: {ep_title}")
        print(INFO_WIDTH * "=")


if __name__ == "__main__":

    if not os.path.exists("~/podcasts"):
        os.system(f"mkdir -p ~/podcasts")

    if not os.path.exists(META_DATA_PATH):
        # os.system(f"mkdir -p ~/podcasts")
        get_metadata()


    if sys.argv[1] == "search":
        keyword = sys.argv[2].lower()
        podcasts = fetch_podcasts_by_keyword(keyword)
        for episode in podcasts:
            print_podcast(episode)          
    
    elif sys.argv[1] == "random":
        print_podcast(fetch_random_podcast())

    elif sys.argv[1] == "list":
        try:
            # check that the arguments are numeric
            val = int(sys.argv[2])
            if val < 0:
                print("podcast list: please enter a positive integer for the page number")
                sys.exit(1)
            
            val = int(sys.argv[3])
            if val < 0:
                print("podast list: please enter a positive integer for the number of podcasts per page")
                sys.exit(1)
        
        except ValueError:
            print("podcast list: please enter an integer for the page number and podcasts per page") 
            sys.exit(1)
            
        podcasts = fetch_paginated_podcasts(sys.argv[2], sys.argv[3])
        for episode in podcasts:
            print_podcast(episode)

    elif sys.argv[1] == "info":
        podcast_info(sys.argv[2])

