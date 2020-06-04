import requests
import json
import random

from typing import List
from string_distance import recursive_levenshtein

# Link to the branch where work on this is happening: https://github.com/MLH-Fellowship/0.0.1-podcast-cli/tree/feat/use-python


# This is how Levensthein work. It falls short when comparing longer strings (e.g titles of podcasts).
# I think string matching can be improved (or rather fixed) using Dice Coefficient.
# This npm module I use (and it works perfectly) uses Dice Coefficient: https://www.npmjs.com/package/string-similarity.
# This whole thing might also be unnecessary. Consulting with The Shell Guys advised.
print(recursive_levenshtein("bartek pacia", "bartk pcia"))
print(recursive_levenshtein("bartek pacia", "bartek paci"))


class PodcastEpisode:
    '''
    Represents a single podcast episode from the dev.to API.
    '''

    id = 0
    path = None
    title = None

    def __init__(self, id, path, title):
        self.id = id
        self.path = f"https://dev.to{path}"
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


def fetch_podcasts_by_title(username: str) -> List[PodcastEpisode]:
    '''
    Fetches a list of podcasts from the dev.to API.

    Parameters
    ----------
    username - title of the whole podcast series
    '''
    username = username.strip().replace(" ", "")
    response = requests.get(
        f"https://dev.to/api/podcast_episodes?username={username}")
    data = json.loads(response.text)

    return parse_podcast_data(data)


def fetch_random_podcast():
    '''
    fetches podcasts via Dev.to API call w/no search param. Returns a single
    random podcast episode from list of episodes returned by API.
    '''

    response = requests.get(
        "https://dev.to/api/podcast_episodes")
    data = json.loads(response.text)
    podcast_episode_list = parse_podcast_data(data)
    random_episode = random.choice(podcast_episode_list)

    return random_episode


def save(podcast_file):
    '''
    This will save the downloaded podcast file to "some" directory.
    e.g mp3-files2/ like in the shell script written by The Shell Guys.
    '''
    pass


# TESTING CODE BELOW


# this will come from ZSH, I guess. For now, let's just use input().
# query_entered_by_the_user = input("Enter podcast name: ").lower()
# this might also come from ZSH side (?)
# podcast_episode_name = input("Enter podcast episode name (empty input will return all): ").lower()

# episodes = fetch_podcasts_by_title(query_entered_by_the_user)

episode = fetch_random_podcast()
print(episode.title)

# best_match_value = 0
# episode_with_best_match = None
#
# for podcast_episode in episodes:
#     match_value = recursive_levenshtein(
#         podcast_episode_name, podcast_episode.title)
#
#     if match_value > best_match_value:
#         best_match_value = match_value
#         episode_with_best_match = podcast_episode
#
#     # Used for debugging and testing how string similarity functionality works.
#     # Currently it works *bad*.
#     print(f"match value for {podcast_episode.title}: {match_value}")
#
#
# print(f"{episode_with_best_match}: {match_value}")
