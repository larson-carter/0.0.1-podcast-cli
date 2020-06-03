import requests
import json
from typing import List


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


def fetch_podcasts() -> List[PodcastEpisode]:
    '''
    Fetches a list of podcasts from the dev.to API.
    '''
    response = requests.get("https://dev.to/api/podcast_episodes")
    data = json.loads(response.text)

    podcast_episodes = []
    for podcast_data in data:
        podcast_episode = PodcastEpisode(
            podcast_data["id"], podcast_data["path"], podcast_data["title"]
        )

        podcast_episodes.append(podcast_episode)

    return podcast_episodes


def save(podcast_file):
    '''
    This will save the downloaded podcast file to "some" directory.
    e.g mp3-files2 like in the shell script
    '''
    pass


# this will come from ZSH, I guess
query_entered_by_the_user = "code newbie".lower()

episodes = fetch_podcasts()
for podcast in episodes:
    print(podcast.title)
