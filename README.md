# YTMDL
### YouTube Music Downloader

## Description
Simple GTK 3 (GUI) wrapper for youtube-dl specifically to convert videos to mp3 files. Allowing you to specify the artist and title to be saved in the ID3 metadata.

## Dependancies

- python 3
- youtube_dl python module
    - `sudo pip3 install youtube_dl`
- eyed3 python module
    - `sudo pip3 install eyed3`
- ffmpeg

## Running ytmdl

I should have an install process for Gnome Shell in the next few days but right now you just have to have config.yml and ytmdl.py in the same directory and run:

```bash
$ ./ytmdl.pl
```