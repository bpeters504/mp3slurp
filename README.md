# MP3Slurp

## Description
Create MP3 files from a list of YouTube URLs. If you specify the Atrist and Title, those tags will be added. If not specified, metadata from youtube will be used.

This is a GTK 3 wrapper for youtube-dl and eyed3. Meant for use on Linux with Gnome.

## Dependancies

- Gtk3
- python 3
- youtube_dl python module
    - `sudo pip3 install youtube_dl`
- eyed3 python module
    - `sudo pip3 install eyed3`
- ffmpeg

## Running ytmdl

I should have an install process for Gnome Shell in the next few days but right now you just have to have config.yml and ytmdl.py in the same directory and run:

```bash
$ ./mp3slurp.pl
```