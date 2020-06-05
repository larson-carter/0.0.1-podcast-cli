# DEV Podcast CLI

**A zsh plugin to manage podcasts from the DEV podcast directory. **

This was developed as part of the MLH Fellowship Kickoff Hackathon.

## Features

* Search the DEV podcast directory for a specific keyword, get a random podcast, or browse the DEV podcast directory page-by-page
* Download podcasts
* Display the album artwork as an ASCII image

![Album Artwork Screenshot](https://raw.githubusercontent.com/MLH-Fellowship/0.0.1-podcast-cli/master/screenshots/podcast%20info%20screenshot.png)

## Installation

1. Clone the repository
2. Install the dependencies
3. `$ source podcast.plugin.zsh`
4. To get more information, `$ podcast -h`

## Usage

```
Usage: podcast <option>
-h, --help
	Show help information
search <search_term>
	Search recent podcasts for the search term
imfeelinglucky
	Show a random podcast episode
podcast download <short_url> <?download_dir>
	Download a podcast
	If the download directory is missing, this will download to ./podcasts
info <short_url>
	Display the show art and any metadata
list <pg_num> <pg_size>
	Browse the list of podcasts page by page
```

## Implementation

The CLI was implemented in `podcast.plugin.zsh`. This is a front-end that delegates out to `podcast.py` and `download.py`. `podcast.py` handles interaction with the DEV podcast API, as well as displaying ASCII album artwork. `download.py` handles downloading podcasts. 
