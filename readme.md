### Usage of podcast.zsh

**Usage**: `zsh podcast.zsh <DEV.TO_URL> <OPTIONAL:MP3_DIR>`

**Specifying only `DEV.TO_URL`**

Note that there is 1 compulsory and 1 optional argument as of now.

Specifying `DEV.TO_URL` is compulsory. If `MP3_DIR` is not specified, it will default to saving mp3_files in `./mp3_files`

```
zsh podcast.zsh https://dev.to/iphreaks/ips-292-evolving-apps-and-hacking-around-with-eric-crichlow
```

**Specifying both `DEV.TO_URL` and `MP3_DIR`**

To save the mp3 file in the default dir, `./mp3_files`:
```
zsh podcast.zsh https://dev.to/iphreaks/ips-292-evolving-apps-and-hacking-around-with-eric-crichlow
```

To save the mp3 file in a custom dir, append the dir name at the end of the command:
```
zsh podcast.zsh https://dev.to/iphreaks/ips-292-evolving-apps-and-hacking-around-with-eric-crichlow ./my_custom_dir
```
