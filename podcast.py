import requests
import json
from typing import List
from string_distance import recursive_levenshtein


print(recursive_levenshtein("bartek pacia", "bartk pcia"))
print(recursive_levenshtein("bartek pacia", "bartek paci"))


class PodcastEpisode:
    '''
    Represents a single podcast episode from the dev.to API.
    '''

    id = 0
    path = None
    title = None

    # the constructor
    def __init__(self, id, path, title):
        self.id = id
        self.path = f"https://dev.to{path}"
        self.title = title

    # equivalent of toString()
    def __str__(self):
        return f"(PodcastEpisode) id={self.id} , path={self.path} , title={self.title}"


def fetch_podcasts(username: str) -> List[PodcastEpisode]:
    '''
    Fetches a list of podcasts from the dev.to API.
    '''
    username = username.strip().replace(" ", "")
    response = requests.get(
        f"https://dev.to/api/podcast_episodes?username={username}")
    data = json.loads(response.text)

    podcast_episodes = []
    if not data:
        print("data is None. Something bad happened")

    for podcast_data in data:
        podcast_episode = PodcastEpisode(
            podcast_data["id"], podcast_data["path"], podcast_data["title"].lower()
        )

        podcast_episodes.append(podcast_episode)

    return podcast_episodes


def save(podcast_file):
    '''
    This will save the downloaded podcast file to "some" directory.
    e.g mp3-files2 like in the shell script
    '''
    pass


# this will come from ZSH, I guess. For now, let's just use input()
query_entered_by_the_user = input("Enter podcast name: ").lower()
# this might also come from ZSH side (?)
podcast_episode_name = input("Enter podcast episode name: ").lower()

episodes = fetch_podcasts(query_entered_by_the_user)
best_match_value = 0
episode_with_best_match = None
for podcast_episode in episodes:
    match_value = recursive_levenshtein(
        podcast_episode_name, podcast_episode.title)
    if match_value > best_match_value:
        best_match_value = match_value
        episode_with_best_match = podcast_episode

    print(f"match value for {podcast_episode.title}: {match_value}")


print(f"{episode_with_best_match}: {match_value}")
